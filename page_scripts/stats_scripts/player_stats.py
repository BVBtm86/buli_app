import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from page_scripts.stats_scripts.utilities import season_player_query, all_player_query, radar_mosaic
from mplsoccer import Radar, PyPizza
from highlight_text import fig_text

player_stats_total = ['Goals', 'Assists', 'Shots', 'Shots on Target', 'xGoal', 'Non-Penalty xGoal', 'xGoal Assist',
                      'xAssist', 'Goal Created Action', 'Shot Created Action', 'Key Passes', 'Penalty Goal',
                      'Penalty Attempted', 'Own Goals', 'Passes', 'Passes Completed', 'Passes Short',
                      'Passes Short Completed', 'Passes Medium', 'Passes Medium Completed', 'Passes Long',
                      'Passes Long Completed', 'Passes Final 3rd', 'Passes PA', 'Progressive Passes',
                      'Passes Distance', 'Passes Progressive Distance', 'Passes Received',
                      'Progressive Passes Received', 'Passes Free Kicks', 'Passes Live', 'Passes Dead',
                      'Passes Switches', 'Passes Offsides', 'Passes Blocked', 'Through Balls', 'Ball Touches',
                      'Touches Def PA', 'Touches Def 3rd', 'Touches Mid 3rd', 'Touches Att 3rd', 'Touches Att PA',
                      'Touches Live Ball', 'Dribbles', 'Dribbles Completed', 'Crosses', 'Crosses PA', 'Interceptions',
                      'Ball Recoveries', 'Corner Kicks', 'Corner Kicks In', 'Corner Kicks Out',
                      'Corner Kicks Straight', 'Tackles', 'Tackles Won', 'Tackles Def 3rd', 'Tackles Mid 3rd',
                      'Tackles Att 3rd', 'Tackles + Interceptions', 'Duel Aerial Won', 'Duel Aerial Lost',
                      'Dribbles Tackled', 'Dribbles Contested', 'Dribbled Past', 'Blocks', 'Blocked Shots',
                      'Blocked Passes', 'Clearances', 'Offsides', 'Penalty Won', 'Penalty Conceded', 'Throw Ins',
                      'Misscontrols', 'Dispossessed', 'Fouls', 'Fouled', 'Yellow Cards', 'Red Cards',
                      'Yellow + Red Cards', 'Errors']

player_stats_avg = ['Goals', 'Assists', 'Shots', 'Shots on Target', 'Shot Accuracy %', 'xGoal', 'Non-Penalty xGoal',
                    'xGoal Assist', 'xAssist', 'Goal Created Action', 'Shot Created Action', 'Key Passes',
                    'Penalty Goal', 'Penalty Attempted', 'Own Goals', 'Passes', 'Passes Completed',
                    'Passes Completed %', 'Passes Short', 'Passes Short Completed', 'Passes Short Completed %',
                    'Passes Medium', 'Passes Medium Completed', 'Passes Medium Completed %', 'Passes Long',
                    'Passes Long Completed', 'Passes Long Completed %', 'Passes Final 3rd', 'Passes PA',
                    'Progressive Passes', 'Passes Distance', 'Passes Progressive Distance', 'Passes Received',
                    'Progressive Passes Received', 'Passes Free Kicks', 'Passes Live', 'Passes Dead',
                    'Passes Switches', 'Passes Offsides', 'Passes Blocked', 'Through Balls', 'Ball Touches',
                    'Touches Def PA', 'Touches Def 3rd', 'Touches Mid 3rd', 'Touches Att 3rd', 'Touches Att PA',
                    'Touches Live Ball', 'Dribbles', 'Dribbles Completed', 'Dribbles Completed %', 'Crosses',
                    'Crosses PA', 'Interceptions', 'Ball Recoveries', 'Corner Kicks', 'Corner Kicks In',
                    'Corner Kicks Out', 'Corner Kicks Straight', 'Tackles', 'Tackles Won', 'Tackles Won %',
                    'Tackles Def 3rd', 'Tackles Mid 3rd', 'Tackles Att 3rd', 'Tackles + Interceptions',
                    'Duel Aerial Won', 'Duel Aerial Lost', 'Duel Aerial Won %', 'Dribbles Tackled',
                    'Dribbles Contested', 'Dribbles Tackled %', 'Dribbled Past', 'Blocks', 'Blocked Shots',
                    'Blocked Passes', 'Clearances', 'Offsides', 'Penalty Won', 'Penalty Conceded', 'Throw Ins',
                    'Misscontrols', 'Dispossessed', 'Fouls', 'Fouled', 'Yellow Cards', 'Red Cards',
                    'Yellow + Red Cards', 'Errors']

