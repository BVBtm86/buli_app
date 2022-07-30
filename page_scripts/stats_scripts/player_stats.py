import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# ##### Team Names
team_name = {"Bayern Munich": "FC Bayern München", "Bayer Leverkusen": "Bayer 04 Leverkusen",
             "Hoffenheim": "TSG 1899 Hoffenheim", "Werder Bremen": "SV Werder Bremen", "Mainz 05": "1. FSV Mainz 05",
             "Hannover 96": "Hannover 96", "Wolfsburg": "VfL Wolfsburg", "Dortmund": "Borussia Dortmund",
             "Hamburger SV": "Hamburger SV", "Augsburg": "FC Augsburg", "Hertha BSC": "Hertha Berlin",
             "Stuttgart": "VfB Stuttgart", "Schalke 04": "FC Schalke 04", "RB Leipzig": "RasenBallsport Leipzig",
             "Freiburg": "Sport-Club Freiburg", "Eintracht Frankfurt": "Eintracht Frankfurt",
             "Mönchengladbach": "Borussia Mönchengladbach", "Köln": "1. FC Köln", "Düsseldorf": "Fortuna Düsseldorf",
             "Nürnberg": "1. FC Nürnberg", "Paderborn 07": "SC Paderborn 07", "Union Berlin": "1. FC Union Berlin",
             "Arminia": "Arminia Bielefeld", "Bochum": "VfL Bochum 1848", "Greuther Fürth": "SpVgg Greuther Fürth",
             "Greuther F�rth": "SpVgg Greuther Fürth"}

players_stats_vars_total = ["goals", "assists", "assisted_shots", "xg", "xa", "shots_total", "shots_on_target",
                            "aerials_won", "crosses", "corner_kicks", "offsides", "cards_yellow", "fouls", "fouled",
                            "tackles", "tackles_won", "tackles_def_3rd", "tackles_mid_3rd", "tackles_att_3rd",
                            "pressures", "pressure_regains", "pressures_def_3rd", "pressures_mid_3rd",
                            "pressures_att_3rd", "ball_recoveries", "interceptions", "blocks", "clearances",
                            "dispossessed", "errors", "sca", "dribbles", "dribbles_completed",
                            "crosses_into_penalty_area", "through_balls", "passes", "passes_completed",
                            "progressive_passes", "passes_pressure", "passes_short", "passes_completed_short",
                            "passes_medium", "passes_completed_medium", "passes_long", "passes_completed_long",
                            "passes_into_final_third", "passes_into_penalty_area", "passes_total_distance",
                            "passes_progressive_distance", "touches", "touches_def_pen_area", "touches_def_3rd",
                            "touches_mid_3rd", "touches_att_3rd", "touches_att_pen_area", "carries",
                            "progressive_carries", "carries_into_final_third", "carries_into_penalty_area",
                            "carry_distance", "carry_progressive_distance"]

player_stats_names_total = ["Goals", "Assists", "Key Passes", "xGoals", "xAssisted", "Shots", "Shots On Target",
                            "Aerials Won", "Crosses", "Corners", "Offsides", "Yellow Cards", "Fouls", "Fouled",
                            "Tackels", "Tackles Won", "Tackles Def 3rd", "Tackles Mid 3rd", "Tackles Att 3rd",
                            "Pressure", "Pressure Regains", "Pressure Def 3rd", "Pressure Mid 3rd", "Pressure Att 3rd",
                            "Ball Recoveries", "Interceptions", "Blocks", "Clearances", "Dispossessed", "Errors",
                            "Shot Created Actions", "Dribbles", "Dribbles Successful", "Crosses Penalty Area",
                            "Through Balls", "Total Passes", "Completed Passes", "Progressive Passes",
                            "Passes Under Pressure", "Passes Short", "Passes Short Completed", "Passes Medium",
                            "Passes Medium Completed", "Passes Long", "Passes Long Completed", "Passes Final Third",
                            "Passes Penalty Area", "Passes Distance", "Passes Progressive Distance", "Touches",
                            "Touches Def Pen Area", "Touches Def 3rd", "Touches Mid 3rd", "Touches Att 3rd",
                            "Touches Att Pen Area", "Carries", "Progressive Carries", "Carries Final 3rd",
                            "Carries Penalty Area", "Carries Distance", "Carries Progressive Distance"]

