from modules.recommender import *
from unittest.mock import patch

MOCK_DF = pd.DataFrame({
    "AppID": [1001, 1002, 1003, 1004, 1005],
    "Positive": range(5),
    "Cluster": [1, 2, 2, 3, 1]
})

MOCK_USER = {
    "games_liked": json.dumps([1001, 1003, 1005]),
    "games_disliked": json.dumps([1004]),
    "saved_games": json.dumps([1005])
}


def test_get_dataframe():
    df = get_dataframe()
    assert isinstance(df, pd.DataFrame)


@patch("modules.recommender.get_current_user", return_value=MOCK_USER)
def test_get_filtered_dataframe(mock_get_current_user):
    filtered_df = get_filtered_dataframe(MOCK_DF)

    assert not filtered_df["AppID"].isin(
        [1001, 1003, 1004, 1005]).any()
    expected_remaining_games = {1002}
    assert set(filtered_df["AppID"]) == expected_remaining_games


@patch("modules.recommender.get_filtered_dataframe", return_value=MOCK_DF)
@patch("modules.recommender.get_dataframe", return_value=MOCK_DF)
def test_pick_popular_games(mock_get_dataframe, mock_get_filtered_dataframe):
    n_of_games = 3
    df_selected = pick_popular_games(n_of_games)

    assert isinstance(df_selected, pd.DataFrame)
    assert len(df_selected) == n_of_games


def test_get_cluster_counts():
    games_liked = json.loads(MOCK_USER["games_liked"])
    result = get_cluster_counts(games_liked, MOCK_DF)
    expected_output = {1: 2, 2: 1}

    assert result == expected_output


@patch("modules.recommender.get_filtered_dataframe", return_value=MOCK_DF)
@patch("modules.recommender.get_user", return_value=MOCK_USER)
@patch("modules.recommender.get_dataframe", return_value=MOCK_DF)
def test_pick_recommended_games(mock_get_dataframe, mock_get_user, mock_get_filtered_dataframe):
    n_of_games = 2
    df_selected = pick_recommended_games("testuser", n_of_games)

    assert isinstance(df_selected, pd.DataFrame)
    assert len(df_selected) == n_of_games
