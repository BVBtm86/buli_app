from page_scripts.stats_scripts.season_predictions import *
from PIL import Image


def prediction_page(prediction_type, season):
    # ##### Season Data
    buli_season_df, current_match_day, season, final_model, final_transform, model_features, \
    prediction_game_df, prediction_data, home_default, away_default = season_data_process(season=season)
    remaining_weeks = list(range(current_match_day + 1, 35))

    if 17 <= current_match_day < 34:
    # if 14 <= current_match_day < 34:
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

            st.markdown(f"<b><font color = red>Game Prediction</font></b> for Season <b><font color = black>{season}"
                        f"</font></b> based on the <b><font color = red>""Averages</font></b> of previous Games Stats "
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

            with home_logo_col:
                for hteam_logo in home_team_names:
                    h_logo = Image.open(f'images/{hteam_logo}.png')
                    st.image(h_logo, width=24)

            with home_name_col:
                for hteam in home_team_names:
                    st.markdown(hteam)

            with away_logo_col:
                for ateam_logo in away_team_names:
                    a_logo = Image.open(f'images/{ateam_logo}.png')
                    st.image(a_logo, width=25)

            with away_name_col:
                for ateam in away_team_names:
                    st.markdown(ateam)

            with hw_col:
                for hprob in home_prob:
                    st.markdown(f"{hprob}%", unsafe_allow_html=True)

            with d_col:
                for dprob in draw_prob:
                    st.markdown(f"{dprob}%", unsafe_allow_html=True)

            with aw_col:
                for aprob in away_prob:
                    st.markdown(f"{aprob}%", unsafe_allow_html=True)

            with accuracy_col:
                st.subheader("")
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=red>{accuracy_combo}%</font></b>",
                            unsafe_allow_html=True)

        elif prediction_type == 'Season':
            season_col, accuracy_col = st.columns([8, 2])
            with season_col:
                st.header(f"Season: {season} Predicted Table")

            st.markdown("<b><font color = black>Final Season Table</font></b> based on the <b><font color = red>"
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

            with logo_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>#</b>", unsafe_allow_html=True)
                teams_logo = buli_predict_df['Team'].unique()
                logo_teams = [Image.open(f'images/{teams_logo[i]}.png') for i in range(len(teams_logo))]
                st.image(logo_teams, width=24)

            with rank_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>Rank</b>", unsafe_allow_html=True)
                rank = buli_predict_df.index
                for i in rank:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with team_col:
                st.markdown(f"<h4 style='text-align: left;'h4><b>Team</b>", unsafe_allow_html=True)
                for i in buli_predict_df['Team'].values:
                    st.markdown(f"<p style='text-align: left;'p>{i}", unsafe_allow_html=True)

            with mp_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>MP</b>", unsafe_allow_html=True)
                for i in buli_predict_df['MP'].values:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with w_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>W</b>", unsafe_allow_html=True)
                for i in buli_predict_df['W'].values:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with d_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>D</b>", unsafe_allow_html=True)
                for i in buli_predict_df['D'].values:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with l_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>L</b>", unsafe_allow_html=True)
                for i in buli_predict_df['L'].values:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with pts_col:
                st.markdown(f"<h4 style='text-align: center;'h4><b>Pts</b>", unsafe_allow_html=True)
                for i in buli_predict_df['Pts'].values:
                    st.markdown(f"<p style='text-align: center;'p>{i}", unsafe_allow_html=True)

            with accuracy_col:
                st.subheader("")
                st.markdown(f"<b>Model Accuracy</b>: <b><font color=red>{accuracy_combo}%</font></b>",
                            unsafe_allow_html=True)
        st.markdown(
            f"<b><font color = red>Note</font></b>: The base model was build using the <b><font color = red>SVM "
            f"</font></b> Algorithm with the following features:  <b><font color = red>"
            f"{str(model_features).replace('[', '').replace(']', '')}</font></b> as features and an Accuracy of <b>"
            f"<font color = red>70%</font></b>", unsafe_allow_html=True)
    else:
        st.markdown("<h2><b>Page will be available after </font></b></h2> <h2><b><font color=red>Match Day: 2"
                    "</font></font></b></h2>",
                    unsafe_allow_html=True)