player_position = {"CB": "Defenders", "RB": "Defenders", "LB": "Defenders", "RWB": "Defenders", "LWB": "Defenders",
                   "WB": "Defenders", "DF": "Defenders", "DM": "Midfielders", "CM": "Midfielders", "CAM": "Midfielders",
                   "LM": "Midfielders", "RM": "Midfielders", "AM": "Midfielders", "MF": "Midfielders", "FW": "Forwards",
                   "LW": "Forwards", "RW": "Forwards"}

player_offensive_stats = ["xGoal", "Key Passes", "Shots", "Shots on Target", "Shot Accuracy %", "Shot Created Action",
                          "Dribbles", "Dribbles Completed %"]

player_defensive_stats = ["Tackles", "Tackles Won %", "Duel Aerial Won", "Duel Aerial Won %", "Clearances",
                          "Interceptions", "Ball Recoveries", "Blocks"]

player_passing_stats = ["Ball Touches", "Passes", "Passes Completed %", "Passes Final 3rd", "Passes PA",
                        "Progressive Passes", 'Dispossessed', "Crosses PA"]

# #### Aggregate Stats for Percentage Calculation
player_perc_calculations = ['Shot Accuracy %', 'Passes Completed %', 'Passes Short Completed %',
                            'Passes Medium Completed %', 'Passes Long Completed %', 'Dribbles Completed %',
                            'Tackles Won %', 'Duel Aerial Won %', 'Dribbles Tackled %', 'Saves %', 'Crosses Stopped %']

player_agg_perc = {
    'Shot Accuracy %': ['Shots', 'Shots on Target'], 'Passes Completed %': ['Passes', 'Passes Completed'],
    'Passes Short Completed %': ['Passes Short', 'Passes Short Completed'],
    'Passes Medium Completed %': ['Passes Medium', 'Passes Medium Completed'],
    'Passes Long Completed %': ['Passes Long', 'Passes Long Completed'],
    'Dribbles Completed %': ['Dribbles', 'Dribbles Completed'], 'Tackles Won %': ['Tackles', 'Tackles Won'],
    'Duel Aerial Won %': ['Duel Aerial', 'Duel Aerial Won'],
    'Dribbles Tackled %': ['Dribbles Contested', 'Dribbles Tackled'], 'Saves %': ['Shots on Target GK', 'Saves'],
    'Crosses Stopped %': ['Crosses Faced', 'Crosses Stopped']}


@st.cache
def season_player_data(season):
    # ##### Read Data
    buli_df_players = season_player_query(season=season)
    buli_df_players = buli_df_players[buli_df_players['Position'] != 'GK'].reset_index(drop=True)

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

    # ##### Extra Statistics needed
    buli_df_players['Duel Aerial'] = buli_df_players['Duel Aerial Won'] + buli_df_players['Duel Aerial Lost']

    # ##### Total Players
    total_players = list(buli_df_players['Name'].unique())
    total_players.sort()

    # ##### Players for the Avg Analysis
    filter_players_avg = pd.DataFrame(buli_df_players.groupby(['Name', 'Team'])['Minutes'].sum().sort_values()). \
        reset_index()
    filter_players_avg['Name_Team'] = filter_players_avg['Team'] + "_" + filter_players_avg['Name']
    minutes_cutoff = (buli_df_players['Week_No'].max() * 90) * 0.1
    avg_players = list(filter_players_avg[filter_players_avg['Minutes'] >= minutes_cutoff]['Name_Team'].unique())
    avg_players.sort()

    return buli_df_players, total_players, avg_players


