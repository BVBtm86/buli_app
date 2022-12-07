import streamlit as st
from page_scripts.stats_scripts.day_stats import general_stats, general_emoji, offensive_stats, offensive_emoji, \
    defensive_stats, defensive_emoji, passing_stats, passing_emoji, gk_stats, gk_emoji, stadiums,  \
    match_day_process_data, match_day_stats
from PIL import Image


def match_day_page(page_season, favourite_team):
    # ##### Match Day Statistics
    team_filter = st.sidebar.selectbox("Team Filter", ['Home', 'Away'])
    st.header(f'Match Day Statistics: {page_season}')
    season_buli_df = match_day_process_data(page_season)
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

    stats_type = ["General", "Offensive", "Defensive", "Passing", "Goalkeeper"]
    stats_options = st.sidebar.selectbox("Statistics", stats_type)

    _, _, home_score, away_score = st.columns([0.2, 0.8, 2.25, 3])
    with home_score:
        home_goals = season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                         (season_buli_df['Venue'] == 'Home')]['Goals'].values[0] + season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                         (season_buli_df['Venue'] == 'Away')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{home_goals}</h1>", unsafe_allow_html=True)
    with away_score:
        away_goals = season_buli_df[
                         (season_buli_df['Opponent'] == home_team) & (season_buli_df['Team'] == away_team) &
                         (season_buli_df['Venue'] == 'Away')]['Goals'].values[0] + season_buli_df[
                         (season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                         (season_buli_df['Venue'] == 'Home')]['Own Goals'].values[0]
        st.markdown(f"<h1 style='text-align: center;'p>{away_goals}</h1>", unsafe_allow_html=True)

    # Select Match Day
    match_day = \
        season_buli_df[(season_buli_df['Team'] == home_team) & (season_buli_df['Opponent'] == away_team) &
                       (season_buli_df['Venue'] == 'Home')]['Week_No'].values[0]

    # ##### General Statistics
    if stats_options == 'General':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>General Stats</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.25, 0.75, 2.25, 3])
        with icon_col:
            [st.markdown(gen_emoji) for gen_emoji in general_emoji]

        with stat_name_col:
            [st.markdown(gen_stat_name) for gen_stat_name in general_stats]

        with home_stat_col:
            home_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=general_stats,
                                        venue="Home")

            [st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    general_stats[i] == "Possession" or general_stats[i] == "Duel Aerial Won %") else (
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}",
                         unsafe_allow_html=True) if (general_stats[i] == "Distance Covered (Km)") else
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]}",
                         unsafe_allow_html=True)) for i in range(len(home_stat))]

        with away_stat_col:
            away_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=general_stats,
                                        venue="Away")
            [st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    general_stats[i] == "Possession" or general_stats[i] == "Duel Aerial Won %") else (
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}",
                         unsafe_allow_html=True) if (general_stats[i] == "Distance Covered (Km)") else
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]}",
                         unsafe_allow_html=True)) for i in range(len(away_stat))]

    # ##### Offensive Statistics
    if stats_options == 'Offensive':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Offensive Stats</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            [st.markdown(off_emoji) for off_emoji in offensive_emoji]

        with stat_name_col:
            [st.markdown(off_stat_name) for off_stat_name in offensive_stats]

        with home_stat_col:
            home_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=offensive_stats,
                                        venue="Home")

            [st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    offensive_stats[i] == "Shot Accuracy %" or offensive_stats[i] == "Dribbles %") else (
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}",
                         unsafe_allow_html=True) if (offensive_stats[i] == "xGoal") else
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.0f}",
                         unsafe_allow_html=True)) for i in range(len(home_stat))]

        with away_stat_col:
            away_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=offensive_stats,
                                        venue="Away")
            [st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    offensive_stats[i] == "Shot Accuracy %" or offensive_stats[i] == "Dribbles %") else (
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}",
                         unsafe_allow_html=True) if (offensive_stats[i] == "xGoal") else
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.0f}",
                         unsafe_allow_html=True)) for i in range(len(away_stat))]

    # ##### Defensive Statistics
    if stats_options == 'Defensive':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Defensive Stats</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            [st.markdown(def_emoji) for def_emoji in defensive_emoji]

        with stat_name_col:
            [st.markdown(def_stat_name) for def_stat_name in defensive_stats]

        with home_stat_col:
            home_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=defensive_stats,
                                        venue="Home")
            [st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    defensive_stats[i] == "Tackles Won %")
             else st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.0f}",
                              unsafe_allow_html=True) for i in range(len(home_stat))]

        with away_stat_col:
            away_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=defensive_stats,
                                        venue="Away")
            [st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    defensive_stats[i] == "Tackles Won %")
             else st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.0f}",
                              unsafe_allow_html=True) for i in range(len(away_stat))]

    # ##### Passing Statistics
    if stats_options == 'Passing':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Passing Stats</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            [st.markdown(pass_emoji) for pass_emoji in passing_emoji]

        with stat_name_col:
            [st.markdown(pass_stat_name) for pass_stat_name in passing_stats]

        with home_stat_col:
            home_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=passing_stats,
                                        venue="Home")
            [st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    passing_stats[i] == "Pass %" or passing_stats[i] == "Pass Short %" or
                    passing_stats[i] == "Pass Medium %" or passing_stats[i] == "Pass Long %")
             else st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.0f}", unsafe_allow_html=True)
             for i in range(len(home_stat))]

        with away_stat_col:
            away_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=passing_stats,
                                        venue="Away")
            [st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    passing_stats[i] == "Pass %" or passing_stats[i] == "Pass Short %" or
                    passing_stats[i] == "Pass Medium %" or passing_stats[i] == "Pass Long %")
             else st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.0f}", unsafe_allow_html=True)
             for i in range(len(away_stat))]

    # ##### Goalkeeper Statistics
    if stats_options == 'Goalkeeper':
        with stat_name:
            st.markdown(" ")
            st.markdown("<h5 style='text-align: center;'p>Goalkeeper Stats</h5>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'p>Match Day: {match_day}</p>", unsafe_allow_html=True)
        icon_col, stat_name_col, home_stat_col, away_stat_col = st.columns([0.35, 0.65, 2.25, 3])
        with icon_col:
            [st.markdown(emoji) for emoji in gk_emoji]

        with stat_name_col:
            [st.markdown(gk_stat_name) for gk_stat_name in gk_stats]

        with home_stat_col:
            home_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=gk_stats,
                                        venue="Home")
            [st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    gk_stats[i] == "Saves %" or gk_stats[i] == "Crosses Stopped %") else (
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.1f}",
                         unsafe_allow_html=True) if (gk_stats[i] == "Post-Shot xGoal") else
             st.markdown(f"<p style='text-align: center;'p>{home_stat[i]:.0f}",
                         unsafe_allow_html=True)) for i in range(len(home_stat))]

        with away_stat_col:
            away_stat = match_day_stats(data=season_buli_df,
                                        home_team=home_team,
                                        away_team=away_team,
                                        stats=gk_stats,
                                        venue="Away")
            [st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}%", unsafe_allow_html=True) if (
                    gk_stats[i] == "Saves %" or gk_stats[i] == "Crosses Stopped %") else (
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.1f}",
                         unsafe_allow_html=True) if (gk_stats[i] == "Post-Shot xGoal") else
             st.markdown(f"<p style='text-align: center;'p>{away_stat[i]:.0f}",
                         unsafe_allow_html=True)) for i in range(len(away_stat))]

    # ##### Stadium Info
    _, stadium_logo, _ = st.columns([2, 1, 1])
    with stadium_logo:
        if (home_team == "Sport-Club Freiburg") and (page_season == '2022-2023'):
            stadium_name = stadiums[home_team][1]
        elif (home_team == "Sport-Club Freiburg") and (page_season == '2021-2022') and (match_day > 6):
            stadium_name = stadiums[home_team][1]
        elif (home_team == "Sport-Club Freiburg") and (page_season == '2021-2022') and (match_day <= 6):
            stadium_name = stadiums[home_team][0]
        elif (home_team == "Sport-Club Freiburg") and (page_season != '2021-2022'):
            stadium_name = stadiums[home_team][0]
        else:
            stadium_name = stadiums[home_team]
        st.markdown(f"🏟️ {stadium_name}")
