import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from scipy.stats import ttest_ind
from page_scripts.stats_scripts.utilities import season_gk_query, all_gk_query

gk_stats_total = ["Shots on Target", "Goals Conceded", "Saves", "Post-Shot xGoal", "Passes 35m+ Completed",
                  "Passes 35m+", "Passes", "Throws", "Avg Pass Length", "Goal Kicks", "Avg Goal Kick Length",
                  "Crosses Faced", "Crosses Stopped", "Sweeper Actions", "Sweeper Avg Distance"]

gk_stats_avg = ["Shots on Target", "Goals Conceded", "Saves", "Saves %", "Post-Shot xGoal", "Passes 35m+ Completed",
                "Passes 35m+", "Passes 35m+ Completed %", "Passes", "Throws", "Avg Pass Length", "Goal Kicks",
                "Goal Kicks %", "Avg Goal Kick Length", "Crosses Faced", "Crosses Stopped", "Crosses Stopped %",
                "Sweeper Actions", "Sweeper Avg Distance"]

# #### Aggregate Stats for Percentage Calculation
gk_perc_calculations = ["Saves %", "Passes 35m+ Completed %", "Crosses Stopped %"]

gk_agg_perc = {
    "Saves %": ["Shots on Target", "Saves"],
    "Passes 35m+ Completed %": ["Passes 35m+", "Passes 35m+ Completed"],
    "Crosses Stopped %": ["Crosses Faced", "Crosses Stopped"]}


@st.cache
def season_gk_data(season):
    # ##### Read Data
    buli_df_gk = season_gk_query(season=season)

    # ##### Add Filter Type Stats
    buli_df_gk['Total'] = 1
    buli_df_gk['Home'] = np.where(buli_df_gk['Venue'] == "Home", 1, 0)
    buli_df_gk['Away'] = np.where(buli_df_gk['Venue'] == "Away", 1, 0)
    buli_df_gk["1st Period"] = np.where(buli_df_gk["Week_No"] <= 17, 1, 0)
    buli_df_gk["2nd Period"] = np.where(buli_df_gk["Week_No"] >= 18, 1, 0)
    buli_df_gk["Win"] = np.where(buli_df_gk["Result"] == 'Win', 1, 0)
    buli_df_gk["Draw"] = np.where(buli_df_gk["Result"] == 'Draw', 1, 0)
    buli_df_gk["Defeat"] = np.where(buli_df_gk["Result"] == 'Defeat', 1, 0)

    # ##### Total Players
    buli_df_gk['Name_Team'] = buli_df_gk['Team'] + "_" + buli_df_gk['Name']
    total_gk = list(buli_df_gk['Name'].unique())
    total_gk.sort()

    # ##### Players for the Avg Analysis
    filter_gk_avg = pd.DataFrame(buli_df_gk.groupby(['Name', 'Team'])['Minutes'].sum().reset_index())
    filter_gk_avg['Name_Team'] = filter_gk_avg['Team'] + "_" + filter_gk_avg['Name']
    minutes_cutoff = (buli_df_gk['Week_No'].max() * 90) * 0.1
    avg_gk = list(filter_gk_avg[filter_gk_avg['Minutes'] >= minutes_cutoff]['Name_Team'].unique())
    avg_gk.sort()

    return buli_df_gk, total_gk, avg_gk


