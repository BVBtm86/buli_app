from page_scripts.stats_scripts.player_vs_player_stats import *
from page_scripts.stats_scripts.player_stats import *
from PIL import Image
import streamlit as st


def player_vs_player_page(page_season, favourite_team):

    buli_player_season_df, _, final_players = season_player_data(season=page_season)
    teams_players = list(buli_player_season_df[buli_player_season_df['Venue'] == 'Home']['Team'].unique())
    teams_players.sort()
    pos_team_players = teams_players.index(favourite_team)

    # ##### Season Filter
    season_filter_player = ["Total", "Home", "Away", "1st Period", "2nd Period"]
    match_day_player = np.max(buli_player_season_df['Week_No'].values)
    if match_day_player <= 17:
        season_filter_player.remove("2nd Period")

    st.subheader(f"Player vs Player Statistics: Season {page_season}")
    radar_player_col, radar_chart_col, radar_vs_player_col = st.columns([3, 8, 3])
    with radar_vs_player_col:
        radar_compare_stat = st.selectbox("Comparison Statistics Type", ["Offensive", "Defensive", "Passing"])

    with radar_player_col:
        radar_compare_season_type = st.selectbox("Comparison Season Filter", season_filter_player)
        radar_team_main_player = st.selectbox("Comparison Player 1 Team", teams_players, pos_team_players)
        radar_main_players_compare = player_comparison_filter(data=buli_player_season_df,
                                                              season_filter=radar_compare_season_type,
                                                              team=radar_team_main_player,
                                                              players=final_players)
        radar_main_player = st.selectbox("Comparison Player 1", radar_main_players_compare)
        radar_main_team_player_logo = Image.open(f'images/{radar_team_main_player}.png')
        st.image(radar_main_team_player_logo, width=100)

    with radar_vs_player_col:
        radar_team_compare_player = st.selectbox("Comparison Player 2 Team", teams_players, pos_team_players)
        radar_compare_players_compare = player_comparison_filter(data=buli_player_season_df,
                                                                 season_filter=radar_compare_season_type,
                                                                 team=radar_team_compare_player,
                                                                 players=final_players,
                                                                 remove_player=radar_main_player)

        radar_compare_player = st.selectbox("Comparison Player 2", radar_compare_players_compare)
        radar_compare_team_player_logo = Image.open(f'images/{radar_team_compare_player}.png')
        st.image(radar_compare_team_player_logo, width=100)

    with radar_chart_col:
        radar_fig, radar_player_1_better, \
        radar_len_stats = player_comparison_radar(data=buli_player_season_df,
                                                  season_filter=radar_compare_season_type,
                                                  player_1=radar_main_player,
                                                  player_2=radar_compare_player,
                                                  stats_type=radar_compare_stat,
                                                  team_player_1=radar_team_main_player,
                                                  team_player_2=radar_team_compare_player)

        st.pyplot(radar_fig)

    with radar_player_col:
        st.markdown(
            f"In <b><font color = green>{radar_player_1_better}</font></b> of the <b><font color = green>"
            f"{radar_len_stats}</font></b> <b><font color = green>{radar_compare_stat}</font></b> Statistics, "
            f"<b><font color = #d20614>{radar_main_player}</font></b> of <b><font color = #d20614>"
            f"{radar_team_main_player}</font></b> has better on average statistics for <b><font color = green>"
            f"{radar_compare_season_type}</font></b> Season Games than <b><font color = grey>{radar_compare_player}"
            f"</font></b> of <b><font color = grey>{radar_team_compare_player}</font></b>.", unsafe_allow_html=True)
        st.markdown("<b><font color = #d20614>Note</font></b>: Only Players with at least <b>"
                    "<font color = #d20614>10%</font></b> of minutes played were included.",
                    unsafe_allow_html=True)

    st.subheader(f"Player vs Player Percentile: Season {page_season}")
    pizza_player_col, pizza_chart_col, pizza_vs_player_col = st.columns([3, 8, 3])
    with pizza_vs_player_col:
        pizza_compare_stat = st.selectbox("Percentile Statistics Type", ["Offensive", "Defensive", "Passing"])

    with pizza_player_col:
        pizza_compare_season_type = st.selectbox("Percentile Season Filter", season_filter_player)
        pizza_team_main_player = st.selectbox("Percentile Player 1 Team", teams_players, pos_team_players)
        pizza_main_players_compare = player_comparison_filter(data=buli_player_season_df,
                                                              season_filter=pizza_compare_season_type,
                                                              team=pizza_team_main_player,
                                                              players=final_players)
        pizza_main_player = st.selectbox("Percentile Player 1", pizza_main_players_compare)
        pizza_main_team_player_logo = Image.open(f'images/{pizza_team_main_player}.png')
        st.image(pizza_main_team_player_logo, width=100)

    with pizza_vs_player_col:
        pizza_team_compare_player = st.selectbox("Percentile Player 2 Team", teams_players, pos_team_players)
        pizza_compare_players_compare = player_comparison_filter(data=buli_player_season_df,
                                                                 season_filter=pizza_compare_season_type,
                                                                 team=pizza_team_compare_player,
                                                                 players=final_players,
                                                                 remove_player=pizza_main_player)

        pizza_compare_player = st.selectbox("Percentile Player 2", pizza_compare_players_compare)
        pizza_compare_team_player_logo = Image.open(f'images/{pizza_team_compare_player}.png')
        st.image(pizza_compare_team_player_logo, width=100)

    with pizza_chart_col:
        pizza_fig, pizza_player_1_better, pizza_player_2_better, pizza_len_stats = \
            player_comparison_pizza(data=buli_player_season_df,
                                    season_filter=pizza_compare_season_type,
                                    player_1=pizza_main_player,
                                    player_2=pizza_compare_player,
                                    stats_type=pizza_compare_stat)

        st.pyplot(pizza_fig)

        with pizza_player_col:
            st.markdown(
                f"In <b><font color = green>{pizza_player_1_better}</font></b> of the <b><font color = green>"
                f"{pizza_len_stats}</font></b> <b><font color = green>{pizza_compare_stat}</font></b> Statistics, "
                f"<b><font color = #d20614>{pizza_main_player}</font></b> of <b><font color = #d20614>"
                f"{pizza_team_main_player}</font></b> has better on average stats then 90% of the League for <b>"
                f"<font color = green>{radar_compare_season_type}</font></b> Season Games while in <b>"
                f"<font color = green>{pizza_player_2_better}</font></b> of the <b><font color = green>"
                f"{pizza_len_stats}</font></b> <b><font color = green>{pizza_compare_stat}</font></b> Statistics, <b>"
                f"<font color = #d20614>{pizza_compare_player}</font></b> of <b><font color = #d20614>"
                f"{pizza_team_compare_player}</font></b> has better on average stats then 90% of the League.",
                unsafe_allow_html=True)
