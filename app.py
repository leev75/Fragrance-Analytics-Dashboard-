import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from collections import Counter

# Page configuration
st.set_page_config(
    page_title="Fragrance Dashboard",
    page_icon="🧴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B9D;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    try:
        # The CSV is semicolon-delimited
        df = pd.read_csv('fra_cleaned.csv', encoding='latin-1', sep=';', on_bad_lines='skip', engine='python')
        
        # Clean column names (remove spaces and convert to proper names)
        df.columns = df.columns.str.strip()
        
        # Convert numeric columns, handling errors gracefully
        numeric_cols = ['Rating Value', 'Rating Count', 'Year']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error("❌ Dataset file 'fra_cleaned.csv' not found.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None

# Load the dataset
df = load_data()

if df is not None:
    # Title
    st.markdown('<div class="main-header">🧴 Fragrance Analytics Dashboard</div>', unsafe_allow_html=True)
    
    # Display basic info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Fragrances", len(df))
    with col2:
        st.metric("Unique Brands", df['Brand'].nunique())
    with col3:
        rating_avg = df['Rating Value'].mean()
        st.metric("Avg Rating", f"{rating_avg:.2f}" if pd.notna(rating_avg) else "N/A")
    with col4:
        st.metric("Countries", df['Country'].nunique())
    
    st.divider()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Get unique values for filters - use consistent casing/stripping
    brands = sorted(df['Brand'].dropna().unique().astype(str))
    countries = sorted(df['Country'].dropna().unique().astype(str))
    genders = sorted(df['Gender'].dropna().unique().astype(str))
    
    # Create default selections
    default_brands = brands[:5] if len(brands) > 5 else brands
    default_countries = countries[:10] if len(countries) > 10 else countries
    default_genders = genders
    
    selected_brands = st.sidebar.multiselect("Select Brands", brands, default=default_brands)
    selected_countries = st.sidebar.multiselect("Select Countries", countries, default=default_countries)
    selected_genders = st.sidebar.multiselect("Select Gender", genders, default=default_genders)
    
    # Ensure we have selections (fallback to defaults)
    if not selected_brands:
        selected_brands = default_brands
    if not selected_countries:
        selected_countries = default_countries
    if not selected_genders:
        selected_genders = default_genders
    
    # Filter data directly on original columns (no need for _clean columns)
    filtered_df = df[
        (df['Brand'].isin(selected_brands)) &
        (df['Country'].isin(selected_countries)) &
        (df['Gender'].isin(selected_genders))
    ]
    
    st.sidebar.metric("Filtered Results", len(filtered_df))
    
    # Debug info
    with st.sidebar.expander("🔍 Debug Info"):
        st.write(f"✅ Total rows loaded: {len(df)}")
        st.write(f"📍 Brands selected: {len(selected_brands)}/{len(brands)}")
        st.write(f"📍 Countries selected: {len(selected_countries)}/{len(countries)}")
        st.write(f"👥 Genders selected: {len(selected_genders)}/{len(genders)}")
        st.write(f"📊 Filtered rows: {len(filtered_df)}")
    
    # If no data after filtering, use all data
    if len(filtered_df) == 0:
        filtered_df = df.copy()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "⭐ Ratings", "🎨 Brands", "🌍 Geographic", "📝 Notes"])
    
    # TAB 1: Overview
    with tab1:
        st.header("Overview Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating distribution
            if len(filtered_df) > 0 and filtered_df['Rating Value'].notna().sum() > 0:
                fig_rating = px.histogram(
                    filtered_df.dropna(subset=['Rating Value']), 
                    x='Rating Value',
                    nbins=30,
                    title='Rating Distribution',
                    color_discrete_sequence=['#FF6B9D']
                )
                st.plotly_chart(fig_rating, use_container_width=True)
            else:
                st.info("No rating data available")
        
        with col2:
            # Gender distribution
            if 'Gender' in filtered_df.columns:
                gender_counts = filtered_df['Gender'].value_counts()
                if len(gender_counts) > 0:
                    fig_gender = px.pie(
                        values=gender_counts.values,
                        names=gender_counts.index,
                        title='Fragrances by Gender',
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    st.plotly_chart(fig_gender, use_container_width=True)
    
    # TAB 2: Ratings Analysis
    with tab2:
        st.header("Ratings Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_rating = filtered_df['Rating Value'].mean()
            st.metric("Avg Rating", f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A")
        with col2:
            med_rating = filtered_df['Rating Value'].median()
            st.metric("Median Rating", f"{med_rating:.2f}" if pd.notna(med_rating) else "N/A")
        with col3:
            std_rating = filtered_df['Rating Value'].std()
            st.metric("Std Dev", f"{std_rating:.2f}" if pd.notna(std_rating) else "N/A")
        
        # Top rated
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 Highest Rated")
            top_rated = filtered_df.nlargest(10, 'Rating Value')[['Perfume', 'Brand', 'Rating Value']]
            st.dataframe(top_rated, use_container_width=True)
        
        with col2:
            st.subheader("Top 10 Most Reviewed")
            most_reviewed = filtered_df.nlargest(10, 'Rating Count')[['Perfume', 'Brand', 'Rating Count']]
            st.dataframe(most_reviewed, use_container_width=True)
    
    # TAB 3: Top Brands
    with tab3:
        st.header("Top Brands Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            brand_counts = filtered_df['Brand'].value_counts().head(15)
            if len(brand_counts) > 0:
                fig_brands = px.bar(
                    x=brand_counts.values,
                    y=brand_counts.index,
                    orientation='h',
                    title='Top 15 Brands',
                    color_discrete_sequence=['#FF6B9D']
                )
                fig_brands.update_layout(height=500)
                st.plotly_chart(fig_brands, use_container_width=True)
        
        with col2:
            brand_ratings = filtered_df.dropna(subset=['Rating Value']).groupby('Brand')['Rating Value'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(15)
            if len(brand_ratings) > 0:
                fig_brand_rating = px.bar(
                    x=brand_ratings['mean'],
                    y=brand_ratings.index,
                    orientation='h',
                    title='Top 15 Brands by Avg Rating',
                    color_discrete_sequence=['#00CC96']
                )
                fig_brand_rating.update_layout(height=500)
                st.plotly_chart(fig_brand_rating, use_container_width=True)
    
    # TAB 4: Geographic Analysis
    with tab4:
        st.header("Geographic Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            country_counts = filtered_df['Country'].value_counts().head(15)
            if len(country_counts) > 0:
                fig_countries = px.bar(
                    x=country_counts.values,
                    y=country_counts.index,
                    orientation='h',
                    title='Top 15 Countries',
                    color_discrete_sequence=['#636EFA']
                )
                fig_countries.update_layout(height=500)
                st.plotly_chart(fig_countries, use_container_width=True)
        
        with col2:
            country_ratings = filtered_df.dropna(subset=['Rating Value']).groupby('Country')['Rating Value'].agg(['mean', 'count']).sort_values('mean', ascending=False).head(15)
            if len(country_ratings) > 0:
                fig_country_rating = px.bar(
                    x=country_ratings['mean'],
                    y=country_ratings.index,
                    orientation='h',
                    title='Top 15 Countries by Avg Rating',
                    color_discrete_sequence=['#AB63FA']
                )
                fig_country_rating.update_layout(height=500)
                st.plotly_chart(fig_country_rating, use_container_width=True)
    
    # TAB 5: Notes Analysis
    with tab5:
        st.header("Fragrance Notes Analysis")
        
        def get_top_notes(col_name, top_n=15):
            """Extract and count notes from column"""
            all_notes = []
            if col_name in filtered_df.columns:
                for notes in filtered_df[col_name].dropna():
                    if isinstance(notes, str) and notes.strip():
                        # Split by space or common delimiters
                        note_list = [n.strip() for n in notes.split() if n.strip()]
                        all_notes.extend(note_list)
            return dict(Counter(all_notes).most_common(top_n))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("Top Notes")
            top_notes = get_top_notes('Top', 15)
            if top_notes:
                fig_top = px.bar(
                    x=list(top_notes.values()),
                    y=list(top_notes.keys()),
                    orientation='h',
                    title='Top Notes',
                    color_discrete_sequence=['#FFA15A']
                )
                fig_top.update_layout(height=500)
                st.plotly_chart(fig_top, use_container_width=True)
        
        with col2:
            st.subheader("Middle Notes")
            middle_notes = get_top_notes('Middle', 15)
            if middle_notes:
                fig_middle = px.bar(
                    x=list(middle_notes.values()),
                    y=list(middle_notes.keys()),
                    orientation='h',
                    title='Middle Notes',
                    color_discrete_sequence=['#00CC96']
                )
                fig_middle.update_layout(height=500)
                st.plotly_chart(fig_middle, use_container_width=True)
        
        with col3:
            st.subheader("Base Notes")
            base_notes = get_top_notes('Base', 15)
            if base_notes:
                fig_base = px.bar(
                    x=list(base_notes.values()),
                    y=list(base_notes.keys()),
                    orientation='h',
                    title='Base Notes',
                    color_discrete_sequence=['#636EFA']
                )
                fig_base.update_layout(height=500)
                st.plotly_chart(fig_base, use_container_width=True)
    
    # Footer
    st.divider()

else:
    st.error("❌ Unable to load the dashboard. Ensure 'fra_cleaned.csv' is in the project directory.")
