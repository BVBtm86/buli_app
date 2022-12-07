import numpy as np
import streamlit as st
from page_scripts.stats_scripts.gk_stats import gk_stats_total, gk_stats_avg, season_gk_data, gk_top_statistics, \
    gk_chart_day, gk_season_filter_stats, gk_relationship_data, buli_gk_data, gk_current_season_team, gk_buli_stats, \
    gk_buli_corr_data
from PIL import Image


def gk_page(all_seasons, page_season, favourite_team):
    # #### Player Statistics Type
    gk_stats = st.sidebar.selectbox("Season Stats", ["Season Stats", "Season by Season Stats"])

    if gk_stats == "Season Stats":
        # ##### Select Season
        buli_gk_season_df, final_total_gk, final_avg_gk = season_gk_data(season=page_season)

        # ##### Season Filter
        filter_type_gk = ["Total", "Home", "Away", "1st Period", "2nd Period"]
        match_day_player = np.max(buli_gk_season_df['Week_No'].values)
        if match_day_player <= 17:
            filter_type_gk.remove("2nd Period")

        # ##### GK Top 10 Statistics
        st.subheader(f"Top 10 GK Statistics: Season {page_season}")
        top10_menu_col, top10_plot_col = st.columns([2.5, 8])
        with top10_menu_col:
            top10_stat_type = st.selectbox("Type Statistics", ["Total", "Average"])
            top10_gk_filter = st.selectbox("Season Type", filter_type_gk)
            if top10_stat_type == "Total":
                top10_gk_stats = gk_stats_total
            else:
                top10_gk_stats = gk_stats_avg
            top10_gk_stat = st.selectbox("Name Statistics", top10_gk_stats)

        with top10_plot_col:
            top10_gk_fig = gk_top_statistics(data=buli_gk_season_df,
                                             season_filter=top10_gk_filter,
                                             avg_gk=final_avg_gk,
                                             stat_top10=top10_gk_stat,
                                             type_top10=top10_stat_type)

            config = {'displayModeBar': False}
            st.plotly_chart(top10_gk_fig, config=config, use_container_width=True)

        with top10_menu_col:
            if top10_stat_type == "Average":
                st.markdown(
                    "<b><font color = #d20614>Note</font></b>: Only Goalkeepers with at least <b>"
                    "<font color = #d20614>10%</font></b> of minutes played were included.", unsafe_allow_html=True)

        # ##### GK Match Data Statistics
        st.subheader(f"GK Match Day Statistics: Season {page_season}")
        gk_day_col, gk_day_chart_col, gk_day_logo_col = st.columns([3.1, 8, 1])
        with gk_day_col:
            stat_gk_day = st.selectbox("Gk Statistics", gk_stats_avg)
            gk_match_day = buli_gk_season_df[(buli_gk_season_df['Team'] == favourite_team)]['Name_Team'].values[0]
            pos_gk = final_avg_gk.index(gk_match_day)
            final_name_avg_gk = [gk.split("_")[1] for gk in final_avg_gk]
            gk_name_day = st.selectbox("Select Match Day Gk", final_name_avg_gk, pos_gk)
        with gk_day_chart_col:
            fig_gk_day, gk_team_name, gk_league_comparison, gk_stat_sig_name = gk_chart_day(data=buli_gk_season_df,
                                                                                            avg_gk=final_avg_gk,
                                                                                            gk_name=gk_name_day,
                                                                                            stat_name=stat_gk_day)

            config = {'displayModeBar': False}
            st.plotly_chart(fig_gk_day, config=config, use_container_width=True)

        with gk_day_logo_col:
            team_gk_logo = Image.open(f'images/{gk_team_name}.png')
            st.image(team_gk_logo, use_column_width=True)

        with gk_day_col:
            if gk_stat_sig_name == "":
                st.markdown(
                    f"<b><font color = #d20614>{gk_name_day}</font></b> has on Average <b><font color = green>"
                    f"{gk_league_comparison}</font></b> <b><font color = #d20614>{stat_gk_day}</font></b> per game "
                    f"then the league Average.", unsafe_allow_html=True)
            else:
                st.markdown(
                    f"<b><font color = #d20614>{gk_name_day}</font></b> has on Average <b><font color = greeen>"
                    f"{gk_league_comparison}</font></b> <b><font color = #d20614>{stat_gk_day}</font></b> per game"
                    f" then the league Average which is <b><font color = #d20614>{gk_stat_sig_name}</font></b>",
                    unsafe_allow_html=True)

            st.markdown("<b><font color = #d20614>Note</font></b>: Only Goalkeepers with at least <b>"
                        "<font color = #d20614>10%</font></b> of minutes played were included.", unsafe_allow_html=True)

        # ##### GK Season Type Statistics
        st.subheader(f"GK Season Type Stats: Season {page_season}")
        gk_team_image_col, gk_team_name_col, type_gk_chart_col = st.columns([1, 3, 9])
        with gk_team_image_col:
            st.image(team_gk_logo, use_column_width=True)

        with gk_team_name_col:
            st.markdown("")
            st.markdown(f"<h4><b>{gk_name_day}</b></h4>", unsafe_allow_html=True)
            gk_type_stat = st.selectbox("Statistics", gk_stats_avg)

        with type_gk_chart_col:
            gk_stat_fig, gk_home_away = gk_season_filter_stats(data=buli_gk_season_df,
                                                               player_name=gk_name_day,
                                                               avg_gk=final_avg_gk,
                                                               stat_name=gk_type_stat)

            config = {'displayModeBar': False}
            st.plotly_chart(gk_stat_fig, config=config, use_container_width=True)

        with gk_team_name_col:
            st.markdown(f"<b><font color = #d20614>{gk_name_day}</font></b> has more <b><font color = green>"
                        f"{gk_type_stat}</font></b> per Game on Average for <b><font color = #d20614>{gk_home_away}"
                        f"</font></b> Season Games.", unsafe_allow_html=True)

            st.markdown("<b><font color = #d20614>Note</font></b>: Only Goalkeepers with at least <b>"
                        "<font color = #d20614>10%</font></b> of minutes played were included.", unsafe_allow_html=True)

        # ##### Gk Stats Relationship Statistics
        st.subheader(f"GK Stats Relationship: Season {page_season}")
        gk_rel_filter_col, gk_rel_chart_col, gk_rel_image_col = st.columns([3, 8, 1])
        with gk_rel_filter_col:
            gk_corr_filter_type = st.selectbox("GK Relationship Season Type", filter_type_gk)
            gk_name = st.selectbox("Highlight Player", final_name_avg_gk, pos_gk)
            gk_stats_names_1 = gk_stats_avg.copy()
            gk_stat_x = st.selectbox("Select X Stat", gk_stats_names_1)
            gk_stats_names_2 = gk_stats_names_1.copy()
            gk_stats_names_2.remove(gk_stat_x)
            gk_stat_y = st.selectbox("Select Y Stat", gk_stats_names_2)
            gk_stats_names_3 = gk_stats_names_2.copy()
            gk_stats_names_3.remove(gk_stat_y)
            gk_stats_z = st.selectbox("Select Size Stat", gk_stats_names_3)

        with gk_rel_chart_col:
            gk_corr_fig, gk_corr_team, gk_corr_value, gk_corr_strength, gk_corr_sign = gk_relationship_data(
                data=buli_gk_season_df,
                filter_type=gk_corr_filter_type,
                player_name=gk_name,
                avg_gk=final_avg_gk,
                stat_x=gk_stat_x,
                stat_y=gk_stat_y,
                stat_size=gk_stats_z)

            config = {'displayModeBar': False}
            st.plotly_chart(gk_corr_fig, config=config, use_container_width=True)

        with gk_rel_image_col:
            gk_corr_logo = Image.open(f'images/{gk_corr_team}.png')
            st.image(gk_corr_logo, width=100)

        with gk_rel_filter_col:
            if gk_corr_value != "":
                st.markdown(f"For <b><font color = #d20614>{gk_corr_filter_type}</font></b> Season Games, <b>"
                            f"<font color = #d20614>{gk_name}</font></b> has a <b><font color = green>{gk_corr_sign}"
                            f"</font></b> <b><font color = #d20614>{gk_corr_strength}</font></b> Correlation (<b>"
                            f"<font color = green>{gk_corr_value}</font></b>) between "
                            f"<b><font color = green>{gk_stat_x}</font></b> and <b><font color = #d20614>{gk_stat_y}"
                            f"</font></b>.", unsafe_allow_html=True)
            else:
                st.markdown(f"Less then <b><font color = black>10</font></b> <b><font color = #d20614>"
                            f"{gk_corr_filter_type}</font></b> Season Games played.", unsafe_allow_html=True)

            st.markdown("<b><font color = #d20614>Note</font></b>: Only Goalkeepers with at least <b>"
                        "<font color = #d20614>10%</font></b> of minutes played were included.", unsafe_allow_html=True)

    elif gk_stats == "Season by Season Stats":
        st.subheader(f"Gk Stats over the Last 5 Seasons")
        gk_filter_col, gk_chart_col, gk_markdown_col = st.columns([3, 7, 2])
        with gk_filter_col:
            # ##### Select Season
            buli_gk_season_df, final_avg_gk = buli_gk_data(season=page_season,
                                                           team=favourite_team,
                                                           all_seasons=all_seasons)

            # ##### Data Filter
            filter_type_gk = ["Total", "Home", "Away", "1st Period", "2nd Period"]
            stat_gk_seasons = st.selectbox("Gk Statistics", gk_stats_avg)
            seasons_gk_filter = st.selectbox("Select Season Type", filter_type_gk)
            default_player_team = buli_gk_season_df[
                (buli_gk_season_df['Team'] == favourite_team) & (buli_gk_season_df['Season'] == page_season)][
                'Name_Team'].unique()[0]
            final_name_avg_gk = [gk.split("_")[1] for gk in final_avg_gk]
            seasons_gk_name = st.selectbox("Gk Name", final_name_avg_gk, final_avg_gk.index(default_player_team))

            gk_team_name = gk_current_season_team(data=buli_gk_season_df,
                                                  season=page_season,
                                                  avg_gk=final_avg_gk,
                                                  player=seasons_gk_name)
            buli_gk_logo = Image.open(f'images/{gk_team_name}.png')
            st.image(buli_gk_logo, width=100)

            st.markdown("<b><font color = #d20614>Note</font></b>: Only Gk with at least <b><font color = #d20614>10%"
                        "</font></b> of minutes played were included.", unsafe_allow_html=True)

        with gk_chart_col:
            gk_buli_fig, gk_rank_season, gk_better_seasons, gk_no_seasons = gk_buli_stats(data=buli_gk_season_df,
                                                                                          gk_team=gk_team_name,
                                                                                          gk_name=seasons_gk_name,
                                                                                          avg_gk=final_avg_gk,
                                                                                          stat_name=stat_gk_seasons,
                                                                                          filter_type=seasons_gk_filter,
                                                                                          analysis_seasons=page_season)

            config = {'displayModeBar': False}
            st.plotly_chart(gk_buli_fig, config=config, use_container_width=True)

        with gk_markdown_col:
            if gk_rank_season == 1:
                gk_rank_name = 'st'
            elif gk_rank_season == 2:
                gk_rank_name = 'nd'
            elif gk_rank_season == 3:
                gk_rank_name = 'rd'
            else:
                gk_rank_name = 'th'

            if gk_no_seasons > 1:
                st.markdown(
                    f"<b><font color = black>{seasons_gk_name}</font></b> has the <b><font color = black>"
                    f"{gk_rank_season}</font></b><b><font color = black>{gk_rank_name}</font></b> "
                    f"highest Average <b><font color = #d20614>{stat_gk_seasons}</font></b> per Game for the "
                    f"<b><font color = black>{seasons_gk_filter}</font></b> Season <b><font color = #d20614>"
                    f"{page_season}</font></b>, if we look at the last <b><font color = black>"
                    f"{gk_no_seasons}</font></b> Seasons. In <b><font color = #d20614>{gk_better_seasons}"
                    f"</font></b> of the last <b><font color = black>{gk_no_seasons}</font></b> Seasons, "
                    f"<b><font color = #d20614>{seasons_gk_name}</font></b> has more <b><font color = black>"
                    f"{stat_gk_seasons}</font></b> on Average per Game then the <b><font color = black>"
                    f"Bundesliga</font></b> League Average for <b><font color = #d20614>"
                    f"{seasons_gk_filter}</font></b> Season Games.", unsafe_allow_html=True)
            elif gk_no_seasons == 1:
                st.markdown(f"<b><font color = #d20614>{gk_rank_season}</font></b>", unsafe_allow_html=True)
            else:
                st.markdown(f"No Data for Season <b><font color = #d20614>{page_season}</font></b>.",
                            unsafe_allow_html=True)

        st.subheader(f"Gk Stats Relationship over the Last 5 Seasons")
        gk_rel_filter_col, gk_rel_chart_col, gk_markdown_col = st.columns([2.5, 6, 2])
        with gk_rel_filter_col:
            gk_corr_filter_type = st.selectbox("Player Relationship Season Type", filter_type_gk)
            gk_stats_names_1 = gk_stats_avg.copy()
            gk_stat_x = st.selectbox("Select X Stat", gk_stats_names_1)
            gk_stats_names_2 = gk_stats_names_1.copy()
            gk_stats_names_2.remove(gk_stat_x)
            gk_stat_y = st.selectbox("Select Y Stat", gk_stats_names_2)
            st.markdown("<b><font color = #d20614>Note</font></b>: Only Players with at least <b>"
                        "<font color = #d20614>10%</font></b> of minutes played were included.", unsafe_allow_html=True)

        with gk_rel_chart_col:
            gk_seasons_fig, gk_overall_corr_value, gk_overall_corr_strength, gk_overall_corr_sign, \
                gk_season_name_best_corr, gk_season_value_best_corr, gk_season_corr_strength, gk_season_corr_sign, \
                gk_no_games = gk_buli_corr_data(data=buli_gk_season_df,
                                                filter_type=gk_corr_filter_type,
                                                team=gk_team_name,
                                                player=seasons_gk_name,
                                                stat_x=gk_stat_x,
                                                stat_y=gk_stat_y,
                                                avg_gk=final_avg_gk,
                                                analysis_seasons=all_seasons)

            config = {'displayModeBar': False}
            st.plotly_chart(gk_seasons_fig, config=config, use_container_width=True)
            st.markdown("<b><font color = #d20614>Size</font></b>: Points 1: <b><font color = #d20614>Defeat</font></b>"
                        ", Points 2: <b><font color = #d20614>Draw</font></b>, Points 3: <b><font color = #d20614>"
                        "Win</font></b>", unsafe_allow_html=True)

        with gk_markdown_col:
            corr_gk_logo = Image.open(f'images/{gk_team_name}.png')
            st.image(corr_gk_logo, width=100)
            st.markdown(f"<b>{seasons_gk_name}</b>", unsafe_allow_html=True)

            if gk_no_seasons == 1:
                no_season_name = "Season"
            else:
                no_season_name = f"{gk_no_seasons} Seasons"

            if gk_no_games > 10:
                st.markdown(f"For <b><font color = #d20614>{gk_corr_filter_type}</font></b> Season Games there is a "
                            f"<b><font color = #d20614>{gk_overall_corr_sign}</font></b> <b><font color = green>"
                            f"{gk_overall_corr_strength}</font></b> Correlation between <b><font color = #d20614>"
                            f"{gk_stat_x}</font></b> and <b><font color = #d20614>{gk_stat_y}</font></b> "
                            f"(<b><font color = purple>{gk_overall_corr_value}</font></b>) if we look at the last "
                            f"{no_season_name} of <b><font color = #d20614>{seasons_gk_name}</font></b> in the "
                            f"Bundesliga.", unsafe_allow_html=True)
                if gk_no_seasons > 1:
                    if gk_season_name_best_corr != "":
                        st.markdown(f"If we look at Season data, Season <b><font color = #d20614>"
                                    f"{gk_season_name_best_corr}</font></b> has the strongest correlation between <b>"
                                    f"<font color = #d20614>{gk_stat_x} </font></b> and <b><font color = #d20614>"
                                    f"{gk_stat_y}</font></b> (<b><font color = purple>{gk_season_value_best_corr}"
                                    f"</font></b>) a <b><font color = #d20614>{gk_season_corr_sign}</font></b><b>"
                                    f"<font color = green> {gk_season_corr_strength}</font></b> Relationship.",
                                    unsafe_allow_html=True)
                    else:
                        st.markdown(f"<b><font color = #d20614>No</font></b> Season with at least "
                                    f"<b><font color = #d20614>10</font></b> games played.", unsafe_allow_html=True)

            elif gk_no_games == 0:
                st.markdown(f"No Data for <b><font color = #d20614>{gk_corr_filter_type}</font></b> Season Games.",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"Less then 10 <b><font color = #d20614>{gk_corr_filter_type}</font></b> Season Games.",
                            unsafe_allow_html=True)