def gk_top_statistics(data, season_filter, avg_gk, stat_top10, type_top10):
    # ##### Filter Data
    avg_data = data.copy()
    avg_data['Name_Team'] = avg_data['Team'] + "_" + avg_data['Name']
    top10_df = data[(data[season_filter] == 1)].reset_index(drop=True)
    top10_avg_df = avg_data[(avg_data[season_filter] == 1) & (avg_data['Name_Team'].isin(avg_gk))].reset_index(drop=True)

    # ##### Create Top 10 Data
    if type_top10 == 'Total':
        stat_plot = stat_top10
        top10_gk_group_df = top10_df.groupby(["Name", "Team"])[stat_plot].sum().reset_index()
        top10_plot_data = top10_gk_group_df.nlargest(10, stat_plot)
        top10_plot_data.rename(columns={stat_plot: stat_top10}, inplace=True)
    elif type_top10 == 'Average':
        stat_plot = stat_top10
        if stat_top10 in gk_perc_calculations:
            stats_agg = gk_agg_perc[stat_top10]
            top10_gk_group_avg_df = top10_avg_df.groupby(["Name", "Team"])[stats_agg].sum()
            top10_gk_group_avg_df[stat_plot] = \
                np.round(top10_gk_group_avg_df[stats_agg[1]] / top10_gk_group_avg_df[stats_agg[0]] * 100,2)
            top10_gk_group_avg_df = top10_gk_group_avg_df[stat_plot]
            top10_gk_group_avg_df = top10_gk_group_avg_df.reset_index()
        else:
            top10_gk_group_avg_df = np.round(top10_avg_df.groupby(["Name", "Team"])[stat_plot].mean().reset_index(), 2)
        top10_plot_data = top10_gk_group_avg_df.nlargest(10, stat_plot).nlargest(10, stat_plot)
        top10_plot_data.rename(columns={stat_plot: stat_top10}, inplace=True)

    if type_top10 == "Total":
        plot_title = f"Top 10 <b>{stat_top10}</b> for <b>{season_filter}</b> Season Games"
    else:
        plot_title = f"Top 10 Average <b>{stat_top10}</b> per Game for <b>{season_filter}</b> Season Games"

    min_value = np.min(top10_plot_data[stat_top10]) * 0.75
    max_value = np.max(top10_plot_data[stat_top10]) * 1.1

    # ##### Create Plot
    top10_gk_fig = px.bar(top10_plot_data,
                          x="Name",
                          y=stat_top10,
                          text=stat_top10,
                          title=plot_title,
                          hover_data=['Team'])

    top10_gk_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value]
    )

    top10_gk_fig.update_traces(marker_color='rgb(200,11,1)')
    if type_top10 == "Total":
        top10_gk_fig.update_yaxes(title_text=f"Total {stat_top10}")
    else:
        top10_gk_fig.update_yaxes(title_text=f"Average {stat_top10} per Game")

    return top10_gk_fig


def gk_chart_day(data, avg_gk, gk_name, stat_name):
    # ##### Filter Player and Stat Data
    full_data = data[(data['Name_Team'].isin(avg_gk))].reset_index(drop=True)
    gk_df = data[(data['Name'] == gk_name) & (data['Name_Team'].isin(avg_gk))].reset_index(drop=True)
    week_no = data['Week_No'].max()
    gk_team_name = gk_df['Team'].unique()[0]

    # ##### Plot Data
    min_value = 0
    max_value = np.max(gk_df[stat_name])

    fig_gk_day = px.bar(gk_df,
                        x="Week_No",
                        y=stat_name,
                        color="Result",
                        color_discrete_map={
                            'Win': "rgb(200,11,1)",
                            'Draw': "rgb(179, 179, 179)",
                            'Defeat': "rgb(78,78,80)"},
                        text=stat_name,
                        title=f"<b>{gk_name}</b>: <b>{stat_name}</b> per Match Day")
    fig_gk_day.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        xaxis=dict(
            tickmode='array',
            tickvals=[i for i in range(1, week_no + 1)],
        ),
        yaxis_range=[min_value, max_value]
    )
    fig_gk_day.update_yaxes(title_text=stat_name, col=1)

    # ##### Markdown
    if stat_name in gk_perc_calculations:
        stats_agg = gk_agg_perc[stat_name]
        gk_average = np.round(gk_df[stats_agg[1]].sum() / gk_df[stats_agg[0]].sum() * 100,2)
        league_average = np.round(full_data[stats_agg[1]].sum() / full_data[stats_agg[0]].sum() * 100,2)
    else:
        gk_average = np.nanmean(gk_df[stat_name])
        league_average = np.nanmean(full_data[stat_name])

    if gk_average > league_average:
        gk_league_comparison = "More"
    else:
        gk_league_comparison = "Less"

    gk_stat_sig = ttest_ind(gk_df[stat_name].values,
                            full_data[stat_name].values)[1]

    if gk_df.shape[0] >= 10:
        if gk_stat_sig <= 0.05:
            if gk_average > league_average:
                gk_stat_sig_name = "Statistically Better"
            elif gk_average < league_average:
                gk_stat_sig_name = "Statistically Worse"
            else:
                gk_stat_sig_name = ""
        else:
            gk_stat_sig_name = ""
    else:
        gk_stat_sig_name = ""

    return fig_gk_day, gk_team_name, gk_league_comparison, gk_stat_sig_name