players_stats_vars_avg = ["goals", "assists", "assisted_shots", "xg", "xa", "shots_total", "shots_on_target",
                          "shot_accuracy", "aerials_won", "aerials_won_pct", "crosses", "corner_kicks", "offsides",
                          "cards_yellow", "fouls", "fouled", "tackles", "tackles_won", "successful_tackles",
                          "tackles_def_3rd", "tackles_mid_3rd", "tackles_att_3rd", "pressures", "pressure_regains",
                          "pressure_regain_pct", "pressures_def_3rd", "pressures_mid_3rd", "pressures_att_3rd",
                          "ball_recoveries", "interceptions", "blocks", "clearances", "dispossessed", "errors", "sca",
                          "dribbles", "dribbles_completed", "successful_dribbles", "crosses_into_penalty_area",
                          "through_balls", "passes", "passes_completed", "passes_pct", "progressive_passes",
                          "passes_pressure", "passes_short", "passes_completed_short", "passes_pct_short",
                          "passes_medium", "passes_completed_medium", "passes_pct_medium", "passes_long",
                          "passes_completed_long", "passes_pct_long", "passes_into_final_third",
                          "passes_into_penalty_area", "passes_total_distance", "passes_progressive_distance",
                          "touches", "touches_def_pen_area", "touches_def_3rd", "touches_mid_3rd", "touches_att_3rd",
                          "touches_att_pen_area", "carries", "progressive_carries", "carries_into_final_third",
                          "carries_into_penalty_area", "carry_distance", "carry_progressive_distance"]

player_stats_names_avg = ["Goals", "Assists", "Key Passes", "xGoals", "xAssisted", "Shots", "Shots On Target",
                          "Shot Accuracy %", "Aerials Won", "Aerials Won %", "Crosses", "Corners", "Offsides",
                          "Yellow Cards", "Fouls", "Fouled", "Tackles", "Tackles Won", "Tackles Won %",
                          "Tackles Def 3rd", "Tackles Mid 3rd", "Tackles Att 3rd", "Pressure", "Pressure Regains",
                          "Pressure Regains Successful %", "Pressure Def 3rd", "Pressure Mid 3rd", "Pressure Att 3rd",
                          "Ball Recoveries", "Interceptions", "Blocks", "Clearances", "Dispossessed", "Errors",
                          "Shot Created Actions", "Dribbles", "Dribbles Successful", "Dribbles Successful %",
                          "Crosses Penalty Area", "Through Balls", "Total Passes", "Completed Passes",
                          "Completed Passes %", "Progressive Passes", "Passes Under Pressure", "Passes Short",
                          "Passes Short Completed", "Passes Short Completed %", "Passes Medium",
                          "Passes Medium Completed", "Passes Medium Completed %", "Passes Long",
                          "Passes Long Completed", "Passes Long Completed %", "Passes Final Third",
                          "Passes Penalty Area", "Passes Distance", "Passes Progressive Distance", "Touches",
                          "Touches Def Pen Area", "Touches Def 3rd", "Touches Mid 3rd", "Touches Att 3rd",
                          "Touches Att Pen Area", "Carries", "Progressive Carries", "Carries Final 3rd",
                          "Carries Penalty Area", "Carries Distance", "Carries Progressive Distance"]

player_position = {"CB": "Defenders", "RB": "Defenders", "LB": "Defenders", "RWB": "Defenders", "LWB": "Defenders",
                   "WB": "Defenders", "DF": "Defenders", "DM": "Midfielders", "CM": "Midfielders", "CAM": "Midfielders",
                   "LM": "Midfielders", "RM": "Midfielders", "AM": "Midfielders", "MF": "Midfielders", "FW": "Forwards",
                   "LW": "Forwards", "RW": "Forwards"}


