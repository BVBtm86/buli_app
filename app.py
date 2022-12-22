import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
from page_scripts.day_page import match_day_page
from page_scripts.table_page import table_page
from page_scripts.team_page import team_page
from page_scripts.player_page import player_page
from page_scripts.gk_page import gk_page
from page_scripts.season_predictions_page import prediction_page
from page_scripts.stats_scripts.utilities import favourite_team_query

# ##### Logo
buli_logo = Image.open('images/Bundesliga.png')

st.set_page_config(layout="wide",
                   page_title="Bundesliga App",
                   page_icon=buli_logo,
                   initial_sidebar_state="expanded")

# ##### Hide Streamlit info
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

buli_logo_col, text_col = st.columns([1, 10])
buli_container = st.container()
with buli_container:
    with buli_logo_col:
        st.image(buli_logo, use_column_width=True)
    with text_col:
        st.markdown("")
        st.markdown(f"<h1><font color = #d20614>Bundesliga</font> Game Statistics <font color = #d20614></font>"
                    f"</h1>", unsafe_allow_html=True)

# ##### Statistic Type
statistics_type = ["Home", "Match Day Statistics", "Season Table", "Team Statistics", "Player Statistics",
                   "Goalkeeper Statistics", "Season Predictions"]
app_seasons = ["2018-2019", "2019-2020", "2020-2021", "2021-2022", "2022-2023"]


def main():
    # Option Menu Bar
    with st.sidebar:
        st.subheader("Select Page")
        statistics_track = option_menu(menu_title=None,
                                       options=statistics_type,
                                       icons=["house-fill", "calendar3", "table", "reception-4",
                                              "person-lines-fill", "shield-shaded", "ui-radios"],
                                       styles={"nav-link": {"--hover-color": "#e5e5e6"}})

    # ##### Seasons
    selected_season = st.sidebar.selectbox("Select Season", app_seasons, index=4)

    # ##### Select Favourite Team
    teams_season = favourite_team_query(season=selected_season)
    teams_season.sort()
    favourite_team = st.sidebar.selectbox(label="Select Favourite Team",
                                          options=teams_season,
                                          index=teams_season.index("Borussia Dortmund"))

    if statistics_track == 'Home':
        st.markdown("")
        st.markdown(
            '<b> A statistical application that allows the user to analyse different types of football statistics for '
            'both Teams and players.</b><br> <br> <font color=#d20614><b>App Features</b></font>',
            unsafe_allow_html=True)

        """ 
        * Select your favourite team
        * Select Season you want to analyse  
        * Types of Statistics:
            * Season Table
            * Team Statistics
            * Player Statistics
            * Player vs Player Statistics
            * Goalkeeper Statistics
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
                  favourite_team=favourite_team,
                  all_seasons=app_seasons)

    # ##### Player Statistics
    elif statistics_track == 'Player Statistics':
        player_page(page_season=selected_season,
                    favourite_team=favourite_team,
                    all_seasons=app_seasons)

    # ##### Goalkeeper Statistics
    elif statistics_track == 'Goalkeeper Statistics':
        gk_page(page_season=selected_season,
                favourite_team=favourite_team,
                all_seasons=app_seasons)

    # ##### Season Predictions
    elif statistics_track == "Season Predictions":
        # ##### Game/Table Predictions
        prediction_type = st.sidebar.selectbox("Select Predictions", ["Games", "Season"])
        prediction_page(prediction_type=prediction_type,
                        season=app_seasons[-1],
                        favourite_team=favourite_team)

    # ##### Footer Page
    if statistics_track == 'Home':
        # ##### App Description
        st.markdown(
                f"<b><font color=#d20614>Data Reference</font></b><ul><li><a href='https://fbref.com' "
                "style='text-decoration: none; '>Team & Players Stats</a></li><li><a href='https://www.bundesliga.com' "
                "style='text-decoration: none; '>Tracking Stats</a></li>", unsafe_allow_html=True)

        st.markdown(
                f"<b><font color=#d20614>App Development</font></b><ul><li><a href='https://supabase.com' "
                "style='text-decoration: none; '>Database Storage</a></li><li><a href='https://streamlit.io' "
                "style='text-decoration: none; '>UI Framework</a></li><li><a href='https://github.com/BVBtm86/buli_app'"
                " style='text-decoration: none; '>Code Repo</a></li>", unsafe_allow_html=True)
        _, fan_club_name, fan_club_logo = st.columns([10, 1, 1])
        with fan_club_name:
            st.markdown(f"<p style='text-align: left;'p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: right;'p>Created By: ", unsafe_allow_html=True)
        with fan_club_logo:
            bvb_ro_logo = Image.open('images/BVB_Romania.png')
            st.image(bvb_ro_logo, width=50)
            st.markdown("@ <b><font color = #d20614 style='text-align: center;'>"
                        "<a href='mailto:omescu.mario.lucian@gmail.com' style='text-decoration: none; '>"
                        "Mario Omescu</a></font></b>", unsafe_allow_html=True)


if __name__ == '__main__':
    main()
