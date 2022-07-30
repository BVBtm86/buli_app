import pandas as pd
import numpy as np
from pickle import load
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
               "VfL Bochum 1848": "VfL Bochum 1848", "Borussia M'gladbach": "Borussia Mönchengladbach"}

team_stats_vars = ["goals", "assists", "assisted_shots", "xg", "xa", "Distance_Covered", "Sprints", "Possession",
                   "shots_total", "shots_on_target", "shot_accuracy", "aerials_won", "aerials_won_pct", "crosses",
                   "corner_kicks", "offsides", "cards_yellow", "fouls", "fouled", "tackles", "tackles_won",
                   "successful_tackles", "tackles_def_3rd", "tackles_mid_3rd", "tackles_att_3rd", "pressures",
                   "pressure_regains", "pressure_regain_pct", "pressures_def_3rd", "pressures_mid_3rd",
                   "pressures_att_3rd", "ball_recoveries", "interceptions", "blocks", "clearances", "dispossessed",
                   "errors", "sca", "dribbles_completed", "dribbles", "successful_dribbles",
                   "crosses_into_penalty_area", "through_balls", "passes", "passes_completed", "passes_pct",
                   "progressive_passes", "passes_pressure", "passes_short", "passes_completed_short",
                   "passes_pct_short", "passes_medium", "passes_completed_medium", "passes_pct_medium", "passes_long",
                   "passes_completed_long", "passes_pct_long", "passes_into_final_third", "passes_into_penalty_area",
                   "passes_total_distance", "passes_progressive_distance", "touches", "touches_def_pen_area",
                   "touches_def_3rd", "touches_mid_3rd", "touches_att_3rd", "touches_att_pen_area", "carries",
                   "progressive_carries", "carries_into_final_third", "carries_into_penalty_area", "carry_distance",
                   "carry_progressive_distance", "saves", "saves_pct", "passes_gk", "passess_successful_gk",
                   "goal_kicks", "goal_kicks_successful"]

team_stats_names = ["Goals", "Assists", "Key Passes", "xGoals", "xAssisted", "Distance Covered (Km)", "Sprint",
                    "Possession", "Shots", "Shots On Target", "Shot Accuracy %", "Aerials Won", "Aerials Won %",
                    "Crosses", "Corners", "Offsides", "Yellow Cards", "Fouls", "Fouled", "Tackles", "Tackles Won",
                    "Tackles Won %", "Tackles Def 3rd", "Tackles Mid 3rd", "Tackles Att 3rd", "Pressure",
                    "Pressure Regains", "Pressure Regains Successful %", "Pressure Def 3rd", "Pressure Mid 3rd",
                    "Pressure Att 3rd", "Ball Recoveries", "Interceptions", "Blocks", "Clearences", "Dispossessed",
                    "Errors", "Shot Created Actions", "Dribbles", "Dribbles Successful", "Dribbles Successful %",
                    "Crosses Penalty Area", "Through Balls", "Passes", "Completed Passes", "Completed Passes %",
                    "Progressive Passes", "Passes Under Pressure", "Passes Short", "Passes Short Completed",
                    "Passes Short Completed %", "Passes Medium", "Passes Medium Completed", "Passes Medium Completed %",
                    "Passes Long", "Passes Long Completed", "Passes Long Completed %", "Passes Final Third",
                    "Passes Penalty Area", "Passes Distance", "Passes Progresive Distance", "Touches",
                    "Touches Def Pen Area", "Touches Def 3rd", "Touches Mid 3rd", "Touches Att 3rd",
                    "Touches Att Pen Area", "Carries", "Progressive Carries", "Carries Final 3rd",
                    "Carries Penalty Area", "Carries Distance", "Carries Progressive Distance", "Saves", "Saves %",
                    "GK Passes", "GK Passes Successful %", "Goal Kicks", "Goal Kicks Successful %"]

main_columns = dict(zip(team_stats_vars, team_stats_names))