def player_top_statistics(data, season_filter, avg_players, stat_top10, type_top10):
    # ##### Filter Data
    top10_df = data[(data[season_filter] == 1)].reset_index(drop=True)
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    top10_avg_df = avg_data[(avg_data[season_filter] == 1) &
                            (avg_data['Name_Team'].isin(avg_players))].reset_index(drop=True)

    # ##### Create Top 10 Data
    if type_top10 == 'Total':
        stat_plot = stat_top10
        top10_player_group_df = top10_df.groupby(["Name", "Team"])[stat_plot].sum().reset_index()
        top10_plot_data = top10_player_group_df.nlargest(10, stat_plot)
        top10_plot_data.rename(columns={stat_plot: stat_top10}, inplace=True)
    else:
        stat_plot = stat_top10
        if stat_plot in player_perc_calculations:
            stats_agg = player_agg_perc[stat_plot]
            top10_player_group_avg_df = top10_avg_df.groupby(["Name", "Team"])[stats_agg].sum()
            top10_player_group_avg_df[stat_plot] = \
                top10_player_group_avg_df[stats_agg[1]] / top10_player_group_avg_df[stats_agg[0]] * 100
            top10_plot_data = top10_player_group_avg_df.nlargest(10, stat_plot)
            top10_plot_data = \
                top10_plot_data[stat_plot].round(2).sort_values(ascending=False).reset_index()
        else:
            top10_player_group_avg_df = \
                np.round(top10_avg_df.groupby(["Name", "Team"])[stat_plot].mean().reset_index(), 2)
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
        # value_counts = top10_plot_data['Team'].value_counts().reset_index()
        # value_counts = value_counts.rename(columns={"index": "Team", "Team": "# Players"})
        # teams_no_top10 = value_counts[value_counts['# Players'] == max_no_players]['Team'].values
        # # print(teams_no_top10)
        # no_teams_top10 = len(teams_no_top10)
        # teams_top10 = ""
        # for team in teams_no_top10:
        #     teams_top10 += team + ", "
        teams_top10 = ""
        no_teams_top10 = 0
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
        final_players_stat = \
            team_player_df.groupby('Name')[stat_name].sum().sort_values(ascending=False).reset_index()
        final_players_stat.columns = ['Name', stat_name]
        final_players_plot = final_players_stat[final_players_stat[stat_name] > 0]
        if stat_name == 'xGoals' or stat_name == 'xAssisted':
            final_players_plot[stat_name] = np.round(final_players_plot[stat_name], 2)
        final_players_avg_plot = None
    else:
        if stat_name in player_perc_calculations:
            stats_agg = player_agg_perc[stat_name]
            final_players_stat_avg = team_player_avg_df.groupby(["Name"])[stats_agg].sum()
            final_players_stat_avg[stat_name] = \
                final_players_stat_avg[stats_agg[1]] / final_players_stat_avg[stats_agg[0]] * 100
            final_players_avg_plot = \
                final_players_stat_avg[stat_name].round(2).sort_values(ascending=False).reset_index()
            final_players_avg_plot = final_players_avg_plot[final_players_avg_plot[stat_name] > 0]
        else:
            final_players_stat_avg = \
                team_player_avg_df.groupby('Name')[stat_name].mean().sort_values(ascending=False).reset_index()
            final_players_stat_avg.columns = ['Name', stat_name]
            final_players_avg_plot = final_players_stat_avg[final_players_stat_avg[stat_name] > 0]
            final_players_avg_plot[stat_name] = np.round(final_players_avg_plot[stat_name], 2)
        final_players_plot = None

    # ##### Season Average
    if stat_type == 'Total':
        full_season = \
            full_player_df.groupby('Name')[stat_name].sum().reset_index()
        full_season_avg = \
            np.round(full_season[full_season[stat_name] > 0][stat_name].mean(), 2)
    else:
        if stat_name in player_perc_calculations:
            stats_agg = player_agg_perc[stat_name]
            full_season = full_player_avg_df.groupby(["Name"])[stats_agg].sum()
            full_season[stat_name] = \
                full_season[stats_agg[1]] / full_season[stats_agg[0]] * 100
            full_season_avg = \
                np.round(full_season[full_season[stat_name] > 0][stat_name].mean(), 2)
        else:
            full_season = full_player_avg_df.groupby('Name')[stat_name].mean().reset_index()
            full_season_avg = \
                np.round(full_season[full_season[stat_name] > 0][stat_name].mean(), 2)

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

    else:
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
    else:
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
    team_max_day = data.groupby('Week_No')[stat_name].max().reset_index()
    team_avg_day = data.groupby('Week_No')[stat_name].mean().reset_index()

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
            if stat_name in player_perc_calculations:
                stats_agg = player_agg_perc[stat_name]
                # ##### Player Calculation
                player_filter_agg = player_df.groupby([stats_types_player[i]])[stats_agg].sum()
                player_filter_agg = pd.DataFrame(player_filter_agg.loc[1, :]).T
                player_filter_agg[stat_name] = \
                    player_filter_agg[stats_agg[1]] / player_filter_agg[stats_agg[0]] * 100
                player_filter_agg = np.round(player_filter_agg[stat_name].values[0], 2)
                player_stats.append(player_filter_agg)
                # ##### Team Calculation
                team_filter_agg = team_df.groupby([stats_types_player[i]])[stats_agg].sum()
                team_filter_agg = pd.DataFrame(team_filter_agg.loc[1, :]).T
                team_filter_agg[stat_name] = \
                    team_filter_agg[stats_agg[1]] / team_filter_agg[stats_agg[0]] * 100
                team_filter_agg = np.round(team_filter_agg[stat_name].values[0], 2)
                player_stats.append(team_filter_agg)
                # ##### League Calculation
                league_filter_agg = league_df.groupby([stats_types_player[i]])[stats_agg].sum()
                league_filter_agg = pd.DataFrame(league_filter_agg.loc[1, :]).T
                league_filter_agg[stat_name] = \
                    league_filter_agg[stats_agg[1]] / league_filter_agg[stats_agg[0]] * 100
                league_filter_agg = np.round(league_filter_agg[stat_name].values[0], 2)
                player_stats.append(league_filter_agg)
            else:
                player_stats.append(np.round(player_df.groupby(stats_types_player[i])[stat_name].mean().values[-1], 2))
                player_stats.append(np.round(team_df.groupby(stats_types_player[i])[stat_name].mean().values[-1], 2))
                player_stats.append(np.round(league_df.groupby(stats_types_player[i])[stat_name].mean().values[-1], 2))
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

    # ##### Create Average Data
    stat_var_1, stat_var_2 = stat_x, stat_y
    if stat_var_1 in player_perc_calculations:
        stats_x_agg = player_agg_perc[stat_var_1]
        stat_x_calculation = filter_df_season.groupby(["Name"])[stats_x_agg].sum()
        stat_x_calculation[stat_var_1] = \
            np.round(stat_x_calculation[stats_x_agg[1]] / stat_x_calculation[stats_x_agg[0]] * 100, 2)
        stat_x_calculation = stat_x_calculation[stat_var_1]
    else:
        stat_x_calculation = np.round(filter_df_season.groupby('Name')[stat_var_1].mean(), 2)

    if stat_var_2 in player_perc_calculations:
        stats_y_agg = player_agg_perc[stat_var_2]
        stat_y_calculation = filter_df_season.groupby(["Name"])[stats_y_agg].sum()
        stat_y_calculation[stat_var_2] = \
            np.round(stat_y_calculation[stats_y_agg[1]] / stat_y_calculation[stats_y_agg[0]] * 100, 2)
        stat_y_calculation = stat_y_calculation[stat_var_2]
    else:
        stat_y_calculation = np.round(filter_df_season.groupby('Name')[stat_var_2].mean(), 2)

    player_group_df = pd.merge(left=stat_x_calculation, right=stat_y_calculation, left_index=True, right_index=True)
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
def buli_player_data(team, season, all_seasons):
    # ##### Read Data
    buli_df_players = all_player_query(team=team, all_seasons=all_seasons)
    buli_df_players = buli_df_players[buli_df_players['Position'] != 'GK'].reset_index(drop=True)

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

    # ##### Extra Statistics needed
    buli_df_players['Duel Aerial'] = buli_df_players['Duel Aerial Won'] + buli_df_players['Duel Aerial Lost']

    # ##### Players for the Avg Analysis
    player_team = buli_df_players[buli_df_players['Season'] == season].reset_index(drop=True)
    filter_players_avg = pd.DataFrame(player_team.groupby('Name')['Minutes'].sum().reset_index())
    filter_players_avg.columns = ['Name', 'Minutes']
    minutes_cutoff = (player_team['Week_No'].max() * 90) * 0.1
    avg_players = list(filter_players_avg[filter_players_avg['Minutes'] >= minutes_cutoff]['Name'].unique())
    avg_players.sort()

    return buli_df_players, avg_players


