import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from page_scripts.stats_scripts.utils import *

team_name_3 = {"Bayern Munich": "FC Bayern München", "Bayer Leverkusen": "Bayer 04 Leverkusen",
               "Hoffenheim": "TSG 1899 Hoffenheim", "Werder Bremen": "SV Werder Bremen", "Mainz 05": "1. FSV Mainz 05",
               "Hannover 96": "Hannover 96", "Wolfsburg": "VfL Wolfsburg", "Borussia Dortmund": "Borussia Dortmund",
               "Hamburger SV": "Hamburger SV", "Augsburg": "FC Augsburg", "Hertha Berlin": "Hertha Berlin",
               "VfB Stuttgart": "VfB Stuttgart", "Schalke 04": "FC Schalke 04",
               "RasenBallsport Leipzig": "RasenBallsport Leipzig", "Freiburg": "Sport-Club Freiburg",
               "Eintracht Frankfurt": "Eintracht Frankfurt", "Borussia M.Gladbach": "Borussia Mönchengladbach",
               "FC Cologne": "1. FC Köln", "Fortuna Duesseldorf": "Fortuna Düsseldorf", "Nuernberg": "1. FC Nürnberg",
               "Paderborn": "SC Paderborn 07", "Union Berlin": "1. FC Union Berlin",
               "Arminia Bielefeld": "Arminia Bielefeld", "Bochum": "VfL Bochum 1848",
               "Greuther Fuerth": "SpVgg Greuther Fürth"}


@st.cache
def shot_event_data_process(season):
    # ##### Read Data
    df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Shot_Events_Statistics_{season}.csv", index_col='Unnamed: 0')
    df['Team'] = df['Team'].map(team_name_3)
    df['Opponent'] = df['Opponent'].map(team_name_3)
    season_df = df[df['Season'] == season].reset_index(drop=True)

    # ##### Add Filter Type Stats
    season_df['Total'] = 1
    season_df['Home'] = np.where(season_df['Venue'] == "Home", 1, 0)
    season_df['Away'] = np.where(season_df['Venue'] == "Away", 1, 0)
    season_df["1st Period"] = np.where(season_df["Week_No"] <= 17, 1, 0)
    season_df["2nd Period"] = np.where(season_df["Week_No"] >= 18, 1, 0)

    return season_df


def team_shot_event_type(data, team_name, season_filter):
    # ##### Event Game Type
    event_data = data[
        ((data['Team'] == team_name) | (data['Opponent'] == team_name)) & (data[season_filter] == 1)].reset_index(
        drop=True)
    event_type_team = event_data['Event'].unique()
    return event_type_team


