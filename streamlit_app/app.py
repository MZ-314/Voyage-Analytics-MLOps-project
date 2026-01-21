import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Voyage Analytics",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 3rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565C0;
    }
</style>
""", unsafe_allow_html=True)

# API endpoints
API_URL = "http://localhost/predict"  # Kubernetes service
DOCKER_API_URL = "http://localhost:5000/predict"  # Docker fallback

# Header
st.markdown('<div class="main-header">✈️ Voyage Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">ML-Powered Travel Intelligence Platform</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")
    page = st.radio(
        "Select Feature",
        ["Flight Price Prediction", "Model Performance", "About"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    
    # Check API status
    try:
        response = requests.get("http://localhost/", timeout=2)
        if response.status_code == 200:
            st.success("✅ API: Online")
            api_status = True
            api_url = API_URL
        else:
            raise Exception("K8s API not responding")
    except:
        try:
            response = requests.get("http://localhost:5000/", timeout=2)
            if response.status_code == 200:
                st.warning("⚠️ Using Docker API")
                api_status = True
                api_url = DOCKER_API_URL
            else:
                raise Exception("Docker API not responding")
        except:
            st.error("❌ API: Offline")
            api_status = False
            api_url = None
    
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Models", "3")
    with col2:
        st.metric("Accuracy", "99.9%")

# Page: Flight Price Prediction
if page == "Flight Price Prediction":
    st.header("✈️ Flight Price Prediction")
    
    if not api_status:
        st.error("⚠️ API is not available. Please start the API service.")
        st.stop()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎫 Flight Details")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            flight_type = st.selectbox(
                "Flight Class",
                ["firstClass", "premium", "economic"]
            )
            
            agency = st.selectbox(
                "Agency",
                ["FlyingDrops", "CloudFy", "Rainbow"]
            )
            
            from_location = st.selectbox(
                "From",
                ["Recife (PE)", "Sao Paulo (SP)", "Rio de Janeiro (RJ)", 
                 "Belo Horizonte (MG)", "Salvador (BA)", "Brasilia (DF)",
                 "Curitiba (PR)", "Porto Alegre (RS)", "Florianopolis (SC)"]
            )
        
        with col_b:
            to_location = st.selectbox(
                "To",
                ["Florianopolis (SC)", "Sao Paulo (SP)", "Rio de Janeiro (RJ)",
                 "Belo Horizonte (MG)", "Salvador (BA)", "Brasilia (DF)",
                 "Curitiba (PR)", "Porto Alegre (RS)", "Recife (PE)"]
            )
            
            distance = st.number_input(
                "Distance (km)",
                min_value=100.0,
                max_value=5000.0,
                value=676.53,
                step=10.0
            )
            
            time = st.number_input(
                "Flight Time (hours)",
                min_value=0.5,
                max_value=10.0,
                value=1.76,
                step=0.1
            )
        
        st.subheader("📅 Date Information")
        
        col_c, col_d, col_e = st.columns(3)
        
        with col_c:
            month = st.selectbox(
                "Month",
                list(range(1, 13)),
                index=8,
                format_func=lambda x: datetime(2024, x, 1).strftime("%B")
            )
        
        with col_d:
            dayofweek = st.selectbox(
                "Day of Week",
                list(range(7)),
                index=3,
                format_func=lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][x]
            )
        
        with col_e:
            quarter = st.selectbox(
                "Quarter",
                [1, 2, 3, 4],
                index=2
            )
        
        st.markdown("---")
        
        predict_button = st.button("🚀 Predict Flight Price", use_container_width=True)
    
    with col2:
        st.subheader("📊 Prediction Result")
        
        if predict_button:
            input_data = {
                "flightType": flight_type,
                "time": float(time),
                "distance": float(distance),
                "agency": agency,
                "from": from_location,
                "to": to_location,
                "month": int(month),
                "dayofweek": int(dayofweek),
                "quarter": int(quarter)
            }
            
            with st.spinner("Predicting..."):
                try:
                    response = requests.post(api_url, json=input_data, timeout=5)
                    
                    if response.status_code == 200:
                        result = response.json()
                        predicted_price = result['predicted_price']
                        
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 30px; border-radius: 15px; text-align: center; color: white;">
                            <h2 style="margin: 0; font-size: 1.2rem;">Predicted Price</h2>
                            <h1 style="margin: 10px 0; font-size: 3rem; font-weight: bold;">
                                ${predicted_price:,.2f}
                            </h1>
                            <p style="margin: 0; opacity: 0.9;">Brazilian Real (BRL)</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.success("✅ Prediction successful!")
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Page: Model Performance
elif page == "Model Performance":
    st.header("📊 Model Performance Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>MAE</h3>
            <h1>$0.00</h1>
            <p>Mean Absolute Error</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>RMSE</h3>
            <h1>$0.03</h1>
            <p>Root Mean Squared Error</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>R² Score</h3>
            <h1>1.0000</h1>
            <p>Perfect Prediction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Samples</h3>
            <h1>271,888</h1>
            <p>Training Records</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("🎯 Feature Importance")
    
    feature_importance = pd.DataFrame({
        'Feature': ['flightType', 'time', 'distance', 'agency', 'from', 'to', 'dayofweek', 'month', 'quarter'],
        'Importance': [37.4, 24.9, 20.7, 9.8, 3.9, 2.1, 0.8, 0.3, 0.1]
    })
    
    fig = px.bar(
        feature_importance,
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance in Flight Price Prediction',
        color='Importance',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Page: About
else:
    st.header("ℹ️ About Voyage Analytics")
    
    st.markdown("""
    ## 🚀 Project Overview
    
    **Voyage Analytics** is an end-to-end MLOps project demonstrating the complete lifecycle of 
    deploying machine learning models for the travel industry.
    
    ### 📊 Models
    
    1. **Flight Price Prediction** (Regression)
       - R² = 1.0000, MAE = $0.00
    
    2. **Gender Classification** (Classification)
       - Accuracy: 35.45%
    
    3. **Hotel Recommendation** (Collaborative Filtering)
       - User-based and item-based filtering
    
    ### 🛠️ Technology Stack
    
    - **ML:** scikit-learn, pandas, numpy
    - **API:** Flask, Docker, Kubernetes
    - **Dashboard:** Streamlit, Plotly
    - **Tracking:** MLflow
    """)