def player_buli_stats(data, season_filter, team, player, avg_players, stat_name, analysis_seasons):
    # ##### Filter Season Data by Season Type
    player_df = data[(data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data['Name'] == player) &
                     (data[season_filter] == 1)].reset_index(drop=True)
    player_df_seasons = list(player_df['Season'].unique())
    team_df = data[(data['Season'].isin(player_df_seasons)) & (data['Team'] == team) & (data['Name'].isin(avg_players))
                   & (data[season_filter] == 1)].reset_index(drop=True)

    # ##### Player Stats Stats
    if stat_name in player_perc_calculations:
        stats_agg = player_agg_perc[stat_name]
        # ##### Player Calculation
        player_season_stats = player_df.groupby('Season')[stats_agg].sum()
        player_season_stats[stat_name] = \
            player_season_stats[stats_agg[1]] / player_season_stats[stats_agg[0]] * 100
        player_season_stats = np.round(player_season_stats[stat_name], 2).reset_index()
        # ##### Team Calculation
        team_season_stats = team_df.groupby('Season')[stats_agg].sum()
        team_season_stats[stat_name] = \
            team_season_stats[stats_agg[1]] / team_season_stats[stats_agg[0]] * 100
        team_season_stats = np.round(team_season_stats[stat_name], 2).reset_index()
    else:
        player_season_stats = np.round(player_df.groupby('Season')[stat_name].mean(), 2).reset_index()
        team_season_stats = np.round(team_df.groupby('Season')[stat_name].mean(), 2).reset_index()

    player_season_stats['Averages'] = player
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

    return player_seasons_fig, player_rank_season, player_better_seasons, player_no_seasons, current_season


