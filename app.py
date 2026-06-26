import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib

model = joblib.load("xgb_best_model.pkl")

feature_columns = [
    'IS_HOME',
    'PTS_ROLL5', 'AST_ROLL5', 'TOV_ROLL5', 'REB_ROLL5', 'FG_PCT_ROLL5',
    'OPP_PTS_ROLL5', 'OPP_AST_ROLL5', 'OPP_TOV_ROLL5', 'OPP_REB_ROLL5', 'OPP_FG_PCT_ROLL5',
    'WIN_STREAK', 'REST_DAYS', 'Opponent_Win_Rate', 'DATE_ORDINAL'
]

feature_limits = {
    'IS_HOME': (0, 1),
    'PTS_ROLL5': (0, 150),
    'AST_ROLL5': (0, 40),
    'TOV_ROLL5': (0, 30),
    'REB_ROLL5': (0, 60),
    'FG_PCT_ROLL5': (0.0, 1.0),
    'OPP_PTS_ROLL5': (0, 150),
    'OPP_AST_ROLL5': (0, 40),
    'OPP_TOV_ROLL5': (0, 30),
    'OPP_REB_ROLL5': (0, 60),
    'OPP_FG_PCT_ROLL5': (0.0, 1.0),
    'WIN_STREAK': (0, 20),
    'REST_DAYS': (0, 10),
    'Opponent_Win_Rate': (0.0, 1.0),
    'DATE_ORDINAL': (0, 1000000)
}

def predict_game_result(df):
    pred_probs = model.predict_proba(df[feature_columns])[:, 1]
    pred_labels = model.predict(df[feature_columns])
    df['Predicted_Win'] = pred_labels
    df['Win_Probability'] = pred_probs.round(4)
    return df

st.set_page_config(layout="wide")
st.title("NBA Insights - Game Outcome Predictor")
st.markdown("Use your model to simulate NBA matchups based on 5-game rolling stats.")

input_mode = st.sidebar.radio("Choose input mode:", ["Manual Input", "Upload CSV"])

if input_mode == "Manual Input":
    st.subheader("Enter Game Stats")
    input_dict = {}
    for col in feature_columns:
        if col == 'DATE_ORDINAL':
            selected_date = st.date_input("Select Game Date")
            input_dict[col] = selected_date.toordinal()
        else:
            min_val, max_val = feature_limits[col]
            if col == 'IS_HOME':
                input_dict[col] = st.selectbox("Is the team playing at home?", [0, 1])
            elif 'FG_PCT' in col or col == 'Opponent_Win_Rate':
                input_dict[col] = st.number_input(f"{col}", min_value=min_val, max_value=max_val, step=0.01)
            else:
                step = 1 if isinstance(min_val, int) else 1.0
                input_dict[col] = st.number_input(f"{col}", min_value=min_val, max_value=max_val, step=step)

    if st.button("Predict"):
        df_input = pd.DataFrame([input_dict])
        result = predict_game_result(df_input)
        st.write(result[['Predicted_Win', 'Win_Probability']])

else:
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Upload a CSV with the correct columns", type=["csv"])
    if uploaded_file:
        df_uploaded = pd.read_csv(uploaded_file)
        st.write("File uploaded successfully. Here's a preview:")
        st.dataframe(df_uploaded.head())
        if not all(col in df_uploaded.columns for col in feature_columns):
            st.error("The uploaded CSV is missing one or more required columns.")
        else:
            if st.button("Predict from CSV"):
                result = predict_game_result(df_uploaded)
                st.subheader("Predictions")
                st.dataframe(result[['Predicted_Win', 'Win_Probability']])

st.markdown("---")
tableau_url = "https://public.tableau.com/views/Book1_17823767213270/Dashboard1?:showVizHome=no&:embed=true"
components.iframe(tableau_url, height=850, scrolling=True)