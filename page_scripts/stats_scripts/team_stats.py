import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

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
                    "Pressure Att 3rd", "Ball Recoveries", "Interceptions", "Blocks", "Clearances", "Dispossessed",
                    "Errors", "Shot Created Actions", "Dribbles", "Dribbles Successful", "Dribbles Successful %",
                    "Crosses Penalty Area", "Through Balls", "Passes", "Completed Passes", "Completed Passes %",
                    "Progressive Passes", "Passes Under Pressure", "Passes Short", "Passes Short Completed",
                    "Passes Short Completed %", "Passes Medium", "Passes Medium Completed", "Passes Medium Completed %",
                    "Passes Long", "Passes Long Completed", "Passes Long Completed %", "Passes Final Third",
                    "Passes Penalty Area", "Passes Distance", "Passes Progressive Distance", "Touches",
                    "Touches Def Pen Area", "Touches Def 3rd", "Touches Mid 3rd", "Touches Att 3rd",
                    "Touches Att Pen Area", "Carries", "Progressive Carries", "Carries Final 3rd",
                    "Carries Penalty Area", "Carries Distance", "Carries Progressive Distance", "Saves", "Saves %",
                    "GK Passes", "GK Passes Successful %", "Goal Kicks", "Goal Kicks Successful %"]


@st.cache
def season_data_process(season, stat_type):
    # ##### Read Data
    if stat_type == "Season Stats":
        buli_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Statistics_{season}.csv", index_col='Unnamed: 0')
        buli_tracking_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Tracking_Statistics_{season}.csv",
                                       index_col='Unnamed: 0')
        buli_gk_df = pd.read_csv(f"./data/Seasons_data/Bundesliga_Gk_Statistics_{season}.csv", index_col='Unnamed: 0')
    else:
        buli_df = pd.read_csv("./data/Full_Seasons_data/Bundesliga_Team_Statistics.csv",
                              index_col='Unnamed: 0')
        buli_tracking_df = pd.read_csv("./data/Full_Seasons_data/Bundesliga_Team_Tracking_Statistics.csv",
                                       index_col='Unnamed: 0')
        buli_gk_df = pd.read_csv("./data/Full_Seasons_data/Bundesliga_Gk_Statistics.csv",
                                 index_col='Unnamed: 0')

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

    # ##### Add Filter Type Stats
    buli_df['Total'] = 1
    buli_df['Home'] = np.where(buli_df['Venue'] == "Home", 1, 0)
    buli_df['Away'] = np.where(buli_df['Venue'] == "Away", 1, 0)
    buli_df["1st Period"] = np.where(buli_df["Week_No"] <= 17, 1, 0)
    buli_df["2nd Period"] = np.where(buli_df["Week_No"] >= 18, 1, 0)
    buli_df["Win"] = np.where(buli_df["Result"] == 'Win', 1, 0)
    buli_df["Draw"] = np.where(buli_df["Result"] == 'Draw', 1, 0)
    buli_df["Defeat"] = np.where(buli_df["Result"] == 'Defeat', 1, 0)

    # ##### Goals Statistics
    home_df = buli_df[buli_df['Venue'] == 'Home']
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away']
    away_df.reset_index(drop=True, inplace=True)
    home_df['goals'] = home_df['goals'] + away_df['own_goals']
    away_df['goals'] = away_df['goals'] + home_df['own_goals']
    final_df = pd.concat([home_df, away_df])

    return final_df


def teams_season_stats(data, stat_name, stat_filter, team_type):
    # #### Filter Season Data by Season Type
    filter_team_stat = data[data[stat_filter] == 1].reset_index(drop=True)

    # ##### Rename Stat Name
    filter_team_stat.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)

    # ##### Create Team Chart
    if team_type == 'Team':
        data_plot = filter_team_stat.groupby('Team')[stat_name].mean().round(2).sort_values(
            ascending=False).reset_index()
    else:
        data_plot = filter_team_stat.groupby('Opponent')[stat_name].mean().round(2).sort_values(
            ascending=True).reset_index()

    min_value_team = np.min(data_plot[stat_name]) * 0.8
    if min_value_team < 5:
        min_value_team = 0
    max_value_team = np.max(data_plot[stat_name]) * 1.05
    if team_type == 'Team':
        season_fig = px.bar(data_plot,
                            x="Team",
                            y=stat_name,
                            text=stat_name,
                            title=f"Team Avg <b>{stat_name}</b> per game for <b>{stat_filter}</b> Season Games")
    else:
        season_fig = px.bar(data_plot,
                            x="Opponent",
                            y=stat_name,
                            text=stat_name,
                            title=f"Opponent Avg <b>{stat_name}</b> per game for <b>{stat_filter}</b> Season Games")

    season_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value_team, max_value_team]
    )
    season_fig.update_traces(marker_color='rgb(200,11,1)')
    season_fig.update_yaxes(title_text=f"Avg {stat_name} per Game")

    avg_value = np.round(np.mean(data_plot[stat_name]), 2)
    if team_type == 'Team':
        better_avg = np.sum(data_plot[stat_name] > avg_value)
    else:
        better_avg = np.sum(data_plot[stat_name] < avg_value)
    return season_fig, avg_value, better_avg


