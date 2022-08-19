import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from page_scripts.stats_scripts.utils import *

# ##### Team Names
team_name_1 = {"Bayern Munich": "FC Bayern München", "Bayer Leverkusen": "Bayer 04 Leverkusen",
               "Hoffenheim": "TSG 1899 Hoffenheim", "Werder Bremen": "SV Werder Bremen", "Mainz 05": "1. FSV Mainz 05",
               "Hannover 96": "Hannover 96", "Wolfsburg": "VfL Wolfsburg", "Dortmund": "Borussia Dortmund",
               "Hamburger SV": "Hamburger SV", "Augsburg": "FC Augsburg", "Hertha BSC": "Hertha Berlin",
               "Stuttgart": "VfB Stuttgart", "Schalke 04": "FC Schalke 04", "RB Leipzig": "RasenBallsport Leipzig",
               "Freiburg": "Sport-Club Freiburg", "Eintracht Frankfurt": "Eintracht Frankfurt",
               "Mönchengladbach": "Borussia Mönchengladbach", "Köln": "1. FC Köln", "Düsseldorf": "Fortuna Düsseldorf",
               "Nürnberg": "1. FC Nürnberg", "Paderborn 07": "SC Paderborn 07", "Union Berlin": "1. FC Union Berlin",
               "Arminia": "Arminia Bielefeld", "Bochum": "VfL Bochum 1848", "Greuther Fürth": "SpVgg Greuther Fürth",
               "Greuther F�rth": "SpVgg Greuther Fürth"}

team_name_2 = {"FC Bayern Mu_nchen": "FC Bayern München", "Bayer 04 Leverkusen": "Bayer 04 Leverkusen",
               "1. FSV Mainz 05": "1. FSV Mainz 05", "Hannover 96": "Hannover 96", "Hamburger SV": "Hamburger SV",
               "FC Augsburg": "FC Augsburg", "Hertha Berlin": "Hertha Berlin", "VfB Stuttgart": "VfB Stuttgart",
               "TSG 1899 Hoffenheim": "TSG 1899 Hoffenheim", "SV Werder Bremen": "SV Werder Bremen",
               "VfL Wolfsburg": "VfL Wolfsburg", "Borussia Dortmund": "Borussia Dortmund",
               "FC Schalke 04": "FC Schalke 04", "RasenBallsport Leipzig": "RasenBallsport Leipzig",
               "Sport-Club Freiburg": "Sport-Club Freiburg", "Eintracht Frankfurt": "Eintracht Frankfurt",
               "Borussia Mo_nchengladbach": "Borussia Mönchengladbach", "1. FC Ko_ln": "1. FC Köln",
               "Fortuna Du_sseldorf": "Fortuna Düsseldorf", "1. FC Nu_rnberg": "1. FC Nürnberg",
               "FC Bayern München": "FC Bayern München", "Fortuna Düsseldorf": "Fortuna Düsseldorf",
               "1. FC Köln": "1. FC Köln", "SC Paderborn 07": "SC Paderborn 07",
               "Borussia Mönchengladbach": "Borussia Mönchengladbach", "1. FC Union Berlin": "1. FC Union Berlin",
               "RB Leipzig": "RasenBallsport Leipzig", "TSG Hoffenheim": "TSG 1899 Hoffenheim",
               "DSC Arminia Bielefeld": "Arminia Bielefeld", "Arminia Bielefeld": "Arminia Bielefeld",
               "SC Freiburg": "Sport-Club Freiburg", "SpVgg Greuther Fürth": "SpVgg Greuther Fürth",
               "VfL Bochum 1848": "VfL Bochum 1848", "Borussia M'gladbach": "Borussia Mönchengladbach",
               "Greuther F�rth": "SpVgg Greuther Fürth"}

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
               "Greuther Fuerth": "SpVgg Greuther Fürth", "Greuther F�rth": "SpVgg Greuther Fürth"}

