---
title: nba_analytics
emoji: 🏀
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# NBA Predictive Modeling and Performance Dashboard

An end-to-end data science and machine learning pipeline that predicts NBA game outcomes using a tuned XGBoost Classifier and visualizes rolling team momentum using an interactive Tableau Dashboard.

## Machine Learning Engine (XGBoost)

Using historical regular-season data fetched dynamically from the NBA API, this project constructs highly predictive features to capture a team's true form going into a matchup.

### Engineered Features:
* 5-Game Rolling Averages: Smoothed indicators for Points, Assists, Rebounds, Turnovers, and FG% for both the target team and the opponent.
* Team and Opponent Current Win Rates: Cumulative season tracking to represent overall strength.
* Active Win Streaks and Rest Days: Built to account for momentum and physical fatigue.

## Tableau Interactive Dashboard

To make model metrics actionable for team analysts, this repository includes a packaged Tableau workbook mapping out seasonal trajectories.

### Dashboard Panes:
1. Cumulative Record Timeline: An accumulating running total of Wins vs. Losses throughout the 82-game campaign.
2. Shooting Momentum: A 5-game moving average comparing team FG% directly against the opponent's FG% using synchronized dual axes.
3. Control of the Glass: 5-game rolling rebounds vs. opponent rebounds.
4. Defensive Aggression: A comparison of team steals against opponent turnovers.
