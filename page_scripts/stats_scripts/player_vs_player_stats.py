import numpy as np
from page_scripts.stats_scripts.utils import *
from mplsoccer import Radar, PyPizza, FontManager
from highlight_text import fig_text
import streamlit as st

player_offensive_stats_var = ['xg', "assisted_shots", "shots_total", "shots_on_target", "shot_accuracy", "sca",
                              "blocked_shots", "dribbles", "successful_dribbles"]

player_offensive_stats_names = ["XG", "Key Passes", "Shots", "Shots on Target", "Accuracy %", "Shot Created Actions",
                                "Blocked Shots", "Dribbles", "Dribbles %"]

player_defensive_stats_var = ['tackles', 'successful_tackles', "aerials_won_pct", "pressures", "pressure_regain_pct",
                              "clearances", "interceptions", "ball_recoveries", "blocks"]

player_defensive_stats_names = ["Tackles", "Tackles Won %", "Aerials Won %", "Pressure", "Pressure Won %", "Clearances",
                                "Interceptions", "Ball recoveries", "Blocks"]

player_passing_stats_var = ["touches", "passes", "passes_pct", "passes_into_final_third", "passes_into_penalty_area",
                            "progressive_passes", "passes_pressure", "crosses_into_penalty_area"]

player_passing_stats_names = ["Touches", "Passes", "Pass %", "Passes Final Third", "Passes Penalty Area",
                              "Progressive Passes", "Passes Under Pressure", "Crosses Penalty Area"]


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
    elif remove_player != "":
        final_buli_players = [player for player in avg_buli_players if player != remove_player]

    return final_buli_players


def player_comparison_radar(data, season_filter, stats_type, player_1, player_2, team_player_1, team_player_2):
    # ##### Season Filter Data
    season_data = data[data[season_filter] == 1].reset_index(drop=True)

    # ##### Select Stats
    if stats_type == 'Offensive':
        plot_stats_vars = player_offensive_stats_var.copy()
        plot_stats_names = player_offensive_stats_names.copy()
    elif stats_type == 'Defensive':
        plot_stats_vars = player_defensive_stats_var.copy()
        plot_stats_names = player_defensive_stats_names.copy()
    elif stats_type == 'Passing':
        plot_stats_vars = player_passing_stats_var.copy()
        plot_stats_names = player_passing_stats_names.copy()

    # ##### Create Player Stats
    player_df_1 = season_data[season_data['Name'] == player_1].reset_index(drop=True)
    player_stats_1 = np.round(player_df_1.groupby('Name')[plot_stats_vars].mean(), 2)
    player_stats_values_1 = player_stats_1.values.tolist()[0]

    player_df_2 = season_data[season_data['Name'] == player_2].reset_index(drop=True)
    player_stats_2 = np.round(player_df_2.groupby('Name')[plot_stats_vars].mean(), 2)
    player_stats_values_2 = player_stats_2.values.tolist()[0]

    # #### Create Plot Ranges
    min_stats = np.round(np.min(season_data.groupby('Name')[plot_stats_vars].mean()).values.tolist(), 2)
    max_stats = np.round(np.max(season_data.groupby('Name')[plot_stats_vars].mean()).values.tolist(), 2)

    # ##### Create Plot
    params = plot_stats_names.copy()

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
    rings_inner = radar.draw_circles(ax=axs['radar'], facecolor='#8265A7', edgecolor='#4e4e50')
    radar_output = radar.draw_radar_compare(player_stats_values_1, player_stats_values_2, ax=axs['radar'],
                                            kwargs_radar={'facecolor': '#c70b01', 'alpha': 0.5},
                                            kwargs_compare={'facecolor': '#4e4e50', 'alpha': 0.5})
    radar_poly, radar_poly2, vertices1, vertices2 = radar_output
    range_labels = radar.draw_range_labels(ax=axs['radar'], fontsize=15)
    param_labels = radar.draw_param_labels(ax=axs['radar'], fontsize=20)

    title1_text = axs['title'].text(0.01, 0.65, player_1, fontsize=25, color='#c70b01', ha='left', va='center')
    title2_text = axs['title'].text(0.01, 0.30, team_player_1, fontsize=20, ha='left', va='center', color='#c70b01')
    title3_text = axs['title'].text(0.99, 0.65, player_2, fontsize=25, ha='right', va='center', color='#4e4e50')
    title4_text = axs['title'].text(0.99, 0.30, team_player_2, fontsize=20, ha='right', va='center', color='#4e4e50')

    # ##### Markdown
    radar_player_1_better = np.sum(np.array(player_stats_values_1) > np.array(player_stats_values_2))
    radar_len_stats = len(player_stats_values_1)
    return fig_radar, radar_player_1_better, radar_len_stats