# ##### Stadiums
stadiums = {"1. FC Köln": "RheinEnergieStadion", "1. FC Nürnberg": "Max-Morlock-Stadion",
            "TSG 1899 Hoffenheim": "PreZero Arena", "Arminia Bielefeld": "Schüco-Arena",
            "Bayer 04 Leverkusen": "BayArena", "FC Bayern München": "Allianz Arena",
            "Borussia Dortmund": "Signal Iduna Park", "Borussia Mönchengladbach": "Borussia-Park",
            "Eintracht Frankfurt": "Commerzbank-Arena", "FC Augsburg": "WWK Arena",
            "Fortuna Düsseldorf": "Merkur Spiel-Arena", "SpVgg Greuther Fürth": "Sportpark Ronhof Thomas Sommer",
            "Hamburger SV": "Volksparkstadion", "Hannover 96": "HDI-Arena", "Hertha Berlin": "Olympiastadion",
            "1. FSV Mainz 05": "Opel Arena", "RasenBallsport Leipzig": "Red Bull Arena",
            "Sport-Club Freiburg": ["Dreisamstadion", "Europa-Park Stadion"], "SC Paderborn 07": "Benteler-Arena",
            "FC Schalke 04": "Veltins-Arena", "1. FC Union Berlin": "Stadion An der Alten Försterei",
            "VfB Stuttgart": "Mercedes-Benz Arena", "VfL Bochum 1848": "Vonovia Ruhrstadion",
            "VfL Wolfsburg": "Volkswagen Arena", "SV Werder Bremen": "Weser-Stadion"}

# ##### General Statistics
general_stats_vars = ["Manager", "Team_Lineup", "Distance_Covered", "Sprints", "Possession", "aerials_won_pct",
                      "offsides", "corner_kicks", "fouls", "cards_yellow", "cards_red"]

general_stats_names = ["Manager", "Lineup", "Distance Covered", "Sprints", "Possession", "Aerial Duels %",
                       "Offsides", "Corners", "Fouls", "Yellow Cards", "Red Cards"]

general_emoji = ["👨‍💼", "📏", "🚄", "🏃‍", "⚽", "🤼‍", "🚫", "📐", "🤒", "🟨", "🟥"]


# ##### Offensive Statistics
offensive_stats_var = ['xg', 'assists', "assisted_shots", "shots_total", "shots_on_target", "shot_accuracy",
                       "blocked_shots", "dribbles", "successful_dribbles"]

offensive_stats_names = ["XG", "Assists", "Key Passes", "Shots", "Shots on Target", "Accuracy %",
                         "Blocked Shots", "Dribbles", "Dribbles %"]

offensive_emoji = ["⚽", "🤝", "🤝⚽", "👟", "🥅", "🎯", "🚫🥅", "⛹️", "⛹️✅"]

# ##### Defensive Statistics
defensive_stats_var = ['tackles', 'successful_tackles', "pressures", "pressure_regain_pct", "clearances",
                       "interceptions", "ball_recoveries", "blocks", "errors"]

defensive_stats_names = ["Tackles", "Tackles Won %", "Pressure", "Pressure Won %", "Clearances", "Interceptions",
                         "Ball recoveries", "Blocks", "Errors"]

defensive_emoji = ["🤼", "🤼✅", "🚿", "🚿✅", "🆑", "🥷", "🤒", "🚫️", "⭕"]

# ##### Passing Statistics
passing_stats_var = ["touches", "passes", "passes_pct", "passes_pct_short", "passes_pct_medium", "passes_pct_long",
                     "passes_into_final_third", "passes_into_penalty_area", "crosses", "crosses_into_penalty_area"]

passing_stats_names = ["Touches", "Passes", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %",
                       "Final Third", "Penalty Area", "Crosses", "Crosses PA"]

passing_emoji = ["👟", "🔁", "🔁✅", "🔁✅", "🔁✅", "🔁✅", "🥅", "🥅", "❎", "❎🥅"]

# ##### Goalkeeper Statistics
gk_stats_var = ["saves", "saves_pct", "passes_gk", "passess_pct_successful_gk", "goal_kicks",
                "goal_kicks_pct_successful", "passes_throws_gk"]

gk_stats_names = ["Saves", "Saves %", "Passes", "Passes %", "Goal Kicks", "Goal Kicks %", "Throws"]