@st.cache
def season_player_data(season):
    # ##### Read Data
    buli_df_players = pd.read_csv("./data/Full_Seasons_data/Bundesliga_Players_Statistics.csv", index_col='Unnamed: 0')
    buli_df_players = buli_df_players[buli_df_players['Position'] != 'GK'].reset_index(drop=True)

    # ##### Create Match Day Statistics
    buli_df_players['shot_accuracy'] = np.round(
        (buli_df_players['shots_on_target'] / buli_df_players['shots_total']) * 100, 1)
    buli_df_players['successful_dribbles'] = np.round(
        (buli_df_players['dribbles_completed'] / buli_df_players['dribbles']) * 100, 1)
    buli_df_players['successful_tackles'] = np.round(
        (buli_df_players['tackles_won'] / buli_df_players['tackles']) * 100, 1)

    # ##### Add Filter Type Stats
    buli_df_players['Total'] = 1
    buli_df_players['Home'] = np.where(buli_df_players['Venue'] == "Home", 1, 0)
    buli_df_players['Away'] = np.where(buli_df_players['Venue'] == "Away", 1, 0)
    buli_df_players["1st Period"] = np.where(buli_df_players["Week_No"] <= 17, 1, 0)
    buli_df_players["2nd Period"] = np.where(buli_df_players["Week_No"] >= 18, 1, 0)
    buli_df_players["Win"] = np.where(buli_df_players["Result"] == 'Win', 1, 0)
    buli_df_players["Draw"] = np.where(buli_df_players["Result"] == 'Draw', 1, 0)
    buli_df_players["Defeat"] = np.where(buli_df_players["Result"] == 'Defeat', 1, 0)
    buli_df_players["Player Position"] = buli_df_players["Position"].map(player_position)

    # ##### Filter Data
    buli_df_players['Team'] = buli_df_players['Team'].map(team_name)
    buli_df_players = buli_df_players[buli_df_players['Season'] == season].reset_index(drop=True)

    # ##### Total Players
    total_players = list(buli_df_players['Name'].unique())
    total_players.sort()

    # ##### Players for the Avg Analysis
    filter_players_avg = pd.DataFrame(buli_df_players.groupby(['Name', 'Team'])['Minutes'].sum().sort_values()).\
        reset_index()
    filter_players_avg['Name_Team'] = filter_players_avg['Team'] + "_" + filter_players_avg['Name']
    minutes_cutoff = (buli_df_players['Week_No'].max() * 90) * 0.1
    avg_players = list(filter_players_avg[filter_players_avg['Minutes'] >= minutes_cutoff]['Name_Team'].unique())
    avg_players.sort()

    return buli_df_players, total_players, avg_players


@st.cache
def player_df_filter(data, season_filter):
    # ##### Filter Data
    buli_team_players_df = data[(data[season_filter] == 1)].reset_index(drop=True)

    return buli_team_players_df


def player_top_statistics(data, season_filter, avg_players, stat_top10, type_top10):
    # ##### Filter Data
    top10_df = data[(data[season_filter] == 1)].reset_index(drop=True)
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    top10_avg_df = avg_data[(avg_data[season_filter] == 1) &
                            (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)

    # ##### Create Top 10 Data
    if type_top10 == 'Total':
        stat_plot = players_stats_vars_total[player_stats_names_total.index(stat_top10)]
        top10_player_group_df = top10_df.groupby(["Name", "Team"])[stat_plot].sum().reset_index()
        top10_plot_data = top10_player_group_df.nlargest(10, stat_plot)
        top10_plot_data.rename(columns={stat_plot: stat_top10}, inplace=True)
    elif type_top10 == 'Average':
        stat_plot = players_stats_vars_avg[player_stats_names_avg.index(stat_top10)]
        top10_player_group_avg_df = np.round(top10_avg_df.groupby(["Name", "Team"])[stat_plot].mean().reset_index(), 2)
        top10_plot_data = top10_player_group_avg_df.nlargest(10, stat_plot)
        top10_plot_data.rename(columns={stat_plot: stat_top10}, inplace=True)

    if type_top10 == "Total":
        plot_title = f"Top 10 <b>{stat_top10}</b> for <b>{season_filter}</b> Season Games"
    else:
        plot_title = f"Top 10 Average <b>{stat_top10}</b> per Game for <b>{season_filter}</b> Season Games"

    min_value = np.min(top10_plot_data[stat_top10]) * 0.75
    max_value = np.max(top10_plot_data[stat_top10]) * 1.1

    # ##### Create Plot
    top10_player_fig = px.bar(top10_plot_data,
                              x="Name",
                              y=stat_top10,
                              text=stat_top10,
                              title=plot_title)

    top10_player_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value]
    )

    top10_player_fig.update_traces(marker_color='rgb(200,11,1)')
    if type_top10 == "Total":
        top10_player_fig.update_yaxes(title_text=f"Total {stat_top10}")
    else:
        top10_player_fig.update_yaxes(title_text=f"Average {stat_top10} per Game")

    # ##### Markdown
    max_no_players = top10_plot_data['Team'].value_counts().max()
    if max_no_players > 1:
        value_counts = top10_plot_data['Team'].value_counts().reset_index()
        teams_no_top10 = list(value_counts[value_counts['Team'] == max_no_players]['index'].unique())
        no_teams_top10 = len(teams_no_top10)
        teams_top10 = ""
        for team in teams_no_top10:
            teams_top10 += team + ", "
    else:
        teams_top10 = ""
        no_teams_top10 = 0

    return top10_player_fig, teams_top10, max_no_players, no_teams_top10


