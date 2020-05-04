import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from database_queries import *
def date_to_index(year, month, day, index):
    # add years
    difference = int(year) - 19
    for addition in range(1, difference + 1):
        if (2019 + addition) % 4 == 0:
            index += 366
        else:
            index += 365
    # add months
    month_to_days = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31,
                     "11": 30, "12": 31}
    if int(year) % 4 == 0:
        month_to_days = {"1": 31, "2": 29, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31,
                         "11": 30, "12": 31}

    month_int = int(month)
    if month_int == 13:
        print("brian is amazing")
    for addition in range(1, month_int):
        index += month_to_days[str(addition)]
    # add days
    index += int(day)

    return index
def time_to_index(hour, minute, second, index):
    # add hours
    index += int(hour) / 24
    # add minutes
    index += int(minute) / (24 * 60)
    # add seconds
    index += int(second) / (24 * 60 * 60)
    return index
def datetime_to_indexQ(datetime):
    index = 0
    # index 0 = January 1, 2019
    date, time = datetime.split(" ")
    hour, minute, second = time.split(":")
    year, month, day = date.split("-")
    year = year[-2:]
    index = date_to_index(year, month, day, index)
    index = time_to_index(hour, minute, second, index)
    return index

def datetime_to_indexP(datetime):
    index = 0
    # index 0 = January 1, 2019
    date, time = datetime.split(" ")
    hour, minute, second = time.split(":")
    month, day, year = date.split("-")
    index = date_to_index(year, month, day, index)
    index = time_to_index(hour, minute, second, index)
    return index


def add_indicesP(pdict):
    pdict["index"] = []
    for datetime in pdict["datetime"]:
        index = datetime_to_indexP(datetime)
        pdict["index"].append(index)
    return pdict
def add_indicesQ(qdict):
    qdict["index"] = []
    for datetime in qdict["datetime"]:
        index = datetime_to_indexQ(datetime)
        qdict["index"].append(index)
    return qdict
def getClosestPressure(q_index, pdict):
    difs = []
    for i in pdict["index"]:
        dif = abs(i - q_index)
        difs.append(dif)
    min_index = np.argmin(difs)
    min_diff = min(difs)
    if min_diff >= (1/24):
        return "too distant"
    else:
        return pdict["pressure"][min_index]
def getClosestPressures(qdict, pdict):
    qs = []
    ps = []
    for i in range(len(qdict["discharge"])):
        q = qdict["discharge"][i]
        q_index = qdict["index"][i]
        p = getClosestPressure(q_index, pdict)
        if p != "too distant":
            qs.append(q)
            ps.append(p)
    return qs, ps


def main():
    conn = sqlite3.connect('C:\\Users\\cougf\\Box\\AbbottLab\\datAbbase.db')
    cursor = conn.cursor()
    path = "C:\\Users\\cougf\\Box\\AbbottLab\\Data\\masterSiteList.csv"
    with open(path, "r+") as file:
        i = 0
        for line in file:
            if i > 0:
                line = line.split(",")
                siteid = line[3]
                if siteid != "":
                    pdict = add_indicesP(getP(cursor, siteid))
                    qdict = add_indicesQ(getQ(cursor, siteid))
                    if len(pdict["pressure"]) > 0 and len(qdict["discharge"]) > 0:
                        qs, ps = getClosestPressures(qdict, pdict)
                        plt.scatter(qs, ps)
                        plt.title(siteid)
                        plt.show()



            i = i+1
main()