goalkeeper_emoji = ["🧤", "🧤✅", "🔁", "🔁✅", "👟", "👟✅", "🤾"]


def match_day_process_data(season):
    # ##### Read Data
    buli_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Statistics_{season}.csv", index_col='Unnamed: 0')
    buli_tracking_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Tracking_Statistics_{season}.csv",
                                   index_col='Unnamed: 0')
    buli_gk_df = pd.read_csv(f"./data/Seasons_data//Bundesliga_Gk_Statistics_{season}.csv", index_col='Unnamed: 0')

    # ##### Merge Tracking Statistics to the Main DataFrame
    buli_df['Team'] = buli_df['Team'].map(team_name_1)
    buli_df['Opponent'] = buli_df['Opponent'].map(team_name_1)
    buli_tracking_df['Team'] = buli_tracking_df['Team'].map(team_name_2)
    buli_tracking_df['Opponent'] = buli_tracking_df['Opponent'].map(team_name_2)
    buli_df = pd.merge(buli_df, buli_tracking_df, left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                       right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])

    # ##### Correct Lineup Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))

    # ##### Create Match Day Statistics
    buli_df['Possession'] = np.round(buli_df['Possession'] * 100, 2)
    buli_df['shot_accuracy'] = np.round((buli_df['shots_on_target'] / buli_df['shots_total']) * 100, 1)
    buli_df['successful_dribbles'] = np.round((buli_df['dribbles_completed'] / buli_df['dribbles']) * 100, 1)
    buli_df['successful_tackles'] = np.round((buli_df['tackles_won'] / buli_df['tackles']) * 100, 1)

    # ##### Add Team Goalkeeper Statistics
    buli_gk_df['Team'] = buli_gk_df['Team'].map(team_name_1)
    buli_gk_df['Opponent'] = buli_gk_df['Opponent'].map(team_name_1)
    buli_gk_df['passess_successful_gk'] = np.round(buli_gk_df['passes_gk'] * buli_gk_df['pct_passes_launched_gk'] / 100)
    buli_gk_df['goal_kicks_successful'] = np.round(
        buli_gk_df['goal_kicks'] * buli_gk_df['pct_goal_kicks_launched'] / 100)
    df_team_gk = buli_gk_df.groupby(["Season", "Week_No", "Team", "Opponent", "Venue"])[
        ["shots_on_target_against", "saves", "passes_gk", "passess_successful_gk", "goal_kicks",
         "goal_kicks_successful", "passes_throws_gk"]].sum()
    df_team_gk.reset_index(inplace=True)
    df_team_gk['saves_pct'] = np.round(df_team_gk['saves'] / df_team_gk['shots_on_target_against'] * 100, 2)
    df_team_gk['passess_pct_successful_gk'] = np.round(
        df_team_gk['passess_successful_gk'] / df_team_gk['passes_gk'] * 100, 2)
    df_team_gk['goal_kicks_pct_successful'] = np.round(
        df_team_gk['goal_kicks_successful'] / df_team_gk['goal_kicks'] * 100, 2)
    df_team_gk.drop(columns=['shots_on_target_against'], inplace=True)
    buli_df = pd.merge(buli_df, df_team_gk, left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                       right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])

    season_buli_df = buli_df[buli_df['Season'] == season].reset_index(drop=True)
    return season_buli_df


def match_day_stats(data, home_team, away_team, stats_type, venue):
    if venue == "Home":
        day_stats = data[(data['Team'] == home_team) & (data['Opponent'] == away_team) &
                         (data['Venue'] == 'Home')][stats_type].values[0]
    else:
        day_stats = data[(data['Opponent'] == home_team) & (data['Team'] == away_team) &
                         (data['Venue'] == 'Away')][stats_type].values[0]
    return day_stats