def gk_season_filter_stats(data, player_name, avg_gk, stat_name):
    # ##### Filter Season Data by Season Type
    avg_data = data.copy()
    gk_df = data[(data['Name'] == player_name) & (data['Name_Team'].isin(avg_gk))].reset_index(drop=True)
    league_df = avg_data[avg_data['Name_Team'].isin(avg_gk)].reset_index(drop=True)

    # ##### Stats Type Results
    stats_types_gk = ['Total', 'Home', 'Away', '1st Period', '2nd Period', 'Win', 'Draw', 'Defeat']

    # ##### Create Data
    names_stats = []
    gk_stats = []
    gk_name = []
    for i in range(len(stats_types_gk)):
        length_stat = gk_df[gk_df[stats_types_gk[i]] == 1].shape[0]
        if length_stat > 0:
            names_stats.append(stats_types_gk[i])
            names_stats.append(stats_types_gk[i])
            if stat_name in gk_perc_calculations:
                stats_agg = gk_agg_perc[stat_name]
                #### Player Calculations
                gk_stats_filter_calc = gk_df.groupby(stats_types_gk[i])[stats_agg].sum()
                gk_stats_filter_calc = pd.DataFrame(gk_stats_filter_calc.loc[1,:]).T
                gk_stats_filter_calc[stat_name] = \
                    np.round(gk_stats_filter_calc[stats_agg[1]] / gk_stats_filter_calc[stats_agg[0]] * 100, 2)
                gk_stats_filter_calc = gk_stats_filter_calc[stat_name].values[0]
                #### League Calculations
                league_stats_filter_calc = league_df.groupby(stats_types_gk[i])[stats_agg].sum()
                league_stats_filter_calc = pd.DataFrame(league_stats_filter_calc.loc[1,:]).T
                league_stats_filter_calc[stat_name] = \
                    np.round(league_stats_filter_calc[stats_agg[1]] / league_stats_filter_calc[stats_agg[0]] * 100, 2)
                league_stats_filter_calc = league_stats_filter_calc[stat_name].values[0]

                gk_stats.append(gk_stats_filter_calc)
                gk_stats.append(league_stats_filter_calc)
            else:
                gk_stats.append(np.round(gk_df.groupby(stats_types_gk[i])[stat_name].mean().values[-1], 2))
                gk_stats.append(np.round(league_df.groupby(stats_types_gk[i])[stat_name].mean().values[-1], 2))
            gk_name.append(player_name)
            gk_name.append("League Average")

    gk_season_type = pd.DataFrame([names_stats, gk_stats, gk_name]).T
    gk_season_type.columns = ['Type', stat_name, 'Averages']

    min_value = np.min(gk_season_type[stat_name]) * 0.75
    max_value = np.max(gk_season_type[stat_name]) * 1.1

    # ##### Plot Data
    gk_stat_fig = px.bar(gk_season_type,
                         x="Type",
                         y=stat_name,
                         color="Averages",
                         barmode='group',
                         color_discrete_map={
                             player_name: "rgb(200,11,1)",
                             "League Average": "rgb(78,78,80)"},
                         text=stat_name,
                         title=f"<b>{player_name}</b> {stat_name} Stats by Season Type")
    gk_stat_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    gk_stat_fig.update_yaxes(title_text=stat_name)

    # ##### Markdown
    if ('Home' in list(gk_season_type['Type'].values)) and ('Away' in list(gk_season_type['Type'].values)):
        if gk_season_type.iloc[2, 1] > gk_season_type.iloc[4, 1]:
            gk_home_away = "Home"
        else:
            gk_home_away = "Away"
    else:
        gk_home_away = ""

    return gk_stat_fig, gk_home_away