def player_df_stat_season(data, team, total_players, avg_players, stat_name, stat_type, season_filter):
    # #### Read Data
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    team_player_df = data[(data['Team'] == team) & (data['Name'].isin(total_players))].reset_index(drop=True)
    team_player_avg_df = avg_data[(avg_data['Team'] == team) &
                                  (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)
    full_player_df = data[data['Name'].isin(total_players)].reset_index(drop=True)
    full_player_avg_df = avg_data[avg_data['Name_Team'].isin(avg_players)].reset_index(drop=True)

    # ##### Create Table
    if stat_type == 'Total':
        final_players_stat = team_player_df.groupby('Name')[
            players_stats_vars_total[player_stats_names_total.index(stat_name)]].sum().sort_values(
            ascending=False).reset_index()
        final_players_stat.columns = ['Name', stat_name]
        final_players_plot = final_players_stat[final_players_stat[stat_name] > 0]
        if stat_name == 'xGoals' or stat_name == 'xAssisted':
            final_players_plot[stat_name] = np.round(final_players_plot[stat_name], 2)
    elif stat_type == "Average":
        final_players_stat_avg = team_player_avg_df.groupby('Name')[
            players_stats_vars_avg[player_stats_names_avg.index(stat_name)]].mean().sort_values(
            ascending=False).reset_index()
        final_players_stat_avg.columns = ['Name', stat_name]
        final_players_avg_plot = final_players_stat_avg[final_players_stat_avg[stat_name] > 0]
        final_players_avg_plot[stat_name] = np.round(final_players_avg_plot[stat_name], 2)

    # ##### Season Average
    if stat_type == 'Total':
        full_season = full_player_df.groupby('Name')[
            players_stats_vars_total[player_stats_names_total.index(stat_name)]].sum().reset_index()
        full_season_avg = \
            np.round(full_season[full_season[players_stats_vars_total[player_stats_names_total.index(stat_name)]] > 0][
                         players_stats_vars_total[player_stats_names_total.index(stat_name)]].mean(), 2)
    elif stat_type == 'Average':
        full_season = full_player_avg_df.groupby('Name')[
            players_stats_vars_avg[player_stats_names_avg.index(stat_name)]].mean().reset_index()
        full_season_avg = \
            np.round(full_season[full_season[players_stats_vars_avg[player_stats_names_avg.index(stat_name)]] > 0][
                         players_stats_vars_avg[player_stats_names_avg.index(stat_name)]].mean(), 2)

    # ##### Create Plot
    if stat_type == 'Total':
        team_player_fig = px.bar(final_players_plot,
                                 x="Name",
                                 y=stat_name,
                                 text=stat_name,
                                 title=f"Total <b>{stat_name}</b> for <b>{season_filter}</b> Season Games")

        team_player_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        )
        team_player_fig.update_traces(marker_color='rgb(200,11,1)')
        team_player_fig.update_yaxes(title_text=f"Total {stat_name}")

    elif stat_type == 'Average':
        team_player_fig = px.bar(final_players_avg_plot,
                                 x="Name",
                                 y=stat_name,
                                 text=stat_name,
                                 title=f"Average <b>{stat_name}</b> per Game for <b>{season_filter}</b> "
                                       f"Season Games")

        team_player_fig.update_layout({
            "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        )
        team_player_fig.update_traces(marker_color='rgb(200,11,1)')
        team_player_fig.update_yaxes(title_text=f"Average {stat_name} per Game")

    # ##### Markdown
    if stat_type == 'Total':
        season_better_avg = np.sum(final_players_plot[stat_name] > full_season_avg)
    elif stat_type == 'Average':
        season_better_avg = np.sum(final_players_avg_plot[stat_name] > full_season_avg)

    return team_player_fig, full_season_avg, season_better_avg


def player_match_day_team(data, team, players):
    # ##### Filter Team
    season_player_team = data[data['Team'] == team].reset_index(drop=True)
    season_player_team['Name_Team'] = season_player_team['Team'] + "_" + season_player_team['Name']
    season_players = list(season_player_team[season_player_team['Name_Team'].isin(players)]['Name'].unique())
    season_players.sort()

    return season_player_team, season_players


def player_chart_day(data, player_name, stat_name):
    # ##### Filter Player and Stat Data
    player_df = data[(data['Name'] == player_name)].reset_index(drop=True)
    player_df.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_name)]: stat_name}, inplace=True)
    week_no = data['Week_No'].max()

    # ##### Plot Data
    min_value = 0
    max_value = np.max(player_df[stat_name])
    fig_player_day = px.bar(player_df,
                            x="Week_No",
                            y=stat_name,
                            color="Result",
                            color_discrete_map={
                                'Win': "rgb(200,11,1)",
                                'Draw': "rgb(179, 179, 179)",
                                'Defeat': "rgb(78,78,80)"},
                            text=stat_name,
                            title=f"<b>{player_name}</b>: <b>{stat_name}</b> per Match Day")
    fig_player_day.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        xaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(1, week_no + 1)],
        ),
        yaxis_range=[min_value, max_value]
    )
    fig_player_day.update_yaxes(title_text=stat_name, col=1)

    # ##### Markdown
    team_max_day = data.groupby('Week_No')[
        players_stats_vars_avg[player_stats_names_avg.index(stat_name)]].max().reset_index()
    team_avg_day = data.groupby('Week_No')[
        players_stats_vars_avg[player_stats_names_avg.index(stat_name)]].mean().reset_index()

    player_comparison = player_df[['Week_No', stat_name]]
    player_comparison = player_comparison[player_comparison[stat_name] > 0]
    player_comparison = pd.merge(player_comparison, team_max_day, on='Week_No', how='left')
    player_comparison = pd.merge(player_comparison, team_avg_day, on='Week_No', how='left')

    day_better = np.sum(player_comparison.iloc[:, 1] == player_comparison.iloc[:, 2])
    avg_better = np.sum(player_comparison.iloc[:, 1] > player_comparison.iloc[:, 3])
    return fig_player_day, max_value, day_better, avg_better


