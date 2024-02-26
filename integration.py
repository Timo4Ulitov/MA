import asyncio
import unittest
import psycopg2
from time import sleep
import json
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

sys.path.append(str(BASE_DIR / 'roulette_service/app'))
sys.path.append(str(BASE_DIR / 'player_service/app'))

from roulette_service.app.main import roulette_health as health_roulette
from player_service.app.main import player_health as health_player

def check_connect():
    try:
        conn = psycopg2.connect(
            dbname='Ulitov',
            user='ulitov',
            password='timur',
            host='localhost',
            port='5432'
        )
        conn.close()
        return True
    except Exception as e:
        return False


class TestIntegration(unittest.TestCase):
    # CMD: python tests/integration.py

    def test_db_connection(self):
        sleep(5)
        self.assertEqual(check_connect(), True)

    def test_roulette_service_connection(self):
        r = asyncio.run(health_roulette())
        self.assertEqual(r, {'message': 'service is active'})

    def test_player_service_connection(self):
        r = asyncio.run(health_player())
        self.assertEqual(r, {'message': 'service is active'})


if __name__ == '__main__':
    unittest.main()