def gk_relationship_data(data, filter_type, player_name, avg_gk, stat_x, stat_y, stat_size):
    # ##### Filter Data
    avg_data = data.copy()
    league_df = avg_data[(avg_data[filter_type] == 1) & (avg_data['Name_Team'].isin(avg_gk))].reset_index(drop=True)
    gk_corr_team = league_df[(league_df['Name'] == player_name) &
                             (avg_data['Name_Team'].isin(avg_gk))]['Team'].unique()[0]

    if stat_x in gk_perc_calculations:
        stats_x_agg = gk_agg_perc[stat_x]
        stat_x_calculation = league_df.groupby(["Name"])[stats_x_agg].sum()
        stat_x_calculation[stat_x] = \
            np.round(stat_x_calculation[stats_x_agg[1]] / stat_x_calculation[stats_x_agg[0]] * 100, 2)
        stat_x_calculation = stat_x_calculation[stat_x]
    else:
        stat_x_calculation = np.round(league_df.groupby('Name')[stat_x].mean(), 2)
    if stat_y in gk_perc_calculations:
        stats_y_agg = gk_agg_perc[stat_y]
        stat_y_calculation = league_df.groupby(["Name"])[stats_y_agg].sum()
        stat_y_calculation[stat_y] = \
            np.round(stat_y_calculation[stats_y_agg[1]] / stat_y_calculation[stats_y_agg[0]] * 100, 2)
        stat_y_calculation = stat_y_calculation[stat_y]
    else:
        stat_y_calculation = np.round(league_df.groupby('Name')[stat_y].mean(), 2)
    if stat_size in gk_perc_calculations:
        stats_size_agg = gk_agg_perc[stat_size]
        stat_size_calculation = league_df.groupby(["Name"])[stats_size_agg].sum()
        stat_size_calculation[stat_size] = \
            np.round(stat_size_calculation[stats_size_agg[1]] / stat_size_calculation[stats_size_agg[0]] * 100, 2)
        stat_size_calculation = stat_size_calculation[stat_size]
    else:
        stat_size_calculation = np.round(league_df.groupby('Name')[stat_size].mean(), 2)

    gk_group_df = pd.merge(left=stat_x_calculation, right=stat_y_calculation, left_index=True, right_index=True)
    gk_group_df = pd.merge(left=gk_group_df, right=stat_size_calculation, left_index=True, right_index=True)
    gk_group_df.reset_index(inplace=True)
    gk_group_df['Group'] = np.where(gk_group_df['Name'] == player_name, player_name, "Bundesliga")

    # ##### Average Plot
    gk_corr_fig = px.scatter(gk_group_df,
                             x=stat_x,
                             y=stat_y,
                             size=stat_size,
                             color='Group',
                             hover_name='Name',
                             color_discrete_map={
                                 player_name: "rgb(200,11,1)",
                                 "Bundesliga": "rgb(78,78,80)"},
                             title=f"<b>{player_name}</b> {stat_x} vs {stat_y} Relationship by {filter_type} "
                                   f"Season Games")

    gk_corr_fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)"})
    gk_corr_fig.update_xaxes(title_text=stat_x)
    gk_corr_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown
    filter_gk_df = league_df[(league_df['Name'] == player_name) & (league_df['Team'] == gk_corr_team)].reset_index(
        drop=True)
    if filter_gk_df[[stat_x, stat_y]].dropna().shape[0] >= 10:
        gk_corr_value = np.round(filter_gk_df[[stat_x, stat_y]].dropna().corr().iloc[0, 1], 2)
        if np.abs(gk_corr_value) <= 0.3:
            gk_corr_strength = "Weak"
        elif (np.abs(gk_corr_value) > 0.3) and (np.abs(gk_corr_value) <= 0.7):
            gk_corr_strength = "Moderate"
        else:
            gk_corr_strength = "Strong"
        if gk_corr_value < 0:
            gk_corr_sign = "Negative"
        else:
            gk_corr_sign = "Positive"
    else:
        gk_corr_value = ""
        gk_corr_strength = ""
        gk_corr_sign = ""

    return gk_corr_fig, gk_corr_team, gk_corr_value, gk_corr_strength, gk_corr_sign


@st.cache
def buli_gk_data(season, team, all_seasons):
    # ##### Read Data
    buli_df_gk = all_gk_query(all_seasons=all_seasons)

    # ##### Add Filter Type Stats
    buli_df_gk['Total'] = 1
    buli_df_gk['Home'] = np.where(buli_df_gk['Venue'] == "Home", 1, 0)
    buli_df_gk['Away'] = np.where(buli_df_gk['Venue'] == "Away", 1, 0)
    buli_df_gk["1st Period"] = np.where(buli_df_gk["Week_No"] <= 17, 1, 0)
    buli_df_gk["2nd Period"] = np.where(buli_df_gk["Week_No"] >= 18, 1, 0)
    buli_df_gk["Win"] = np.where(buli_df_gk["Result"] == 'Win', 1, 0)
    buli_df_gk["Draw"] = np.where(buli_df_gk["Result"] == 'Draw', 1, 0)
    buli_df_gk["Defeat"] = np.where(buli_df_gk["Result"] == 'Defeat', 1, 0)

    # ##### Filter Data
    buli_df_gk['Name_Team'] = buli_df_gk['Team'] + "_" + buli_df_gk['Name']
    gk_current_season = buli_df_gk[buli_df_gk['Season'] == season].reset_index(drop=True)

    # ##### Players for the Avg Analysis
    filter_gk_avg = pd.DataFrame(gk_current_season.groupby(['Name', 'Team'])['Minutes'].sum().reset_index())
    filter_gk_avg['Name_Team'] = filter_gk_avg['Team'] + "_" + filter_gk_avg['Name']
    minutes_cutoff = (gk_current_season['Week_No'].max() * 90) * 0.1
    avg_gk = list(filter_gk_avg[filter_gk_avg['Minutes'] >= minutes_cutoff]['Name_Team'].unique())
    avg_gk.sort()

    return buli_df_gk, avg_gk