def player_season_filter_stats(data, team, player, avg_players, stat_name, vs_player_type):
    # ##### Filter Season Data by Season Type
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    player_df = data[(data['Team'] == team) & (data['Name'] == player)].reset_index(drop=True)
    team_df = avg_data[(avg_data['Team'] == team) & (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)
    league_df = data[(data['Player Position'] == vs_player_type)].reset_index(drop=True)

    # ##### Stats Type Results
    stats_types_player = ['Total', 'Home', 'Away', '1st Period', '2nd Period', 'Win', 'Draw', 'Defeat']

    # ##### Create Data
    names_stats = []
    player_stats = []
    player_name = []
    for i in range(len(stats_types_player)):
        length_stat = player_df[player_df[stats_types_player[i]] == 1].shape[0]
        if length_stat > 0:
            names_stats.append(stats_types_player[i])
            names_stats.append(stats_types_player[i])
            names_stats.append(stats_types_player[i])
            player_stats.append(np.round(player_df.groupby(stats_types_player[i])[players_stats_vars_avg[
                player_stats_names_avg.index(stat_name)]].mean().values[-1], 2))
            player_stats.append(np.round(team_df.groupby(stats_types_player[i])[players_stats_vars_avg[
                player_stats_names_avg.index(stat_name)]].mean().values[-1], 2))
            player_stats.append(np.round(league_df.groupby(stats_types_player[i])[players_stats_vars_avg[
                player_stats_names_avg.index(stat_name)]].mean().values[-1], 2))
            player_name.append(player)
            player_name.append(team)
            player_name.append(f"League: {vs_player_type}s")

    player_season_type = pd.DataFrame([names_stats, player_stats, player_name]).T
    player_season_type.columns = ['Type', stat_name, 'Averages']

    min_value = np.min(player_season_type[stat_name]) * 0.75
    if min_value < 10:
        min_value = 0
    max_value = np.max(player_season_type[stat_name]) * 1.1

    # ##### Plot Data
    player_stat_fig = px.bar(player_season_type,
                             x="Type",
                             y=stat_name,
                             color="Averages",
                             barmode='group',
                             color_discrete_map={
                                 player: "rgb(200,11,1)",
                                 team: "rgb(179, 179, 179)",
                                 f"League: {vs_player_type}s": "rgb(78,78,80)"},
                             text=stat_name,
                             title=f"<b>{player}</b> {stat_name} Stats vs Player Positions by Team & League Averages")
    player_stat_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    player_stat_fig.update_yaxes(title_text=stat_name)

    # ##### Markdown
    if player_season_type.iloc[0, 1] > player_season_type.iloc[1, 1]:
        player_team_comparison = "More"
    else:
        player_team_comparison = "Less"

    if player_season_type.iloc[0, 1] > player_season_type.iloc[2, 1]:
        player_league_comparison = "More"
    else:
        player_league_comparison = "Less"

    if ('Home' in list(player_season_type['Type'].values)) and ('Away' in list(player_season_type['Type'].values)):
        if player_season_type.iloc[3, 1] > player_season_type.iloc[6, 1]:
            player_home_away = "Home"
        else:
            player_home_away = "Away"
    else:
        player_home_away = ""

    return player_stat_fig, player_team_comparison, player_league_comparison, player_home_away


def player_corr_filter_team(data, season_filter, team, players):
    # ##### Filter Team
    season_player_team = data[(data['Team'] == team) & (data[season_filter] == 1)].reset_index(drop=True)
    season_player_team['Name_Team'] = season_player_team['Team'] + "_" + season_player_team['Name']
    season_players = list(season_player_team[season_player_team['Name_Team'].isin(players)]['Name'].unique())
    season_players.sort()

    return season_player_team, season_players


def player_relationship_data(data, filter_type, team, player, avg_players, stat_x, stat_y):
    # ##### Filter Data
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    filter_df_team = avg_data[(avg_data['Team'] == team) &
                              (avg_data[filter_type] == 1) &
                              (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)
    filter_df_season = avg_data[(avg_data[filter_type] == 1) &
                                (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)

    # ##### Rename Stat Name
    filter_df_team.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_x)]: stat_x}, inplace=True)
    filter_df_team.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_y)]: stat_y}, inplace=True)
    filter_df_season.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_x)]: stat_x},
                            inplace=True)
    filter_df_season.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_y)]: stat_y},
                            inplace=True)

    # ##### Create Average Data
    stat_var_1, stat_var_2 = stat_x, stat_y

    player_group_df = np.round(filter_df_season.groupby('Name')[[stat_var_1, stat_var_2]].mean(), 2).reset_index()
    player_group_df = pd.merge(player_group_df, filter_df_season[["Name", "Team"]].drop_duplicates(keep="last"),
                               on="Name", how="left")

    player_group_df['Group'] = np.where(player_group_df['Name'] == player, player,
                                        np.where(player_group_df['Team'] == team, team, "Bundesliga"))

    # ##### Create Team Data
    filter_df_team['Group'] = np.where(filter_df_team['Name'] == player, player, team)

    # ##### Average Plot
    player_league_fig = px.scatter(player_group_df,
                                   x=stat_var_1,
                                   y=stat_var_2,
                                   color='Group',
                                   hover_name='Name',
                                   color_discrete_map={
                                       player: "rgb(200,11,1)",
                                       team: "rgb(78,78,80)",
                                       "Bundesliga": "rgb(179, 179, 179)"},
                                   title=f"<b>{player}</b> {stat_x} vs {stat_y} Relationship by {filter_type} Season "
                                         f"Games Average")

    player_league_fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)"})
    player_league_fig.update_xaxes(title_text=stat_x)
    player_league_fig.update_yaxes(title_text=stat_y)

    # ##### Total Plot
    player_team_fig = px.scatter(filter_df_team,
                                 x=stat_var_1,
                                 y=stat_var_2,
                                 color='Group',
                                 hover_name='Name',
                                 hover_data=['Week_No'],
                                 color_discrete_map={
                                     player: "rgb(200,11,1)",
                                     team: "rgb(78,78,80)"},
                                 title=f"<b>{player}</b> {stat_x} vs {stat_y} Relationship by Games")

    player_team_fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)"})
    player_team_fig.update_xaxes(title_text=stat_x)
    player_team_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown
    filter_player_df = filter_df_team[filter_df_team['Name'] == player].reset_index(drop=True)
    if filter_player_df[[stat_var_1, stat_var_2]].dropna().shape[0] >= 10:
        player_corr_value = np.round(filter_player_df[[stat_var_1, stat_var_2]].dropna().corr().iloc[0, 1], 2)
        if np.isnan(player_corr_value):
            player_corr_value = ""
            player_corr_strength = ""
            player_corr_sign = ""
        else:
            if np.abs(player_corr_value) <= 0.3:
                player_corr_strength = "Weak"
            elif (np.abs(player_corr_value) > 0.3) and (np.abs(player_corr_value) <= 0.7):
                player_corr_strength = "Moderate"
            else:
                player_corr_strength = "Strong"

            if player_corr_value < 0:
                player_corr_sign = "Negative"
            else:
                player_corr_sign = "Positive"

    else:
        player_corr_value = ""
        player_corr_strength = ""
        player_corr_sign = ""

    return player_league_fig, player_team_fig, player_corr_value, player_corr_strength, player_corr_sign


