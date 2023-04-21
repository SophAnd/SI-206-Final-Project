import unittest
import sqlite3
import requests
import json

def get_player_info(site):
    response = requests.get(site)
    data = response.text
    in_dict = json.loads(data)
    data = in_dict["data"]
    id_list = []
    name_list = []
    team_list = []
    for person in data:
        id = person["id"]
        first_name = person["first_name"]
        last_name = person["last_name"]
        full_name = first_name + " " + last_name
        team = person["team"]["full_name"]
        id_list.append(id)
        name_list.append(full_name)
        team_list.append(team)
    tuple_list = []
    for i in range(len(id_list)):
        tuple1 = (id_list[i], name_list[i], team_list[i])
        tuple_list.append(tuple1)
    return tuple_list

def main():
    name = 'https://www.balldontlie.io/api/v1/players'
    print(get_player_info(name))

if __name__ == "__main__":
    main()
    unittest.main(verbosity = 2)