from page_scripts.stats_scripts.event_shots_stats import *
import numpy as np
from PIL import Image


def shot_event_page(page_season, favourite_team):
    # ##### Season and Type of Event
    event_shots_type = st.sidebar.selectbox("Event Type", ['Team', 'Player'])
    season_event_shot_data = shot_event_data_process(season=page_season)
    filter_type = ["Total", "Home", "Away", "1st Period", "2nd Period"]
    if np.max(season_event_shot_data['Week_No']) < 18:
        filter_type.remove("2nd Period")
    teams_season = list(season_event_shot_data['Team'].unique())
    teams_season.sort()
    pos_team_event = teams_season.index(favourite_team)

    if event_shots_type == 'Team':
        header_col, logo_col, team_name_col, opp_col = st.columns([3, 0.5, 4, 4])
        with header_col:
            st.header("Team Shot Events")
        legend_col, pitch_col = st.columns([3, 11])
        with legend_col:
            season_type_filter = st.selectbox("Season Filter", filter_type)
            shot_event_team = st.selectbox("Select Team", teams_season, pos_team_event)

            shot_team_event_type = team_shot_event_type(data=season_event_shot_data,
                                                        team_name=shot_event_team,
                                                        season_filter=season_type_filter)

            st.markdown("<h4><b>Legend: </b></h4>", unsafe_allow_html=True)
            st.markdown("Size reflects <b>xGoal</b>", unsafe_allow_html=True)

            shot_events_type = []
            if 'Goal' in shot_team_event_type:
                goals_see = st.checkbox("⭐ Goals", True)
                if goals_see:
                    shot_events_type.append("Goal")
            if 'OwnGoal' in shot_team_event_type:
                own_goals_see = st.checkbox("➕ Own Goals", False)
                if own_goals_see:
                    shot_events_type.append("OwnGoal")
            if 'SavedShot' in shot_team_event_type:
                saved_shots_see = st.checkbox("🔴 Saved Shots", False)
                if saved_shots_see:
                    shot_events_type.append("SavedShot")
            if 'MissedShots' in shot_team_event_type:
                missed_shots_see = st.checkbox("🔺 Missed Shots", False)
                if missed_shots_see:
                    shot_events_type.append("MissedShots")
            if 'BlockedShot' in shot_team_event_type:
                blocked_shots_see = st.checkbox("🔻 Blocked Shots", False)
                if blocked_shots_see:
                    shot_events_type.append("BlockedShot")
            if 'ShotOnPost' in shot_team_event_type:
                shot_post_see = st.checkbox("🟥 Shot on Post", False)
                if shot_post_see:
                    shot_events_type.append("ShotOnPost")

        with pitch_col:
            shot_event_data, team_goals_box, team_shots_box, opp_goals_box, opp_shots_box, \
            best_team_goals_half_value, best_team_goals_half_score, best_team_shots_half_value, \
            best_team_shots_half_score, best_opp_goals_half_value, best_opp_goals_half_score, \
            best_opp_shots_half_value, best_opp_shots_half_score = team_event_data(data=season_event_shot_data,
                                                                                   team_name=shot_event_team,
                                                                                   season_filter=season_type_filter,
                                                                                   event_type=shot_events_type)

            shot_event_fig = team_event_plot(data=shot_event_data)
            st.pyplot(fig=shot_event_fig.figure)

        with logo_col:
            st.markdown("")
            team_logo = Image.open(f'images/{shot_event_team}.png')
            st.image(team_logo, width=50)
        with team_name_col:
            st.markdown("")
            st.subheader(shot_event_team)
        with opp_col:
            st.markdown("")
            st.subheader("Opponents")

        if team_goals_box != "":
            st.markdown(f"For <b><font color = #d20614>{season_type_filter}</font></b> Season Games, <b>"
                        f"<font color = #d20614>{team_goals_box}%</font></b> of <b><font color = black>{shot_event_team}"
                        f"</font></b> Goals were scored from Inside the Box, with <b><font color = #d20614>"
                        f"{best_team_goals_half_score}%</font></b> of them in the <b><font color = black>"
                        f"{best_team_goals_half_value}</font></b>, while her Opponents had <b><font color = #d20614>"
                        f"{opp_goals_box}%</font></b> Goals from Inside the Box, with <b><font color = #d20614>"
                        f"{best_opp_goals_half_score}%</font></b> of them in the <b><font color = black>"
                        f"{best_opp_goals_half_value}</font></b>. If we look at Total Shots, "
                        f"<b><font color = #d20614>{team_shots_box}%</font></b> of <b><font color = black>"
                        f"{shot_event_team}</font></b> Shots were from Inside the Box, with <b><font color = #d20614>"
                        f"{best_team_shots_half_score}%</font></b> of them in the <b><font color = #d20614>"
                        f"{best_team_shots_half_value}</font></b>, while her Opponents had <b><font color = #d20614>"
                        f"{opp_shots_box}%</font></b> Shots from Inside the Box, with <b><font color = #d20614>"
                        f"{best_opp_shots_half_score}%</font></b> of them in the <b><font color = black>"
                        f"{best_opp_shots_half_value}</font></b>.", unsafe_allow_html=True)

    else:
        header_col, logo_col, player_name_col = st.columns([6, 0.5, 4])
        with header_col:
            st.header("Player Shot Events")
        legend_col, _, pitch_col = st.columns([4, 1, 10])
        with legend_col:
            season_type_filter = st.selectbox("Season Filter", filter_type)
            shot_event_team = st.selectbox("Select Team", teams_season, pos_team_event)
            shot_event_players = players_team_events(data=season_event_shot_data,
                                                     team_name=shot_event_team,
                                                     season_filter=season_type_filter)
            shot_event_player = st.selectbox("Select Player", shot_event_players)

            player_event_type = player_shot_event_type(data=season_event_shot_data,
                                                       team_name=shot_event_team,
                                                       player_name=shot_event_player,
                                                       season_filter=season_type_filter)

            st.markdown("<h4><b>Legend: </b></h4>", unsafe_allow_html=True)
            st.markdown("Size reflects <b>xGoal</b>", unsafe_allow_html=True)

            shot_events_type = []
            if 'Goal' in player_event_type:
                goals_see = st.checkbox("⭐ Goals", True)
                if goals_see:
                    shot_events_type.append("Goal")
            if 'OwnGoal' in player_event_type:
                own_goals_see = st.checkbox("➕ Own Goals", False)
                if own_goals_see:
                    shot_events_type.append("OwnGoal")
            if 'SavedShot' in player_event_type:
                saved_shots_see = st.checkbox("🔴 Saved Shots", False)
                if saved_shots_see:
                    shot_events_type.append("SavedShot")
            if 'MissedShots' in player_event_type:
                missed_shots_see = st.checkbox("🔺 Missed Shots", False)
                if missed_shots_see:
                    shot_events_type.append("MissedShots")
            if 'BlockedShot' in player_event_type:
                blocked_shots_see = st.checkbox("🔻 Blocked Shots", False)
                if blocked_shots_see:
                    shot_events_type.append("BlockedShot")
            if 'ShotOnPost' in player_event_type:
                shot_post_see = st.checkbox("🟥 Shot on Post", False)
                if shot_post_see:
                    shot_events_type.append("ShotOnPost")

        with pitch_col:
            shot_event_data, player_goals_box, player_shots_box, best_player_goals_half_value, \
            best_player_goals_half_score, best_player_shots_half_value, \
            best_player_shots_half_score = player_event_data(data=season_event_shot_data,
                                                             team_name=shot_event_team,
                                                             player_name=shot_event_player,
                                                             season_filter=season_type_filter,
                                                             event_type=shot_events_type)

            shot_event_fig = player_event_plot(data=shot_event_data,
                                               event_type=shot_events_type)
            st.pyplot(fig=shot_event_fig.figure)

        with logo_col:
            st.markdown("")
            team_logo = Image.open(f'images/{shot_event_team}.png')
            st.image(team_logo, width=50)
        with player_name_col:
            st.markdown("")
            st.subheader(shot_event_player)

        if player_goals_box != "":
            st.markdown(f"For <b><font color = #d20614>{season_type_filter}</font></b> Season Games, <b>"
                        f"<font color = #d20614>{player_goals_box}%</font></b> of <b><font color = black>"
                        f"{shot_event_player}</font></b> Goals were scored from Inside the Box, with <b>"
                        f"<font color = #d20614>{best_player_goals_half_score}%</font></b> of them in the <b>"
                        f"<font color = black>{best_player_goals_half_value}</font></b> and <b><font color = #d20614>"
                        f"{player_shots_box}%</font></b> of Total Shots were from Inside the Box, with <b>"
                        f"<font color = #d20614>{best_player_shots_half_score}%</font></b> of them in the <b>"
                        f"<font color = black> {best_player_shots_half_value}</font></b>.", unsafe_allow_html=True)
        else:
            st.markdown(f"For <b><font color = #d20614>{season_type_filter}</font></b> Season Games, <b>"
                        f"<font color = #d20614>{player_shots_box}%</font></b> of Total Shots were from Inside the Box, "
                        f"with <b><font color = #d20614>{best_player_shots_half_score}%</font></b> of them in the <b>"
                        f"<font color = black> {best_player_shots_half_value}</font></b>.", unsafe_allow_html=True)