@st.cache
def buli_player_data(season):
    # ##### Read Data
    buli_df_players = pd.read_csv("./data/Full_Seasons_data/Bundesliga_Players_Statistics.csv", index_col='Unnamed: 0')
    buli_df_players = buli_df_players[buli_df_players['Position'] != 'GK'].reset_index(drop=True)

    # ##### Create Match Day Statistics
    buli_df_players['shot_accuracy'] = np.round(
        (buli_df_players['shots_on_target'] / buli_df_players['shots_total']) * 100, 1)
    buli_df_players['successful_dribbles'] = np.round(
        (buli_df_players['dribbles_completed'] / buli_df_players['dribbles']) * 100, 1)
    buli_df_players['successful_tackles'] = np.round(
        (buli_df_players['tackles_won'] / buli_df_players['tackles']) * 100, 1)

    # ##### Add Filter Type Stats
    buli_df_players['Total'] = 1
    buli_df_players['Home'] = np.where(buli_df_players['Venue'] == "Home", 1, 0)
    buli_df_players['Away'] = np.where(buli_df_players['Venue'] == "Away", 1, 0)
    buli_df_players["1st Period"] = np.where(buli_df_players["Week_No"] <= 17, 1, 0)
    buli_df_players["2nd Period"] = np.where(buli_df_players["Week_No"] >= 18, 1, 0)
    buli_df_players["Win"] = np.where(buli_df_players["Result"] == 'Win', 1, 0)
    buli_df_players["Draw"] = np.where(buli_df_players["Result"] == 'Draw', 1, 0)
    buli_df_players["Defeat"] = np.where(buli_df_players["Result"] == 'Defeat', 1, 0)
    buli_df_players["Player Position"] = buli_df_players["Position"].map(player_position)
    buli_df_players['Team'] = buli_df_players['Team'].map(team_name)

    # Season Teams
    player_teams = list(buli_df_players[buli_df_players['Season'] == season]['Team'].unique())
    player_teams.sort()

    return buli_df_players, player_teams


