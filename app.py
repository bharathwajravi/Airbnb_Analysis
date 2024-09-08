import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from textblob import TextBlob

# MongoDB connection
def connect_to_mongodb(connection_string):
    try:
        client = MongoClient(connection_string)
        print("Connected successfully to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def retrieve_data(client, db_name, collection_name):
    try:
        db = client[db_name]
        collection = db[collection_name]
        cursor = collection.find({})
        documents = list(cursor)
        print(f"Retrieved {len(documents)} documents from collection '{collection_name}'")
        return documents
    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")
        return []

def get_document_count(client, db_name, collection_name):
    try:
        db = client[db_name]
        collection = db[collection_name]
        count = collection.count_documents({})
        return count
    except Exception as e:
        print(f"Error getting document count from MongoDB: {e}")
        return 0

# Function to clean text and extract keywords
def extract_keywords(text):
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    return words

# Function to get top keywords
def get_top_keywords(df, column, top_n=10):
    all_text = " ".join(df[column].dropna())
    keywords = extract_keywords(all_text)
    keyword_counts = Counter(keywords)
    top_keywords = keyword_counts.most_common(top_n)
    keyword_df = pd.DataFrame(top_keywords, columns=['Keyword', 'Count'])
    return keyword_df

# Function for sentiment analysis
def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

def get_sentiment_distribution(df, column):
    sentiments = df[column].dropna().apply(analyze_sentiment)
    sentiment_counts = sentiments.value_counts()
    sentiment_df = pd.DataFrame(sentiment_counts).reset_index()
    sentiment_df.columns = ['Sentiment', 'Count']
    return sentiment_df

def main():
    st.set_page_config(page_title="Airbnb Data Analysis", layout="wide")
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .reportview-container .main .block-container {
        padding: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Airbnb Data Analysis Dashboard")
    
    # MongoDB connection details
    connection_string = "mongodb+srv://Bharathwajravi:charanpooja@cluster0.fhgbfbk.mongodb.net/"
    db_name = 'sample_airbnb'
    collection_name = 'CLEANED_AIRBNB'

    # Connect to MongoDB
    client = connect_to_mongodb(connection_string)

    if client:
        # Check the number of documents in the collection
        doc_count = get_document_count(client, db_name, collection_name)
        st.write(f"Number of documents in collection '{collection_name}': {doc_count}")

        if doc_count > 0:
            # Retrieve documents from MongoDB
            documents = retrieve_data(client, db_name, collection_name)
            client.close()

            if documents:
                df = pd.DataFrame(documents)
                st.write(f"Retrieved {df.shape[0]} documents")

                # Tab layout for chart selection
                tabs = ["Accommodation Capacity", "Bedrooms", "Bathrooms", "Neighborhood Overview", "Transit Options", "Price Analysis"]

                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(tabs)

                with tab1:
                    if 'accommodates' in df.columns:
                        st.subheader("Accommodation Capacity")
                        fig1 = px.histogram(df, x='accommodates', nbins=15, title='Distribution of Accommodation Capacity',
                                            labels={'accommodates': 'Number of Guests Accommodated', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig1.update_layout(template='plotly_dark')
                        st.plotly_chart(fig1)

                with tab2:
                    if 'bedrooms' in df.columns:
                        st.subheader("Number of Bedrooms")
                        fig2 = px.histogram(df, x='bedrooms', nbins=15, title='Distribution of Number of Bedrooms',
                                            labels={'bedrooms': 'Number of Bedrooms', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig2.update_layout(template='plotly_dark')
                        st.plotly_chart(fig2)

                with tab3:
                    if 'bathrooms' in df.columns:
                        st.subheader("Number of Bathrooms")
                        fig3 = px.histogram(df, x='bathrooms', nbins=15, title='Distribution of Number of Bathrooms',
                                            labels={'bathrooms': 'Number of Bathrooms', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig3.update_layout(template='plotly_dark')
                        st.plotly_chart(fig3)

                with tab4:
                    if 'neighborhood_overview' in df.columns:
                        st.subheader("Neighborhood Overview")

                        # Get sentiment distribution
                        sentiment_df = get_sentiment_distribution(df, 'neighborhood_overview')

                        # Display sentiment distribution as bar chart
                        st.subheader("Sentiment Distribution in Neighborhood Overview")
                        fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', title='Sentiment Distribution of Neighborhood Descriptions',
                                              color='Count', labels={'Sentiment': 'Sentiment', 'Count': 'Number of Listings'},
                                              color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig_sentiment.update_layout(template='plotly_dark')
                        st.plotly_chart(fig_sentiment)

                        # Option for pie chart
                        if st.checkbox("Show Pie Chart of Sentiments"):
                            fig_sentiment_pie = px.pie(sentiment_df, names='Sentiment', values='Count', title='Sentiment Distribution in Neighborhood Descriptions')
                            st.plotly_chart(fig_sentiment_pie)

                        # Option to display detailed neighborhood descriptions
                        if st.checkbox("Show Detailed Neighborhood Descriptions"):
                            st.write(df[['name', 'neighborhood_overview']])

                with tab5:
                    if 'transit' in df.columns:
                        st.subheader("Transit Options")
                        transit_counts = df['transit'].apply(lambda x: len(str(x).split(',')))
                        fig5 = px.histogram(transit_counts, nbins=10, title='Number of Transit Options',
                                            labels={'value': 'Number of Transit Options', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig5.update_layout(template='plotly_dark')
                        st.plotly_chart(fig5)

                with tab6:
                    if 'price' in df.columns:
                        st.subheader("Price Analysis")

                        # Display price distribution as histogram
                        fig_price_hist = px.histogram(df, x='price', nbins=30, title='Distribution of Prices',
                                                      labels={'price': 'Price (in USD)', 'count': 'Number of Listings'},
                                                      color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig_price_hist.update_layout(template='plotly_dark')
                        st.plotly_chart(fig_price_hist)

                        # Option for pie chart (if price categories are used)
                        if st.checkbox("Show Pie Chart of Price Ranges"):
                            # Define price ranges
                            price_ranges = {
                                'Low': df[df['price'] < 100].shape[0],
                                'Medium': df[(df['price'] >= 100) & (df['price'] < 250)].shape[0],
                                'High': df[df['price'] >= 250].shape[0]
                            }
                            price_range_df = pd.DataFrame(list(price_ranges.items()), columns=['Price Range', 'Count'])
                            fig_price_pie = px.pie(price_range_df, names='Price Range', values='Count', title='Distribution of Price Ranges')
                            st.plotly_chart(fig_price_pie)

if __name__ == "__main__":
    main()
