#!/usr/local/bin/python3

from dotenv import load_dotenv
load_dotenv()

from .butler import api

if __name__ == "__main__":
    api.copy_all(api.get_stage("Daily"), api.get_stage("Today"))
    api.move_all(api.get_stage("Done"), api.get_stage("Done this week"))
