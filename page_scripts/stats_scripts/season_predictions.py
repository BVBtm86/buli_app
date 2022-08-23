import pandas as pd
import numpy as np
from joblib import load
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
                   "carry_progressive_distance"]

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
                    "Carries Penalty Area", "Carries Distance", "Carries Progressive Distance"]

main_columns = dict(zip(team_stats_vars, team_stats_names))


# ##### Read Data
@st.cache
def season_data_process(season):
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

    model_no = buli_df.groupby(['Venue'])['Team'].value_counts().min()
    if model_no > 5:
        model_no = 5
    return df_analysis, current_match_day, model_no


@st.cache
def data_processing(data, current_match_day, rolling_data):
    buli_prediction = pd.read_csv("././data/Season_Prediction_Games.csv")
    buli_prediction = buli_prediction[buli_prediction['Week_No'] > current_match_day].reset_index(drop=True)
    df_home = data[(data['Venue'] == 'Home')].reset_index(drop=True)
    df_away = data[(data['Venue'] == 'Away')].reset_index(drop=True)

    # ##### Home Stats
    df_home.drop(columns=['Manager', 'Team_Lineup', 'Opp_Lineup', 'Venue'], inplace=True)
    df_home.rename(columns={'Team': 'Home Team', 'Opponent': 'Away Team', 'Result': 'Home Result'}, inplace=True)
    home_new_cols = [col for col in df_home.columns[:5]]
    home_new_cols.extend([f"{col} Home" for col in df_home.columns[5:]])
    df_home.columns = home_new_cols

    # ##### Away Stats
    df_away.drop(columns=['Manager', 'Team_Lineup', 'Opp_Lineup', 'Venue'], inplace=True)
    df_away.rename(columns={'Team': 'Away Team', 'Opponent': 'Home Team', 'Result': 'Away Result'}, inplace=True)
    away_new_cols = [col for col in df_away.columns[:5]]
    away_new_cols.extend([f"{col} Away" for col in df_away.columns[5:]])
    df_away.columns = away_new_cols

    if rolling_data == 1:
        final_df_home = pd.DataFrame()
        for home in df_home['Home Team'].unique():
            df_home_filter = df_home[df_home['Home Team'] == home].drop(
                columns=['Week_No', 'Season', 'Away Team', 'Home Result'])
            df_home_filter = pd.DataFrame(df_home_filter.iloc[-1, :]).T
            final_df_home = pd.concat([final_df_home, df_home_filter])

        final_df_away = pd.DataFrame()
        for away in df_away['Away Team'].unique():
            df_away_filter = df_away[df_away['Away Team'] == away].drop(
                columns=['Week_No', 'Season', 'Home Team', 'Away Result'])
            df_away_filter = pd.DataFrame(df_away_filter.iloc[-1, :]).T
            final_df_away = pd.concat([final_df_away, df_away_filter])
    else:
        final_df_home = pd.DataFrame()
        for home in df_home['Home Team'].unique():
            home_filter = df_home[df_home['Home Team'] == home].drop(
                columns=['Week_No', 'Season', 'Away Team', 'Home Result'])
            df_home_filter = home_filter.groupby(['Home Team'])[[f"{col} Home" for col in team_stats_names]].rolling(
                rolling_data).mean().dropna(subset=['Distance Covered (Km) Home']).reset_index()
            df_home_filter = pd.DataFrame(df_home_filter.iloc[-1, :]).T
            final_df_home = pd.concat([final_df_home, df_home_filter])

        final_df_away = pd.DataFrame()
        for away in df_away['Away Team'].unique():
            away_filter = df_away[df_away['Away Team'] == away].drop(
                columns=['Week_No', 'Season', 'Home Team', 'Away Result'])
            df_away_filter = away_filter.groupby(['Away Team'])[[f"{col} Away" for col in team_stats_names]].rolling(
                rolling_data).mean().dropna(subset=['Distance Covered (Km) Away']).reset_index()
            df_away_filter = pd.DataFrame(df_away_filter.iloc[-1, :]).T
            final_df_away = pd.concat([final_df_away, df_away_filter])

    prediction_df = pd.merge(buli_prediction, final_df_home, on='Home Team')
    prediction_df = pd.merge(prediction_df, final_df_away, on='Away Team')
    prediction_df = prediction_df.sort_values(by='Week_No').reset_index(drop=True)

    for col in team_stats_names:
        home_stat = prediction_df[f'{col} Home']
        away_stat = prediction_df[f'{col} Away']
        prediction_df[col] = home_stat - away_stat

    # ##### Final Data
    final_cols = ['Week_No', 'Home Team', 'Away Team']
    final_cols.extend(team_stats_names)
    final_df = prediction_df[final_cols]

    return final_df


