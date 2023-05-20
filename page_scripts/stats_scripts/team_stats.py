import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind
from page_scripts.stats_scripts.utilities import season_team_query, season_gk_query, all_team_query, all_gk_query
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# ##### Stats
stats_team = ['Possession', 'Goals', 'Assists', 'Shots', 'Shots on Target', 'Shot Accuracy %', 'xGoal',
              'Non-Penalty xGoal', 'xGoal Assist', 'xAssist', 'Goal Created Action', 'Shot Created Action',
              'Key Passes', 'Penalty Goal', 'Penalty Attempted', 'Own Goals', 'Distance Covered (Km)', 'Sprints',
              'Passes', 'Passes Completed', 'Passes Completed %', 'Passes Short', 'Passes Short Completed',
              'Passes Short Completed %', 'Passes Medium', 'Passes Medium Completed', 'Passes Medium Completed %',
              'Passes Long', 'Passes Long Completed', 'Passes Long Completed %', 'Passes Final 3rd', 'Passes PA',
              'Progressive Passes', 'Passes Distance', 'Passes Progressive Distance', 'Passes Received',
              'Progressive Passes Received', 'Passes Free Kicks', 'Passes Live', 'Passes Dead', 'Passes Switches',
              'Passes Offsides', 'Passes Blocked', 'Through Balls', 'Ball Touches', 'Touches Def PA', 'Touches Def 3rd',
              'Touches Mid 3rd', 'Touches Att 3rd', 'Touches Att PA', 'Touches Live Ball', 'Dribbles',
              'Dribbles Completed', 'Dribbles Completed %', 'Crosses', 'Crosses PA', 'Interceptions', 'Ball Recoveries',
              'Corner Kicks', 'Corner Kicks In', 'Corner Kicks Out', 'Corner Kicks Straight', 'Tackles',
              'Tackles Won', 'Tackles Won %', 'Tackles Def 3rd', 'Tackles Mid 3rd', 'Tackles Att 3rd',
              'Tackles + Interceptions', 'Duel Aerial Won', 'Duel Aerial Lost', 'Duel Aerial Won %', 'Dribbles Tackled',
              'Dribbles Contested', 'Dribbled Past', 'Dribbles Tackled %', 'Blocks', 'Blocked Shots', 'Blocked Passes',
              'Clearances', 'Offsides', 'Penalty Won', 'Penalty Conceded', 'Throw Ins', 'Misscontrols', 'Dispossessed',
              'Fouls', 'Fouled', 'Yellow Cards', 'Red Cards', 'Yellow + Red Cards', 'Errors', 'Saves', 'Saves %',
              'Goal Kicks', 'Throws', 'Crosses Faced', 'Crosses Stopped', 'Crosses Stopped %']

# #### Aggregate Stats for Percentage Calculation
stats_perc_calculations = ['Shot Accuracy %', 'Passes Completed %', 'Passes Short Completed %',
                           'Passes Medium Completed %', 'Passes Long Completed %', 'Dribbles Completed %',
                           'Tackles Won %', 'Duel Aerial Won %', 'Dribbles Tackled %', 'Saves %', 'Crosses Stopped %']

stats_agg_perc = {
    'Shot Accuracy %': ['Shots', 'Shots on Target'], 'Passes Completed %': ['Passes', 'Passes Completed'],
    'Passes Short Completed %': ['Passes Short', 'Passes Short Completed'],
    'Passes Medium Completed %': ['Passes Medium', 'Passes Medium Completed'],
    'Passes Long Completed %': ['Passes Long', 'Passes Long Completed'],
    'Dribbles Completed %':  ['Dribbles', 'Dribbles Completed'], 'Tackles Won %': ['Tackles', 'Tackles Won'],
    'Duel Aerial Won %': ['Duel Aerial', 'Duel Aerial Won'],
    'Dribbles Tackled %': ['Dribbles Contested', 'Dribbles Tackled'], 'Saves %': ['Shots on Target GK', 'Saves'],
    'Crosses Stopped %': ['Crosses Faced', 'Crosses Stopped']}


@st.cache
def season_data_process(season, stat_type, all_seasons):
    # ##### Read Data
    if stat_type == "Season Stats":
        buli_df = season_team_query(season=season)
        buli_gk_df = season_gk_query(season=season)
    else:
        buli_df = all_team_query(all_seasons=all_seasons)
        buli_gk_df = all_gk_query(all_seasons=all_seasons)

    # ##### Correct Lineup Statistics
    buli_df['Team_Lineup'] = buli_df['Team_Lineup'].apply(lambda x: x.replace("◆", ""))
    buli_df['Opp_Lineup'] = buli_df['Opp_Lineup'].apply(lambda x: x.replace("◆", ""))

    # ##### Extra Statistics needed
    buli_df['Duel Aerial'] = buli_df['Duel Aerial Won'] + buli_df['Duel Aerial Lost']

    # ##### Add Team Goalkeeper Statistics
    df_team_gk = \
        buli_gk_df.groupby(["Season", "Week_No", "Team", "Opponent", "Venue"])[["Shots on Target",
                                                                               "Saves", "Post-Shot xGoal",
                                                                               "Passes", "Goal Kicks", "Throws",
                                                                               "Crosses Faced", "Crosses Stopped"]].sum()

    df_team_gk.reset_index(inplace=True)
    df_team_gk['Saves %'] = np.round(df_team_gk['Saves'] / df_team_gk['Shots on Target'] * 100, 2)
    df_team_gk['Crosses Stopped %'] = np.round(df_team_gk['Crosses Stopped'] / df_team_gk['Crosses Faced'] * 100, 2)
    df_team_gk.rename(columns={"Passes": "Total Passes", "Shots on Target": "Shots on Target GK"}, inplace=True)
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
    home_df = buli_df[buli_df['Venue'] == 'Home'].copy()
    home_df.reset_index(drop=True, inplace=True)
    away_df = buli_df[buli_df['Venue'] == 'Away'].copy()
    away_df.reset_index(drop=True, inplace=True)
    home_df['Goals'] = home_df['Goals'] + away_df['Own Goals']
    away_df['Goals'] = away_df['Goals'] + home_df['Own Goals']
    final_df = pd.concat([home_df, away_df])
    final_df.reset_index(drop=True, inplace=True)

    return final_df


