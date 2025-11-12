import streamlit as st
from utils import load_data, plot_boxplot, top_regions

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Solar Data Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# CUSTOM CSS FOR MODERN STYLING
# -----------------------------
st.markdown("""
<style>
    /* Main background color */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #ffffff;
    }
    
    /* Dropdown cursor pointer */
    .stSelectbox > div > div {
        cursor: pointer !important;
    }
    
    /* Card-like containers */
    .dashboard-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    /* Header styling */
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* Metric styling */
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    /* Custom title styling */
    .custom-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .custom-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR: FILTERS
# -----------------------------
def setup_sidebar():
    """Configure and return sidebar filters"""
    with st.sidebar:
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.header("🔍 Filters")
        
        # CSV selection with custom styling
        csv_file = st.selectbox(
            "Select CSV File",
            ["data/benin_raw.csv", "data/togo_dapaong_raw.csv", "data/sierraleone_bumbna_raw.csv"],
            key="csv_select"
        )
        
        # Load data with error handling
        try:
            df = load_data(csv_file)
        except FileNotFoundError:
            st.error(f"File not found: {csv_file}")
            st.stop()
        
        # Numeric columns for KPI
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if not numeric_cols:
            st.error("No numeric columns available for KPI selection.")
            st.stop()
        
        kpi_column = st.selectbox("Select KPI", numeric_cols, key="kpi_select")
        
        # Categorical columns for x-axis (optional)
        categorical_cols = df.select_dtypes(include='object').columns.tolist()
        x_column = None
        if categorical_cols:
            x_column = st.selectbox("Group by (x-axis)", ["None"] + categorical_cols, index=0, key="x_select")
            if x_column == "None":
                x_column = None
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return df, kpi_column, x_column

# -----------------------------
# DASHBOARD HEADER
# -----------------------------
def display_header():
    """Display the dashboard header"""
    st.markdown("""
    <div class="dashboard-header">
        <h1 class="custom-title">☀️ Solar Energy Insights Dashboard</h1>
        <p class="custom-subtitle">Explore solar energy data interactively. Use the sidebar to select KPI and groupings.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# KEY METRICS ROW
# -----------------------------
def display_metrics(df, kpi_column):
    """Display key metrics cards"""
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size:0.9rem; color:#6c757d;">Average</h3>
            <p style="margin:0; font-size:1.5rem; font-weight:bold; color:#333;">{df[kpi_column].mean():.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size:0.9rem; color:#6c757d;">Median</h3>
            <p style="margin:0; font-size:1.5rem; font-weight:bold; color:#333;">{df[kpi_column].median():.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size:0.9rem; color:#6c757d;">Max</h3>
            <p style="margin:0; font-size:1.5rem; font-weight:bold; color:#333;">{df[kpi_column].max():.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin:0; font-size:0.9rem; color:#6c757d;">Min</h3>
            <p style="margin:0; font-size:1.5rem; font-weight:bold; color:#333;">{df[kpi_column].min():.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# MAIN DASHBOARD CONTENT
# -----------------------------
def display_main_content(df, kpi_column, x_column):
    """Display the main dashboard content"""
    # Boxplot section
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(f"📦 {kpi_column} Distribution")
    boxplot_fig = plot_boxplot(df, y_column=kpi_column, x_column=x_column)
    st.plotly_chart(boxplot_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top regions table
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader(f"🏆 Top Regions by {kpi_column}")
    top_df = top_regions(df, column=kpi_column)
    st.dataframe(top_df, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Summary statistics
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.subheader("📋 Summary Statistics")
    st.dataframe(df.describe(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# MAIN APPLICATION
# -----------------------------
def main():
    """Main application function"""
    # Setup sidebar and get filters
    df, kpi_column, x_column = setup_sidebar()
    
    # Display dashboard components
    display_header()
    display_metrics(df, kpi_column)
    display_main_content(df, kpi_column, x_column)

if __name__ == "__main__":
    main()