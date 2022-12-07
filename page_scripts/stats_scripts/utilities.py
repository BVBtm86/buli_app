import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from supabase import create_client


# ##### SQL Database Query
# ##### Supabase Connection
@st.experimental_singleton(show_spinner=False)
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)


supabase = init_connection()


# ##### Supabase Load Team Data
@st.experimental_memo(ttl=600, show_spinner=False)
def seasons_query():
    """ Return Available Seasons """
    data_query = supabase.table('buli_stats_team').select('*').execute().data
    data = pd.DataFrame(data_query)
    all_seasons = list(data['Season'].unique())
    final_seasons = all_seasons[-5:]

    return final_seasons


@st.experimental_memo(ttl=600, show_spinner=False)
def favourite_team_query(season):
    """ Return Available Teams """
    team_query = supabase.table('buli_stats_team').select('*').eq("Season", season).execute().data
    team_data = pd.DataFrame(team_query)
    all_teams = list(team_data['Team'].unique())

    return all_teams


@st.experimental_memo(ttl=600, show_spinner=False)
def season_team_query(season):
    """ Return Team Data """
    team_query = supabase.table('buli_stats_team').select('*').eq("Season", season).execute().data
    team_data = pd.DataFrame(team_query)

    return team_data


@st.experimental_memo(ttl=600, show_spinner=False)
def all_team_query(all_seasons):
    """ Return Team Data """
    final_team_data = pd.DataFrame()
    for season in all_seasons:
        team_query = \
            supabase.table('buli_stats_team').select('*').eq("Season", season).execute().data
        team_data = pd.DataFrame(team_query)
        final_team_data = pd.concat([final_team_data, team_data])

    final_team_data = final_team_data.reset_index(drop=True)

    return final_team_data


# ##### Supabase Load Player Data
@st.experimental_memo(ttl=600, show_spinner=False)
def season_player_query(season):
    """ Return Player Data """
    player_query = supabase.table('buli_stats_player').select('*').eq("Season", season).execute().data
    player_data = pd.DataFrame(player_query)

    return player_data


@st.experimental_memo(ttl=600, show_spinner=False)
def all_player_query(team, all_seasons):
    """ Return Player Data """
    final_player_data = pd.DataFrame()
    for season in all_seasons:
        player_query = \
            supabase.table('buli_stats_player').select('*').eq("Season", season).eq("Team", team).execute().data
        player_data = pd.DataFrame(player_query)
        final_player_data = pd.concat([final_player_data, player_data])

    final_player_data = final_player_data.reset_index(drop=True)

    return final_player_data


# ##### Supabase Load GK Data
@st.experimental_memo(ttl=600, show_spinner=False)
def season_gk_query(season):
    """ Return GK Data """
    gk_query = supabase.table('buli_stats_gk').select('*').eq("Season", season).execute().data
    gk_data = pd.DataFrame(gk_query)

    return gk_data


@st.experimental_memo(ttl=600, show_spinner=False)
def all_gk_query(all_seasons):
    """ Return GK Data """
    final_gk_data = pd.DataFrame()
    for season in all_seasons:
        gk_query = supabase.table('buli_stats_gk').select('*').eq("Season", season).execute().data
        gk_data = pd.DataFrame(gk_query)
        final_gk_data = pd.concat([final_gk_data, gk_data])

    final_gk_data = final_gk_data.reset_index(drop=True)

    return final_gk_data


# ##### Supabase Load Prediction Games
@st.experimental_memo(ttl=600, show_spinner=False)
def prediction_query():
    """ Return Prediction Data """
    games_query = supabase.table('buli_stats_game_prediction').select('*').execute().data
    games_data = pd.DataFrame(games_query)

    return games_data


# ##### Mosaic Plot
def radar_mosaic(radar_height=0.500, title_height=0, figheight=2):
    if title_height + radar_height > 1:
        error_msg = 'Reduce one of the radar_height or title_height so the total is ≤ 1.'
        raise ValueError(error_msg)
    endnote_height = 1 - title_height - radar_height
    figwidth = figheight * radar_height
    figure, axes = plt.subplot_mosaic([['title'], ['radar'], ['endnote']],
                                      gridspec_kw={'height_ratios': [title_height, radar_height,
                                                                     endnote_height],
                                                   'bottom': 0, 'left': 0, 'top': 1,
                                                   'right': 1, 'hspace': 0},
                                      figsize=(figwidth, figheight))
    axes['title'].axis('off')
    axes['endnote'].axis('off')
    return figure, axes
