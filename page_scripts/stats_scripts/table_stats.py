import pandas as pd
import numpy as np
import streamlit as st
from page_scripts.stats_scripts.utilities import season_team_query


# ##### Team Names
@st.cache
def filter_data(season):
    # ##### Read Data
    buli_df = season_team_query(season=season)

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
    home_df['Goals'] = home_df['Goals'] + away_df['Own Goals']
    away_df['Goals'] = away_df['Goals'] + home_df['Own Goals']
    home_df['Goals Ag'] = away_df['Goals']
    away_df['Goals Ag'] = home_df['Goals']
    final_df = pd.concat([home_df, away_df])

    # Filter Data
    filter_season = final_df[final_df['Season'] == season].reset_index(drop=True)
    match_day = np.max(filter_season['Week_No'])

    return filter_season, match_day


def buli_table_data(data, table_type):
    # #####season Data
    buli_season = data[data[table_type] == 1].reset_index(drop=True)

    # ##### Create Tab
    buli_tab = buli_season.groupby(['Team'])[['Total', 'Win', 'Draw', 'Defeat', 'Goals', 'Goals Ag']].sum()
    buli_tab['Goal_Diff'] = buli_tab['Goals'] - buli_tab['Goals Ag']
    buli_tab['Points'] = buli_tab['Win'] * 3 + buli_tab['Draw']
    buli_tab.sort_values(by=['Points', 'Goal_Diff'], ascending=[False, False], inplace=True)
    buli_tab.reset_index(inplace=True)
    buli_tab['Rank'] = [i for i in range(1, len(buli_tab) + 1)]
    buli_tab.set_index('Rank', inplace=True)
    buli_tab.columns = ["Team", "MP", "W", "D", "L", "GF", "GA", "GD", "Pts"]

    return buli_tab