def player_buli_corr_data(data, filter_type, team, player, stat_x, stat_y, analysis_seasons):
    # ##### Filter Data
    filter_df_player = data[(data['Season'].isin(analysis_seasons)) & (data['Team'] == team) & (data['Name'] == player)
                            & (data[filter_type] == 1)].reset_index(
        drop=True)

    no_seasons_player = len(list(filter_df_player['Season'].unique()))
    filter_df_player['Points'] = np.where(filter_df_player['Result'] == 'Win', 3,
                                          np.where(filter_df_player['Result'] == 'Defeat', 1, 2))

    colors_plot = {analysis_seasons[4]: 'rgb(216,62,135)',
                   analysis_seasons[3]: 'rgb(130,101,167)',
                   analysis_seasons[2]: 'rgb(179, 179, 179)',
                   analysis_seasons[1]: 'rgb(78,78,80)',
                   analysis_seasons[0]: 'rgb(200,11,1)'}

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


@st.cache
def player_comparison_filter(data, season_filter, team, players, remove_player=""):
    # ##### Filter Data by Team and Filter
    buli_team_players = data[(data[season_filter] == 1) & (data['Team'] == team)].reset_index(drop=True)
    buli_team_players['Name_Team'] = buli_team_players['Team'] + "_" + buli_team_players['Name']

    # ##### Players for the Comparison Analysis
    avg_buli_players = buli_team_players[buli_team_players['Name_Team'].isin(players)]['Name'].unique()
    avg_buli_players.sort()

    if remove_player == "":
        final_buli_players = avg_buli_players.copy()
    else:
        final_buli_players = [player for player in avg_buli_players if player != remove_player]

    return final_buli_players