def teams_season_stats(data, stat_name, stat_filter, team_type):
    # #### Filter Season Data by Season Type
    filter_team_stat = data[data[stat_filter] == 1].reset_index(drop=True)

    # ##### Create Team Chart
    if team_type == 'Team':
        if stat_name in stats_perc_calculations:
            stats_agg = stats_agg_perc[stat_name]
            data_plot = filter_team_stat.groupby('Team')[stats_agg].sum()
            data_plot[stat_name] = data_plot[stats_agg[1]] / data_plot[stats_agg[0]] * 100
            data_plot = data_plot[stat_name].round(2).sort_values(ascending=False).reset_index()
        else:
            data_plot = filter_team_stat.groupby('Team')[stat_name].mean().round(2).sort_values(
                    ascending=False).reset_index()
    else:
        if stat_name in stats_perc_calculations:
            stats_agg = stats_agg_perc[stat_name]
            data_plot = filter_team_stat.groupby('Opponent')[stats_agg].sum()
            data_plot[stat_name] = data_plot[stats_agg[1]] / data_plot[stats_agg[0]] * 100
            data_plot = data_plot[stat_name].round(2).sort_values(ascending=False).reset_index()
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
    if stat_name in stats_perc_calculations:
        stats_agg = stats_agg_perc[stat_name]
        avg_team_calc = pd.DataFrame(filter_team_stat[stats_agg].sum()).T
        avg_team = np.round(avg_team_calc[stats_agg[1]] / avg_team_calc[stats_agg[0]] * 100, 2).values[0]
        avg_opp_calc = pd.DataFrame(filter_opp_stat[stats_agg].sum()).T
        avg_opp = np.round(avg_opp_calc[stats_agg[1]] / avg_opp_calc[stats_agg[0]] * 100, 2).values[0]
    else:
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
            if stat_name in stats_perc_calculations:
                stats_agg = stats_agg_perc[stat_name]
                team_agg_stats = df_team.groupby(stats_types_team[i])[stats_agg].sum()
                results_stats.append(
                    np.round([team_agg_stats[stats_agg[1]] / team_agg_stats[stats_agg[0]] * 100][0][1], 2))
            else:
                results_stats.append(np.round(
                    df_team.groupby(stats_types_team[i])[stat_name].mean().values[-1], 2))
            results_team.append(team)
        if len(df_opp) > 0:
            results_names.append(stats_types_team[i])
            if stat_name in stats_perc_calculations:
                stats_agg = stats_agg_perc[stat_name]
                opp_agg_stats = df_opp.groupby(stats_types_opp[i])[stats_agg].sum()
                results_stats.append(
                    np.round([opp_agg_stats[stats_agg[1]] / opp_agg_stats[stats_agg[0]] * 100][0][1], 2))
            else:
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

    team_part_name = ""
    team_value_3 = np.nan
    team_value_4 = np.nan
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

    return team_stat_fig, team_data_name, team_value_1, team_value_2, team_part_name, team_value_3, team_value_4


def relationship_data(data, team, filter_type, stat_x, stat_y, stat_size, ols_line):
    # ##### Filter Season Data by Season Type
    if team != 'All Teams':
        filter_df_team = data[(data['Team'] == team)].reset_index(drop=True)
    else:
        filter_df_team = data.copy()
    final_df = filter_df_team[filter_df_team[filter_type] == 1].reset_index(drop=True)

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

    # ##### Stats Type Results
    if stat_name in stats_perc_calculations:
        stats_agg = stats_agg_perc[stat_name]
        home_agg_stats = filter_df_team.groupby('Season')[stats_agg].sum()
        home_agg_stats[stat_name] = home_agg_stats[stats_agg[1]] / home_agg_stats[stats_agg[0]] * 100
        home_stats = np.round(home_agg_stats[stat_name], 2).reset_index()
        away_agg_stats = filter_df_opp.groupby('Season')[stats_agg].sum()
        away_agg_stats[stat_name] = away_agg_stats[stats_agg[1]] / away_agg_stats[stats_agg[0]] * 100
        away_stats = np.round(away_agg_stats[stat_name], 2).reset_index()
    else:
        home_stats = np.round(filter_df_team.groupby('Season')[stat_name].mean(), 2).reset_index()
        away_stats = np.round(filter_df_opp.groupby('Season')[stat_name].mean(), 2).reset_index()

    home_stats['Team'] = team
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

    return team_stat_fig, rank_season, better_seasons, no_seasons, current_season


def relationship_buli_data(data, team, analysis_seasons, filter_type, stat_x, stat_y, ols_line):
    # ##### Filter Season Data by Season Type
    final_df = data[(data['Team'] == team) & (data[filter_type] == 1)].reset_index(drop=True)
    final_df['Points'] = np.where(final_df['Result'] == 'Win', 3, np.where(final_df['Result'] == 'Defeat', 1, 2))

    colors_plot = {analysis_seasons[4]: 'rgb(216,62,135)',
                   analysis_seasons[3]: 'rgb(130,101,167)',
                   analysis_seasons[2]: 'rgb(179, 179, 179)',
                   analysis_seasons[1]: 'rgb(78,78,80)',
                   analysis_seasons[0]: 'rgb(200,11,1)'}

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
