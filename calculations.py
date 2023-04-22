import unittest
import os
import sqlite3

def open_database (db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect (path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calculate_avg_position_height(cur, conn):
    cur.execute("SELECT NBA_Players.height, Positions.position FROM NBA_Players JOIN Positions ON NBA_Players.position_id = Positions.id")
    rows = cur.fetchall()
    total_g_height = 0
    total_f_height = 0
    total_c_height = 0
    total_g = 0.0
    total_f = 0.0
    total_c = 0.0
    for row in rows:
        if row[1] == "Guard":
            total_g_height += row[0]
            total_g += 1
        elif row[1] == "Forward":
            total_f_height += row[0]
            total_f += 1
        elif row[1] == "Center":
            total_c_height += row[0]
            total_c += 1
    avg_g = round(total_g_height / total_g, 1)
    avg_f = round(total_f_height / total_f, 1)
    avg_c = round(total_c_height / total_c, 1)
    file1 = open("calc_output.txt", "w")
    file1.writelines(f"The average height of an NBA Guard is {avg_g} inches. \n")
    file1.writelines(f"The average height of an NBA Forward is {avg_f} inches. \n")
    file1.writelines(f"The average height of an NBA Center is {avg_c} inches. \n")
    file1.close()
    conn.commit()

def main():
    name = "https://www.ncaa.com/stats/basketball-men/d1/current/individual/136"
    cur, conn = open_database ('NBA.db')
    calculate_avg_position_height(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)