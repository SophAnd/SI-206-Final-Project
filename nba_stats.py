import unittest
import requests
from bs4 import BeautifulSoup
import json

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
        height = tds[4].text
        position = tds[5].text
        name_list.append(name)
        height_list.append(height)
        position_list.append(position)

    tuple_list = []
    for i in range(len(name_list)):
        tuple1 = (name_list[i], height_list[i], position[i])
        tuple_list.append(tuple1)
    return tuple_list

    
def main():
    name = "https://www.ncaa.com/stats/basketball-men/d1/current/individual/136"
    tuple_list = (get_player_info(name))
    print(tuple_list)

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)