def buli_players_avg(data, team, season):
    # ##### Team Name
    player_team = data[(data['Team'] == team) & (data['Season'] == season)].reset_index(drop=True)

    # ##### Players for the Avg Analysis
    filter_players_avg = pd.DataFrame(player_team.groupby('Name')['Minutes'].sum().reset_index())
    filter_players_avg.columns = ['Name', 'Minutes']
    minutes_cutoff = (player_team['Week_No'].max() * 90) * 0.1
    avg_players = list(filter_players_avg[filter_players_avg['Minutes'] >= minutes_cutoff]['Name'].unique())
    avg_players.sort()

    return avg_players


def player_buli_stats(data, season_filter, team, player, avg_players, stat_name, analysis_seasons):
    # ##### Filter Season Data by Season Type
    player_df = data[(data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data['Name'] == player) &
                     (data[season_filter] == 1)].reset_index(drop=True)
    player_df_seasons = list(player_df['Season'].unique())
    team_df = data[(data['Season'].isin(player_df_seasons)) & (data['Team'] == team) & (data['Name'].isin(avg_players))
                   & (data[season_filter] == 1)].reset_index(drop=True)

    player_df.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_name)]: stat_name}, inplace=True)
    team_df.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_name)]: stat_name}, inplace=True)

    # ##### Create Stats
    player_season_stats = np.round(player_df.groupby('Season')[stat_name].mean(), 3).reset_index()
    player_season_stats['Averages'] = player
    team_season_stats = np.round(team_df.groupby('Season')[stat_name].mean(), 3).reset_index()
    team_season_stats['Averages'] = team
    season_stats = pd.concat([player_season_stats, team_season_stats])

    min_value = np.min(season_stats[stat_name]) * 0.5
    max_value = np.max(season_stats[stat_name]) * 1.1

    # ##### Plot Data
    player_seasons_fig = px.bar(season_stats,
                                x="Season",
                                y=stat_name,
                                color="Averages",
                                barmode='group',
                                color_discrete_map={
                                    player: "rgb(200,11,1)",
                                    team: "rgb(179, 179, 179)"},
                                text=stat_name,
                                title=f"<b>{player}</b> {stat_name} Stats by Seasons")
    player_seasons_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    player_seasons_fig.update_yaxes(title_text=stat_name)

    # ##### Markdown
    current_season = analysis_seasons[-1]
    if current_season in list(player_df['Season'].unique()):
        if len(player_df_seasons) > 1:
            player_season_stats['Rank'] = player_season_stats[stat_name].rank(ascending=False)
            player_rank_season = int(player_season_stats[player_season_stats['Season'] == current_season]['Rank'])
            player_better_seasons = np.sum(player_season_stats[stat_name] > team_season_stats[stat_name])
            player_no_seasons = len(player_df_seasons)
        else:
            player_rank_season = f"Only 1 season for {team} over the past 5 years."
            player_better_seasons = ""
            player_no_seasons = 1
    else:
        player_rank_season = "No Data"
        player_better_seasons = ""
        player_no_seasons = 0

    return player_seasons_fig, player_rank_season, player_better_seasons, player_no_seasons