def teams_charts_day(data, team, stat_name, stat_filter):
    # ##### Filter Season Data by Season Type
    filter_df_team = data[(data['Team'] == team)].reset_index(drop=True)
    filter_df_opp = data[(data['Opponent'] == team)].reset_index(drop=True)

    # ##### Rename Stat Name
    filter_df_team.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)
    filter_df_opp.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)

    filter_team_stat = filter_df_team[filter_df_team[stat_filter] == 1].reset_index(drop=True)
    if stat_filter == 'Home':
        filter_opp_stat = filter_df_opp[filter_df_opp['Away'] == 1].reset_index(drop=True)
    elif stat_filter == 'Away':
        filter_opp_stat = filter_df_opp[filter_df_opp['Home'] == 1].reset_index(drop=True)
    else:
        filter_opp_stat = filter_df_opp[filter_df_opp[stat_filter] == 1].reset_index(drop=True)

    filter_team_stat = filter_team_stat.sort_values(by='Week_No')
    filter_team_stat.reset_index(drop=True, inplace=True)
    filter_opp_stat = filter_opp_stat.sort_values(by='Week_No')
    filter_opp_stat.reset_index(drop=True, inplace=True)

    # ##### Create Team Chart
    filter_team_stat['TEAM'] = filter_team_stat['Team']
    filter_opp_stat['TEAM'] = "Opponent"
    filter_team_stat['Game'] = [i for i in range(1, len(filter_team_stat) + 1)]
    filter_opp_stat['Game'] = [i for i in range(1, len(filter_opp_stat) + 1)]
    plot_data = pd.concat([filter_team_stat, filter_opp_stat])
    min_value = np.min(plot_data[stat_name]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(plot_data[stat_name]) * 1.1
    fig = px.bar(plot_data,
                 x="Game",
                 y=stat_name,
                 color="Result",
                 facet_col="TEAM",
                 color_discrete_map={
                     'Win': "rgb(200,11,1)",
                     'Draw': "rgb(179, 179, 179)",
                     'Defeat': "rgb(78,78,80)"},
                 text=stat_name,
                 hover_name='Team',
                 )
    fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)",
    },
        xaxis1=dict(
            tickmode='array',
            tickvals=[i for i in range(1, len(filter_team_stat) + 1)],
            ticktext=plot_data['Game'].unique(),
        ),
        xaxis2=dict(
            tickmode='array',
            tickvals=[i for i in range(1, len(filter_team_stat) + 1)],
            ticktext=plot_data['Game'].unique(),
        ),
        yaxis_range=[min_value, max_value]
    )
    fig.update_yaxes(title_text=stat_name, col=1)

    # #### Statistics
    avg_team = np.round(filter_team_stat[stat_name].mean(), 2)
    avg_opp = np.round(filter_opp_stat[stat_name].mean(), 2)
    better = np.round(np.sum(filter_team_stat[stat_name] > filter_opp_stat[stat_name]) / len(filter_opp_stat) * 100, 2)
    stat_sig = ttest_ind(filter_team_stat[stat_name].values,
                         filter_opp_stat[stat_name].values)[1]

    if len(filter_team_stat) >= 10:
        if stat_sig <= 0.05:
            if avg_team > avg_opp:
                stat_sig_name = "Statistically Better"
            elif avg_team < avg_opp:
                stat_sig_name = "Statistically Worse"
            else:
                stat_sig_name = ""
        else:
            stat_sig_name = ""
    else:
        stat_sig_name = ""

    return fig, avg_team, avg_opp, better, stat_sig_name


