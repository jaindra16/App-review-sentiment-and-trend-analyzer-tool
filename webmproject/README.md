# App Review Sentiment and Trend Analysis Tool

This project provides a tool to analyze sentiment and trends from app reviews, specifically focusing on the "Threads" app from Google Play Store and other sources. Using Natural Language Processing (NLP), it assesses and visualizes the emotional tone and patterns in user feedback.

## Introduction

- **Objective**: To develop a tool that analyzes sentiments, identifies trends over time using keywords, categorizes feedback into sentiment categories, and provides an interactive dashboard for users to explore these sentiments and trends.

## Technical Setup

- **Programming Language**: Python
- **Libraries and Tools**:
  - **NLTK** for natural language processing, using the VADER module for sentiment analysis.
  - **Pandas** for data manipulation and time-series analysis.
  - **Seaborn** and **Matplotlib** for data visualization.
  - **Streamlit** for creating an interactive dashboard.

## Workflow

1. **Preprocessing**: Convert dates to a standardized format for time-series analysis and sort the data by `review_date`.
2. **Sentiment Analysis**: Perform sentiment analysis on each review using NLTK’s VADER tool, assigning a sentiment score from -1 (Negative) to 1 (Positive).
3. **Data Aggregation**: Group data by Day and Week, calculating the average sentiment score for each timeframe to trace sentiment trends.
4. **Visualization**: Use Seaborn and Matplotlib to graph the trends and create an interactive dashboard on Streamlit showcasing pie charts of sentiment categories and fields for keyword entry and timeframe selection.

## Installation - To run this, open the file directory in the terminal and type the following command


streamlit run app.py
