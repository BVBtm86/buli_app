import streamlit as st
from page_scripts.stats_scripts.season_predictions import season_data_process, data_processing, data_prediction_game, \
    create_predictions_season
from PIL import Image

accuracy_combo = [0.5069, 0.5302, 0.5200, 0.5699, 0.5469]
model_data = ["last 5 seasons", "last 4 seasons", "last season", "last 2 seasons", "last 3 seasons"]


def prediction_page(prediction_type, season, favourite_team):
    # ##### Season Data
    buli_season_df, current_match_day, model_no = season_data_process(season=season)
    remaining_weeks = list(range(current_match_day + 1, 35))

    if 2 <= current_match_day < 34:
        agg_stats_options = ['Last Game', 'Last 2 Games', 'Last 3 Games', 'Last 4 Games', 'Last 5 Games']
        final_agg_stats_options = agg_stats_options[:model_no]

        agg_stats = st.sidebar.selectbox("Aggregate Stats", final_agg_stats_options)
        agg_step = agg_stats_options.index(agg_stats) + 1

        # ##### Data Processing
        processed_df = data_processing(data=buli_season_df,
                                       current_match_day=current_match_day,
                                       rolling_data=agg_step)

        # ##### Game Prediction
        if prediction_type == 'Games':
            week_no = st.sidebar.selectbox("Select Week No", remaining_weeks, index=0)

            match_day_col, accuracy_col, _ = st.columns([8, 2, 0.5])
            with match_day_col:
                st.header(f"Season: {season} Match Day {week_no} Predictions")

            st.markdown(
                f"<b><font color = #d20614>Game Prediction</font></b> for Season <b><font color = black>{season}"
                f"</font></b> based on the <b><font color = #d20614>""Averages</font></b> of previous Home vs Away "
                "Team Stats that captures a Teams form for Home/Away games", unsafe_allow_html=True)

            _, hw_prob_col, d_prob_col, aw_prob_col, _ = st.columns([4, 1, 1, 1, 4])

            with hw_prob_col:
                st.markdown("")
                st.markdown("<b>HWin</b>", unsafe_allow_html=True)

            with d_prob_col:
                st.markdown("")
                st.markdown("<b>Draw</b>", unsafe_allow_html=True)

            with aw_prob_col:
                st.markdown("")
                st.markdown("<b>AWin</b>", unsafe_allow_html=True)

            prediction_results, model_features = data_prediction_game(data=processed_df,
                                                                      step=agg_step,
                                                                      week_no=week_no)

            home_team_names = prediction_results['Home Team'].values
            away_team_names = prediction_results['Away Team'].values
            home_prob = prediction_results['Win %'].values
            draw_prob = prediction_results['Draw %'].values
            away_prob = prediction_results['Defeat %'].values

            _, home_logo_col, home_name_col, hw_col, d_col, aw_col, away_logo_col, away_name_col, _ = \
                st.columns([0.5, 0.35, 3, 1, 1, 1.1, 0.35, 3, 0.5])

            for i in range(len(home_team_names)):
                with home_logo_col:
                    h_logo = Image.open(f'images/{home_team_names[i]}.png')
                    st.image(h_logo, width=26)

                with home_name_col:
                    if home_team_names[i] == favourite_team or away_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{home_team_names[i]}</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(home_team_names[i])

                with away_logo_col:
                    a_logo = Image.open(f'images/{away_team_names[i]}.png')
                    st.image(a_logo, width=26)

                with away_name_col:
                    if away_team_names[i] == favourite_team or home_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{away_team_names[i]}</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(away_team_names[i])

                with hw_col:
                    if away_team_names[i] == favourite_team or home_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{home_prob[i]}%</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"{home_prob[i]}%")

                with d_col:
                    if away_team_names[i] == favourite_team or home_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{draw_prob[i]}%</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"{draw_prob[i]}%")
                with aw_col:
                    if away_team_names[i] == favourite_team or home_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{away_prob[i]}%</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"{away_prob[i]}%")

            with accuracy_col:
                st.subheader("")
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=#d20614>"
                            f"{accuracy_combo[agg_stats_options.index(agg_stats)]:.2%}</font></b>",
                            unsafe_allow_html=True)
            st.markdown(
                f"<b><font color = #d20614>Note</font></b>: The model was build using the <b><font color = #d20614"
                f">Logistic Regression </font></b> Algorithm on the {model_data[agg_stats_options.index(agg_stats)]} "
                f"of data using <b><font color = #d20614>{len(model_features)}</font></b> match day stats.",
                unsafe_allow_html=True)
            st.sidebar.markdown("")

        elif prediction_type == 'Season':
            season_col, accuracy_col, _ = st.columns([15, 2, 0.5])
            with season_col:
                st.header(f"Season: {season} Predicted Table")

            st.markdown("<b><font color = black>Final Season Table</font></b> based on the <b><font color = #d20614>"
                        "Averages</font></b> of previous Home vs Away Team Stats that captures a Teams form for "
                        "Home/Away games", unsafe_allow_html=True)

            final_predict_tab, model_features = create_predictions_season(data=processed_df,
                                                                          current_data=buli_season_df,
                                                                          step=agg_step)

            logo_col, rank_col, team_col, mp_col, w_col, d_col, l_col, pts_col = st.columns([0.42, 1, 5, 1, 1, 1, 1, 1])

            with logo_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b><font color='white'>#</font></b>",
                            unsafe_allow_html=True)
            with rank_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>Rank</b>", unsafe_allow_html=True)

            with team_col:
                st.markdown(f"<h4 style='text-align: left;'h4><b>Team</b>", unsafe_allow_html=True)

            with mp_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>MP</b>", unsafe_allow_html=True)

            with w_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>W</b>", unsafe_allow_html=True)

            with d_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>D</b>", unsafe_allow_html=True)

            with l_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>L</b>", unsafe_allow_html=True)

            with pts_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>Pts</b>", unsafe_allow_html=True)

            for i in range(len(final_predict_tab)):
                with logo_col:
                    logo_teams = Image.open(f'images/{final_predict_tab.iloc[i, 0]}.png')
                    st.image(logo_teams, width=26)

                with rank_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.index[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.index[i]}",
                                    unsafe_allow_html=True)

                with team_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: left;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 0]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: left;'p>{final_predict_tab.iloc[i, 0]}",
                                    unsafe_allow_html=True)

                with mp_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 1]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.iloc[i, 1]}",
                                    unsafe_allow_html=True)

                with w_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 2]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.iloc[i, 2]}",
                                    unsafe_allow_html=True)

                with d_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 3]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.iloc[i, 3]}",
                                    unsafe_allow_html=True)

                with l_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 4]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.iloc[i, 4]}",
                                    unsafe_allow_html=True)

                with pts_col:
                    if final_predict_tab.iloc[i, 0] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{final_predict_tab.iloc[i, 5]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{final_predict_tab.iloc[i, 5]}",
                                    unsafe_allow_html=True)

            with accuracy_col:
                st.subheader("")
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=#d20614>"
                            f"{accuracy_combo[agg_stats_options.index(agg_stats)]:.2%}</font></b>",
                            unsafe_allow_html=True)
            st.markdown(
                f"<b><font color = #d20614>Note</font></b>: The model was build using the <b><font color = #d20614"
                f">Logistic Regression </font></b> Algorithm on the {model_data[agg_stats_options.index(agg_stats)]} "
                f"of data using <b><font color = #d20614>{len(model_features)}</font></b> match day stats.",
                unsafe_allow_html=True)
        st.sidebar.markdown("")
    else:
        st.markdown("<h2><b>Page will be available after </font></b></h2> <h2><b><font color=#d20614>Match Day: 2"
                    "</font></font></b></h2>",
                    unsafe_allow_html=True)