@st.cache
def shot_events_data_day(season, match_day):
    # ##### Read Data
    df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Shot_Events_Statistics_{season}.csv", index_col='Unnamed: 0')
    df['Team'] = df['Team'].map(team_name_3)
    df['Opponent'] = df['Opponent'].map(team_name_3)
    season_df = df[df['Season'] == season].reset_index(drop=True)

    # ##### Format Data
    game_event_data_home = season_df[(season_df['Venue'] == 'Home') & (season_df['Week_No'] == match_day)].reset_index(
        drop=True)
    game_event_data_home['X_cord'] = game_event_data_home['X_cord'] * 105 - 105
    game_event_data_home['X_cord'] = game_event_data_home['X_cord'] * -1
    game_event_data_home['Y_cord'] = game_event_data_home['Y_cord'] * 68 - 68
    game_event_data_home['Y_cord'] = game_event_data_home['Y_cord'] * -1
    game_event_data_away = season_df[(season_df['Venue'] == 'Away') & (season_df['Week_No'] == match_day)].reset_index(
        drop=True)
    game_event_data_away['X_cord'] = game_event_data_away['X_cord'] * 105
    game_event_data_away['Y_cord'] = game_event_data_away['Y_cord'] * 68

    season_shots_event_data = pd.concat([game_event_data_home, game_event_data_away])
    season_shots_event_data['Shot Result'] = np.where(season_shots_event_data['Event'] == 'Goal', 'Goal', 'Shot')
    season_shots_event_data[['X_cord', 'Y_cord', 'xGoal']] = np.round(
        season_shots_event_data[['X_cord', 'Y_cord', 'xGoal']], 3)

    season_shots_event_data.reset_index(drop=True, inplace=True)

    return season_shots_event_data


def day_shot_event_type(data, home_team, away_team):
    # ##### Event Game Type
    game_event_data = data[(data['Team'] == home_team) | (data['Team'] == away_team)].reset_index(drop=True)
    event_type_day = game_event_data['Event'].unique()
    return event_type_day


def shot_events_day_plot(data, home_team, away_team, event_type):
    # ##### Game Event Filter Data
    game_event_data = data[(data['Team'] == home_team) | (data['Team'] == away_team)].reset_index(drop=True)
    final_event_data = game_event_data[game_event_data['Event'].isin(event_type)]

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

    shot_event_fig = sns.scatterplot(data=final_event_data, x="X_cord", y="Y_cord", hue='Shot Result', size="xGoal",
                                     sizes=(100, 1000), style="Event", markers=event_markers, palette=color_dict,
                                     legend=False, alpha=0.7)

    if len(event_type) == 1:
        home_team_events = final_event_data[final_event_data['Venue'] == 'Home'].reset_index(drop=True)
        home_team_events_assists = home_team_events.dropna(subset=['Assist Player']).reset_index(drop=True)
        away_team_events = final_event_data[final_event_data['Venue'] == 'Away'].reset_index(drop=True)
        away_team_events_assists = away_team_events.dropna(subset=['Assist Player']).reset_index(drop=True)

        for i in range(home_team_events.shape[0]):
            shot_event_fig.text(x=home_team_events['X_cord'][i] + 1, y=home_team_events['Y_cord'][i] + 1,
                                s=home_team_events['Player Name'][i],
                                fontdict=dict(color="white", weight='bold', size=10))

        for i in range(away_team_events.shape[0]):
            shot_event_fig.text(x=away_team_events['X_cord'][i] - 10, y=away_team_events['Y_cord'][i] - 2,
                                s=away_team_events['Player Name'][i],
                                fontdict=dict(color="white", weight='bold', size=10))

        if event_type[0] == 'Goal':
            for i in range(home_team_events_assists.shape[0]):
                shot_event_fig.text(x=home_team_events_assists.X_cord[i] + 2, y=home_team_events_assists.Y_cord[i] - 1,
                                    s="Assist: " + home_team_events_assists['Assist Player'][i],
                                    fontdict=dict(color="red", weight='bold', size=10))

            for i in range(away_team_events_assists.shape[0]):
                shot_event_fig.text(x=away_team_events_assists.X_cord[i] - 11, y=away_team_events_assists.Y_cord[i] - 4,
                                    s="Assist: " + away_team_events_assists['Assist Player'][i],
                                    fontdict=dict(color="red", weight='bold', size=10))

    return shot_event_fig
