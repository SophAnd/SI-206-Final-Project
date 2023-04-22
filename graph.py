import unittest
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np


def open_database (db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect (path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def calculate_avg_position_height(cur, conn):
    cur.execute("SELECT NBA_Players.height, Positions.position FROM NBA_Players JOIN Positions ON NBA_Players.position_id = Positions.id")
    rows = cur.fetchall()
    guard_heights = []
    forward_heights = []
    center_heights = []
    for row in rows:
        if row[1] == "Guard":
            guard_heights.append(row[0])
        elif row[1] == "Forward":
            forward_heights.append(row[0])
        elif row[1] == "Center":
            center_heights.append(row[0])
    data = [guard_heights, forward_heights, center_heights]
    fig = plt.figure(figsize =(10, 7))
    ax = fig.add_subplot(111)
    ax.set_xticklabels(['Guard', 'Forward',
                    'Center'])
    plt.boxplot(data)
    plt.show()

def main():
    cur, conn = open_database ('NBA.db')
    calculate_avg_position_height(cur, conn)
    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)