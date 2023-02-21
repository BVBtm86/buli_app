import pandas as pd
import numpy as np
from joblib import load
import streamlit as st
from page_scripts.stats_scripts.utilities import season_team_query, prediction_query


# ##### Read Data
@st.cache
def season_data_process(season):
    # ##### Season Data
    df_analysis = season_team_query(season=season)
    current_match_day = np.max(df_analysis['Week_No'])
    model_no = df_analysis.groupby(['Venue'])['Team'].value_counts().min()
    if model_no > 5:
        model_no = 5
    return df_analysis, current_match_day, model_no


@st.cache
def data_processing(data, current_match_day, rolling_data):
    # ##### Df & Prediction Data
    df = data.copy()
    buli_prediction = prediction_query()
    buli_prediction = buli_prediction[buli_prediction['Week_No'] > current_match_day].reset_index(drop=True)
    df_home = df[(df['Venue'] == 'Home')].reset_index(drop=True)
    df_away = df[(df['Venue'] == 'Away')].reset_index(drop=True)
    team_stats_names = df.columns[10:]

    # ##### Home Stats
    df_home.drop(columns=['Manager', 'Team_Lineup', 'Opp_Lineup', 'Venue'], inplace=True)
    df_home.rename(columns={'Team': 'Home Team', 'Opponent': 'Away Team', 'Result': 'Home Result'}, inplace=True)
    home_new_cols = [col for col in df_home.columns[:6]]
    home_new_cols.extend([f"{col} Home" for col in df_home.columns[6:]])
    df_home.columns = home_new_cols

    # ##### Away Stats
    df_away.drop(columns=['Manager', 'Team_Lineup', 'Opp_Lineup', 'Venue'], inplace=True)
    df_away.rename(columns={'Team': 'Away Team', 'Opponent': 'Home Team', 'Result': 'Away Result'}, inplace=True)
    away_new_cols = [col for col in df_away.columns[:6]]
    away_new_cols.extend([f"{col} Away" for col in df_away.columns[6:]])
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
    if step == 1:
        final_model = load(open(f"././final_models/Last Game Model.pkl", 'rb'))
        final_transform = load(open(f"././final_models/Last Game Transform.pkl", 'rb'))
    else:
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

    final_results = data[['Week_No', 'Home Team', 'Away Team']].copy()
    final_results['Win %'] = pd.Series(hprob)
    final_results['Draw %'] = pd.Series(dprob)
    final_results['Defeat %'] = pd.Series(aprob)

    final_results = final_results[final_results['Week_No'] == week_no].reset_index(drop=True)

    return final_results, model_features


def create_predictions_season(data, current_data, step):
    # ###### Load Prediction Data
    if step == 1:
        final_model = load(open(f"././final_models/Last Game Model.pkl", 'rb'))
        final_transform = load(open(f"././final_models/Last Game Transform.pkl", 'rb'))
    else:
        final_model = load(open(f"././final_models/Last {step} Games Model.pkl", 'rb'))
        final_transform = load(open(f"././final_models/Last {step} Games Transform.pkl", 'rb'))
    model_features = list(final_transform.get_feature_names_out())

    # ##### Predictions
    prediction_data = data[model_features]
    prediction_transformed = final_transform.transform(prediction_data)
    prediction_results = final_model.predict(prediction_transformed)
    final_results = data[['Week_No', 'Home Team', 'Away Team']].copy()
    final_results['Predicted Result'] = pd.Series(prediction_results)
    final_results['Result'] = final_results['Predicted Result'].map({0: 2, 1: 1, 2: 0})

    # ##### Home and Away Data
    home_df = final_results[['Home Team', 'Predicted Result']].rename(
        columns={"Home Team": "Team", "Predicted Result": "Result"})
    away_df = final_results[['Away Team', 'Result']].rename(columns={"Away Team": "Team"})
    predicted_tab = pd.concat([home_df, away_df])

    # ##### Merge with current Data
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
