import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px

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

def main():
    st.set_page_config(page_title="Airbnb Data Analysis", layout="wide")
    
    # Custom CSS
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
    
    # Replace with your MongoDB connection string and collection details
    connection_string = "mongodb+srv://bharathwajravi:FxcugqUZncJSZU4u@cluster0.yid1esl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db_name = 'Airbub_Analysis'
    collection_name = 'CLEANED_AIRBUB'

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

                # Dropdown menu for chart selection
                chart_options = []
                if 'price' in df.columns:
                    chart_options.append('Price Distribution')
                if 'availability_30' in df.columns:
                    chart_options.append('Availability in Next 30 Days')
                if 'latitude' in df.columns and 'longitude' in df.columns:
                    chart_options.append('Price Distribution by Location')
                if 'number_of_reviews' in df.columns:
                    chart_options.append('Number of Reviews Distribution')
                if 'accommodates' in df.columns:
                    chart_options.append('Accommodation Capacity')
                if 'bathrooms' in df.columns:
                    chart_options.append('Number of Bathrooms')
                if 'bedrooms' in df.columns:
                    chart_options.append('Number of Bedrooms')
                if 'beds' in df.columns:
                    chart_options.append('Number of Beds')
                if 'cleaning_fee' in df.columns:
                    chart_options.append('Cleaning Fee Distribution')
                if 'security_deposit' in df.columns:
                    chart_options.append('Security Deposit Distribution')
                if 'weekly_price' in df.columns:
                    chart_options.append('Weekly Price Distribution')
                if 'monthly_price' in df.columns:
                    chart_options.append('Monthly Price Distribution')

                selected_charts = st.multiselect('Select Charts to Display', options=chart_options)

                # Display selected charts
                for chart in selected_charts:
                    if chart == 'Price Distribution':
                        st.subheader("Price Distribution")
                        fig1 = px.histogram(df, x='price', nbins=50, title='Distribution of Listing Prices',
                                            labels={'price': 'Price (USD)', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig1.update_layout(template='plotly_dark')
                        st.plotly_chart(fig1)

                    if chart == 'Availability in Next 30 Days':
                        st.subheader("Availability in Next 30 Days")
                        fig2 = px.histogram(df, x='availability_30', nbins=30, title='Availability of Listings in the Next 30 Days',
                                            labels={'availability_30': 'Days Available', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig2.update_layout(template='plotly_dark')
                        st.plotly_chart(fig2)

                    if chart == 'Price Distribution by Location':
                        st.subheader("Price Distribution by Location")
                        fig3 = px.scatter_mapbox(df, lat='latitude', lon='longitude', color='price',
                                                 size='price', color_continuous_scale=px.colors.cyclical.IceFire,
                                                 size_max=15, zoom=10, mapbox_style="carto-positron",
                                                 title='Geographic Distribution of Listings by Price',
                                                 labels={'price': 'Price (USD)'})
                        fig3.update_layout(template='plotly_dark', margin=dict(r=0, t=0, l=0, b=0))
                        st.plotly_chart(fig3, use_container_width=True)

                    if chart == 'Number of Reviews Distribution':
                        st.subheader("Number of Reviews Distribution")
                        fig4 = px.histogram(df, x='number_of_reviews', nbins=50, title='Distribution of Number of Reviews',
                                            labels={'number_of_reviews': 'Number of Reviews', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig4.update_layout(template='plotly_dark')
                        st.plotly_chart(fig4)

                    if chart == 'Accommodation Capacity':
                        st.subheader("Accommodation Capacity")
                        fig5 = px.histogram(df, x='accommodates', nbins=15, title='Distribution of Accommodation Capacity',
                                            labels={'accommodates': 'Number of Guests Accommodated', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig5.update_layout(template='plotly_dark')
                        st.plotly_chart(fig5)

                    if chart == 'Number of Bathrooms':
                        st.subheader("Number of Bathrooms")
                        fig6 = px.histogram(df, x='bathrooms', nbins=15, title='Distribution of Number of Bathrooms',
                                            labels={'bathrooms': 'Number of Bathrooms', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig6.update_layout(template='plotly_dark')
                        st.plotly_chart(fig6)

                    if chart == 'Number of Bedrooms':
                        st.subheader("Number of Bedrooms")
                        fig7 = px.histogram(df, x='bedrooms', nbins=15, title='Distribution of Number of Bedrooms',
                                            labels={'bedrooms': 'Number of Bedrooms', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig7.update_layout(template='plotly_dark')
                        st.plotly_chart(fig7)

                    if chart == 'Number of Beds':
                        st.subheader("Number of Beds")
                        fig8 = px.histogram(df, x='beds', nbins=15, title='Distribution of Number of Beds',
                                            labels={'beds': 'Number of Beds', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig8.update_layout(template='plotly_dark')
                        st.plotly_chart(fig8)

                    if chart == 'Cleaning Fee Distribution':
                        st.subheader("Cleaning Fee Distribution")
                        fig9 = px.histogram(df, x='cleaning_fee', nbins=50, title='Distribution of Cleaning Fees',
                                            labels={'cleaning_fee': 'Cleaning Fee (USD)', 'count': 'Number of Listings'},
                                            color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig9.update_layout(template='plotly_dark')
                        st.plotly_chart(fig9)

                    if chart == 'Security Deposit Distribution':
                        st.subheader("Security Deposit Distribution")
                        fig10 = px.histogram(df, x='security_deposit', nbins=50, title='Distribution of Security Deposits',
                                             labels={'security_deposit': 'Security Deposit (USD)', 'count': 'Number of Listings'},
                                             color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig10.update_layout(template='plotly_dark')
                        st.plotly_chart(fig10)

                    if chart == 'Weekly Price Distribution':
                        st.subheader("Weekly Price Distribution")
                        fig11 = px.histogram(df, x='weekly_price', nbins=50, title='Distribution of Weekly Prices',
                                             labels={'weekly_price': 'Weekly Price (USD)', 'count': 'Number of Listings'},
                                             color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig11.update_layout(template='plotly_dark')
                        st.plotly_chart(fig11)

                    if chart == 'Monthly Price Distribution':
                        st.subheader("Monthly Price Distribution")
                        fig12 = px.histogram(df, x='monthly_price', nbins=50, title='Distribution of Monthly Prices',
                                             labels={'monthly_price': 'Monthly Price (USD)', 'count': 'Number of Listings'},
                                             color_discrete_sequence=px.colors.qualitative.Pastel)
                        fig12.update_layout(template='plotly_dark')
                        st.plotly_chart(fig12)

if __name__ == "__main__":
    main()
