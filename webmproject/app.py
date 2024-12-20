import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

data_path = '/Users/jaindra/Desktop/hws/webmproject/threads_reviews.csv'
data = pd.read_csv(data_path)

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return sia.polarity_scores(text)['compound']

# Apply sentiment analysis
data['Sentiment_Score'] = data['review_description'].apply(get_sentiment)

# Convert review_date to datetime and sort the data
data['review_date'] = pd.to_datetime(data['review_date'])
data.sort_values('review_date', inplace=True)

# Categorize sentiments into Positive, Neutral, Negative
data['Sentiment_Category'] = pd.cut(
    data['Sentiment_Score'], 
    bins=[-1, -0.05, 0.05, 1], 
    labels=['Negative', 'Neutral', 'Positive']
)

def filter_reviews_by_keyword_and_date(keyword, start_date, end_date):
    start_timestamp = pd.to_datetime(start_date)
    end_timestamp = pd.to_datetime(end_date)
    
    filtered_data = data[data['review_description'].str.contains(keyword, case=False, na=False)]
    filtered_data = filtered_data[(filtered_data['review_date'] >= start_timestamp) & (filtered_data['review_date'] <= end_timestamp)]
    
    sentiment_sort_order = {'Positive': 1, 'Neutral': 2, 'Negative': 3}
    filtered_data['Sort_Key'] = filtered_data['Sentiment_Category'].map(sentiment_sort_order)
    filtered_data_sorted = filtered_data.sort_values('Sort_Key')
    
    return filtered_data_sorted

def main():
    st.title('App Review Sentiment Analysis')
    
    st.sidebar.title("Keyword Sentiment Analysis")
    keyword = st.sidebar.text_input("Enter a keyword to analyze:")
    start_date = st.sidebar.date_input("Start date:", data['review_date'].min().date())
    end_date = st.sidebar.date_input("End date:", data['review_date'].max().date())
    
    if keyword:
        filtered_data_sorted = filter_reviews_by_keyword_and_date(keyword, start_date, end_date)
        if not filtered_data_sorted.empty:
            filtered_daily_sentiment = filtered_data_sorted.resample('D', on='review_date')['Sentiment_Score'].mean().reset_index()
            filtered_weekly_sentiment = filtered_data_sorted.resample('W', on='review_date')['Sentiment_Score'].mean().reset_index()
            
            st.write(f"### Daily Sentiment Trend for '{keyword}'")
            fig_daily, ax_daily = plt.subplots()
            sns.lineplot(data=filtered_daily_sentiment, x='review_date', y='Sentiment_Score', ax=ax_daily)
            ax_daily.set_title(f"Daily Sentiment Trend for '{keyword}'")
            ax_daily.set_xlabel('Date')
            ax_daily.set_ylabel('Average Sentiment Score')
            st.pyplot(fig_daily)
            
            st.write(f"### Weekly Sentiment Trend for '{keyword}'")
            fig_weekly, ax_weekly = plt.subplots()
            sns.lineplot(data=filtered_weekly_sentiment, x='review_date', y='Sentiment_Score', ax=ax_weekly)
            ax_weekly.set_title(f"Weekly Sentiment Trend for '{keyword}'")
            ax_weekly.set_xlabel('Date')
            ax_weekly.set_ylabel('Average Sentiment Score')
            st.pyplot(fig_weekly)
            

            st.write(f"### Sentiment Distribution for '{keyword}'")
            sentiment_counts = filtered_data_sorted['Sentiment_Category'].value_counts()
            fig_pie, ax_pie = plt.subplots()
            ax_pie.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
            ax_pie.set_title('Sentiment Category Distribution')
            st.pyplot(fig_pie)

            st.write(f"### Reviews mentioning '{keyword}' sorted by sentiment")
            st.table(filtered_data_sorted[['review_date', 'review_description', 'Sentiment_Category']])

        else:
            st.sidebar.write(f"No reviews found containing the keyword '{keyword}' in the given date range.")

if __name__ == "__main__":
    main()


#run the code uing streamlit run app.py command in the terminal