def team_event_data(data, team_name, season_filter, event_type):
    # ##### Game Event Filter Data
    event_data = data[
        ((data['Team'] == team_name) | (data['Opponent'] == team_name)) & (data[season_filter] == 1)].reset_index(
        drop=True)

    # ##### Format Data
    game_event_data_team = event_data[(event_data['Team'] == team_name)].reset_index(
        drop=True)
    game_event_data_team['X_cord'] = game_event_data_team['X_cord'] * 105 - 105
    game_event_data_team['X_cord'] = game_event_data_team['X_cord'] * -1
    game_event_data_team['Y_cord'] = game_event_data_team['Y_cord'] * 68 - 68
    game_event_data_team['Y_cord'] = game_event_data_team['Y_cord'] * -1
    game_event_data_opp = event_data[(event_data['Opponent'] == team_name)].reset_index(
        drop=True)
    game_event_data_opp['X_cord'] = game_event_data_opp['X_cord'] * 105
    game_event_data_opp['Y_cord'] = game_event_data_opp['Y_cord'] * 68

    final_event_data = pd.concat([game_event_data_team, game_event_data_opp])
    final_event_data['Shot Result'] = np.where(final_event_data['Event'] == 'Goal', 'Goal', 'Shot')
    final_event_data[['X_cord', 'Y_cord', 'xGoal']] = np.round(
        final_event_data[['X_cord', 'Y_cord', 'xGoal']], 3)

    team_shots_event_data = final_event_data[final_event_data['Event'].isin(event_type)].reset_index(drop=True)

    # ##### Markdown
    goals_data_team = game_event_data_team[game_event_data_team['Event'] == 'Goal']
    shots_data_team = game_event_data_team.copy()
    if goals_data_team.shape[0] > 0:
        team_goals_box = np.round(np.sum(goals_data_team['X_cord'] <= 18) / goals_data_team.shape[0] * 100, 2)
        goals_data_team['Half'] = np.where(goals_data_team['Minute'] < 46, "1st Half", "2nd Half")
        best_team_goals_half = goals_data_team['Half'].value_counts(normalize=True).reset_index()
        best_team_goals_half_value = best_team_goals_half.iloc[0, 0]
        best_team_goals_half_score = np.round(best_team_goals_half.iloc[0, 1] * 100, 2)
    else:
        team_goals_box = ""
        best_team_goals_half_value = ""
        best_team_goals_half_score = ""

    if shots_data_team.shape[0] > 0:
        team_shots_box = np.round(np.sum(shots_data_team['X_cord'] <= 18) / shots_data_team.shape[0] * 100, 2)
        shots_data_team['Half'] = np.where(shots_data_team['Minute'] < 46, "1st Half", "2nd Half")
        best_team_shots_half = shots_data_team['Half'].value_counts(normalize=True).reset_index()
        best_team_shots_half_value = best_team_shots_half.iloc[0, 0]
        best_team_shots_half_score = np.round(best_team_shots_half.iloc[0, 1] * 100, 2)
    else:
        team_shots_box = ""
        best_team_shots_half_value = ""
        best_team_shots_half_score = ""

    goals_data_opp = game_event_data_opp[game_event_data_opp['Event'] == 'Goal']
    shots_data_opp = game_event_data_opp.copy()
    if goals_data_opp.shape[0] > 0:
        opp_goals_box = np.round(np.sum(goals_data_opp['X_cord'] >= 87) / goals_data_opp.shape[0] * 100, 2)
        goals_data_opp['Half'] = np.where(goals_data_opp['Minute'] < 46, "1st Half", "2nd Half")
        best_opp_goals_half = goals_data_opp['Half'].value_counts(normalize=True).reset_index()
        best_opp_goals_half_value = best_opp_goals_half.iloc[0, 0]
        best_opp_goals_half_score = np.round(best_opp_goals_half.iloc[0, 1] * 100, 2)
    else:
        opp_goals_box = "0"
        best_opp_goals_half_value = ""
        best_opp_goals_half_score = ""

    if shots_data_opp.shape[0] > 0:
        opp_shots_box = np.round(np.sum(shots_data_opp['X_cord'] >= 87) / shots_data_opp.shape[0] * 100, 2)
        shots_data_opp['Half'] = np.where(shots_data_opp['Minute'] < 46, "1st Half", "2nd Half")
        best_opp_shots_half = shots_data_opp['Half'].value_counts(normalize=True).reset_index()
        best_opp_shots_half_value = best_opp_shots_half.iloc[0, 0]
        best_opp_shots_half_score = np.round(best_opp_shots_half.iloc[0, 1] * 100, 2)
    else:
        opp_shots_box = "0"
        best_opp_shots_half_value = ""
        best_opp_shots_half_score = ""

    return team_shots_event_data, team_goals_box, team_shots_box, opp_goals_box, opp_shots_box, \
           best_team_goals_half_value, best_team_goals_half_score, best_team_shots_half_value, \
           best_team_shots_half_score, best_opp_goals_half_value, best_opp_goals_half_score, \
           best_opp_shots_half_value, best_opp_shots_half_score


def team_event_plot(data):
    # ##### PLot Data
    background = "#4E4E50"

    shot_event_fig, ax = plt.subplots(figsize=(15, 10))
    shot_event_fig.set_facecolor(background)

    draw_pitch(orientation="h",
               aspect="full",
               pitch_color=background,
               line_color="lightgrey",
               ax=ax)

    color_dict = dict({'Goal': 'red',
                       'Shot': 'white'})

    event_markers = {'Goal': '*',
                     'OwnGoal': 'P',
                     'SavedShot': 'o',
                     'MissedShots': '^',
                     'BlockedShot': 'v',
                     'ShotOnPost': ','
                     }

    shot_event_fig = sns.scatterplot(data=data, x="X_cord", y="Y_cord", hue='Shot Result', size="xGoal",
                                     sizes=(100, 1000), style="Event", markers=event_markers, palette=color_dict,
                                     legend=False, alpha=0.7)

    return shot_event_fig


@st.cache
def players_team_events(data, team_name, season_filter):
    # ##### Team Event Data
    event_data = data[(data['Team'] == team_name) & (data[season_filter] == 1)].reset_index(drop=True)
    team_players_events = list(event_data['Player Name'].unique())
    team_players_events.sort()

    return team_players_events