def teams_season_type(data, team, stat_name):
    # ##### Filter Season Data by Season Type
    filter_df_team = data[(data['Team'] == team)].reset_index(drop=True)
    filter_df_opp = data[(data['Opponent'] == team)].reset_index(drop=True)

    # ##### Rename Stat Name
    filter_df_team.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)
    filter_df_opp.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)

    # ##### Stats Type Results
    stats_types_team = ['Total', 'Home', 'Away', '1st Period', '2nd Period', 'Win', 'Draw', 'Defeat']
    stats_types_opp = ['Total', 'Away', 'Home', '1st Period', '2nd Period', 'Defeat', 'Draw', 'Win']

    results_stats = []
    results_names = []
    results_team = []
    for i in range(len(stats_types_team)):
        df_team = filter_df_team[filter_df_team[stats_types_team[i]] == 1]
        df_opp = filter_df_opp[filter_df_opp[stats_types_opp[i]] == 1]
        if len(df_team) > 0:
            results_names.append(stats_types_team[i])
            results_stats.append(np.round(
                df_team.groupby(stats_types_team[i])[stat_name].mean().values[-1], 2))
            results_team.append(team)
        if len(df_opp) > 0:
            results_names.append(stats_types_team[i])
            results_stats.append(
                np.round(df_opp.groupby(stats_types_opp[i])[stat_name].mean().values[-1], 2))
            results_team.append("Opponent")

    data_season_type = pd.DataFrame([results_names, results_team, results_stats]).T
    data_season_type.columns = ['Type', 'Team', stat_name]
    min_value = np.min(data_season_type[stat_name]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(data_season_type[stat_name]) * 1.1

    # ##### Plot Data
    team_stat_fig = px.bar(data_season_type,
                           x="Type",
                           y=stat_name,
                           color="Team",
                           barmode='group',
                           color_discrete_map={
                               team: "rgb(200,11,1)",
                               'Opponent': "rgb(179, 179, 179)"},
                           text=stat_name,
                           title=f"<b>{team}</b> {stat_name} per game by Different Season Type Games")
    team_stat_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    team_stat_fig.update_yaxes(title_text=stat_name)

    # ##### Stats for markdown
    team_home_data = \
        data_season_type[(data_season_type['Team'] == team) & (data_season_type['Type'] == 'Home')][stat_name].values
    team_away_data = \
        data_season_type[(data_season_type['Team'] == team) & (data_season_type['Type'] == 'Away')][stat_name].values
    if team_home_data[0] > team_away_data[0]:
        team_data_name = ['Home', 'Away']
        team_value_1 = team_home_data[0]
        team_value_2 = team_away_data[0]
    else:
        team_data_name = ['Away', 'Home']
        team_value_1 = team_away_data[0]
        team_value_2 = team_home_data[0]

    if "2nd Period" in data_season_type['Type'].values:
        team_half1_data = \
            data_season_type[(data_season_type['Team'] == team) & (data_season_type['Type'] == '1st Period')][
                stat_name].values
        team_half2_data = \
            data_season_type[(data_season_type['Team'] == team) & (data_season_type['Type'] == '2nd Period')][
                stat_name].values
        if team_half1_data[0] >= team_half2_data[0]:
            team_part_name = ['1st Period', '2nd Period']
            team_value_3 = team_half1_data[0]
            team_value_4 = team_half2_data[0]
        elif team_half1_data[0] < team_half2_data[0]:
            team_part_name = ['2nd Period', '1st Period']
            team_value_3 = team_half2_data[0]
            team_value_4 = team_half1_data[0]
    else:
        team_part_name = ""
        team_value_3 = np.nan
        team_value_4 = np.nan

    return team_stat_fig, team_data_name, team_value_1, team_value_2, team_part_name, team_value_3, team_value_4


def relationship_data(data, team, filter_type, stat_x, stat_y, stat_size, ols_line):
    # ##### Filter Season Data by Season Type
    if team != 'All Teams':
        filter_df_team = data[(data['Team'] == team)].reset_index(drop=True)
    else:
        filter_df_team = data.copy()
    final_df = filter_df_team[filter_df_team[filter_type] == 1].reset_index(drop=True)

    # ##### Rename Stat Name
    final_df.rename(columns={team_stats_vars[team_stats_names.index(stat_x)]: stat_x}, inplace=True)
    final_df.rename(columns={team_stats_vars[team_stats_names.index(stat_y)]: stat_y}, inplace=True)
    final_df.rename(columns={team_stats_vars[team_stats_names.index(stat_size)]: stat_size}, inplace=True)

    # ##### Relationship Chart
    if ols_line:
        relationship_fig = px.scatter(final_df,
                                      x=stat_x,
                                      y=stat_y,
                                      color="Result",
                                      trendline="ols",
                                      trendline_scope="overall",
                                      color_discrete_map={
                                          'Win': "rgb(200,11,1)",
                                          'Draw': "rgb(179, 179, 179)",
                                          'Defeat': "rgb(78,78,80)"},
                                      size=stat_size,
                                      title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship for <b>{filter_type}</b> "
                                            f"Season Games")
    else:
        relationship_fig = px.scatter(final_df,
                                      x=stat_x,
                                      y=stat_y,
                                      color="Result",
                                      color_discrete_map={
                                          'Win': "rgb(200,11,1)",
                                          'Draw': "rgb(179, 179, 179)",
                                          'Defeat': "rgb(78,78,80)"},
                                      size=stat_size,
                                      title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship for <b>{filter_type}</b> "
                                            f"Season Games")
    relationship_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"})
    relationship_fig.update_xaxes(title_text=stat_x)
    relationship_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown stats
    corr_cols = [stat_x, stat_y]
    corr_value = [np.round(final_df[corr_cols].corr().iloc[1, 0], 3)]
    corr_name = [filter_type]

    for result in ['Win', 'Draw', 'Defeat']:
        df_result = final_df[final_df['Result'] == result]
        if len(df_result) > 0:
            value = np.round(df_result[corr_cols].corr().iloc[1, 0], 3)
            if np.isnan(value):
                corr_value.append(0)
            else:
                corr_value.append(value)
            corr_name.append(result)

    if np.abs(corr_value[0]) <= 0.3:
        overall_corr_strength = "Weak"
    elif (np.abs(corr_value[0]) > 0.3) and (np.abs(corr_value[0]) <= 0.7):
        overall_corr_strength = "Moderate"
    else:
        overall_corr_strength = "Strong"

    if corr_value[0] < 0:
        overall_corr_sign = "Negative"
    else:
        overall_corr_sign = "Positive"

    max_result = np.argmax(np.abs(corr_value[1:])) + 1

    if np.abs(corr_value[max_result]) <= 0.3:
        result_corr_strength = "Weak"
    elif (np.abs(corr_value[max_result]) > 0.3) and (np.abs(corr_value[max_result]) <= 0.7):
        result_corr_strength = "Moderate"
    else:
        result_corr_strength = "Strong"

    if corr_value[max_result] < 0:
        result_corr_sign = "Negative"
    else:
        result_corr_sign = "Positive"

    return relationship_fig, corr_value, corr_name, overall_corr_strength, overall_corr_sign, result_corr_strength, \
           result_corr_sign, max_result


@st.cache
def season_teams(data, page_season):
    # ##### Current season Teams
    analyze_teams = list(data[data['Season'] == page_season]['Team'].unique())
    analyze_teams.sort()

    return analyze_teams


@st.cache
def teams_buli_type(data, analysis_seasons, filter_type, team, stat_name):
    # ##### Filter Season Data by Season Type
    filter_df_team = data[
        (data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data[filter_type] == 1)].reset_index(
        drop=True)
    filter_df_opp = data[
        (data['Season'].isin(analysis_seasons)) & (data['Opponent'] == team) & (data[filter_type] == 1)].reset_index(
        drop=True)

    # ##### Rename Stat Name
    filter_df_team.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)
    filter_df_opp.rename(columns={team_stats_vars[team_stats_names.index(stat_name)]: stat_name}, inplace=True)

    # ##### Stats Type Results
    home_stats = np.round(filter_df_team.groupby('Season')[stat_name].mean(), 2).reset_index()
    home_stats['Team'] = team
    away_stats = np.round(filter_df_opp.groupby('Season')[stat_name].mean(), 2).reset_index()
    away_stats['Team'] = 'Opponent'

    data_seasons = pd.concat([home_stats, away_stats])
    min_value = np.min(data_seasons[stat_name]) * 0.8
    if min_value < 10:
        min_value = 0
    max_value = np.max(data_seasons[stat_name]) * 1.1

    # ##### Plot Data
    team_stat_fig = px.bar(data_seasons,
                           x="Season",
                           y=stat_name,
                           color="Team",
                           barmode='group',
                           color_discrete_map={
                               team: "rgb(200,11,1)",
                               'Opponent': "rgb(179, 179, 179)"},
                           text=stat_name,
                           title=f"<b>{team}</b> {stat_name} per game by Season")
    team_stat_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    team_stat_fig.update_yaxes(title_text=stat_name)

    # ##### Stats for markdown
    current_season = filter_df_team['Season'].unique()[-1]
    if len(home_stats) > 1:
        home_stats['Rank'] = home_stats[stat_name].rank(ascending=False)
        rank_season = int(home_stats[home_stats['Season'] == current_season]['Rank'])
        better_seasons = np.sum(home_stats[stat_name] > away_stats[stat_name])
        no_seasons = len(home_stats)
    else:
        rank_season = "Only 1 season in the Bundesliga over the past 5 years."
        better_seasons = ""
        no_seasons = 1

    return team_stat_fig, rank_season, better_seasons, no_seasons


