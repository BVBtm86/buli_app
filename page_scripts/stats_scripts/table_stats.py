import pandas as pd
import numpy as np
import streamlit as st

# ##### Team Names
team_name_1 = {"Bayern Munich": "FC Bayern München", "Bayer Leverkusen": "Bayer 04 Leverkusen",
               "Hoffenheim": "TSG 1899 Hoffenheim", "Werder Bremen": "SV Werder Bremen", "Mainz 05": "1. FSV Mainz 05",
               "Hannover 96": "Hannover 96", "Wolfsburg": "VfL Wolfsburg", "Dortmund": "Borussia Dortmund",
               "Hamburger SV": "Hamburger SV", "Augsburg": "FC Augsburg", "Hertha BSC": "Hertha Berlin",
               "Stuttgart": "VfB Stuttgart", "Schalke 04": "FC Schalke 04", "RB Leipzig": "RasenBallsport Leipzig",
               "Freiburg": "Sport-Club Freiburg", "Eintracht Frankfurt": "Eintracht Frankfurt",
               "Mönchengladbach": "Borussia Mönchengladbach", "Köln": "1. FC Köln", "Düsseldorf": "Fortuna Düsseldorf",
               "Nürnberg": "1. FC Nürnberg", "Paderborn 07": "SC Paderborn 07", "Union Berlin": "1. FC Union Berlin",
               "Arminia": "Arminia Bielefeld", "Bochum": "VfL Bochum 1848", "Greuther Fürth": "SpVgg Greuther Fürth"}


@st.cache
def filter_data(season):
    # ##### Read Data
    buli_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Statistics_{season}.csv", index_col='Unnamed: 0')

    # ##### Creating Tabel Stats
    buli_df['Win'] = np.where(buli_df['Result'] == 'Win', 1, 0)
    buli_df['Draw'] = np.where(buli_df['Result'] == 'Draw', 1, 0)
    buli_df['Defeat'] = np.where(buli_df['Result'] == 'Defeat', 1, 0)
    buli_df['Total'] = 1
    buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
    buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
    buli_df["1st Period"] = np.where(buli_df["Week_No"] <= 17, 1, 0)
    buli_df["2nd Period"] = np.where(buli_df["Week_No"] >= 18, 1, 0)

    # ##### Goals Statistics
    home_df = buli_df[buli_df['Venue'] == 'Home']
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away']
    away_df.reset_index(drop=True, inplace=True)
    home_df['goals'] = home_df['goals'] + away_df['own_goals']
    away_df['goals'] = away_df['goals'] + home_df['own_goals']
    home_df['goals_ag'] = away_df['goals']
    away_df['goals_ag'] = home_df['goals']
    final_df = pd.concat([home_df, away_df])

    # Filter Data
    filter_season = final_df[final_df['Season'] == season].reset_index(drop=True)
    match_day = np.max(filter_season['Week_No'])
    filter_season['Team'] = filter_season['Team'].map(team_name_1)
    filter_season['Opponent'] = filter_season['Opponent'].map(team_name_1)

    return filter_season, match_day


def buli_table_data(data, table_type):
    # #####season Data
    buli_season = data[data[table_type] == 1].reset_index(drop=True)

    # ##### Create Tab
    buli_tab = buli_season.groupby(['Team'])[['Total', 'Win', 'Draw', 'Defeat', 'goals', 'goals_ag']].sum()
    buli_tab['Goal_Diff'] = buli_tab['goals'] - buli_tab['goals_ag']
    buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
    buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
    buli_tab.reset_index(inplace=True)
    buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
    buli_tab.set_index('Rank', inplace=True)
    buli_tab.columns = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return buli_tab