def gk_current_season_team(data, season, avg_gk, player):
    # ##### Player Data
    gk_team = data[(data['Season'] == season)
                   & (data['Name'] == player)
                   & (data['Name_Team'].isin(avg_gk))]['Team'].unique()[0]

    return gk_team


def gk_buli_stats(data, gk_team, gk_name, avg_gk, stat_name, filter_type, analysis_seasons):
    # ##### Filter Season Data by Season Type
    gk_df = data[(data['Team'] == gk_team) & (data['Name'] == gk_name)
                 & (data['Name_Team'].isin(avg_gk)) & (data[filter_type] == 1)].reset_index(drop=True)
    gk_df_seasons = list(gk_df['Season'].unique())
    league_df = data[(data['Season'].isin(gk_df_seasons)) & (data['Name_Team'].isin(avg_gk))
                     & (data[filter_type] == 1)].reset_index(drop=True)

    # ##### Create Stats
    if stat_name in gk_agg_perc:
        stats_agg = gk_agg_perc[stat_name]
        # ##### Player Calculations
        gk_season_stats = gk_df.groupby(["Season"])[stats_agg].sum()
        gk_season_stats[stat_name] = \
            np.round(gk_season_stats[stats_agg[1]] / gk_season_stats[stats_agg[0]] * 100, 2)
        gk_season_stats = gk_season_stats[stat_name]
        # ##### League Calculations
        league_season_stats = league_df.groupby(["Season"])[stats_agg].sum()
        league_season_stats[stat_name] = \
            np.round(league_season_stats[stats_agg[1]] / league_season_stats[stats_agg[0]] * 100, 2)
        league_season_stats = league_season_stats[stat_name]
        gk_season_stats = gk_season_stats.reset_index()
        league_season_stats = league_season_stats.reset_index()
    else:
        gk_season_stats = np.round(gk_df.groupby('Season')[stat_name].mean(), 2).reset_index()
        league_season_stats = np.round(league_df.groupby('Season')[stat_name].mean(), 2).reset_index()
    gk_season_stats['Averages'] = gk_name
    league_season_stats['Averages'] = 'League Average'
    season_stats = pd.concat([gk_season_stats, league_season_stats])

    min_value = np.min(season_stats[stat_name]) * 0.5
    max_value = np.max(season_stats[stat_name]) * 1.1

    # ##### Plot Data
    gk_buli_fig = px.bar(season_stats,
                         x="Season",
                         y=stat_name,
                         color="Averages",
                         barmode='group',
                         color_discrete_map={
                             gk_name: "rgb(200,11,1)",
                             "League Average": "rgb(78,78,80)"},
                         text=stat_name,
                         title=f"<b>{gk_name}</b> {stat_name} Stats by Season Type")
    gk_buli_fig.update_layout({
        "plot_bgcolor": "rgba(0, 0, 0, 0)"},
        yaxis_range=[min_value, max_value])

    gk_buli_fig.update_yaxes(title_text=stat_name)

    # ##### Markdown
    current_season = analysis_seasons
    if current_season in list(gk_season_stats['Season'].unique()):
        if len(gk_df_seasons) > 1:
            gk_season_stats['Rank'] = gk_season_stats[stat_name].rank(ascending=False)
            gk_rank_season = int(gk_season_stats[gk_season_stats['Season'] == current_season]['Rank'])
            gk_better_seasons = sum(gk_season_stats[stat_name] > league_season_stats[stat_name])
            gk_no_seasons = len(gk_df_seasons)
        else:
            gk_rank_season = f"Only 1 season for {gk_team} over the past 5 years."
            gk_better_seasons = ""
            gk_no_seasons = 1
    else:
        gk_rank_season = "No Data"
        gk_better_seasons = ""
        gk_no_seasons = 0

    return gk_buli_fig, gk_rank_season, gk_better_seasons, gk_no_seasons


