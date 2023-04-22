import unittest
import requests
from bs4 import BeautifulSoup
import os
import sqlite3

def get_player_info(site):
    r = requests.get(site)
    soup = BeautifulSoup(r.content, 'html.parser')
    body = soup.find_all('tbody')[0]
    trs = body.find_all('tr')
    name_list = []
    height_list = []
    position_list = []
    for tr in trs:
        tds = tr.find_all('td')
        name = tds[1].text
        height_unconverted = tds[4].text
        ft_in = height_unconverted.split("-")
        ft = int(ft_in[0])
        inch = int(ft_in[1])
        height = ft * 12 + inch
        position = tds[5].text
        name_list.append(name)
        height_list.append(height)
        position_list.append(position)
    position_id_list = []
    for position in position_list:
        if position == 'G':
            id = 0
        elif position == 'F':
            id = 1
        elif position == 'C':
            id = 2
        position_id_list.append(id)
    tuple_list = []
    for i in range(len(name_list)):
        tuple1 = (name_list[i], height_list[i], position_id_list[i])
        tuple_list.append(tuple1)
    return tuple_list

def random_data(site):
    t1 = get_player_info(site)
    site2 = site + "/p" + str(2)
    t2 = get_player_info(site2)
    tuple3 = t1 + t2
    return tuple3
    
def open_database (db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect (path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_player_table(tuple_list, cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS NBA_Players (id INTEGER PRIMARY KEY, name TEXT UNIQUE, height INT, position_id TEXT)")
    cur.execute("SELECT count(id) FROM NBA_Players")
    count = cur.fetchone()[0]
    old_count = count
    for i in range(len(tuple_list)):
        cur.execute("SELECT count(id) FROM NBA_Players")
        count = cur.fetchone()[0]
        count += 1
        if count == old_count + 26:
            break
        name = tuple_list[i][0]
        height = tuple_list[i][1]
        position_id = tuple_list[i][2]
        cur.execute("INSERT OR IGNORE INTO NBA_Players (id, name, height, position_id) VALUES (?,?,?,?)", (count, name, height, position_id))
    conn.commit()

def make_position_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Positions (id INTEGER PRIMARY KEY, position TEXT)")
    positions = ["Guard", "Forward", "Center"]
    for i in range(len(positions)):
        cur.execute("INSERT OR IGNORE INTO Positions (id, position) VALUES (?,?)", (i, positions[i]))
    conn.commit()

def main():
    name = "https://www.ncaa.com/stats/basketball-men/d1/current/individual/136"
    tuple_list = (random_data(name))
    cur, conn = open_database ('NBA.db')
    make_player_table(tuple_list, cur, conn)
    make_position_table(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)