def player_buli_corr_data(data, filter_type, team, player, stat_x, stat_y, analysis_seasons):
    # ##### Filter Data
    filter_df_player = data[(data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data['Name'] == player)
                            & (data[filter_type] == 1)].reset_index(
        drop=True)

    no_seasons_player = len(list(filter_df_player['Season'].unique()))
    # ##### Rename Stat Name
    filter_df_player.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_x)]: stat_x},
                            inplace=True)
    filter_df_player.rename(columns={players_stats_vars_avg[player_stats_names_avg.index(stat_y)]: stat_y},
                            inplace=True)

    filter_df_player['Points'] = np.where(filter_df_player['Result'] == 'Win', 3,
                                          np.where(filter_df_player['Result'] == 'Defeat', 1, 2))

    colors_plot = {analysis_seasons[-5]: 'rgb(216,62,135)',
                   analysis_seasons[-4]: 'rgb(130,101,167)',
                   analysis_seasons[-3]: 'rgb(179, 179, 179)',
                   analysis_seasons[-2]: 'rgb(78,78,80)',
                   analysis_seasons[-1]: 'rgb(200,11,1)'}

    # ##### Average Plot
    player_seasons_fig = px.scatter(filter_df_player,
                                    x=stat_x,
                                    y=stat_y,
                                    color='Season',
                                    hover_name='Name',
                                    color_discrete_map=colors_plot,
                                    size='Points',
                                    title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship by {filter_type} Season "
                                          f"Games")

    player_seasons_fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)"})
    player_seasons_fig.update_xaxes(title_text=stat_x)
    player_seasons_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown stats
    # Overall Correlation
    pl_overall_corr_value = np.round(filter_df_player[[stat_x, stat_y]].corr().iloc[1, 0], 3)
    if np.isnan(pl_overall_corr_value):
        pl_overall_corr_strength = ""
        pl_overall_corr_sign = ""
    else:
        if np.abs(pl_overall_corr_value) <= 0.3:
            pl_overall_corr_strength = "Weak"
        elif (np.abs(pl_overall_corr_value) > 0.3) and (np.abs(pl_overall_corr_value) <= 0.7):
            pl_overall_corr_strength = "Moderate"
        else:
            pl_overall_corr_strength = "Strong"

        if pl_overall_corr_value < 0:
            pl_overall_corr_sign = "Negative"
        else:
            pl_overall_corr_sign = "Positive"

    # Season Correlation
    if no_seasons_player > 1:
        pl_season_corr = filter_df_player.groupby('Season')[stat_x, stat_y].corr().reset_index()
        if pl_season_corr.dropna().shape[0] > 0:
            pl_season_corr = pl_season_corr[pl_season_corr['level_1'] == stat_y]
            pl_season_corr['Rank'] = np.abs(pl_season_corr[stat_x]).rank(ascending=False)
            pl_season_name_best_corr = pl_season_corr[pl_season_corr['Rank'] == 1]['Season'].values[0]
            pl_season_value_best_corr = np.round(pl_season_corr[pl_season_corr['Rank'] == 1][stat_x].values[0], 3)

            if np.abs(pl_season_value_best_corr) <= 0.3:
                pl_season_corr_strength = "Weak"
            elif (np.abs(pl_season_value_best_corr) > 0.3) and (np.abs(pl_season_value_best_corr) <= 0.7):
                pl_season_corr_strength = "Moderate"
            else:
                pl_season_corr_strength = "Strong"

            if pl_season_value_best_corr < 0:
                pl_season_corr_sign = "Negative"
            else:
                pl_season_corr_sign = "Positive"
        else:
            pl_season_name_best_corr = ""
            pl_season_value_best_corr = 0
            pl_season_corr_strength = 0
            pl_season_corr_sign = 0
    else:
        pl_season_name_best_corr = ""
        pl_season_value_best_corr = 0
        pl_season_corr_strength = 0
        pl_season_corr_sign = 0

    return player_seasons_fig, pl_overall_corr_value, pl_overall_corr_strength, pl_overall_corr_sign, \
           pl_season_name_best_corr, pl_season_value_best_corr, pl_season_corr_strength, pl_season_corr_sign
