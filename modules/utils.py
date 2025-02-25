import streamlit as st


def display_games(games_df):
    for idx, game in games_df.iterrows():
        # Display game information
        st.markdown(f"### {game['Name']}")
        st.write(f"**Release Date:** {game['Release date']}")
        st.image(game["Header image"], width=200)
        st.write(f"**Price:** {game['Price']}")

        # Create columns for the three buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Add/Remove Liked", key=f"liked_{idx}"):
                # Add your logic here to toggle liked status
                st.write(f"Toggled liked for {game['title']}")
        with col2:
            if st.button("Add/Remove Disliked", key=f"disliked_{idx}"):
                # Add your logic here to toggle disliked status
                st.write(f"Toggled disliked for {game['title']}")
        with col3:
            if st.button("Add/Remove Saved", key=f"saved_{idx}"):
                # Add your logic here to toggle saved status
                st.write(f"Toggled saved for {game['title']}")

        st.markdown("---")  # Separator between games