def player_comparison_radar(data, season_filter, stats_type, player_1, player_2, team_player_1, team_player_2):
    # ##### Season Filter Data
    season_data = data[data[season_filter] == 1].reset_index(drop=True)

    # ##### Select Stats
    if stats_type == 'Offensive':
        plot_stats = player_offensive_stats.copy()
    elif stats_type == 'Defensive':
        plot_stats = player_defensive_stats.copy()
    else:
        plot_stats = player_passing_stats.copy()

    # ##### Create Player Stats
    player_df_1 = season_data[season_data['Name'] == player_1].reset_index(drop=True)
    player_df_2 = season_data[season_data['Name'] == player_2].reset_index(drop=True)
    player_stats_values_1 = []
    player_stats_values_2 = []
    for stat_name in plot_stats:
        if stat_name in player_perc_calculations:
            stats_agg = player_agg_perc[stat_name]
            # ##### Player Calculation 1
            player_stats_1 = player_df_1.groupby('Name')[stats_agg].sum()
            player_stats_1[stat_name] = \
                player_stats_1[stats_agg[1]] / player_stats_1[stats_agg[0]] * 100
            player_stats_1 = player_stats_1[stat_name]
            # ##### Player Calculation 2
            player_stats_2 = player_df_2.groupby('Name')[stats_agg].sum()
            player_stats_2[stat_name] = \
                player_stats_2[stats_agg[1]] / player_stats_2[stats_agg[0]] * 100
            player_stats_2 = player_stats_2[stat_name]
        else:
            # ##### Player Calculation 1
            player_stats_1 = player_df_1.groupby('Name')[stat_name].mean()
            # ##### Player Calculation 2
            player_stats_2 = player_df_2.groupby('Name')[stat_name].mean()
        player_stats_values_1.append(np.round(player_stats_1.values[0], 2))
        player_stats_values_2.append(np.round(player_stats_2.values[0], 2))

    # #### Create Plot Ranges
    min_stats = []
    max_stats = []
    for stat_name in plot_stats:
        if stat_name in player_perc_calculations:
            stats_agg = player_agg_perc[stat_name]
            # ##### Player Calculation 1
            range_stats = season_data.groupby('Name')[stats_agg].sum()
            range_stats[stat_name] = \
                range_stats[stats_agg[1]] / range_stats[stats_agg[0]] * 100
            range_stats = range_stats[stat_name]
        else:
            range_stats = season_data.groupby('Name')[stat_name].mean()
        min_stats.append(np.round(np.nanmin(range_stats), 2))
        max_stats.append(np.round(np.nanmax(range_stats), 2))

    # ##### Create Plot
    params = plot_stats.copy()

    # Create Figure
    radar = Radar(params,
                  min_stats,
                  max_stats,
                  num_rings=10,
                  ring_width=1,
                  center_circle_radius=1)

    # PLot Data
    fig_radar, axs = radar_mosaic(radar_height=0.9, title_height=0.1, figheight=14)

    radar.setup_axis(ax=axs['radar'])
    radar.draw_circles(ax=axs['radar'], facecolor='#8265A7', edgecolor='#4e4e50')
    radar.draw_radar_compare(player_stats_values_1, player_stats_values_2, ax=axs['radar'],
                             kwargs_radar={'facecolor': '#c70b01', 'alpha': 0.5},
                             kwargs_compare={'facecolor': '#4e4e50', 'alpha': 0.5})
    # radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    radar.draw_range_labels(ax=axs['radar'], fontsize=15)
    radar.draw_param_labels(ax=axs['radar'], fontsize=20)

    axs['title'].text(0.01, 0.65, player_1, fontsize=25, color='#c70b01', ha='left', va='center')
    axs['title'].text(0.01, 0.30, team_player_1, fontsize=20, ha='left', va='center', color='#c70b01')
    axs['title'].text(0.99, 0.65, player_2, fontsize=25, ha='right', va='center', color='#4e4e50')
    axs['title'].text(0.99, 0.30, team_player_2, fontsize=20, ha='right', va='center', color='#4e4e50')

    # ##### Markdown
    radar_player_1_better = np.sum(np.array(player_stats_values_1) > np.array(player_stats_values_2))
    radar_len_stats = len(player_stats_values_1)
    return fig_radar, radar_player_1_better, radar_len_stats


