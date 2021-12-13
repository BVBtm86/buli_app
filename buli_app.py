from page_scripts.day_page import *
from page_scripts.table_page import *
from page_scripts.team_page import *
from page_scripts.player_page import *
from page_scripts.player_vs_player_page import *
from page_scripts.gk_page import *
from page_scripts.event_shots_page import *
from page_scripts.season_predictions_page import *
import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

# ##### Logo
buli_logo = Image.open('images/Bundesliga.png')
buli_logo_col, text_col = st.columns([1, 10])
buli_container = st.container()
with buli_container:
    with buli_logo_col:
        st.image(buli_logo, use_column_width=True)
    with text_col:
        st.title("Bundesliga App")

# ##### Statistic Type
statistics_type = ["Match Day Statistics", "Season Table", "Team Statistics", "Player Statistics",
                   "Player vs Player Statistics", "Goalkeeper Statistics", "Event Data", "Season Predictions"]
statistics_track = st.sidebar.selectbox("Select Page", statistics_type)

# ##### Favourite Team
favourite_buli_teams = ["1. FC Köln", "1. FSV Mainz 05", "1. FC Union Berlin", "Arminia Bielefeld",
                        "Bayer 04 Leverkusen", "Borussia Dortmund", "Borussia Mönchengladbach", "Eintracht Frankfurt",
                        "FC Augsburg", "FC Bayern München", "Hertha Berlin", "RasenBallsport Leipzig",
                        "Sport-Club Freiburg", "SpVgg Greuther Fürth", "TSG 1899 Hoffenheim", "VfB Stuttgart",
                        "VfL Bochum 1848", "VfL Wolfsburg"]
favourite_team = st.sidebar.selectbox("Favourite Team", favourite_buli_teams)


def main():
    # ##### Seasons
    seasons = ['2017-2018', '2018-2019', '2019-2020', '2020-2021', '2021-2022']
    start_season = len(seasons) - 1

    # ##### Match Day Statistics
    if statistics_track == 'Match Day Statistics':
        match_day_page(seasons=seasons,
                       start_season=start_season,
                       favourite_team=favourite_team)

    # ##### Season Table
    elif statistics_track == 'Season Table':
        table_page(seasons=seasons,
                   start_season=start_season,
                   favourite_team=favourite_team)

    # ##### Team Statistics
    elif statistics_track == 'Team Statistics':
        team_page(seasons=seasons,
                  start_season=start_season,
                  favourite_team=favourite_team)

    # ##### Player Statistics
    elif statistics_track == 'Player Statistics':
        player_page(seasons=seasons,
                    start_season=start_season,
                    favourite_team=favourite_team)

    # ##### Player vs Player Statistics
    elif statistics_track == 'Player vs Player Statistics':
        player_vs_player_page(seasons=seasons,
                              start_season=start_season,
                              favourite_team=favourite_team)

    # ##### Goalkeeper Statistics
    elif statistics_track == 'Goalkeeper Statistics':
        gk_page(seasons=seasons,
                start_season=start_season,
                favourite_team=favourite_team)

    # ##### Shots Event Statistics
    elif statistics_track == 'Event Data':
        shot_event_page(seasons=seasons,
                        start_season=start_season,
                        favourite_team=favourite_team)

    # ##### Season Predictions
    elif statistics_track == "Season Predictions":
        # ##### Game/Table Predictions
        prediction_type = st.sidebar.selectbox("Select Predictions", ["Games", "Season"])
        prediction_page(prediction_type=prediction_type,
                        season=seasons[-1])

    # ##### Footer Page
    _, fan_club_name, fan_club_logo = st.columns([10, 1, 1])
    with fan_club_name:
        st.markdown(f"<p style='text-align: left;'p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: left;'p>Created By: ", unsafe_allow_html=True)
    with fan_club_logo:
        bvb_ro_logo = Image.open('images/BVB_Romania.png')
        st.image(bvb_ro_logo, width=50)
    _, name_col = st.columns([10, 1.75])
    with name_col:
        st.markdown("@ <b><font color = red><a href='mailto:omescu.mario.lucian@gmail.com' "
                    "style='text-decoration: none;'>Mario Omescu</a></font></b>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
