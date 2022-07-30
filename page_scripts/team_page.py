from page_scripts.stats_scripts.team_stats import *
from PIL import Image


def team_page(page_season, favourite_team):
    # #### Team Statistics Type
    team_stats = st.sidebar.selectbox("Season Stats", ["Season Stats", "Season by Season Stats"])

    if team_stats == "Season Stats":
        # ##### Select Season
        buli_season_df = season_data_process(season=page_season, stat_type=team_stats)

        # ##### Season Filter
        filter_type = ["Total", "Home", "Away", "1st Period", "2nd Period"]
        match_day = np.max(buli_season_df['Week_No'].values)
        if match_day <= 17:
            filter_type.remove("2nd Period")

        st.subheader(f"Analysis by Team: Season {page_season}")
        menu_filter_col, chart_team_col = st.columns([2, 5])
        with menu_filter_col:
            season_type_team = st.selectbox("Team Season Filter", filter_type)
            stat_name_team = st.selectbox("Team Season Statistics", team_stats_names)
            team_type = st.selectbox("Team Type", ['Team', 'Opponent'])
            fig_team, avg_value, better_avg = teams_season_stats(data=buli_season_df,
                                                                 stat_name=stat_name_team,
                                                                 stat_filter=season_type_team,
                                                                 team_type=team_type)
            if team_type == 'Team':
                st.markdown(
                    f"The top <b><font color = #d20614>{better_avg}</font></b> teams had and average value better then "
                    f"the league average value of <b><font color = #d20614>{avg_value}</font></b> "
                    f"<b><font color = green>{stat_name_team}</font></b> per game for "
                    f"<b><font color = #d20614>{season_type_team}</font></b> Season Games.", unsafe_allow_html=True)
            elif team_type == 'Opponent':
                st.markdown(
                    f"The top <b><font color = #d20614>{better_avg}</font></b> teams by opponent had and average value "
                    f"better then the league average value of <b><font color = #d20614>{avg_value}</font></b> "
                    f"<b><font color = green>{stat_name_team}</font></b> per game for "
                    f"<b><font color = #d20614>{season_type_team}</font></b> Season Games.", unsafe_allow_html=True)

        with chart_team_col:
            config = {'displayModeBar': False}
            st.plotly_chart(fig_team, config=config, use_container_width=True)

        st.subheader(f"Team Stats vs Opponent by Match Day: Season {page_season}")
        team_col, team_logo_col, type_col_day, _, stat_col_day = st.columns([4, 1, 2, 0.25, 2])
        with team_col:
            # ##### Teams Filter
            teams = list(buli_season_df['Team'].unique())
            teams.sort()
            pos_team = teams.index(favourite_team)
            team_chart = st.selectbox("Select Team", teams, pos_team)

        with team_logo_col:
            team_logo = Image.open(f'images/{team_chart}.png')
            st.image(team_logo, use_column_width=True)

        with type_col_day:
            season_type_day = st.selectbox("Game Filter", filter_type)

        with stat_col_day:
            # ##### Data Charts
            stat_name_day = st.selectbox("Game Statistics", team_stats_names)
            fig_day, avg_team, avg_opp, better, stat_sig_name = teams_charts_day(data=buli_season_df,
                                                                                 team=team_chart,
                                                                                 stat_name=stat_name_day,
                                                                                 stat_filter=season_type_day)
        if stat_sig_name == "":
            st.markdown(
                f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{season_type_day}"
                f"</font></b> Season games {team_chart} had more <b><font color = green>{stat_name_day}</font></b> "
                f"then her opponent. {team_chart} had an average of <b><font color = #d20614>{avg_team}</font></b> "
                f"<b><font color = green>{stat_name_day}</font></b> per game while her opponents had an average of "
                f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = green>{stat_name_day}</font></b> per "
                f"game.", unsafe_allow_html=True)
        else:
            st.markdown(
                f"In <b><font color = #d20614>{better}%</font></b> of the <b><font color = #d20614>{season_type_day}"
                f"</font></b> Season games {team_chart} had more <b><font color = green>{stat_name_day}</font></b> then"
                f" her opponent. {team_chart} had an average of <b><font color = #d20614>{avg_team}</font></b> <b>"
                f"<font color = green>{stat_name_day}</font></b> per game while her opponents had an average of "
                f"<b><font color = #d20614>{avg_opp}</font></b> <b><font color = green>{stat_name_day}</font></b> per "
                f"game, which is <b><font color = #d20614>{stat_sig_name}</font></b>.", unsafe_allow_html=True)

        config = {'displayModeBar': False}
        st.plotly_chart(fig_day, config=config, use_container_width=True)

        st.subheader(f"Team Stats vs Opponent by Season Type: Season {page_season}")
        filter_image_col, type_team_col = st.columns([3, 9])
        with filter_image_col:
            st.image(team_logo, width=100)

            fig_type_team, team_data_name, team_value_1, team_value_2, team_part_name, \
            team_value_3, team_value_4 = teams_season_type(data=buli_season_df,
                                                           team=team_chart,
                                                           stat_name=stat_name_day)
            st.markdown(
                f"<b><font color = #d20614>{team_chart}</font></b> performs much better at <b><font color = #d20614>"
                f"{team_data_name[0]}</font></b> Games with <b><font color = #d20614>{team_value_1}</font></b> <b>"
                f"<font color = green>{stat_name_day}</font></b> per Game on average in comparison to <b><font color = "
                f"#d20614>{team_data_name[1]}</font></b> Games where they had  <b><font color = #d20614>{team_value_2}"
                f"</font></b> <b><font color = green>{stat_name_day}</font></b> per Game on average.",
                unsafe_allow_html=True)

            if team_part_name != "":
                st.markdown(
                    f"It also performs much better in the <b><font color = #d20614>{team_part_name[0]}</font></b> "
                    f"Season Games with <b><font color = #d20614>{team_value_3}</font></b> <b><font color = green>"
                    f"{stat_name_day}</font></b> per Game on average in comparison to the <b><font color = #d20614>"
                    f"{team_part_name[1]}</font></b> Season Games where they had  <b><font color = #d20614>"
                    f"{team_value_4}</font></b> <b><font color = green>{stat_name_day}</font></b> per Game on average.",
                    unsafe_allow_html=True)

        with type_team_col:
            config = {'displayModeBar': False}
            st.plotly_chart(fig_type_team, config=config, use_container_width=True)

        st.subheader(f"Team Stats Relationship: Season {page_season}")
        corr_filter_col, corr_team_col, corr_team_image = st.columns([2, 6, 1])
        with corr_filter_col:
            corr_filter_type = st.selectbox("Relationship Season Selection", filter_type)
            stats_names_1 = team_stats_names.copy()
            corr_stat_x = st.selectbox("Select X Stat", stats_names_1)
            stats_names_2 = stats_names_1.copy()
            stats_names_2.remove(corr_stat_x)
            corr_stat_y = st.selectbox("Select Y Stat", stats_names_2)
            stats_names_3 = stats_names_1.copy()
            corr_stat_size = st.selectbox("Select Size Stat", stats_names_3)

        with corr_team_image:
            regression_line = st.checkbox("OLS Line")
            st.markdown("Select to Plot the <b><font color = #d20614>OLS Regression Line</font></b>",
                        unsafe_allow_html=True)

        # ##### Relationship Plot
        with corr_team_col:
            final_team = ["All Teams"]
            final_team.extend(teams)
            corr_name_team = st.selectbox("Relationship Team Selection", final_team)
            relationship_fig, corr_value, corr_name, overall_corr_strength, overall_corr_sign, result_corr_strength, \
            result_corr_sign, max_result = relationship_data(data=buli_season_df,
                                                             team=corr_name_team,
                                                             filter_type=corr_filter_type,
                                                             stat_x=corr_stat_x,
                                                             stat_y=corr_stat_y,
                                                             stat_size=corr_stat_size,
                                                             ols_line=regression_line)

            config = {'displayModeBar': False}
            st.plotly_chart(relationship_fig, config=config, use_container_width=True)

        with corr_team_image:
            if corr_name_team != "All Teams":
                corr_logo = Image.open(f'images/{corr_name_team}.png')
                st.image(corr_logo, width=100)

        with corr_filter_col:
            st.markdown(f"For <b><font color = #d20614>{corr_filter_type}</font></b> Season Games there is a "
                        f"<b><font color = #d20614>{overall_corr_sign}</font></b> <b><font color = green>"
                        f"{overall_corr_strength}</font></b> Correlation between <b><font color = #d20614>{corr_stat_x}"
                        f"</font></b> and <b><font color = #d20614>{corr_stat_y}</font></b> (<b><font color = purple>"
                        f"{corr_value[0]}</font></b>) if we look at <b><font color = #d20614>{corr_name_team}</font>"
                        f"</b> Games. By result the Best Correlation is a <b><font color = #d20614>{result_corr_sign}"
                        f"</font></b> <b><font color = green>{result_corr_strength}</font></b> Correlation for "
                        f"<b><font color = #d20614>{corr_name[max_result]}</font></b> Games (<b><font color = purple>"
                        f"{corr_value[max_result]}</font></b>).", unsafe_allow_html=True)
    elif team_stats == "Season by Season Stats":

        buli_df = season_data_process(season="", stat_type=1)
        seasons = list(buli_df['Season'].unique())[-5:]
        current_season = page_season
        buli_teams = season_teams(buli_df, page_season)
        pos_team = buli_teams.index(favourite_team)
        st.subheader(f"Team Stats vs Opponent over the Last 5 Seasons")

        filter_col, team_chart_col, team_logo_col = st.columns([3, 9, 1])
        with filter_col:
            filter_type = ["Total", "Home", "Away", "1st Period", "2nd Period"]
            season_type_team = st.selectbox("Season Filter", filter_type)
            stat_name_team = st.selectbox("Select Season Statistics", team_stats_names)
            buli_team = st.selectbox("Select Team", buli_teams, pos_team)

        with team_logo_col:
            team_logo = Image.open(f'images/{buli_team}.png')
            st.image(team_logo, use_column_width=True)

        with team_chart_col:
            fig_seasons_team, rank_season, better_seasons, no_seasons = teams_buli_type(data=buli_df,
                                                                                        analysis_seasons=seasons,
                                                                                        filter_type=season_type_team,
                                                                                        team=buli_team,
                                                                                        stat_name=stat_name_team)

        with team_chart_col:
            config = {'displayModeBar': False}
            st.plotly_chart(fig_seasons_team, config=config, use_container_width=True)

        with filter_col:
            if rank_season == 1:
                rank_name = 'st'
            elif rank_season == 2:
                rank_name = 'nd'
            elif rank_season == 3:
                rank_name = 'rd'
            else:
                rank_name = 'th'

            if no_seasons > 1:
                st.markdown(
                    f"<b><font color = #d20614>{buli_team}</font></b> has the <b><font color = black>{rank_season}"
                    f"</font></b><b><font color = black>{rank_name}</font></b> highest Average "
                    f"<b><font color = #d20614>{stat_name_team}</font></b> per Game for the <b><font color = black>"
                    f"{season_type_team}</font></b> Season <b><font color = #d20614>{current_season}</font></b>, "
                    f"if we look at the last <b><font color = black>{no_seasons}</font></b>"
                    f" Seasons. In <b><font color = #d20614>{better_seasons}</font></b> of the last <b>"
                    f"<font color = black>{no_seasons}</font></b> Seasons, <b><font color = #d20614>{buli_team}"
                    f"</font></b> has more <b><font color = black>{stat_name_team}</font></b> on Average per "
                    f"Game then her opponents for <b><font color = #d20614>{season_type_team}</font></b> Season "
                    f"Games.", unsafe_allow_html=True)
            elif no_seasons == 1:
                st.markdown(f"<b><font color = #d20614>{rank_season}</font></b>", unsafe_allow_html=True)
            else:
                st.markdown(f"No Data for Season <b><font color = #d20614>{current_season}</font></b>.",
                            unsafe_allow_html=True)

        st.subheader(f"Team Stats Relationship over the Last 5 Seasons")

        corr_filter_col, corr_team_col, corr_team_image = st.columns([2.5, 6, 1])
        with corr_filter_col:
            corr_filter_type = st.selectbox("Relationship Filter Selection", filter_type)
            stats_names_x = team_stats_names.copy()
            corr_stat_x = st.selectbox("Select X Stat", stats_names_x)
            stats_names_y = stats_names_x.copy()
            stats_names_y.remove(corr_stat_x)
            corr_stat_y = st.selectbox("Select Y Stat", stats_names_y)

        with corr_team_image:
            regression_line = st.checkbox("OLS Line")
            st.markdown("Select to Plot the <b><font color = #d20614>OLS Regression Line</font></b>",
                        unsafe_allow_html=True)
            team_logo = Image.open(f'images/{buli_team}.png')
            st.image(team_logo, use_column_width=True)

        with corr_team_col:

            relationship_fig, overall_corr_value, overall_corr_strength, overall_corr_sign, \
            season_name_best_corr, season_value_best_corr, season_corr_strength, season_corr_sign = \
                relationship_buli_data(data=buli_df,
                                       analysis_seasons=seasons,
                                       team=buli_team,
                                       filter_type=corr_filter_type,
                                       stat_x=corr_stat_x,
                                       stat_y=corr_stat_y,
                                       ols_line=regression_line)

            config = {'displayModeBar': False}
            st.plotly_chart(relationship_fig, config=config, use_container_width=True)
            st.markdown(
                "<b><font color = #d20614>Size</font></b>: Points 1: <b><font color = #d20614>Defeat</font></b>, "
                "Points 2: <b><font color = #d20614>Draw</font></b>, Points 3: <b><font color = #d20614>Win</font></b>",
                unsafe_allow_html=True)

        with corr_filter_col:
            if no_seasons == 1:
                no_season_name = "Season"
            else:
                no_season_name = f"{no_seasons} Seasons"
            st.markdown(f"For <b><font color = #d20614>{corr_filter_type}</font></b> Season Games there is a "
                        f"<b><font color = #d20614>{overall_corr_sign}</font></b> <b><font color = green>"
                        f"{overall_corr_strength}</font></b> Correlation between <b><font color = #d20614>{corr_stat_x}"
                        f"</font></b> and <b><font color = #d20614>{corr_stat_y}</font></b> (<b><font color = purple>"
                        f"{overall_corr_value}</font></b>) if we look at the last {no_season_name} of "
                        f"<b><font color = #d20614>{buli_team}</font></b> in the Bundesliga.", unsafe_allow_html=True)
            if no_seasons > 1:
                st.markdown(f"If we look at Season data, Season <b><font color = #d20614>{season_name_best_corr}"
                            f"</font></b> has the strongest correlation between <b><font color = #d20614>{corr_stat_x} "
                            f"</font></b> and <b><font color = #d20614>{corr_stat_y}</font></b> (<b>"
                            f"<font color = purple>{season_value_best_corr}</font></b>) a <b><font color = #d20614>"
                            f"{season_corr_sign}</font></b><b><font color = green> {season_corr_strength}</font></b> "
                            f"Relationship.", unsafe_allow_html=True)
