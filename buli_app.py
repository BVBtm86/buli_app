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
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide",
                   page_title="Bundesliga App",
                   page_icon="⚽",
                   initial_sidebar_state="expanded")

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
statistics_type = ["Home", "Match Day Statistics", "Season Table", "Team Statistics", "Player Statistics",
                   "Player vs Player Statistics", "Goalkeeper Statistics", "Event Data", "Season Predictions"]
# statistics_track = st.sidebar.selectbox("Select Page", statistics_type)


def main():
    # Option Menu Bar
    with st.sidebar:
        st.subheader("Select Page")
        statistics_track = option_menu(menu_title=None,
                                       options=statistics_type,
                                       icons=["house-fill", "calendar3", "table", "reception-4",
                                              "person-lines-fill", "people-fill", "shield-shaded",
                                              "skip-forward-circle", "ui-radios"])

    # ##### Seasons
    # """To be changed at the beginning of each season to only contain the last 5 Seasons"""
    seasons = ['2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023']
    selected_season = st.sidebar.selectbox("Select Season", seasons, index=4)
    start_season = len(seasons) - 1

    # ##### Select Favourite Team
    season_teams = pd.read_csv(f"./data/Seasons_data/Bundesliga_Team_Statistics_{selected_season}.csv",
                               usecols=['Team'])['Team'].map(team_name_1).unique()
    season_teams.sort()
    favourite_team = st.sidebar.selectbox("Select Favourite Team", season_teams)

    if statistics_track == 'Home':
        st.header("")
        st.subheader("")
        st.markdown(
            'A statistical application that allows to analyse different types of football statistics for both Teams '
            'and players.<br> <br> <b>App Features</b>', unsafe_allow_html=True)

        """ 
        * Select your favourite team
        * Select Season you want to analyse  
        * Types of Statistics:
            * Season Table
            * Team Statistics
            * Player Statistics
            * Player vs Player Statistics
            * Goalkeeper Statistics
            * Event Data
        * Season Prediction based on historical team performance
        """

    # ##### Match Day Statistics
    elif statistics_track == 'Match Day Statistics':
        match_day_page(page_season=selected_season,
                       favourite_team=favourite_team)

    # ##### Season Table
    elif statistics_track == 'Season Table':
        table_page(page_season=selected_season,
                   favourite_team=favourite_team)

    # ##### Team Statistics
    elif statistics_track == 'Team Statistics':
        team_page(page_season=selected_season,
                  favourite_team=favourite_team)

    # ##### Player Statistics
    elif statistics_track == 'Player Statistics':
        player_page(all_seasons=seasons,
                    page_season=selected_season,
                    favourite_team=favourite_team)

    # ##### Player vs Player Statistics
    elif statistics_track == 'Player vs Player Statistics':
        player_vs_player_page(page_season=selected_season,
                              favourite_team=favourite_team)

    # ##### Goalkeeper Statistics
    elif statistics_track == 'Goalkeeper Statistics':
        gk_page(all_seasons=seasons,
                page_season=selected_season,
                favourite_team=favourite_team)

    # ##### Shots Event Statistics
    elif statistics_track == 'Event Data':
        shot_event_page(page_season=selected_season,
                        favourite_team=favourite_team)

    # ##### Season Predictions
    elif statistics_track == "Season Predictions":
        # ##### Game/Table Predictions
        prediction_type = st.sidebar.selectbox("Select Predictions", ["Games", "Season"])
        prediction_page(prediction_type=prediction_type,
                        season=seasons[-1],
                        favourite_team=favourite_team)

    # ##### Footer Page
    ref_col, fan_club_name, fan_club_logo = st.columns([10, 1, 1])
    with fan_club_name:
        st.markdown(f"<p style='text-align: left;'p>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right;'p>Created By: ", unsafe_allow_html=True)
    with fan_club_logo:
        bvb_ro_logo = Image.open('images/BVB_Romania.png')
        st.image(bvb_ro_logo, width=50)
        st.markdown("@ <b><font color = #d20614 style='text-align: center;'>"
                    "<a href='mailto:omescu.mario.lucian@gmail.com' style='text-decoration: none; '>"
                    "Mario Omescu</a></font></b>", unsafe_allow_html=True)
    with ref_col:
        st.markdown(
            f"<b><font color=#d20614>Data Reference:</font></b><ul><li><a href='https://fbref.com' "
            "style='text-decoration: none; '>Team & Players Stats</a></li><li><a href='https://www.bundesliga.com' "
            "style='text-decoration: none; '>Tracking Stats</a></li><li><a href='https://understat.com' "
            "style='text-decoration: none; '>Event Stats</a></li></ul>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
