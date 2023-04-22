import requests
from bs4 import BeautifulSoup

url = "https://www.collegesportsmadness.com/womens-basketball/recruiting"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
player_names = soup.find_all("td", class_ = "name")

for i in range(len(player_names)):
    name = player_names[i].text
    player_names[i] = name[:-1]

player_pos = soup.find_all("td", class_ = "position")

for i in range(len(player_pos)):
    pos = player_pos[i].text
    player_pos[i] = pos

player_heights = soup.find_all("td", class_ = "height")

# make sure to store in total inches 
for i in range(len(player_heights)):
    height = player_heights[i].text[0]
    height = height + player_heights[i].text[1:-1]
    feet = int(height[0])
    inches = int(height[2:])
    final_height = (12 * feet) + inches

    player_heights[i] = final_height

player_homes = soup.find_all("td", class_ = "high-school")

for i in range(len(player_homes)):
    temp = player_homes[i].text
    temp_list = temp.split(" ")
    home = temp_list[-1]

    if (home[0] != "("):
        player_homes[i] = "unknown"
    else:
        temp_home = home.strip("(")
        final_home = temp_home.strip(")")
        player_homes[i] = final_home


# create the database now
import sqlite3
conn = sqlite3.connect('hsplayers.sqlite')
cur= conn.cursor()

def createTable():
    cur.execute('DROP TABLE IF EXISTS hsplayers')
    cur.execute('CREATE TABLE hsplayers (name TEXT, height INTEGER, position TEXT, hometown TEXT)') 

def loadIntoTable(player_names, player_heights, player_pos, player_homes, index):
    
    for i in range(index, (index + 24)): # never read more than 24 values 
        cur.execute('INSERT INTO hsplayers (name, height, position, hometown) VALUES(?, ?, ?, ?)', 
                (player_names[i], player_heights[i], player_pos[i], player_homes[i]))
        
    
     

createTable()
index = 0
for i in range(5):   # will load 128 different rows into the data base
    loadIntoTable(player_names, player_heights, player_pos, player_homes, index)
    index += 24

# the final data base has been created 
# does this get limited to 25 lines as well at a time or is that just the later combinations 

conn.commit()
conn.close()