def player_comparison_pizza(data, season_filter, stats_type, player_1, player_2):
    # ##### Season Filter Data
    season_data = data[data[season_filter] == 1].reset_index(drop=True)

    # ##### Select Stats
    if stats_type == 'Offensive':
        plot_stats = player_offensive_stats.copy()
    elif stats_type == 'Defensive':
        plot_stats = player_defensive_stats.copy()
    else:
        plot_stats = player_passing_stats.copy()

    # ##### Player Stats
    player_stats = np.round(season_data.groupby('Name')[plot_stats[0]].mean().rank(pct=True) * 100)
    for stat_name in plot_stats[1:]:
        if stat_name in player_perc_calculations:
            stats_agg = player_agg_perc[stat_name]
            stats_calculation = season_data.groupby('Name')[stats_agg].sum()
            stats_calculation[stat_name] = stats_calculation[stats_agg[1]] / stats_calculation[stats_agg[0]] * 100
            stats_calculation = np.round(stats_calculation[stat_name].rank(pct=True) * 100)
        else:
            stats_calculation = np.round(
                season_data.groupby('Name')[stat_name].mean().rank(pct=True) * 100)
        player_stats = pd.merge(left=player_stats, right=stats_calculation, left_index=True, right_index=True)
    player_stats.reset_index(inplace=True)
    player_1_values = list(player_stats[player_stats['Name'] == player_1].values[0][1:])
    player_2_values = list(player_stats[player_stats['Name'] == player_2].values[0][1:])
    for i in range(len(player_1_values)):
        if np.isnan(player_1_values[i]):
            player_1_values[i] = 0
        if np.isnan(player_2_values[i]):
            player_2_values[i] = 0

    # ##### Pizza PLot
    baker = PyPizza(
        params=plot_stats,
        background_color="#FFFFFF",
        straight_line_color="#808080",
        straight_line_lw=1,
        last_circle_lw=1,
        last_circle_color="#808080",
        other_circle_ls="-.",
        other_circle_lw=1)

    # plot pizza
    pizza_fig, ax = baker.make_pizza(
        player_1_values,
        compare_values=player_2_values,
        figsize=(8, 8),
        kwargs_slices=dict(
            facecolor="#c70b01", edgecolor="#808080",
            zorder=2, linewidth=1
        ),
        kwargs_compare=dict(
            facecolor="#4e4e50", edgecolor="#808080",
            zorder=2, linewidth=1,
        ),
        kwargs_params=dict(
            color="#8265A7", fontsize=8,
            va="center"
        ),
        kwargs_values=dict(
            color="#FFFFFF", fontsize=8,
            zorder=3,
            bbox=dict(
                edgecolor="#8265A7", facecolor="#c70b01",
                boxstyle="round,pad=0.2", lw=1
            )
        ),
        kwargs_compare_values=dict(
            color="#FFFFFF", fontsize=8, zorder=3,
            bbox=dict(edgecolor="#808080", facecolor="#4e4e50", boxstyle="round,pad=0.2", lw=1)
        ),
    )

    fig_text(
        0.515, 0.99, f"<{player_1}> vs <{player_2}>", size=17, fig=pizza_fig,
        highlight_textprops=[{"color": '#c70b01'}, {"color": '#4e4e50'}],
        ha="center", color="#8265A7")

    # ##### Markdown
    pizza_player_1_better = np.sum(np.array(player_1_values) >= 90)
    pizza_player_2_better = np.sum(np.array(player_2_values) >= 90)
    pizza_len_stats = len(plot_stats)

    return pizza_fig, pizza_player_1_better, pizza_player_2_better, pizza_len_stats
