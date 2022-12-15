import pandas as pd
import numpy as np
from page_scripts.stats_scripts.utilities import season_team_query, season_gk_query

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
general_stats = ["Manager", "Lineup", "Distance Covered (Km)", "Sprints", "Possession", "Duel Aerial Won %",
                 "Offsides", "Corners", "Fouls", "Yellow Cards", "Red Cards"]

general_emoji = ["👨‍💼", "📏", "🚄", "🏃‍", "⚽", "🤼‍", "🚫", "📐", "🤒", "🟨", "🟥"]

# ##### Offensive Statistics
offensive_stats = ["xGoal", "Assists", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %",
                   "Blocked Shots", "Dribbles", "Dribbles %"]

offensive_emoji = ["⚽", "🤝", "🤝⚽", "👟", "🥅", "🎯", "🚫🥅", "⛹️", "⛹️✅"]

# ##### Defensive Statistics
defensive_stats = ["Tackles", "Tackles Won %", "Clearances", "Interceptions", "Ball Recoveries", "Blocks", "Errors"]

defensive_emoji = ["🤼", "🤼✅", "🆑", "🥷", "🤒", "🚫️", "⭕"]

# ##### Passing Statistics
passing_stats = ["Ball Touches", "Passes", "Pass %", "Pass Short %", "Pass Medium %", "Pass Long %", "Final Third",
                 "Crosses", "Crosses PA"]

passing_emoji = ["👟", "🔁", "🔁✅", "🔁✅", "🔁✅", "🔁✅", "🥅", "❎", "❎🥅"]

# ##### Goalkeeper Statistics
gk_stats = ["Saves", "Saves %", "Post-Shot xGoal", "Total Passes", "Goal Kicks", "Throws", "Crosses Stopped",
            "Crosses Stopped %"]

gk_emoji = ["🧤", "🧤✅", "⚽", "🔁", "👟", "🤾", "❎", "❎🚫"]


def match_day_process_data(season):
    # ##### Read Data
    buli_df = season_team_query(season=season)
    buli_gk_df = season_gk_query(season=season)

    # ##### Change Name Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df.rename(columns={"Team_Lineup": "Lineup",
                            "Corner Kicks": "Corners",
                            "Dribbles": "Dribbles",
                            "Dribbles Completed": "Dribbles Completed",
                            "Dribbles Completed %": "Dribbles %",
                            "Passes Completed %": 'Pass %',
                            "Passes Short Completed %": 'Pass Short %',
                            "Passes Medium Completed %": 'Pass Medium %',
                            "Passes Long Completed %": 'Pass Long %',
                            "Passes Final 3rd": 'Final Third'}, inplace=True)

    # ##### Add Team Goalkeeper Statistics
    df_team_gk = \
        buli_gk_df.groupby(["Season", "Week_No", "Team", "Opponent", "Venue"])["Shots on Target",
                                                                               "Saves", "Post-Shot xGoal",
                                                                               "Passes", "Goal Kicks", "Throws",
                                                                               "Crosses Faced", "Crosses Stopped"].sum()

    df_team_gk.reset_index(inplace=True)
    df_team_gk['Saves %'] = np.round(df_team_gk['Saves'] / df_team_gk['Shots on Target'] * 100, 2)
    df_team_gk['Crosses Stopped %'] = np.round(df_team_gk['Crosses Stopped'] / df_team_gk['Crosses Faced'] * 100, 2)
    df_team_gk.drop(columns=['Shots on Target', "Crosses Faced"], inplace=True)
    df_team_gk.rename(columns={"Passes": "Total Passes"}, inplace=True)
    buli_df = pd.merge(buli_df, df_team_gk, left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                       right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])
    season_buli_df = buli_df.reset_index(drop=True)

    return season_buli_df


def match_day_stats(data, home_team, away_team, stats, venue):
    if venue == "Home":
        day_stats = data[(data['Team'] == home_team) & (data['Opponent'] == away_team) &
                         (data['Venue'] == 'Home')][stats].values[0]
    else:
        day_stats = data[(data['Opponent'] == home_team) & (data['Team'] == away_team) &
                         (data['Venue'] == 'Away')][stats].values[0]
    return day_stats