def data_prediction_game(data, step, week_no):

    # ###### Load Prediction Data
    final_model = load(open(f"././final_models/Last {step} Games Model.pkl", 'rb'))
    final_transform = load(open(f"././final_models/Last {step} Games Transform.pkl", 'rb'))
    model_features = list(final_transform.get_feature_names_out())

    # ##### Predictions
    prediction_data = data[model_features]
    prediction_transformed = final_transform.transform(prediction_data)
    prediction_prob = final_model.predict_proba(prediction_transformed)
    hprob = [np.round(prediction_prob[i][2] * 100, 2) for i in range(len(prediction_prob))]
    dprob = [np.round(prediction_prob[i][1] * 100, 2) for i in range(len(prediction_prob))]
    aprob = [np.round(prediction_prob[i][0] * 100, 2) for i in range(len(prediction_prob))]

    final_results = data[['Week_No', 'Home Team', 'Away Team']]
    final_results['Win %'] = pd.Series(hprob)
    final_results['Draw %'] = pd.Series(dprob)
    final_results['Defeat %'] = pd.Series(aprob)

    final_results = final_results[final_results['Week_No'] == week_no].reset_index(drop=True)

    return final_results, model_features


def create_predictions_season(data, current_data, step):
    # ###### Load Prediction Data
    final_model = load(open(f"././final_models/Last {step} Games Model.pkl", 'rb'))
    final_transform = load(open(f"././final_models/Last {step} Games Transform.pkl", 'rb'))
    model_features = list(final_transform.get_feature_names_out())

    # ##### Predictions
    prediction_data = data[model_features]
    prediction_transformed = final_transform.transform(prediction_data)
    prediction_results = final_model.predict(prediction_transformed)
    final_results = data[['Week_No', 'Home Team', 'Away Team']]
    final_results['Predicted Result'] = pd.Series(prediction_results)

    # ##### Merge with current Data
    predicted_tab = pd.melt(final_results, id_vars=["Predicted Result"], value_vars=["Home Team", "Away Team"])
    predicted_tab = predicted_tab[['value', 'Predicted Result']]
    predicted_tab.columns = ['Team', 'Result']
    predicted_tab['Result'] = predicted_tab['Result'].map({0: "Defeat", 1: "Draw", 2: "Win"})

    season_predicted = pd.concat([current_data[['Team', "Result"]], predicted_tab])

    # ##### Create Current Table
    season_predicted['Win'] = np.where(season_predicted['Result'] == 'Win', 1, 0)
    season_predicted['Draw'] = np.where(season_predicted['Result'] == 'Draw', 1, 0)
    season_predicted['Defeat'] = np.where(season_predicted['Result'] == 'Defeat', 1, 0)
    season_tab = season_predicted[['Team', 'Result', 'Win', 'Draw', 'Defeat']]

    # ##### Final Season Tab
    season_tab['Total'] = 1
    final_predict_tab = season_tab.groupby(['Team'])[['Total', 'Win', 'Draw', 'Defeat']].sum()
    final_predict_tab['Points'] = final_predict_tab['Win'] * 3 + final_predict_tab['Draw']
    final_predict_tab.sort_values(by=['Points', 'Win'], ascending=[False, False], inplace=True)
    final_predict_tab.reset_index(inplace=True)
    final_predict_tab['Rank'] = [i for i in range(1, len(final_predict_tab) + 1)]
    final_predict_tab.set_index('Rank', inplace=True)
    final_predict_tab.columns = ["Team", "MP", "W", "D", "L", "Pts"]

    return final_predict_tab, model_features