# ##### Read Data
@st.cache(allow_output_mutation=True)
def season_data_process(season):
    # ###### Load Prediction Data
    final_model = load(open('././final_models/final_model.pkl', 'rb'))
    final_transform = load(open('././final_models/final_transform.pkl', 'rb'))
    feature_importance = pd.read_csv("././final_models/Final Feature Importance.csv", index_col='Features')
    model_features = feature_importance.index.to_list()
    prediction_game_df = pd.read_csv("././data/Season_Prediction_Games.csv")
    prediction_data = pd.read_csv("././data/New_Predictions_df.csv")

    default_steps = prediction_data[prediction_data['Accuracy'] == prediction_data['Accuracy'].max()][
        ['Home Steps', 'Away Steps']].values[0]
    home_default = int(default_steps[0] - 1)
    away_default = int(default_steps[1] - 1)

    # ##### Read Data
    buli_df = pd.read_csv(f"././data/Seasons_data/Bundesliga_Team_Statistics_{season}.csv", index_col='Unnamed: 0')
    buli_tracking_df = pd.read_csv(f"././data/Seasons_data/Bundesliga_Team_Tracking_Statistics_{season}.csv",
                                   index_col='Unnamed: 0')

    # ##### Merge Tracking Statistics to the Main DataFrame
    buli_df['Team'] = buli_df['Team'].map(team_name_1)
    buli_df['Opponent'] = buli_df['Opponent'].map(team_name_1)
    buli_tracking_df['Team'] = buli_tracking_df['Team'].map(team_name_2)
    buli_tracking_df['Opponent'] = buli_tracking_df['Opponent'].map(team_name_2)
    df_analysis = pd.merge(buli_df, buli_tracking_df, left_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'],
                           right_on=['Season', 'Week_No', 'Team', 'Opponent', 'Venue'])

    # ##### Create Match Day Statistics
    df_analysis['Possession'] = np.round(df_analysis['Possession'] * 100, 2)
    df_analysis['shot_accuracy'] = np.round((df_analysis['shots_on_target'] / df_analysis['shots_total']) * 100, 1)
    df_analysis['successful_dribbles'] = np.round((df_analysis['dribbles_completed'] / df_analysis['dribbles']) * 100,
                                                  1)
    df_analysis['successful_tackles'] = np.round((df_analysis['tackles_won'] / df_analysis['tackles']) * 100, 1)
    df_analysis.rename(columns=main_columns, inplace=True)
    current_match_day = np.max(df_analysis['Week_No'])

    return df_analysis, current_match_day, season, final_model, final_transform, model_features, prediction_game_df, \
           prediction_data, home_default, away_default


@st.cache
def transform_data(data, features, scalar):
    # ##### Final Variables
    group_vars = ["Season", "Week_No", "Team", "Opponent", "Venue", "Result"]
    group_vars.extend(features)
    work_df = data.copy()

    # #### Create Home Data for Analysis
    home_data = work_df[work_df["Venue"] == "Home"][group_vars]
    home_name = ["Home " + col for col in features]
    home_data.rename(columns=dict(zip(features, home_name)), inplace=True)
    home_data.rename(columns={"Team": "Home Team", "Opponent": "Away Team"}, inplace=True)

    # #### Create Away Data for Analysis
    away_data = work_df[work_df["Venue"] == "Away"][group_vars]
    away_name = ["Away " + col for col in features]
    away_data.rename(columns=dict(zip(features, away_name)), inplace=True)
    away_data.drop(columns=['Result', 'Venue'], inplace=True)
    away_data.rename(columns={"Team": "Away Team", "Opponent": "Home Team"}, inplace=True)

    # ##### Home / Away Data
    final_model_features = home_name + away_name
    model_df = pd.merge(home_data, away_data,
                        left_on=["Season", "Week_No", "Home Team", "Away Team"],
                        right_on=["Season", "Week_No", "Home Team", "Away Team"])

    # ##### Transformed Data
    model_df[final_model_features] = scalar.transform(model_df[final_model_features])
    model_df.drop(columns='Venue', inplace=True)

    index_agg_home_team = np.min(model_df.groupby(by='Home Team').count()['Season'])
    index_agg_away_team = np.min(model_df.groupby(by='Away Team').count()['Season'])

    return model_df, final_model_features, index_agg_home_team, index_agg_away_team


def game_prediction_teams(data, features, match_day, games_predict, home_agg_steps, away_agg_steps, predict_data,
                          model):
    # ##### Prediction Data
    home_agg_function, away_agg_function = predict_data[(predict_data['Home Steps'] == home_agg_steps)
                                                        & (predict_data['Away Steps'] == away_agg_steps)][
        'Agg Function'].values[0].split('-')

    accuracy_combo = np.round(predict_data[(predict_data['Home Steps'] == home_agg_steps) &
                                           (predict_data['Away Steps'] == away_agg_steps)]['Accuracy'].values[0], 1)

    # ##### Prediction df
    prediction_df = games_predict[games_predict['Week_No'] == match_day].reset_index(drop=True)
    prediction_df['Game_No'] = [i for i in range(1, len(prediction_df) + 1)]

    # ##### Create Home/Away Teams
    home_team_names = list(prediction_df['Home Team'].values)
    away_team_names = list(prediction_df['Away Team'].values)

    # ##### Create Home/Away Aggregate
    cutoff = int(len(features) / 2)
    home_team = data.groupby('Home Team').rolling(home_agg_steps)[features[:cutoff]].agg(home_agg_function). \
        reset_index()
    home_team['Last_Stats'] = np.where(home_team['Home Team'].duplicated(keep='last'), 0, 1)
    home_stats = home_team[home_team['Last_Stats'] == 1].reset_index(drop=True)
    home_stats.drop(columns=['level_1', 'Last_Stats'], inplace=True)

    away_team = data.groupby('Away Team').rolling(away_agg_steps)[features[cutoff:]].agg(away_agg_function). \
        reset_index()
    away_team['Last_Stats'] = np.where(away_team['Away Team'].duplicated(keep='last'), 0, 1)
    away_stats = away_team[away_team['Last_Stats'] == 1].reset_index(drop=True)
    away_stats.drop(columns=['level_1', 'Last_Stats'], inplace=True)

    # ##### Add Stats to New Games
    prediction_games = pd.merge(prediction_df, home_stats, on='Home Team')
    prediction_games = pd.merge(prediction_games, away_stats, on='Away Team')
    prediction_games.sort_values(by='Game_No', inplace=True)

    # ##### Prediction
    final_proba = model.predict_proba(prediction_games[features].values)
    hprob = [np.round(final_proba[i][2] * 100, 2) for i in range(9)]
    dprob = [np.round(final_proba[i][1] * 100, 2) for i in range(9)]
    aprob = [np.round(final_proba[i][0] * 100, 2) for i in range(9)]

    return home_team_names, away_team_names, hprob, dprob, aprob, accuracy_combo


