from preswald import text, plotly, connect, get_df, table, slider, dropdown, sidebar
import pandas as pd
import plotly.express as px

# Minimal component to ensure something renders
text("# Walmart Sales Explorer")
print("Text component added")

# Add sidebar
try:
    sidebar()
    print("Sidebar added")
except Exception as e:
    print(f"Sidebar error: {e}")

# Load the CSV
try:
    connect()
    df = get_df('Walmart_Sales')
    print("Dataset loaded successfully")
    print("Columns:", df.columns.tolist())
    print("First row:", df.head(1).to_dict())
except Exception as e:
    print(f"Error loading dataset: {e}")
    text("Error: Could not load Walmart_Sales.csv")
    df = None

# Proceed only if dataset loaded
if df is not None:
    # Query the data
    try:
        from preswald import query
        sql = "SELECT Store, Date, Weekly_Sales, Holiday_Flag, Temperature FROM Walmart_Sales WHERE Weekly_Sales > 1000000"
        filtered_df = query(sql, 'Walmart_Sales')
        table(filtered_df, title="High Sales (> $1M)")
        print("Query and table (High Sales) added")
    except Exception as e:
        print(f"Query error: {e}")
        text("Error: Could not query data")

    # Slider for Weekly_Sales
    try:
        threshold = slider("Sales Threshold ($)", min_val=0, max_val=2000000, default=1000000)
        dynamic_df = df[df['Weekly_Sales'] > threshold]
        table(dynamic_df, title="Dynamic Sales View")
        print("Slider and dynamic table added")
    except Exception as e:
        print(f"Slider error: {e}")
        text("Error: Could not render slider")

    # Dropdown for Holiday_Flag
    try:
        holiday_options = ['All', 'Non-Holiday (0)', 'Holiday (1)']
        holiday = dropdown("Holiday Filter", options=holiday_options)
        if holiday == 'Non-Holiday (0)':
            filtered_by_holiday = df[df['Holiday_Flag'] == 0]
        elif holiday == 'Holiday (1)':
            filtered_by_holiday = df[df['Holiday_Flag'] == 1]
        else:
            filtered_by_holiday = df
        table(filtered_by_holiday, title="Holiday Filtered Sales")
        print("Dropdown and holiday table added")
    except Exception as e:
        print(f"Dropdown error: {e}")
        text("Error: Could not render dropdown")

    # Scatter plot
    try:
        fig = px.scatter(df, x='Temperature', y='Weekly_Sales', text='Store',
                         title='Weekly Sales vs. Temperature',
                         labels={'Temperature': 'Temperature (°F)', 'Weekly_Sales': 'Weekly Sales ($)'},
                         color='Holiday_Flag')
        fig.update_traces(textposition='top center', marker=dict(size=12))
        fig.update_layout(template='plotly_white')
        plotly(fig)
        print("Scatter plot added")
    except Exception as e:
        print(f"Scatter plot error: {e}")
        text("Error: Could not render scatter plot")

    # Histogram
    try:
        fig2 = px.histogram(df, x='Weekly_Sales', title='Weekly Sales Distribution',
                            labels={'Weekly_Sales': 'Weekly Sales ($)'})
        fig2.update_layout(template='plotly_white')
        plotly(fig2)
        print("Histogram added")
    except Exception as e:
        print(f"Histogram error: {e}")
        text("Error: Could not render histogram")

    # Full dataset table
    try:
        table(df, title="All Sales Data")
        print("Full dataset table added")
    except Exception as e:
        print(f"Table error: {e}")
        text("Error: Could not render full table")
else:
    text("Please check dataset configuration and try again")
    