def player_comparison_pizza(data, season_filter, stats_type, player_1, player_2):
    # ##### Season Filter Data
    season_data = data[data[season_filter] == 1].reset_index(drop=True)

    # ##### Select Stats
    if stats_type == 'Offensive':
        plot_stats_vars = player_offensive_stats_var.copy()
        plot_stats_names = player_offensive_stats_names.copy()
    elif stats_type == 'Defensive':
        plot_stats_vars = player_defensive_stats_var.copy()
        plot_stats_names = player_defensive_stats_names.copy()
    elif stats_type == 'Passing':
        plot_stats_vars = player_passing_stats_var.copy()
        plot_stats_names = player_passing_stats_names.copy()

    # ##### Player Stats
    player_stats = np.round(
        season_data.groupby('Name')[plot_stats_vars].mean().rank(pct=True) * 100).reset_index()

    player_1_values = list(player_stats[player_stats['Name'] == player_1].values[0][1:])
    player_2_values = list(player_stats[player_stats['Name'] == player_2].values[0][1:])
    for i in range(len(player_1_values)):
        if np.isnan(player_1_values[i]):
            player_1_values[i] = 0
        if np.isnan(player_2_values[i]):
            player_2_values[i] = 0

    # ##### Pizza PLot
    # font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
    #                            "Roboto-Regular.ttf?raw=true"))
    # font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
    #                          "Roboto-Medium.ttf?raw=true"))

    baker = PyPizza(
        params=plot_stats_names,
        background_color="#FFFFFF",
        straight_line_color="#808080",
        straight_line_lw=1,
        last_circle_lw=1,
        last_circle_color="#808080",
        other_circle_ls="-.",
        other_circle_lw=1
    )

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
            color="#8265A7", fontsize=12,
            # fontproperties=font_normal.prop, va="center"
            va="center"
        ),
        kwargs_values=dict(
            color="#FFFFFF", fontsize=12,
            # fontproperties=font_bold.prop, zorder=3,
            zorder=3,
            bbox=dict(
                edgecolor="#8265A7", facecolor="#c70b01",
                boxstyle="round,pad=0.2", lw=1
            )
        ),
        kwargs_compare_values=dict(
            # color="#FFFFFF", fontsize=12, fontproperties=font_bold.prop, zorder=3,
            color="#FFFFFF", fontsize=12, zorder=3,
            bbox=dict(edgecolor="#808080", facecolor="#4e4e50", boxstyle="round,pad=0.2", lw=1)
        ),
    )

    fig_text(
        0.515, 0.99, f"<{player_1}> vs <{player_2}>", size=17, fig=pizza_fig,
        highlight_textprops=[{"color": '#c70b01'}, {"color": '#4e4e50'}],
        # ha="center", fontproperties=font_bold.prop, color="#8265A7")
        ha="center", color="#8265A7")

    # ##### Markdown
    pizza_player_1_better = np.sum(np.array(player_1_values) >= 90)
    pizza_player_2_better = np.sum(np.array(player_2_values) >= 90)
    pizza_len_stats = len(plot_stats_names)
    return pizza_fig, pizza_player_1_better, pizza_player_2_better, pizza_len_stats