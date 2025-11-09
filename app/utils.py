import pandas as pd
import plotly.express as px

# -------------------------
# Data Loading
# -------------------------
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file into a Pandas DataFrame.
    
    Parameters:
        file_path (str): Path to the CSV file
        
    Returns:
        pd.DataFrame: Loaded data
    """
    return pd.read_csv(file_path)

# -------------------------
# Visualization
# -------------------------
def plot_boxplot(
    df: pd.DataFrame,
    y_column: str,
    x_column: str = None
) -> px.box:
    """
    Create a boxplot for a numeric column with an optional categorical x-axis.

    Parameters:
        df (pd.DataFrame): Input data.
        y_column (str): Column to visualize (numeric).
        x_column (str, optional): Column for x-axis grouping (categorical).

    Returns:
        plotly.graph_objs._figure.Figure: Boxplot figure.
    """
    if x_column and x_column not in df.columns:
        x_column = None  # fallback if column doesn't exist
    
    fig = px.box(
        df,
        x=x_column,
        y=y_column,
        points="all",
        color=x_column if x_column else None,
        title=f"{y_column} Distribution"
    )

    # Modern styling for the plot
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins, sans-serif"),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True if x_column else False
    )
    
    # Update marker style for better visibility
    fig.update_traces(
        marker=dict(
            size=4,
            opacity=0.6,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        selector=dict(mode='markers')
    )
    
    return fig

# -------------------------
# Data Processing
# -------------------------
def top_regions(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
    """
    Returns top N regions based on a numeric column.
    If 'Region' column doesn't exist, returns top rows sorted by column.

    Parameters:
        df (pd.DataFrame): Input data
        column (str): Column to sort by
        n (int): Number of top regions to return

    Returns:
        pd.DataFrame: Top N regions sorted by the specified column
    """
    if 'Region' in df.columns:
        top_df = (
            df.groupby('Region')[column]
            .mean()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )
    else:
        top_df = df[[column]].sort_values(by=column, ascending=False).head(n).reset_index()
    
    # Rename columns for better display
    top_df.columns = ['Region' if 'Region' in col else 'Index' if 'index' in col else column for col in top_df.columns]
    
    return top_df

def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Get basic summary statistics for the dataset.
    
    Parameters:
        df (pd.DataFrame): Input data
        
    Returns:
        dict: Summary statistics
    """
    return {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'numeric_columns': len(df.select_dtypes(include='number').columns),
        'categorical_columns': len(df.select_dtypes(include='object').columns),
        'missing_values': df.isnull().sum().sum()
    }