def create_predictions_season(season_data, data, games_predict, home_agg_steps, away_agg_steps, final_features,
                              match_day, predict_data, model):
    # ##### Prediction Data
    home_agg_function, away_agg_function = predict_data[(predict_data['Home Steps'] == home_agg_steps)
                                                        & (predict_data['Away Steps'] == away_agg_steps)][
        'Agg Function'].values[0].split('-')

    accuracy_combo = np.round(predict_data[(predict_data['Home Steps'] == home_agg_steps) &
                                           (predict_data['Away Steps'] == away_agg_steps)]['Accuracy'].values[0], 1)

    # ##### Prediction df
    prediction_df = games_predict[games_predict['Week_No'] > match_day].reset_index(drop=True)
    prediction_df['Game_No'] = [i for i in range(1, len(prediction_df) + 1)]

    # ##### Create Home/Away Aggregate
    cutoff = int(len(final_features) / 2)
    home_team = data.groupby('Home Team').rolling(home_agg_steps)[final_features[:cutoff]].agg(home_agg_function). \
        reset_index()
    home_team['Last_Stats'] = np.where(home_team['Home Team'].duplicated(keep='last'), 0, 1)
    home_stats = home_team[home_team['Last_Stats'] == 1].reset_index(drop=True)
    home_stats.drop(columns=['level_1', 'Last_Stats'], inplace=True)

    away_team = data.groupby('Away Team').rolling(away_agg_steps)[final_features[cutoff:]].agg(away_agg_function). \
        reset_index()
    away_team['Last_Stats'] = np.where(away_team['Away Team'].duplicated(keep='last'), 0, 1)
    away_stats = away_team[away_team['Last_Stats'] == 1].reset_index(drop=True)
    away_stats.drop(columns=['level_1', 'Last_Stats'], inplace=True)

    # ##### Add Stats to New Games
    prediction_games = pd.merge(prediction_df, home_stats, on='Home Team')
    prediction_games = pd.merge(prediction_games, away_stats, on='Away Team')
    prediction_games.sort_values(by='Game_No', inplace=True)

    # ##### Prediction
    prediction_games['Home Result'] = model.predict(prediction_games[final_features].values)
    prediction_games['Away Result'] = np.where(prediction_games['Home Result'] == 2, 0,
                                               np.where(prediction_games['Home Result'] == 1, 1, 2))

    # ##### Create Predicted Table
    home_predict_tab = prediction_games[['Home Team', 'Home Result']]
    away_predict_tab = prediction_games[['Away Team', 'Away Result']]
    home_predict_tab.rename(columns={'Home Team': 'Team', 'Home Result': 'Result'}, inplace=True)
    away_predict_tab.rename(columns={'Away Team': 'Team', 'Away Result': 'Result'}, inplace=True)
    predict_tab = pd.concat([home_predict_tab, away_predict_tab], axis=0)
    predict_tab['Win'] = np.where(predict_tab['Result'] == 2, 1, 0)
    predict_tab['Draw'] = np.where(predict_tab['Result'] == 1, 1, 0)
    predict_tab['Defeat'] = np.where(predict_tab['Result'] == 0, 1, 0)

    # ##### Create Current Table
    season_data['Win'] = np.where(season_data['Result'] == 'Win', 1, 0)
    season_data['Draw'] = np.where(season_data['Result'] == 'Draw', 1, 0)
    season_data['Defeat'] = np.where(season_data['Result'] == 'Defeat', 1, 0)
    current_tab = season_data[['Team', 'Result', 'Win', 'Draw', 'Defeat']]

    # ##### Create Final Table
    final_predict_tab = pd.concat([current_tab, predict_tab], axis=0)
    final_predict_tab['Total'] = 1
    final_predict_tab = final_predict_tab.groupby(['Team'])[['Total', 'Win', 'Draw', 'Defeat']].sum()
    final_predict_tab['Points'] = final_predict_tab['Win'] * 3 + final_predict_tab['Draw']
    final_predict_tab.sort_values(by=['Points', 'Win'], ascending=[False, False], inplace=True)
    final_predict_tab.reset_index(inplace=True)
    final_predict_tab['Rank'] = [i for i in range(1, len(final_predict_tab) + 1)]
    final_predict_tab.set_index('Rank', inplace=True)
    final_predict_tab.columns = ["Team", "MP", "W", "D", "L", "Pts"]

    return final_predict_tab, accuracy_combo