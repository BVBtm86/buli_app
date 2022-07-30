from page_scripts.stats_scripts.season_predictions import *
from PIL import Image


def prediction_page(prediction_type, season, favourite_team):
    # ##### Season Data
    buli_season_df, current_match_day, season, final_model, final_transform, model_features, \
    prediction_game_df, prediction_data, home_default, away_default = season_data_process(season=season)
    remaining_weeks = list(range(current_match_day + 1, 35))

    if 17 <= current_match_day < 34:
        season_transformed_data, final_model_features, index_agg_home_team, \
        index_agg_away_team = transform_data(data=buli_season_df,
                                             features=model_features,
                                             scalar=final_transform)

        agg_stats_options = ['Last Game', 'Last 2 Games', 'Last 3 Games', 'Last 4 Games', 'Last 5 Games']
        if index_agg_home_team < 6:
            home_agg_stats_options = agg_stats_options[:index_agg_home_team]
        else:
            home_agg_stats_options = agg_stats_options[:5]

        if index_agg_away_team < 6:
            away_agg_stats_options = agg_stats_options[:index_agg_away_team]
        else:
            away_agg_stats_options = agg_stats_options[:5]

        # ##### Game Prediction
        if prediction_type == 'Games':
            week_no = st.sidebar.selectbox("Select Week No", remaining_weeks, index=0)

            match_day_col, accuracy_col = st.columns([8, 2])
            with match_day_col:
                st.header(f"Season: {season} Match Day {week_no} Predictions")

            st.markdown(
                f"<b><font color = #d20614>Game Prediction</font></b> for Season <b><font color = black>{season}"
                f"</font></b> based on the <b><font color = #d20614>""Averages</font></b> of previous Games Stats "
                "that captures a Teams form for Home/Away games", unsafe_allow_html=True)

            _, home_agg_col, _, away_agg_col, _ = st.columns([1, 2.5, 3, 2.5, 2])
            with home_agg_col:
                home_agg_stats = st.selectbox("Home Aggregate Stats", home_agg_stats_options, home_default)
                home_agg_step = agg_stats_options.index(
                    home_agg_stats) + 1

            with away_agg_col:
                away_agg_stats = st.selectbox("Away Aggregate Stats", away_agg_stats_options, away_default)
                away_agg_step = agg_stats_options.index(
                    away_agg_stats) + 1

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

            home_team_names, away_team_names, home_prob, draw_prob, away_prob, accuracy_combo = game_prediction_teams(
                data=season_transformed_data,
                features=final_model_features,
                match_day=week_no,
                games_predict=prediction_game_df,
                home_agg_steps=home_agg_step,
                away_agg_steps=away_agg_step,
                predict_data=prediction_data,
                model=final_model)

            _, home_logo_col, home_name_col, hw_col, d_col, aw_col, away_logo_col, away_name_col, _ = \
                st.columns([0.5, 0.35, 3, 1, 1, 1.1, 0.35, 3, 0.5])

            for i in range(len(home_team_names)):
                with home_logo_col:
                    h_logo = Image.open(f'images/{home_team_names[i]}.png')
                    if current_match_day % 2 == 0:
                        st.image(h_logo, width=24)
                    else:
                        st.image(h_logo, width=25)

                with home_name_col:
                    if home_team_names[i] == favourite_team or away_team_names[i] == favourite_team:
                        st.markdown(f"<b><font color = #d20614>{home_team_names[i]}</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(home_team_names[i])

                with away_logo_col:
                    a_logo = Image.open(f'images/{away_team_names[i]}.png')
                    if current_match_day % 2 == 0:
                        st.image(a_logo, width=25)
                    else:
                        st.image(a_logo, width=24)

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
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=#d20614>{accuracy_combo}%</font></b>",
                            unsafe_allow_html=True)

        elif prediction_type == 'Season':
            season_col, accuracy_col = st.columns([8, 2])
            with season_col:
                st.header(f"Season: {season} Predicted Table")

            st.markdown("<b><font color = black>Final Season Table</font></b> based on the <b><font color = #d20614>"
                        "Averages</font></b> of previous Games Stats that captures a Teams form for Home/Away games",
                        unsafe_allow_html=True)

            season_home_agg_col, season_away_agg_col, _ = st.columns([2, 2, 8])
            with season_home_agg_col:
                home_agg_stats = st.selectbox("Home Aggregate Stats", home_agg_stats_options, home_default)
                home_agg_step = ['Last Game', 'Last 2 Games', 'Last 3 Games', 'Last 4 Games', 'Last 5 Games'].index(
                    home_agg_stats) + 1

            with season_away_agg_col:
                away_agg_stats = st.selectbox("Away Aggregate Stats", away_agg_stats_options, away_default)
                away_agg_step = ['Last Game', 'Last 2 Games', 'Last 3 Games', 'Last 4 Games', 'Last 5 Games'].index(
                    away_agg_stats) + 1

            buli_predict_df, accuracy_combo = create_predictions_season(season_data=buli_season_df,
                                                                        data=season_transformed_data,
                                                                        games_predict=prediction_game_df,
                                                                        home_agg_steps=home_agg_step,
                                                                        away_agg_steps=away_agg_step,
                                                                        final_features=final_model_features,
                                                                        match_day=current_match_day,
                                                                        predict_data=prediction_data,
                                                                        model=final_model)
            logo_col, rank_col, team_col, mp_col, w_col, d_col, l_col, pts_col = st.columns([0.42, 1, 5, 1, 1, 1, 1, 1])

            teams_logo = buli_predict_df['Team'].unique()
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

            for i in range(len(teams_logo)):
                with logo_col:
                    logo_teams = Image.open(f'images/{teams_logo[i]}.png')
                    st.image(logo_teams, width=24)

                with rank_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df.index[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df.index[i]}",
                                    unsafe_allow_html=True)

                with team_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: left;'p><b><font color=#d20614>{buli_predict_df['Team'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: left;'p>{buli_predict_df['Team'].values[i]}",
                                    unsafe_allow_html=True)

                with mp_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df['MP'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df['MP'].values[i]}",
                                    unsafe_allow_html=True)

                with w_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df['W'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df['W'].values[i]}",
                                    unsafe_allow_html=True)

                with d_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df['D'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df['D'].values[i]}",
                                    unsafe_allow_html=True)

                with l_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df['L'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df['L'].values[i]}",
                                    unsafe_allow_html=True)

                with pts_col:
                    if teams_logo[i] == favourite_team:
                        st.markdown(
                            f"<p style='text-align: center;'p><b><font color=#d20614>{buli_predict_df['Pts'].values[i]}"
                            f"</font></b>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<p style='text-align: center;'p>{buli_predict_df['Pts'].values[i]}",
                                    unsafe_allow_html=True)

            with accuracy_col:
                st.subheader("")
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=#d20614>{accuracy_combo}%</font></b>",
                            unsafe_allow_html=True)
        st.markdown(
            f"<b><font color = #d20614>Note</font></b>: The base model was build using the <b><font color = #d20614>"
            f"Logistic Regression </font></b> Algorithm on the last 3 seasons of data with the following features:  <b>"
            f"<font color = #d20614>{str(model_features).replace('[', '').replace(']', '')}</font></b> as features "
            f"with an Accuracy of <b><font color = #d20614>70%</font></b>", unsafe_allow_html=True)
    else:
        st.markdown("<h2><b>Page will be available after </font></b></h2> <h2><b><font color=#d20614>Match Day: 2"
                    "</font></font></b></h2>",
                    unsafe_allow_html=True)
