from page_scripts.stats_scripts.player_stats import *
from PIL import Image
import streamlit as st


def player_page(all_seasons, page_season, favourite_team):
    # #### Player Statistics Type
    player_stats = st.sidebar.selectbox("Season Stats", ["Season Stats", "Season by Season Stats"])

    if player_stats == "Season Stats":
        # ##### Select Season
        buli_player_season_df, final_total_players, final_avg_players = season_player_data(season=page_season)
        teams_players = list(buli_player_season_df[buli_player_season_df['Venue'] == 'Home']['Team'].unique())
        teams_players.sort()
        pos_team_players = teams_players.index(favourite_team)

        # ##### Season Filter
        filter_type_player = ["Total", "Home", "Away", "1st Period", "2nd Period"]
        match_day_player = np.max(buli_player_season_df['Week_No'].values)
        if match_day_player <= 17:
            filter_type_player.remove("2nd Period")

        # ##### Player Top 10 Statistics
        st.subheader(f"Top 10 Players Statistics: Season {page_season}")
        top10_menu_col, top10_plot_col = st.columns([3, 8])
        with top10_menu_col:
            top10_stat_type = st.selectbox("Type Statistics", ["Total", "Average"])
            top10_player_filter = st.selectbox("Season Type", filter_type_player)
            if top10_stat_type == "Total":
                top10_player_stats = player_stats_names_total
            else:
                top10_player_stats = player_stats_names_avg
            top10_player_stat = st.selectbox("Name Statistics", top10_player_stats)

        with top10_plot_col:
            top10_player_fig, teams_top10, max_no_players, no_teams_top10 = player_top_statistics(
                data=buli_player_season_df,
                season_filter=top10_player_filter,
                avg_players=final_avg_players,
                stat_top10=top10_player_stat,
                type_top10=top10_stat_type)

            config = {'displayModeBar': False}
            st.plotly_chart(top10_player_fig, config=config, use_container_width=True)

        if top10_stat_type == "Average":
            top10_player_stat = top10_player_stat + " per Game"
        with top10_menu_col:
            if teams_top10 == "":
                st.markdown(
                    f"No team has more then 1 player in the Top 10 <b><font color = green>{top10_stat_type}</font>"
                    f"</b> <b><font color = #d20614>{top10_player_stat}</font></b> for <b><font color = #d20614>"
                    f"{top10_player_filter}</font></b> Season Games.", unsafe_allow_html=True)
            else:
                if no_teams_top10 == 1:
                    st.markdown(
                        f"<b><font color = green>{teams_top10}</font></b>has <b><font color = #d20614>{max_no_players}"
                        f"</font></b> players in the Top 10 <b><font color = green>{top10_stat_type}</font></b> "
                        f"<b><font color = #d20614>{top10_player_stat}</font></b> for <b><font color = #d20614>"
                        f"{top10_player_filter}</font></b> Season Games.", unsafe_allow_html=True)
                else:
                    st.markdown(
                        f"<b><font color = green>{teams_top10}</font></b>have <b><font color = #d20614>{max_no_players}"
                        f"</font></b> players in the Top 10 <b><font color = green>{top10_stat_type}</font></b> "
                        f"<b><font color = #d20614>{top10_player_stat}</font></b> for <b><font color = #d20614>"
                        f"{top10_player_filter}</font></b> Season Games.", unsafe_allow_html=True)

            if top10_stat_type == "Average":
                st.markdown("<b><font color = #d20614>Note</font></b>: Only Players with at least <b>"
                            "<font color = #d20614>10%</font></b> of minutes played were included.",
                            unsafe_allow_html=True)

        # ##### Player Season Statistics
        st.subheader(f"Players Season Statistics: Season {page_season}")
        player_menu_col, player_plot_col, player_stat_col = st.columns([3, 8, 3])
        with player_menu_col:
            season_player_filter = st.selectbox("Select Season Type", filter_type_player)
            season_player_team = st.selectbox("Select Team", teams_players, pos_team_players)
            team_player_logo = Image.open(f'images/{season_player_team}.png')
            st.image(team_player_logo, width=100)

        with player_stat_col:
            player_stat_type = st.selectbox("Statistics Type", ["Total", "Average"])
            if player_stat_type == "Total":
                player_stat = st.selectbox("Select Statistics", player_stats_names_total)
            elif player_stat_type == "Average":
                player_stat = st.selectbox("Select Statistics", player_stats_names_avg)

        buli_player_filter_df = player_df_filter(data=buli_player_season_df,
                                                 season_filter=season_player_filter)

        with player_plot_col:
            team_player_fig, league_avg, league_better = player_df_stat_season(data=buli_player_filter_df,
                                                                               team=season_player_team,
                                                                               total_players=final_total_players,
                                                                               avg_players=final_avg_players,
                                                                               stat_name=player_stat,
                                                                               stat_type=player_stat_type,
                                                                               season_filter=season_player_filter)

            config = {'displayModeBar': False}
            st.plotly_chart(team_player_fig, config=config, use_container_width=True)

        with player_menu_col:
            if player_stat_type == "Average":
                st.markdown("<b><font color = #d20614>Note</font></b>: Only Players with at least <b>"
                            "<font color = #d20614>10%</font></b> of minutes played were included.",
                            unsafe_allow_html=True)

        with player_stat_col:
            if league_better > 0:
                if player_stat_type == 'Total':
                    st.markdown(
                        f"The Top <b><font color = #d20614>{league_better}</font></b> Players of <b><"
                        f"font color = #d20614>{season_player_team}</font></b> had more <b><font color = green>"
                        f"{player_stat}</font></b> than the league average of (<b><font color = Silver>{league_avg}"
                        f"</font></b>) <b><font color = green>{player_stat}</font></b> for <b><font color = #d20614>"
                        f"{season_player_filter}</font></b> Season Games.", unsafe_allow_html=True)
                elif player_stat_type == 'Average':
                    st.markdown(
                        f"The Top <b><font color = #d20614>{league_better}</font></b> Players of <b>"
                        f"<font color = #d20614>{season_player_team}</font></b> had more <b><font color = green>"
                        f"{player_stat}</font></b> per Game than the league average of (<b><font color = Silver>"
                        f"{league_avg}</font></b>) <b><font color = green>{player_stat}</font></b> per Game for <b>"
                        f"<font color = #d20614>{season_player_filter}</font></b> Season Games.",
                        unsafe_allow_html=True)
            else:
                if player_stat_type == 'Total':
                    st.markdown(f"<b><font color = #d20614>None</font></b> of the <b><font color = #d20614>"
                                f"{season_player_team}</font></b>  Players had more <b><font color = green>"
                                f"{player_stat}</font></b> per Game than the league average of (<b>"
                                f"<font color = Silver>{league_avg}</font></b>) <b><font color = green>{player_stat}"
                                f"</font></b> per Game for <b><font color = #d20614>{season_player_filter}</font></b> "
                                f"Season Games.", unsafe_allow_html=True)
                elif player_stat_type == 'Average':
                    st.markdown(
                        f"<b><font color = #d20614>None</font></b> of the <b><font color = #d20614>{season_player_team}"
                        f"</font></b> had more <b><font color = green>{player_stat}</font></b> "
                        f"per Game than the league average of (<b><font color = Silver>{league_avg}</font></b>) "
                        f"<b><font color = green>{player_stat}</font></b> per Game for <b><font color = #d20614>"
                        f"{season_player_filter}</font></b> Season Games.", unsafe_allow_html=True)

        # ##### Player Match Day Statistics
        st.subheader(f"Players Match Day Statistics: Season {page_season}")
        player_day_col, player_day_chart_col, player_day_logo_col = st.columns([3, 8, 1])
        with player_day_col:
            stat_player_day = st.selectbox("Player Statistics", player_stats_names_avg)
            team_season_player_df, team_players = player_match_day_team(data=buli_player_season_df,
                                                                        team=season_player_team,
                                                                        players=final_avg_players)
            player_name_day = st.selectbox("Select Match Day Player", team_players)

        with player_day_chart_col:
            fig_player_day, fig_max_value, team_max_day, team_avg_day = player_chart_day(data=team_season_player_df,
                                                                                         player_name=player_name_day,
                                                                                         stat_name=stat_player_day)
            if fig_max_value == 0:
                st.subheader("No data")

            else:
                config = {'displayModeBar': False}
                st.plotly_chart(fig_player_day, config=config, use_container_width=True)

        with player_day_logo_col:
            st.image(team_player_logo, use_column_width=True)

        with player_day_col:
            if fig_max_value == 0:
                pass
            else:
                st.markdown(
                    f"<b><font color = #d20614>{player_name_day}</font></b> had the most <b><font color = green>"
                    f"{stat_player_day}</font></b> for <b><font color = #d20614>{season_player_team}</font></b> in "
                    f"<b><font color = #d20614>{team_max_day}</font></b> Games and had more <b><font color = green>"
                    f"{stat_player_day}</font></b> then the team average in <b><font color = #d20614>{team_avg_day}"
                    f"</font></b> Games.", unsafe_allow_html=True)

            st.markdown(
                "<b><font color = #d20614>Note</font></b>: Only Players with at least <b><font color = #d20614>10%"
                "</font></b> of minutes played were included.", unsafe_allow_html=True)

        # ##### Player vs Player Position Statistics
        st.subheader(f"Player Season vs Player Position Stats: Season {page_season}")
        player_team_image_col, player_team_name_col, type_player_chart_col = st.columns([1, 3, 9])
        with player_team_image_col:
            st.image(team_player_logo, use_column_width=True)

        with player_team_name_col:
            st.markdown("")
            st.markdown(f"<h4><b>{player_name_day}</b></h4>", unsafe_allow_html=True)
            vs_player_type = st.selectbox("vs Player Type", ["Defenders", "Midfielders", "Forwards"])

        with type_player_chart_col:
            fig_player_type, player_team_comparison, player_league_comparison, player_home_away = \
                player_season_filter_stats(data=buli_player_season_df,
                                           team=season_player_team,
                                           player=player_name_day,
                                           avg_players=final_avg_players,
                                           stat_name=stat_player_day,
                                           vs_player_type=vs_player_type)

            if fig_max_value == 0:
                st.subheader("No data")
            else:
                config = {'displayModeBar': False}
                st.plotly_chart(fig_player_type, config=config, use_container_width=True)

        with player_team_name_col:
            if fig_max_value == 0:
                pass
            else:
                st.markdown(f"<b><font color = #d20614>{player_name_day}</font></b> has <b><font color = green>"
                            f"{player_team_comparison}</font></b> <b><font color = green>{stat_player_day}</font></b> "
                            f"per Game on Average than <b><font color = #d20614>{season_player_team}</font></b>'s teams"
                            f" Average and <b><font color = green>{player_league_comparison}</font></b> <b>"
                            f"<font color = green>{stat_player_day}</font></b> per Game than the Leagues <b>"
                            f"<font color = #d20614>{vs_player_type}</font></b> Average.", unsafe_allow_html=True)
                if player_home_away != "":
                    st.markdown(
                        f"<b><font color = #d20614>{player_name_day}</font></b> has more <b><font color = green>"
                        f"{stat_player_day}</font></b> per Game on Average for <b><font color = #d20614>"
                        f"{player_home_away}</font></b> Season Games.", unsafe_allow_html=True)

            st.markdown(
                "<b><font color = #d20614>Note</font></b>: Only Players with at least <b><font color = #d20614>10%"
                "</font></b> of minutes played were included.", unsafe_allow_html=True)

        # ##### Player Stats Relationship Statistics
        st.subheader(f"Player Stats Relationship: Season {page_season}")
        player_rel_filter_col, player_rel_chart_col = st.columns([3, 8])
        with player_rel_filter_col:
            player_corr_filter_type = st.selectbox("Player Relationship Season Type", filter_type_player)
            team_corr_name = st.selectbox("Highlight Team", teams_players, pos_team_players)
            _, players_corr = player_corr_filter_team(data=buli_player_season_df,
                                                      season_filter=player_corr_filter_type,
                                                      team=team_corr_name,
                                                      players=final_avg_players)
            player_corr_name = st.selectbox("Highlight Player", players_corr)
            player_stats_names_1 = player_stats_names_avg.copy()
            player_stat_x = st.selectbox("Select X Stat", player_stats_names_1)
            player_stats_names_2 = player_stats_names_1.copy()
            player_stats_names_2.remove(player_stat_x)
            player_stat_y = st.selectbox("Select Y Stat", player_stats_names_2)

        player_league_fig, player_team_fig, player_corr_value, \
        player_corr_strength, player_corr_sign = player_relationship_data(
            data=buli_player_season_df,
            filter_type=player_corr_filter_type,
            team=team_corr_name,
            player=player_corr_name,
            avg_players=final_avg_players,
            stat_x=player_stat_x,
            stat_y=player_stat_y)

        config = {'displayModeBar': False}
        with player_rel_chart_col:
            st.plotly_chart(player_league_fig, config=config, use_container_width=True)
            st.plotly_chart(player_team_fig, config=config, use_container_width=True)

        with player_rel_filter_col:
            team_corr_logo = Image.open(f'images/{team_corr_name}.png')
            st.image(team_corr_logo, width=100)

            if player_corr_value != "":
                st.markdown(f"For <b><font color = #d20614>{player_corr_filter_type}</font></b> Season Games, <b>"
                            f"<font color = #d20614>{player_corr_name}</font></b> has a <b><font color = green>"
                            f"{player_corr_sign}</font></b> <b><font color = #d20614>{player_corr_strength}</font></b> "
                            f"Correlation (<b><font color = green>{player_corr_value}</font></b>) between "
                            f"<b><font color = green>{player_stat_x}</font></b> and <b><font color = #d20614>"
                            f"{player_stat_y}</font></b>.", unsafe_allow_html=True)

            st.markdown(
                "<b><font color = #d20614>Note</font></b>: Only Players with at least <b><font color = #d20614>10%"
                "</font></b> of minutes played were included.", unsafe_allow_html=True)

    elif player_stats == "Season by Season Stats":
        st.subheader(f"Player Stats over the Last 5 Seasons")
        player_filter_col, player_chart_col, player_stat_col = st.columns([3, 7, 3])
        with player_filter_col:
            seasons = all_seasons
            # ##### Select Season
            buli_player_season_df, season_teams = buli_player_data(season=page_season)
            pos_team_players = season_teams.index(favourite_team)

            # ##### Data Filter
            filter_type_player = ["Total", "Home", "Away", "1st Period", "2nd Period"]
            seasons_player_filter = st.selectbox("Select Season Type", filter_type_player)
            seasons_player_team = st.selectbox("Select Team", season_teams, pos_team_players)
            current_season = page_season
            final_avg_players = buli_players_avg(data=buli_player_season_df,
                                                 team=seasons_player_team,
                                                 season=current_season)
            seasons_player_name = st.selectbox("Player Name", final_avg_players)

            buli_player_logo = Image.open(f'images/{seasons_player_team}.png')
            st.image(buli_player_logo, width=100)

            st.markdown(
                "<b><font color = #d20614>Note</font></b>: Only Players with at least <b><font color = #d20614>10%"
                "</font></b> of minutes played were included.", unsafe_allow_html=True)

        with player_stat_col:
            stat_player_seasons = st.selectbox("Player Statistics", player_stats_names_avg)

        with player_chart_col:
            player_seasons_fig, player_rank_season, player_better_seasons, player_no_seasons = player_buli_stats(
                data=buli_player_season_df,
                season_filter=seasons_player_filter,
                team=seasons_player_team,
                player=seasons_player_name,
                avg_players=final_avg_players,
                stat_name=stat_player_seasons,
                analysis_seasons=seasons)
            config = {'displayModeBar': False}
            st.plotly_chart(player_seasons_fig, config=config, use_container_width=True)

        with player_stat_col:
            if player_rank_season == 1:
                player_rank_name = 'st'
            elif player_rank_season == 2:
                player_rank_name = 'nd'
            elif player_rank_season == 3:
                player_rank_name = 'rd'
            else:
                player_rank_name = 'th'

            if player_no_seasons > 1:
                st.markdown(f"<b><font color = black>{seasons_player_name}</font></b> has the <b><font color = black>"
                            f"{player_rank_season}</font></b><b><font color = black>{player_rank_name}</font></b> "
                            f"highest Average <b><font color = #d20614>{stat_player_seasons}</font></b> per Game for "
                            f"the <b><font color = black>{seasons_player_filter}</font></b> Season <b>"
                            f"<font color = #d20614>{current_season}</font></b>, if we look at the last <b>"
                            f"<font color = black>{player_no_seasons}</font></b> Seasons. In <b><font color = #d20614>"
                            f"{player_better_seasons}</font></b> of the last <b><font color = black>{player_no_seasons}"
                            f"</font></b> Seasons, <b><font color = #d20614>{seasons_player_name}</font></b> has more "
                            f"<b><font color = black>{stat_player_seasons}</font></b> on Average per Game then <b>"
                            f"<font color = black>{seasons_player_team}</font></b> Team Average for <b>"
                            f"<font color = #d20614>{seasons_player_filter}</font></b> Season Games.",
                            unsafe_allow_html=True)
            elif player_no_seasons == 1:
                st.markdown(f"<b><font color = #d20614>{player_rank_season}</font></b>", unsafe_allow_html=True)
            else:
                st.markdown(f"No Data for Season <b><font color = #d20614>{current_season}</font></b>.",
                            unsafe_allow_html=True)

        st.subheader(f"Player Stats Relationship over the Last 5 Seasons")
        player_rel_filter_col, player_rel_chart_col, player_markdown_col = st.columns([2.5, 6, 2])
        with player_rel_filter_col:
            player_corr_filter_type = st.selectbox("Player Relationship Season Type", filter_type_player)
            player_stats_names_1 = player_stats_names_avg.copy()
            player_stat_x = st.selectbox("Select X Stat", player_stats_names_1)
            player_stats_names_2 = player_stats_names_1.copy()
            player_stats_names_2.remove(player_stat_x)
            player_stat_y = st.selectbox("Select Y Stat", player_stats_names_2)
            st.markdown(
                "<b><font color = #d20614>Note</font></b>: Only Players with at least <b><font color = #d20614>10%"
                "</font></b> of minutes played were included.", unsafe_allow_html=True)

        with player_markdown_col:
            corr_player_logo = Image.open(f'images/{seasons_player_team}.png')
            st.image(corr_player_logo, width=100)

        with player_rel_chart_col:
            player_seasons_fig, pl_overall_corr_value, pl_overall_corr_strength, pl_overall_corr_sign, \
            pl_season_name_best_corr, pl_season_value_best_corr, pl_season_corr_strength, pl_season_corr_sign = \
                player_buli_corr_data(data=buli_player_season_df,
                                      filter_type=player_corr_filter_type,
                                      team=seasons_player_team,
                                      player=seasons_player_name,
                                      stat_x=player_stat_x,
                                      stat_y=player_stat_y,
                                      analysis_seasons=seasons)

            config = {'displayModeBar': False}
            st.plotly_chart(player_seasons_fig, config=config, use_container_width=True)
            st.markdown(
                "<b><font color = #d20614>Size</font></b>: Points 1: <b><font color = #d20614>Defeat</font></b>,"
                "Points 2: <b><font color = #d20614>Draw</font></b>, Points 3: <b><font color = #d20614>Win</font></b>",
                unsafe_allow_html=True)

        with player_markdown_col:
            st.markdown(f"<b>{seasons_player_name}</b>", unsafe_allow_html=True)

            if np.isnan(pl_overall_corr_value):
                st.markdown(
                    f"For <b><font color = #d20614>{player_corr_filter_type}</font></b> Season Games there is a "
                    f"<b><font color = #d20614>No</font></b> <b><font color = green> Correlation</font></b> between "
                    f"<b><font color = #d20614>{player_stat_x}</font></b> and <b><font color = #d20614>{player_stat_y}"
                    f"</font></b>.", unsafe_allow_html=True)
            else:
                if player_no_seasons == 1:
                    no_season_name = "Season"
                else:
                    no_season_name = f"{player_no_seasons} Seasons"
                st.markdown(f"For <b><font color = #d20614>{player_corr_filter_type}</font></b> Season Games there is a "
                            f"<b><font color = #d20614>{pl_overall_corr_sign}</font></b> <b><font color = green>"
                            f"{pl_overall_corr_strength}</font></b> Correlation between <b><font color = #d20614>"
                            f"{player_stat_x}</font></b> and <b><font color = #d20614>{player_stat_y}</font></b> "
                            f"(<b><font color = purple>{pl_overall_corr_value}</font></b>) if we look at the last "
                            f"{no_season_name} of <b><font color = #d20614>{seasons_player_name}</font></b> in the "
                            f"Bundesliga.", unsafe_allow_html=True)
                if player_no_seasons > 1:
                    st.markdown(f"If we look at Season data, Season <b><font color = #d20614>{pl_season_name_best_corr}"
                                f"</font></b> has the strongest correlation between <b><font color = #d20614>"
                                f"{player_stat_x} </font></b> and <b><font color = #d20614>{player_stat_y}</font></b> "
                                f"(<b><font color = purple>{pl_season_value_best_corr}</font></b>) a <b>"
                                f"<font color = #d20614>{pl_season_corr_sign}</font></b><b><font color = green> "
                                f"{pl_season_corr_strength}</font></b> Relationship.", unsafe_allow_html=True)