def player_shot_event_type(data, team_name, player_name, season_filter):
    # ##### Event Game Type
    event_data = data[
        ((data['Team'] == team_name) | (data['Opponent'] == team_name)) & (data["Player Name"] == player_name) & (
                data[season_filter] == 1)].reset_index(drop=True)
    event_type_player = event_data['Event'].unique()
    return event_type_player


def player_event_data(data, team_name, player_name, season_filter, event_type):
    # ##### Game Event Filter Data
    event_data = data[
        (data['Team'] == team_name) & (data[season_filter] == 1)].reset_index(
        drop=True)

    # ##### Format Data
    game_event_data_player = event_data[(event_data['Player Name'] == player_name)].reset_index(drop=True)
    game_event_data_player['X_cord'] = game_event_data_player['X_cord'] * 105
    game_event_data_player['Y_cord'] = game_event_data_player['Y_cord'] * 68 - 68
    game_event_data_player['Y_cord'] = game_event_data_player['Y_cord'] * -1

    game_event_data_player['Shot Result'] = np.where(game_event_data_player['Event'] == 'Goal', 'Goal', 'Shot')
    game_event_data_player[['X_cord', 'Y_cord', 'xGoal']] = np.round(
        game_event_data_player[['X_cord', 'Y_cord', 'xGoal']], 3)

    final_event_player_data = game_event_data_player[game_event_data_player['Event'].isin(event_type)].reset_index(
        drop=True)

    # ##### Markdown
    goals_data_player = game_event_data_player[game_event_data_player['Event'] == 'Goal']
    shots_data_player = game_event_data_player.copy()
    if goals_data_player.shape[0] > 0:
        player_goals_box = np.round(np.sum(goals_data_player['X_cord'] >= 87) / goals_data_player.shape[0] * 100, 2)
        goals_data_player['Half'] = np.where(goals_data_player['Minute'] < 46, "1st Half", "2nd Half")
        best_player_goals_half = goals_data_player['Half'].value_counts(normalize=True).reset_index()
        best_player_goals_half_value = best_player_goals_half.iloc[0, 0]
        best_player_goals_half_score = np.round(best_player_goals_half.iloc[0, 1] * 100, 2)
    else:
        player_goals_box = ""
        best_player_goals_half_value = ""
        best_player_goals_half_score = ""
    if shots_data_player.shape[0] > 0:
        player_shots_box = np.round(np.sum(shots_data_player['X_cord'] >= 87) / shots_data_player.shape[0] * 100, 2)
        shots_data_player['Half'] = np.where(shots_data_player['Minute'] < 46, "1st Half", "2nd Half")
        best_player_shots_half = shots_data_player['Half'].value_counts(normalize=True).reset_index()
        best_player_shots_half_value = best_player_shots_half.iloc[0, 0]
        best_player_shots_half_score = np.round(best_player_shots_half.iloc[0, 1] * 100, 2)
    else:
        player_shots_box = ""
        best_player_shots_half_value = ""
        best_player_shots_half_score = ""

    return final_event_player_data, player_goals_box, player_shots_box, best_player_goals_half_value, \
           best_player_goals_half_score, best_player_shots_half_value, best_player_shots_half_score


def player_event_plot(data, event_type):
    # ##### PLot Data
    background = "#4E4E50"

    shot_event_fig, ax = plt.subplots(figsize=(15, 10))
    shot_event_fig.set_facecolor(background)

    draw_pitch(orientation="v",
               aspect="half",
               pitch_color=background,
               line_color="lightgrey",
               ax=ax)

    color_dict = dict({'Goal': 'red',
                       'Shot': 'white'})

    event_markers = {'Goal': '*',
                     'OwnGoal': 'P',
                     'SavedShot': 'o',
                     'MissedShots': '^',
                     'BlockedShot': 'v',
                     'ShotOnPost': ','
                     }

    shot_event_fig = sns.scatterplot(data=data, x="Y_cord", y="X_cord", hue='Shot Result', size="xGoal",
                                     sizes=(100, 1000), style="Event", markers=event_markers, palette=color_dict,
                                     legend=False, alpha=0.7)

    if len(event_type) == 1 and event_type[0] == 'Goal':
        player_events_assists = data.dropna(subset=['Assist Player']).reset_index(drop=True)
        for i in range(player_events_assists.shape[0]):
            shot_event_fig.text(x=player_events_assists.Y_cord[i] + 1, y=player_events_assists.X_cord[i] - 0.5,
                                s=player_events_assists['Assist Player'][i],
                                fontdict=dict(color="white", weight='bold', size=10))

    return shot_event_fig