def gk_buli_corr_data(data, filter_type, team, player, stat_x, stat_y, avg_gk, analysis_seasons):
    # ##### Filter Data
    filter_df_gk = data[(data['Season'].isin(analysis_seasons))
                        & (data['Name_Team'].isin(avg_gk))
                        & (data['Team'] == team)
                        & (data['Name'] == player)
                        & (data[filter_type] == 1)].reset_index(
        drop=True)

    filter_df_gk['Points'] = np.where(filter_df_gk['Result'] == 'Win', 3,
                                      np.where(filter_df_gk['Result'] == 'Defeat', 1, 2))

    colors_plot = {analysis_seasons[-5]: 'rgb(216,62,135)',
                   analysis_seasons[-4]: 'rgb(130,101,167)',
                   analysis_seasons[-3]: 'rgb(179, 179, 179)',
                   analysis_seasons[-2]: 'rgb(78,78,80)',
                   analysis_seasons[-1]: 'rgb(200,11,1)'}

    # ##### Average Plot
    gk_seasons_fig = px.scatter(filter_df_gk,
                                x=stat_x,
                                y=stat_y,
                                color='Season',
                                hover_name='Name',
                                color_discrete_map=colors_plot,
                                size='Points',
                                title=f"<b>{stat_x}</b> vs <b>{stat_y}</b> Relationship by {filter_type} Season "
                                      f"Games")

    gk_seasons_fig.update_layout({"plot_bgcolor": "rgba(0, 0, 0, 0)"})
    gk_seasons_fig.update_xaxes(title_text=stat_x)
    gk_seasons_fig.update_yaxes(title_text=stat_y)

    # ##### Markdown stats
    # Overall Correlation
    gk_overall_corr_value = np.round(filter_df_gk[[stat_x, stat_y]].corr().iloc[1, 0], 3)
    if np.abs(gk_overall_corr_value) <= 0.3:
        gk_overall_corr_strength = "Weak"
    elif (np.abs(gk_overall_corr_value) > 0.3) and (np.abs(gk_overall_corr_value) <= 0.7):
        gk_overall_corr_strength = "Moderate"
    else:
        gk_overall_corr_strength = "Strong"

    if gk_overall_corr_value < 0:
        gk_overall_corr_sign = "Negative"
    else:
        gk_overall_corr_sign = "Positive"

    filter_df_gk['Games'] = 1
    no_games_season = filter_df_gk.groupby('Season')['Games'].count().reset_index()
    valid_seasons_gk = no_games_season[no_games_season['Games'] >= 10]['Season'].values
    corr_season_df = filter_df_gk[filter_df_gk['Season'].isin(valid_seasons_gk)].reset_index()

    no_seasons_gk = len(valid_seasons_gk)
    # Season Correlation
    if no_seasons_gk > 1:
        gk_season_corr = corr_season_df.groupby('Season')[stat_x, stat_y].corr().reset_index()
        gk_season_corr = gk_season_corr[gk_season_corr['level_1'] == stat_y]
        gk_season_corr['Rank'] = np.abs(gk_season_corr[stat_x]).rank(ascending=False)
        gk_season_name_best_corr = gk_season_corr[gk_season_corr['Rank'] == 1]['Season'].values[0]
        gk_season_value_best_corr = np.round(gk_season_corr[gk_season_corr['Rank'] == 1][stat_x].values[0], 3)

        if np.abs(gk_season_value_best_corr) <= 0.3:
            gk_season_corr_strength = "Weak"
        elif (np.abs(gk_season_value_best_corr) > 0.3) and (np.abs(gk_season_value_best_corr) <= 0.7):
            gk_season_corr_strength = "Moderate"
        else:
            gk_season_corr_strength = "Strong"

        if gk_season_value_best_corr < 0:
            gk_season_corr_sign = "Negative"
        else:
            gk_season_corr_sign = "Positive"
    else:
        gk_season_name_best_corr = ""
        gk_season_value_best_corr = 0
        gk_season_corr_strength = 0
        gk_season_corr_sign = 0

    gk_no_games = len(filter_df_gk)
    return gk_seasons_fig, gk_overall_corr_value, gk_overall_corr_strength, gk_overall_corr_sign, \
           gk_season_name_best_corr, gk_season_value_best_corr, gk_season_corr_strength, gk_season_corr_sign, \
           gk_no_games