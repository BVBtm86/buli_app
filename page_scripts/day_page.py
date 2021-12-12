from page_scripts.stats_scripts.day_stats import *
from page_scripts.stats_scripts.table_stats import *
from PIL import Image


def match_day_page(seasons, start_season, favourite_team):
    # ##### Match Day Statistics
    buli_season = st.sidebar.selectbox("Select Season", seasons, index=start_season)
    team_filter = st.sidebar.selectbox("Team Filter", ['Home', 'Away'])
    st.header(f'Match Day Statistics: {buli_season}')
    season_buli_df = match_day_process_data(buli_season)
    stat_name, home_col, home_logo_col, _, away_col, away_logo_col = st.columns([1.75, 2, 1, 0.5, 2, 1])

    if team_filter == 'Home':
        with home_col:
            teams_1 = list(season_buli_df[season_buli_df['Venue'] == 'Home']['Team'].unique())
            pos_team = teams_1.index(favourite_team)
            home_team = st.selectbox("Home Team", teams_1, pos_team)
        with away_col:
            teams_2 = list(season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Venue'] == 'Home')][
                               'Opponent'].unique())
            away_team = st.selectbox("Away Team", teams_2)
    else:
        with away_col:
            teams_2 = list(season_buli_df[season_buli_df['Venue'] == 'Away']['Team'].unique())
            pos_team = teams_2.index(favourite_team)
            away_team = st.selectbox("Away Team", teams_2, pos_team)
        with home_col:
            teams_1 = list(season_buli_df[(season_buli_df['Team'] == away_team) & (season_buli_df['Venue'] == 'Away')][
                               'Opponent'].unique())
            home_team = st.selectbox("Home Team", teams_1)

    with home_logo_col:
        home_logo = Image.open(f'images/{home_team}.png')
        st.image(home_logo, width=100)

    with away_logo_col:
        away_logo = Image.open(f'images/{away_team}.png')
        st.image(away_logo, width=100)

    stats_type = ["General", "Offensive", "Defensive", "Passing", "Goalkeeper", "Shot Events"]
    stats_options = st.sidebar.selectbox("Statistics", stats_type)

    _, _, home_score, away_score = st.columns([0.2, 0.8, 2.25, 3])
    with home_score:
        home_goals = season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                         (season_buli_df['Venue'] == 'Home')]['goals'].values[0] + season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team)][
                         'own_goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{home_goals}</h1>", unsafe_allow_html=True)
    with away_score:
        away_goals = season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                         (season_buli_df['Venue'] == 'Away')]['goals'].values[0] + season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team)][
                         'own_goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{away_goals}</h1>", unsafe_allow_html=True)

    # ##### General Statistics
    if stats_options == 'General':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>General Stats</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.25, 0.75, 2.25, 3])
        with icon_col:
            for i in range(len(general_stats_names)):
                st.markdown(general_emoji[i])

        with stat_name_col:
            for i in range(len(general_stats_names)):
                st.markdown(general_stats_names[i])

        with home_stat_col:
            for i in range(len(general_stats_names)):
                home_stat = \
                    season_buli_df[
                        (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                        (season_buli_df['Venue'] == 'Home')][general_stats_vars[i]].values[0]
                if general_stats_names[i] == "Possession" or general_stats_names[i] == "Aerial Duels %":
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}", unsafe_allow_html=True)

        with away_stat_col:
            for i in range(len(general_stats_names)):
                away_stat = \
                    season_buli_df[
                        (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                        (season_buli_df['Venue'] == 'Away')][general_stats_vars[i]].values[0]
                if general_stats_names[i] == "Possession" or general_stats_names[i] == "Aerial Duels %":
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}", unsafe_allow_html=True)

    # ##### Offensive Statistics
    if stats_options == 'Offensive':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Offensive Stats</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            for i in range(len(offensive_stats_names)):
                st.markdown(offensive_emoji[i])

        with stat_name_col:
            for i in range(len(offensive_stats_names)):
                st.markdown(offensive_stats_names[i])

        with home_stat_col:
            for i in range(len(offensive_stats_names)):
                home_stat = \
                    season_buli_df[
                        (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                        (season_buli_df['Venue'] == 'Home')][offensive_stats_var[i]].values[0]
                if offensive_stats_names[i] == "Accuracy %" or offensive_stats_names[i] == "Dribbles %":
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}", unsafe_allow_html=True)

        with away_stat_col:
            for i in range(len(offensive_stats_names)):
                away_stat = \
                    season_buli_df[
                        (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                        (season_buli_df['Venue'] == 'Away')][offensive_stats_var[i]].values[0]
                if offensive_stats_names[i] == "Accuracy %" or offensive_stats_names[i] == "Dribbles %":
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}", unsafe_allow_html=True)

    # ##### Defensive Statistics
    if stats_options == 'Defensive':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Defensive Stats</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            for i in range(len(defensive_stats_names)):
                st.markdown(defensive_emoji[i])

        with stat_name_col:
            for i in range(len(defensive_stats_names)):
                st.markdown(defensive_stats_names[i])

        with home_stat_col:
            for i in range(len(defensive_stats_names)):
                home_stat = \
                    season_buli_df[
                        (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                        (season_buli_df['Venue'] == 'Home')][defensive_stats_var[i]].values[0]
                if defensive_stats_names[i] == "Tackles Won %" or defensive_stats_names[i] == "Pressure Won %":
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}", unsafe_allow_html=True)

        with away_stat_col:
            for i in range(len(defensive_stats_names)):
                away_stat = \
                    season_buli_df[
                        (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                        (season_buli_df['Venue'] == 'Away')][defensive_stats_var[i]].values[0]
                if defensive_stats_names[i] == "Tackles Won %" or defensive_stats_names[i] == "Pressure Won %":
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}", unsafe_allow_html=True)

    # ##### Passing Statistics
    if stats_options == 'Passing':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Passing Stats</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            for i in range(len(passing_stats_names)):
                st.markdown(passing_emoji[i])

        with stat_name_col:
            for i in range(len(passing_stats_names)):
                st.markdown(passing_stats_names[i])

        with home_stat_col:
            for i in range(len(passing_stats_names)):
                home_stat = \
                    season_buli_df[
                        (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                        (season_buli_df['Venue'] == 'Home')][passing_stats_var[i]].values[0]
                if passing_stats_names[i] == "Pass %" or passing_stats_names[i] == "Pass Short %" or \
                        passing_stats_names[i] == "Pass Medium %" or passing_stats_names[i] == "Pass Long %":
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}", unsafe_allow_html=True)

        with away_stat_col:
            for i in range(len(passing_stats_names)):
                away_stat = \
                    season_buli_df[
                        (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                        (season_buli_df['Venue'] == 'Away')][passing_stats_var[i]].values[0]
                if passing_stats_names[i] == "Pass %" or passing_stats_names[i] == "Pass Short %" or \
                        passing_stats_names[i] == "Pass Medium %" or passing_stats_names[i] == "Pass Long %":
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}", unsafe_allow_html=True)

    # ##### Goalkeeper Statistics
    if stats_options == 'Goalkeeper':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Goalkeeper Stats</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            for i in range(len(gk_stats_names)):
                st.markdown(gk_emoji[i])

        with stat_name_col:
            for i in range(len(gk_stats_names)):
                st.markdown(gk_stats_names[i])

        with home_stat_col:
            for i in range(len(gk_stats_names)):
                home_stat = \
                    season_buli_df[
                        (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                        (season_buli_df['Venue'] == 'Home')][gk_stats_var[i]].values[0]
                if gk_stats_names[i] == "Saves %" or gk_stats_names[i] == "Passes %" or \
                        gk_stats_names[i] == "Goal Kicks %":
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{home_stat}", unsafe_allow_html=True)

        with away_stat_col:
            for i in range(len(gk_stats_names)):
                away_stat = \
                    season_buli_df[
                        (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                        (season_buli_df['Venue'] == 'Away')][gk_stats_var[i]].values[0]
                if gk_stats_names[i] == "Saves %" or gk_stats_names[i] == "Passes %" or \
                        gk_stats_names[i] == "Goal Kicks %":
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}%", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='text-align: center;'p>{away_stat}", unsafe_allow_html=True)

    if stats_options == 'Shot Events':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Shot Events</h5>", unsafe_allow_html=True)
            match_day = \
                season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                               (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)

        shot_events_df = shot_events_data_day(season=buli_season,
                                              match_day=match_day)

        # ##### Plot Data
        legend_col, pitch_col = st.columns([3, 11])
        day_event_type = day_shot_event_type(data=shot_events_df,
                                             home_team=home_team,
                                             away_team=away_team)

        with legend_col:
            st.markdown("<h4><b>Legend: </b></h4>", unsafe_allow_html=True)
            st.markdown("Size reflects <b>xGoal</b>", unsafe_allow_html=True)

            shot_events_type = []
            if 'Goal' in day_event_type:
                goals_see = st.checkbox("⭐ Goals", True)
                if goals_see:
                    shot_events_type.append("Goal")
            if 'OwnGoal' in day_event_type:
                own_goals_see = st.checkbox("➕ Own Goals", False)
                if own_goals_see:
                    shot_events_type.append("OwnGoal")
            if 'SavedShot' in day_event_type:
                saved_shots_see = st.checkbox("🔴 Saved Shots", False)
                if saved_shots_see:
                    shot_events_type.append("SavedShot")
            if 'MissedShots' in day_event_type:
                missed_shots_see = st.checkbox("🔺 Missed Shots", False)
                if missed_shots_see:
                    shot_events_type.append("MissedShots")
            if 'BlockedShot' in day_event_type:
                blocked_shots_see = st.checkbox("🔻 Blocked Shots", False)
                if blocked_shots_see:
                    shot_events_type.append("BlockedShot")
            if 'ShotOnPost' in day_event_type:
                shot_post_see = st.checkbox("🟥 Shot on Post", False)
                if shot_post_see:
                    shot_events_type.append("ShotOnPost")

        if len(shot_events_type) > 0:
            shot_event_fig = shot_events_day_plot(data=shot_events_df,
                                                  home_team=home_team,
                                                  away_team=away_team,
                                                  event_type=shot_events_type)
            with pitch_col:
                st.pyplot(fig=shot_event_fig.figure)

    # ##### Stadium Info
    _, stadium_logo, _ = st.columns([2, 1, 1])
    with stadium_logo:
        if (home_team == "Sport-Club Freiburg") and (buli_season == '2021-2022') and (match_day > 6):
            stadium_name = stadiums[home_team][1]
        elif (home_team == "Sport-Club Freiburg") and (buli_season == '2021-2022') and (match_day <= 6):
            stadium_name = stadiums[home_team][0]
        elif (home_team == "Sport-Club Freiburg") and (buli_season != '2021-2022'):
            stadium_name = stadiums[home_team][0]
        else:
            stadium_name = stadiums[home_team]
        st.markdown(f"🏟️ {stadium_name}")
