import requests
from uuid import UUID, uuid4
from datetime import datetime
import unittest


player_url = 'http://localhost:8000'
get_players_url = f'{player_url}/get_players'
add_player_url = f'{player_url}/add_player'
get_player_by_id_url = f'{player_url}/get_player_by_id/'
get_player_by_nickname_url = f'{player_url}/get_player_by_id_nickname/'
delete_player_url = f'{player_url}/delete_player'
switch_discipline_url = f'{player_url}/switch_discipline'
switch_team_url = f'{player_url}/switch_team'

roulette_url = 'http://localhost:8001'
roulette_roll_url = f"{roulette_url}/roll"
roulette_deposit_url = f"{roulette_url}/deposit"
roulette_cashup_url = f"{roulette_url}/cash_up"

player = {
    "id": "1",
    "name": "Timur",
    "age": 99,
    "nickname": "loser",
    "discipline": "dota2",
    "team": "TeamNoHomo"
}


class TestComponent(unittest.TestCase):

    def test_1_get_players(self):
        res = requests.get(f"{get_players_url}")
        self.assertTrue(res != None)

    def test_2_add_player(self):
        res = requests.post(f"{add_player_url}", json=player)
        self.assertEqual(res.status_code, 200)

    def test_3_get_player_by_id(self):
        res = requests.get(f"{get_player_by_id_url}?player_id=1").json()
        self.assertTrue(res, player)

    def test_4_get_player_by_nickname(self):
        res = requests.get(f"{get_player_by_nickname_url}?player_nickname=1").json()
        self.assertTrue(res, player)

    def test_5_switch_discipline(self):
        res = requests.post(f"{switch_discipline_url}?player_id=1&new_discipline=test")
        self.assertEqual(res.status_code, 200)

    def test_6_switch_team(self):
        res = requests.post(f"{switch_team_url}?player_id=1&new_team=test")
        self.assertEqual(res.status_code, 200)

    def test_7_delete_player(self):
        res = requests.delete(f"{delete_player_url}?player_id=1").json()
        self.assertEqual(res, "Success")

    def test_8_cashup(self):
        res = requests.post(f"{roulette_cashup_url}")
        self.assertEqual(res.status_code, 200)

    def test_9_deposit(self):
        res = requests.get(f"{roulette_deposit_url}?amount=9999")
        self.assertEqual(res.text, '"Your current balance is 9999"')

    def test_10_wrong_roulette(self):
        res = requests.post(f"{roulette_roll_url}?amount=10&point=test")
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()