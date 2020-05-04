def greet(name):
    print("Hello, " + name + ". How are you today? Is your code still not working?")
greet("Jacob")
import sqlite3
def getP(cursor, siteid):
    sqlquery = "SELECT *, MAX(batch_id) FROM (hobo_logs INNER JOIN hobo_batches USING(batch_id)) where site_id = ? group by date_sampled, time_sampled order by (date_sampled);"
    sitetuple = (siteid,)
    cursor.execute(sqlquery, sitetuple)
    result = cursor.fetchall()
    date_to_pressure = {}
    date_to_pressure["datetime"] = []
    date_to_pressure["pressure"] = []
    for item in result:
        date = item[0]
        time = item[1]
        pressure = item[2]
        date = date.split(" ")[0]
        datetime = date + " " + time
        date_to_pressure["datetime"].append(datetime)
        date_to_pressure["pressure"].append(pressure)
    return date_to_pressure
def getQ(cursor, siteid):
    sqlquery = "SELECT * FROM q_reads JOIN q_batches USING (q_batch_id) where site_id = ? group by date_sampled, time_sampled order by (date_sampled);"
    sitetuple = (siteid,)
    cursor.execute(sqlquery, sitetuple)
    result = cursor.fetchall()
    date_to_discharge = {}
    date_to_discharge["datetime"] = []
    date_to_discharge["discharge"] = []
    for item in result:
        date = item[2]
        time = item[3]
        discharge = item[4]
        date = date.split(" ")[0]
        datetime = date + " " + time
        date_to_discharge["datetime"].append(datetime)
        date_to_discharge["discharge"].append(discharge)
    return date_to_discharge
