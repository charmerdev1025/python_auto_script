from ast import For
import pyodbc

server = 'sql5030.smarterasp.net'
database = 'DB_A17D64_trinovitech'
username = 'DB_A17D64_trinovitech_admin'
password = 'Schmuck@dmin1!'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password + ';Trusted_Connection=no')
cursor = cnxn.cursor()
SqlSelectCommand = ("select b.BoardKey, b.season, b.ScoreAwayTotal, b.ScoreHomeTotal, b.Total, b.TotalUnder, b.TotalOver, s.PickColumn, s.WinValue, s.BetSlipKey, s.fkUserID, s.PickValue, b.SpreadAway, b.SpreadHome, s.SelectedTeam, t.TeamName AS AwayName, tt.TeamName AS HomeName from BetSlips s left join Board b on b.MatchupKey = s.fkMatchupID left join teams t on t.TeamAbbrev = b.AwayTeam AND t.fkSportKey = b.fkSportKey left join teams tt on tt.TeamAbbrev = b.HomeTeam AND tt.fkSportKey = b.fkSportKey where b.fkSportKey = 2 and b.season='FINAL' and s.BetStatus != 2 and s.BetStatus != 3")
cursor.execute(SqlSelectCommand)
rows = cursor.fetchall()
def run_query(SQLUpdateCommand, Values):
    cursor.execute(SQLUpdateCommand, Values)
    cnxn.commit()
for row in rows:
    BetSlipKey = row[9]
    fkUserID = row[10]
    WinValue = row[8]
    w_l = ""
    if(row[7] == "Under" or row[7] == "Over"):
        bet_total = int(row[2] + row[3])
        def_total = row[4]
        if(def_total == ""): def_total = row[5]
        if(def_total == ""): def_total = row[6]
        def_total = float(def_total)
        u_o_bet = ""
        if(bet_total > def_total): u_o_bet = "Over"
        if(bet_total < def_total): u_o_bet = "Under"
        BetStatus = "1"
        if(u_o_bet == row[7]):
            w_l = "win"
            BetStatus = "2"
            Values = [WinValue, fkUserID]
            query = ("update UserBalance set CashBucket = CashBucket + ? where fkUserID = ?")
            run_query(query, Values)
        else:
            w_l = "loss"
            BetStatus = "3"
        Values = [BetStatus, BetSlipKey]            
        query = ("UPDATE BetSlips SET BetStatus=? WHERE BetSlipKey=?")
        run_query(query, Values)   
        print("Type => Under/Over | BetSlipKey => ", BetSlipKey, "| Bet_total => ", bet_total, "| Def_total => ", def_total, "| PickColumn => ", row[7], "| Result => ", w_l)
    if(row[7] == "Spread"):
        ScoreAwayTotal = int(row[2])
        ScoreHomeTotal = int(row[3])
        SpreadAway = row[12]
        SpreadAway = SpreadAway.replace("-.", "-").replace("+.", "+")
        SpreadHome = row[13]
        SpreadHome = SpreadHome.replace("-.", "-").replace("+.", "+")
        PickValue = row[11]
        BetStatus = "1"
        if(float(PickValue) == float(SpreadAway)):
            if(ScoreAwayTotal + float(PickValue) > ScoreHomeTotal):
                w_l = "win"
                BetStatus = "2"
                Values = [WinValue, fkUserID]
                query = ("update UserBalance set CashBucket = CashBucket + ? where fkUserID = ?")
                run_query(query, Values)
            else: 
                w_l = "loss"
                BetStatus = "3"
        if(float(PickValue) == float(SpreadHome)):
            if(ScoreHomeTotal + float(PickValue) > ScoreAwayTotal):
                w_l = "win"
                BetStatus = "2"
                Values = [WinValue, fkUserID]
                query = ("update UserBalance set CashBucket = CashBucket + ? where fkUserID = ?")
                run_query(query, Values)                
            else:
                w_l = "loss"
                BetStatus = "3"
        Values = [BetStatus, BetSlipKey]
        query = ("UPDATE BetSlips SET BetStatus=? WHERE BetSlipKey=?")
        run_query(query, Values)
        print("Type => Spread | BetSlipKey => ", BetSlipKey, "| ScoreAwayTotal => ", ScoreAwayTotal, "| ScoreHomeTotal => ", ScoreHomeTotal, "| PickValue => ", PickValue, "| SpreadAway => ", SpreadAway, "| SpreadHome => ", SpreadHome, "| Result =>", w_l)
    if(row[7] == "M/L"):
        selectedTeam = row[14]
        WinTeam = ""
        ScoreAwayTotal = int(row[2])
        ScoreHomeTotal = int(row[3])
        AwayName = row[15]
        HomeName = row[16]
        BetStatus = "1"
        if(ScoreAwayTotal > ScoreHomeTotal):
            WinTeam = AwayName
        if(ScoreHomeTotal > ScoreAwayTotal):
            WinTeam = HomeName       
        if(selectedTeam == WinTeam):
            w_l = "win"
            BetStatus = "2"
            Values = [WinValue, fkUserID]
            query = ("update UserBalance set CashBucket = CashBucket + ? where fkUserID = ?")
            run_query(query, Values)
        else:
            w_l = "loss"
            BetStatus = "3"
        Values = [BetStatus, BetSlipKey]
        query = ("UPDATE BetSlips SET BetStatus=? WHERE BetSlipKey=?")
        run_query(query, Values)
        print("Type => M/L | BetSlipKey => ", BetSlipKey, "| ScoreAwayTotal => ", ScoreAwayTotal, "| ScoreHomeTotal => ", ScoreHomeTotal, "| AwayTeam => ", AwayName, "| HomeTeam => ", HomeName, "| WinTeam => ", WinTeam, "| Result =>", w_l)

cursor.close()        