def relationship_buli_data(data, team, analysis_seasons, filter_type, stat_x, stat_y, ols_line):
    # ##### Filter Season Data by Season Type
    final_df = data[
        (data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data[filter_type] == 1)].reset_index(
        drop=True)

    # ##### Rename Stat Name
    final_df.rename(columns={team_stats_vars[team_stats_names.index(stat_x)]: stat_x}, inplace=True)
    final_df.rename(columns={team_stats_vars[team_stats_names.index(stat_y)]: stat_y}, inplace=True)
    final_df['Points'] = np.where(final_df['Result'] == 'Win', 3, np.where(final_df['Result'] == 'Defeat', 1, 2))

    colors_plot = {analysis_seasons[-5]: 'rgb(216,62,135)',
                   analysis_seasons[-4]: 'rgb(130,101,167)',
                   analysis_seasons[-3]: 'rgb(179, 179, 179)',
                   analysis_seasons[-2]: 'rgb(78,78,80)',
                   analysis_seasons[-1]: 'rgb(200,11,1)'}

    # ##### Relationship Chart
    if ols_line:
        relationship_fig = px.scatter(final_df,
                                      x=stat_x,
                                      y=stat_y,
                                      color="Season",
                                      trendline="ols",
                                      trendline_scope="overall",
                                      color_discrete_map=colors_plot,
                                      size='Points',
                                      title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship for <b>{filter_type}</b> "
                                            f"Season Games")
    else:
        relationship_fig = px.scatter(final_df,
                                      x=stat_x,
                                      y=stat_y,
                                      color="Season",
                                      color_discrete_map=colors_plot,
                                      size='Points',
                                      title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship for <b>{filter_type}</b> "
                                            f"Season Games")
    relationship_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"})
    relationship_fig.update_xaxes(title_text=stat_x)
    relationship_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown stats
    # Overall Correlation
    overall_corr_value = np.round(final_df[[stat_x, stat_y]].corr().iloc[1, 0], 3)
    if np.abs(overall_corr_value) <= 0.3:
        overall_corr_strength = "Weak"
    elif (np.abs(overall_corr_value) > 0.3) and (np.abs(overall_corr_value) <= 0.7):
        overall_corr_strength = "Moderate"
    else:
        overall_corr_strength = "Strong"

    if overall_corr_value < 0:
        overall_corr_sign = "Negative"
    else:
        overall_corr_sign = "Positive"

    # Season Correlation
    season_corr = final_df.groupby('Season')[stat_x, stat_y].corr().reset_index()
    season_corr = season_corr[season_corr['level_1'] == stat_y]
    season_corr['Rank'] = np.abs(season_corr[stat_x]).rank(ascending=False)
    season_name_best_corr = season_corr[season_corr['Rank'] == 1]['Season'].values[0]
    season_value_best_corr = np.round(season_corr[season_corr['Rank'] == 1][stat_x].values[0], 3)

    if np.abs(season_value_best_corr) <= 0.3:
        season_corr_strength = "Weak"
    elif (np.abs(season_value_best_corr) > 0.3) and (np.abs(season_value_best_corr) <= 0.7):
        season_corr_strength = "Moderate"
    else:
        season_corr_strength = "Strong"

    if season_value_best_corr < 0:
        season_corr_sign = "Negative"
    else:
        season_corr_sign = "Positive"

    return relationship_fig, overall_corr_value, overall_corr_strength, overall_corr_sign, season_name_best_corr, \
           season_value_best_corr, season_corr_strength, season_corr_sign
