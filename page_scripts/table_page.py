import streamlit as st
from page_scripts.stats_scripts.table_stats import filter_data, buli_table_data
from PIL import Image


def table_page(page_season, favourite_team):
    filter_season_df, match_day = filter_data(season=page_season)

    start_type = ["Total", "Home", "Away", "1st Period", "2nd Period"]
    if match_day <= 17:
        start_type.remove("2nd Period")

    season_type = st.sidebar.selectbox("Table Type", start_type)
    buli_season_df = buli_table_data(data=filter_season_df, table_type=season_type)

    st.header(f'Season {page_season}: {season_type} Table Games')

    logo_col, rank_col, team_col, mp_col, w_col, d_col, l_col, gf_col, ga_col, gd_col, pts_col = st.columns(
        [0.5, 1, 5, 1, 1, 1, 1, 1, 1, 1, 1])

    with logo_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b><font color='white'>#</font></b>", unsafe_allow_html=True)
        teams_logo = buli_season_df['Team'].unique()
        [st.image(Image.open(f'images/{teams_logo[i]}.png'),  width=26) for i in range(len(teams_logo))]
        pos_favourite_team = list(teams_logo).index(favourite_team)

    with rank_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>Rank</b>", unsafe_allow_html=True)
        rank = buli_season_df.index
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{rank[i]}</b></font>",
                     unsafe_allow_html=True)
         if i == pos_favourite_team else st.markdown(f"<p style='text-align: center;'p>{rank[i]}",
                                                     unsafe_allow_html=True) for i in range(len(rank))]

    with team_col:
        st.markdown(f"<h4 style='text-align: left;'h4><b>Team</b>", unsafe_allow_html=True)
        team_names = buli_season_df['Team'].values
        [st.markdown(f"<p style='text-align: left;'p><font color=#d20614><b>{team_names[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: left;'p>{team_names[i]}", unsafe_allow_html=True)
         for i in range(len(team_names))]

    with mp_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>MP</b>", unsafe_allow_html=True)
        matches_played = buli_season_df['MP'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{matches_played[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{matches_played[i]}", unsafe_allow_html=True)
         for i in range(len(matches_played))]

    with w_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>W</b>", unsafe_allow_html=True)
        team_wins = buli_season_df['W'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_wins[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_wins[i]}", unsafe_allow_html=True)
         for i in range(len(team_wins))]

    with d_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>D</b>", unsafe_allow_html=True)
        team_draws = buli_season_df['D'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_draws[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_draws[i]}", unsafe_allow_html=True)
         for i in range(len(team_draws))]

    with l_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>L</b>", unsafe_allow_html=True)
        team_defeats = buli_season_df['L'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_defeats[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_defeats[i]}", unsafe_allow_html=True)
         for i in range(len(team_defeats))]

    with gf_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>GF</b>", unsafe_allow_html=True)
        team_goals_for = buli_season_df['GF'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_for[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_goals_for[i]}", unsafe_allow_html=True)
         for i in range(len(team_goals_for))]

    with ga_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>GA</b>", unsafe_allow_html=True)
        team_goals_aga = buli_season_df['GA'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_aga[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_goals_aga[i]}", unsafe_allow_html=True)
         for i in range(len(team_goals_aga))]

    with gd_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>GD</b>", unsafe_allow_html=True)
        team_goals_diff = buli_season_df['GD'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_goals_diff[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_goals_diff[i]}", unsafe_allow_html=True)
         for i in range(len(team_goals_diff))]

    with pts_col:
        st.markdown(f"<h4 style='text-align: center;'h4><b>Pts</b>", unsafe_allow_html=True)
        team_points = buli_season_df['Pts'].values
        [st.markdown(f"<p style='text-align: center;'p><font color=#d20614><b>{team_points[i]}</b></font>",
                     unsafe_allow_html=True) if i == pos_favourite_team else
         st.markdown(f"<p style='text-align: center;'p>{team_points[i]}", unsafe_allow_html=True)
         for i in range(len(team_points))]
