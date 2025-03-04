import os
import pandas as pd
from modules.auth import *
import json


def get_dataframe():
    current_dir = os.path.dirname(__file__)
    pkl_path = os.path.join(current_dir, '..', 'data', 'clusteredDataset.pkl')
    return pd.read_pickle(pkl_path)


def get_filtered_dataframe(df):
    user = get_current_user()
    games_liked = json.loads(user["games_liked"])
    games_disliked = json.loads(user["games_disliked"])
    saved_games = json.loads(user["saved_games"])
    df_filtered = df[
        ~(df['AppID'].isin(games_liked) | df['AppID'].isin(games_disliked) | df['AppID'].isin(saved_games))]
    return df_filtered


def pick_popular_games(n_of_games):
    df = get_filtered_dataframe(get_dataframe())
    top_1000 = df.sort_values(by="Positive", ascending=False).head(1000)
    return top_1000.sample(n_of_games)


def get_cluster_counts(games_liked, df):
    liked_games_df = df[df['AppID'].isin(games_liked)]
    cluster_counts = liked_games_df['Cluster'].value_counts().to_dict()
    return cluster_counts


def pick_recommended_games(username, n_of_games):
    df = get_dataframe()
    user = get_user(username)
    games_liked = json.loads(user["games_liked"])
    cluster_counts = get_cluster_counts(games_liked, df)
    df_filtered = get_filtered_dataframe(df)
    samples = []

    for cluster, liked_count in cluster_counts.items():
        cluster_df = df_filtered[df_filtered['Cluster'] == cluster]
        n_to_sample = 10 * liked_count
        sample = cluster_df.sample(n=n_to_sample)
        sample_popular_games = sample.sort_values(by="Positive", ascending=False).head(n_to_sample // 2)
        samples.append(sample_popular_games)

    recommended_df = pd.concat(samples)
    return recommended_df.sample(n=n_of_games)
