import pandas as pd
import yfinance as yf
import dash
from dash import dcc, html
import plotly.graph_objects as go
from datetime import timedelta
import plotly.express as px
import numpy as np
from dash.dependencies import Input, Output, State

# Initialize the Dash app first
app = dash.Dash(__name__)

# Fetch SPY data using yfinance
def get_spy_data():
    spy = yf.Ticker("SPY")
    # Fetch historical data for the last year
    spy_data = spy.history(period="1y")
    spy_data.reset_index(inplace=True)
    # Convert 'Date' to a datetime object and remove timezone
    spy_data['Date'] = pd.to_datetime(spy_data['Date']).dt.tz_localize(None)
    return spy_data

# Load the CSV data and fetch SPY data
# file_path = 'sample_daily_financial_data.csv'
file_path = '/Users/suseelkumar/Documents/sandbox/Stocks_April_2024/robn/dashboard.csv'
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])

# Fetch SPY data
spy_data = get_spy_data()

# Get the most recent values from the CSV data
latest_data = df.iloc[-1]
recent_market_value = f"${latest_data['market_value']:,}"
recent_net_value = f"${latest_data['net_value']:,}"
recent_total_percentage = f"{latest_data['total_percentage']}%"
recent_profit_percentage = f"{latest_data['profit_percentage']}%"
recent_net_value_numeric = latest_data['net_value']
recent_dividend_all_time = latest_data['dividend_all_time']

# Calculate values for the pie chart
margin_value = recent_net_value_numeric / 2
money_by_value = recent_net_value_numeric - margin_value

# External CSS for modern styling
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'
})
app.css.append_css({
    'external_url': 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap'
})

# First Line Chart Component
line_chart_1 = html.Div([
    # Convert bull.gif to dark mode toggle button
    html.Button(
        html.Img(
            id='dark-mode-icon',
            src='/assets/bull1.gif',
            style={
                'width': '200px',
                'height': '80px',
                'objectFit': 'contain'
            }
        ),
        id='dark-mode-toggle',
        className='toggle-button',
        style={
            'position': 'absolute',
            'top': '5px',
            'right': '800px',
            'width': '100px',
            'height': '120px',
            'borderRadius': '50%',
            'border': 'none',
            'backgroundColor': 'transparent',
            'cursor': 'pointer',
            'padding': '0',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center',
            'zIndex': '1000',
            'boxShadow': 'none'
        }
    ),
    dcc.Dropdown(
        id='date-filter-1',
        options=[
            {'label': '1wk', 'value': '1wk'},
            {'label': '1mo', 'value': '1mo'},
            {'label': '3mo', 'value': '3mo'},
            {'label': '6mo', 'value': '6mo'},
            {'label': '1yr', 'value': '1yr'}
        ],
        value='1wk',
        clearable=False,
        className='dropdown-dark-theme',
        style={'width': '80px'}
    ),
    dcc.Graph(
        id='line-chart-1',
        config={'displayModeBar': False}
    )
], style={
    'padding': '20px',
    'backgroundColor': '#fff',
    'borderRadius': '8px',
    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
    'flex': '1',
    'position': 'relative'
}, className='chart-container')

# Second Line Chart Component
line_chart_2 = html.Div([
    dcc.Dropdown(
        id='date-filter-2',
        options=[
            {'label': '1wk', 'value': '1wk'},
            {'label': '1mo', 'value': '1mo'},
            {'label': '3mo', 'value': '3mo'},
            {'label': '6mo', 'value': '6mo'},
            {'label': '1yr', 'value': '1yr'}
        ],
        value='1wk',
        clearable=False,
        style={'width': '80px'}
    ),
    dcc.Graph(
        id='line-chart-2',
        config={'displayModeBar': False},
        style={'flex': '1', 'minHeight': '0'}
    )
], style={
    'padding': '20px',
    'backgroundColor': '#fff',
    'borderRadius': '8px',
    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
    'flex': '1',
    'display': 'flex',
    'flexDirection': 'column',
    'minHeight': '0' 
    # 'marginBottom': '20px'
}, className='chart-container')
print("test done")
# Create a bar chart showing the last 5 days of data
def create_bar_chart(is_dark_mode):
    # Get the last 5 days of data
    last_five_df = df.tail(5)

    # Define the colors
    colors = ['#40a0fc', '#50e7a6', '#febc4b', '#ff6478', '#8c75d7']

    fig = go.Figure(data=[
        go.Bar(
            x=last_five_df['Date'],
            y=last_five_df['market_value'],
            text=last_five_df['market_value'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside',
            textfont=dict(size=12, color='white' if is_dark_mode else '#000000'),
            cliponaxis=False,
            width=24 * 60 * 60 * 1000 * 0.5,
            marker=dict(
                color=colors[:len(last_five_df)],
                line=dict(
                    color=colors[:len(last_five_df)],
                    width=1.5
                )
            ),
            hovertemplate='Date: %{x}<br>Value: $%{y:,.0f}<extra></extra>'
        )
    ])

    # Set the template based on dark mode
    template = 'plotly_dark' if is_dark_mode else 'plotly_white'

    fig.update_layout(
        title=dict(
            text='Last 5 Days Market Value',
            x=0.48,  # Moves the title to the right (0.5 is center, 1.0 is far right)
            xanchor='center'  # Keeps the title centered around the x position
        ),
        xaxis=dict(
            title=None,
            tickformat='%b %d',
            showgrid=False,
            color='#ffffff' if is_dark_mode else '#000000'
        ),
        yaxis=dict(
            title=None,
            showgrid=False,
            gridcolor='rgba(255,255,255,0.1)',
            color='#ffffff' if is_dark_mode else '#000000'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, r=20, b=20, l=20),
        showlegend=False,
        uniformtext=dict(mode='hide', minsize=8),
        bargap=0.15,
        template=template,
        barcornerradius=10
    )

    return fig

# Create a pie chart for net value breakdown
def create_pie_chart(is_dark_mode):
    fig = go.Figure(
        data=[go.Pie(
            labels=['Margin', 'Money by Values', 'Dividend'],
            values=[margin_value, money_by_value, recent_dividend_all_time],
            hole=0.5,
            textinfo='label+percent',
            hoverinfo='label+value+percent',
            marker=dict(
                colors=['#40a0fc', '#ff6478', '#32cd32'],
                line=dict(color='rgba(0,0,0,0)', width=0)  # Transparent borders
            )
        )]
    )

    # Set the template based on dark mode
    template = 'plotly_dark' if is_dark_mode else 'plotly_white'

    fig.update_layout(
        title=dict(
            text="Net Value Breakdown with Dividend",
            x=0.5,  # Moves the title to the right (0.5 is center, 1.0 is far right)
            xanchor='center'  # Keeps the title centered around the x position
        ),
        showlegend=True,
        legend=dict(orientation="h", x=0.5, y=-0.1, xanchor="center", yanchor="top"),
        margin=dict(t=60, r=20, b=20, l=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template=template
    )
    return fig

# Layout of the Dash app
app.layout = html.Div([
    # Store to keep track of dark mode - add persistence
    dcc.Store(
        id='dark-mode-store',
        data=False,
        storage_type='local'  # Use local storage to persist across refreshes
    ),
    # Container for all content
    html.Div([
        # Container for all charts
        html.Div([
            # Left side with line charts (75% width)
            html.Div([
                line_chart_1,
                line_chart_2
            ], style={
                'width': '75%',
                'display': 'flex',
                'flexDirection': 'column',
                'gap': '10px',
                'padding': '20px',
                'height': '96%'
            }),
            
            # Right side with bar and pie charts (25% width)
            html.Div([
                # Bar chart
                html.Div([
                    dcc.Graph(
                        id='last-five-days-bar',
                        config={'displayModeBar': False}
                    )
                ], style={
                    'backgroundColor': '#fff',
                    'borderRadius': '8px',
                    'padding': '15px',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
                    'marginBottom': '20px',
                    'height': '45vh'
                }, className='chart-container'),
                
                # Pie chart
                html.Div([
                    dcc.Graph(
                        id='donut-pie-chart',
                        config={'displayModeBar': False}
                    ),
                    # Add gif here
                    html.Img(
                        src='/assets/dark4.gif',
                        style={
                            'position': 'absolute',
                            'bottom': '190px',
                            'right': '142px',
                            'width': '200px',
                            'height': '120px',
                            'zIndex': 1000
                        }
                    )
                ], style={
                    'backgroundColor': '#fff',
                    'borderRadius': '8px',
                    'padding': '15px',
                    'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
                    'height': '45vh',
                    'position': 'relative'  # Add this to allow absolute positioning of the gif
                }, className='chart-container')
            ], style={
                'width': '25%',
                'display': 'flex',
                'flexDirection': 'column',
                'padding': '20px',
                'gap': '20px'
            })
        ], style={
            'display': 'flex',
            'height': '100vh',
            'width': '100%',
            'backgroundColor': 'inherit'
        })
    ], id='page-content', style={'backgroundColor': '#fff'})
])

# Callback to toggle dark mode
@app.callback(
    Output('dark-mode-store', 'data'),
    [Input('dark-mode-toggle', 'n_clicks')],
    [State('dark-mode-store', 'data')]
)
def toggle_dark_mode(n_clicks, is_dark_mode):
    if n_clicks is None:
        # Return the stored value on initial load
        return is_dark_mode
    return not is_dark_mode

# Callback to update the page class based on dark mode
@app.callback(
    [Output('page-content', 'className'),
     Output('page-content', 'style')],
    [Input('dark-mode-store', 'data')]
)
def update_page_class(is_dark_mode):
    if is_dark_mode:
        return 'dark-mode', {'backgroundColor': '#000000'}
    return '', {'backgroundColor': '#fff'}

# Callback to update the first line chart
@app.callback(
    Output('line-chart-1', 'figure'),
    [Input('date-filter-1', 'value'),
     Input('dark-mode-store', 'data')]
)
def update_graph_1(selected_range, is_dark_mode):
    end_date = df['Date'].max()
    if selected_range == '1wk':
        start_date = end_date - timedelta(weeks=1)
    elif selected_range == '1mo':
        start_date = end_date - timedelta(days=30)
    elif selected_range == '3mo':
        start_date = end_date - timedelta(days=90)
    elif selected_range == '6mo':
        start_date = end_date - timedelta(days=180)
    elif selected_range == '1yr':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = df['Date'].min()

    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['market_value'],
        mode='lines',
        line=dict(shape='spline', color='#8c75d7'),
        showlegend=False,
        name='Market Value'
    ))
    fig1.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['net_value'],
        mode='lines',
        line=dict(shape='spline', color='#febc4b'),
        showlegend=False,
        name='Net Value'
    ))

    template = "plotly_dark" if is_dark_mode else "plotly_white"
    spike_color = "black" if is_dark_mode else "black"
    spike_dash = "dot" if is_dark_mode else "dot"
    spike_thickness = 0.01 if is_dark_mode else 1  # Thinner line in dark mode
    
    fig1.update_layout(
        template=template,
        title={
            'text': f"Market Value vs Net Value<br>"
                    f"<span style='font-size:16px; color:#8c75d7'>{recent_market_value}</span> | "
                    f"<span style='font-size:16px; color:#febc4b'>{recent_net_value}</span>",
            'x': 0.52,
            'y': 0.99,
            'xanchor': 'center',
            'yanchor': 'top',
            'pad': {'t': 10}
        },
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            title=None,
            tickformat='%b %d',
            range=[start_date, end_date],
            showspikes=True,
            spikecolor=spike_color,
            spikesnap="cursor",
            spikemode="across",
            spikethickness=spike_thickness,  # Dynamic thickness based on mode
            spikedash=spike_dash
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            title=None,
            showspikes=False,
            automargin=True 
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        # margin=dict(t=80, r=20, b=40, l=40)
        margin=dict(t=5, b=40, l=40, r=20)
    )

    return fig1

# Callback to update the second line chart
@app.callback(
    Output('line-chart-2', 'figure'),
    [Input('date-filter-2', 'value'),
     Input('dark-mode-store', 'data')]
)
def update_graph_2(selected_range, is_dark_mode):
    template = "plotly_dark" if is_dark_mode else "plotly_white"
    spike_color = "black"
    spike_dash = "dot"
    spike_thickness = 0.1 if is_dark_mode else 1

    # Use the maximum date available in df as the common end_date
    end_date = df['Date'].max()
    
    # Calculate the start_date based on the selected_range
    if selected_range == '1wk':
        start_date = end_date - timedelta(weeks=1)
    elif selected_range == '1mo':
        start_date = end_date - timedelta(days=30)
    elif selected_range == '3mo':
        start_date = end_date - timedelta(days=90)
    elif selected_range == '6mo':
        start_date = end_date - timedelta(days=180)
    elif selected_range == '1yr':
        start_date = end_date - timedelta(days=365)
    else:
        start_date = df['Date'].min()
    
    # Filter the DataFrames based on the adjusted date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    filtered_spy_data = spy_data[(spy_data['Date'] >= start_date) & (spy_data['Date'] <= end_date)]
    
    # Ensure SPY data does not extend beyond df's max date
    filtered_spy_data = filtered_spy_data[filtered_spy_data['Date'] <= end_date]
    
    # Initialize variables
    title_components = []
    percentage_texts = []
    
    # Create the figure
    fig2 = go.Figure()
    
    # Check and plot total_percentage
    if 'total_percentage' in filtered_df.columns:
        total_percentage_series = filtered_df['total_percentage'].dropna()
        if not total_percentage_series.empty:
            # Adjust the series to start from zero
            total_percentage_change = total_percentage_series - total_percentage_series.iloc[0]
            cumulative_total_percentage_change = total_percentage_change.iloc[-1]
            total_percentage_text = f"{cumulative_total_percentage_change:.2f}%"
            percentage_texts.append(f"<span style='font-size:16px; color:#40a0fc'>Total: {total_percentage_text}</span>")
            fig2.add_trace(go.Scatter(
                x=filtered_df['Date'],
                y=total_percentage_change,
                mode='lines',
                line=dict(shape='spline', color='#40a0fc'),
                name='Total Percentage'
            ))
            title_components.append("Total Percentage")
    
    # Check and plot profit_percentage
    if 'profit_percentage' in filtered_df.columns:
        profit_percentage_series = filtered_df['profit_percentage'].dropna()
        if not profit_percentage_series.empty:
            # Adjust the series to start from zero
            profit_percentage_change = profit_percentage_series - profit_percentage_series.iloc[0]
            cumulative_profit_percentage_change = profit_percentage_change.iloc[-1]
            profit_percentage_text = f"{cumulative_profit_percentage_change:.2f}%"
            percentage_texts.append(f"<span style='font-size:16px; color:#50e7a6'>Profit: {profit_percentage_text}</span>")
            fig2.add_trace(go.Scatter(
                x=filtered_df['Date'],
                y=profit_percentage_change,
                mode='lines',
                line=dict(shape='spline', color='#50e7a6'),
                name='Profit Percentage'
            ))
            title_components.append("Profit Percentage")
    
    # Check and plot SPY Percentage Change
    spy_close_series = filtered_spy_data['Close'].dropna()
    if not spy_close_series.empty:
        # Calculate percentage change over the selected date range
        spy_percentage_change = ((spy_close_series / spy_close_series.iloc[0]) - 1) * 100
        cumulative_spy_percentage_change = spy_percentage_change.iloc[-1]
        spy_percentage_text = f"{cumulative_spy_percentage_change:.2f}%"
        fig2.add_trace(go.Scatter(
            x=filtered_spy_data['Date'],
            y=spy_percentage_change,
            mode='lines',
            line=dict(shape='spline', color='#ff6478'),
            name='SPY Percentage Change'
        ))
        percentage_texts.append(f"<span style='font-size:16px; color:#ff6478'>SPY: {spy_percentage_text}</span>")
        title_components.append("SPY Percentage Change")
    
    # Build the dynamic title
    if title_components:
        title_text = ', '.join(title_components) + "<br>" + ' | '.join(percentage_texts)
    else:
        title_text = "No data available for the selected date range."
    
    # Set the template based on dark mode
    fig2.update_layout(
        template=template,
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            title=None,
            tickformat='%b %d',
            range=[start_date, end_date],
            showspikes=True,
            spikecolor=spike_color,
            spikesnap="cursor",
            spikemode="across",
            spikethickness=spike_thickness,
            spikedash=spike_dash
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=True,
            zeroline=False,
            title=None
        ),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, r=20, b=40, l=40),
        showlegend=False
    )
    
    return fig2
# Callback to update the bar chart
@app.callback(
    Output('last-five-days-bar', 'figure'),
    [Input('dark-mode-store', 'data')]
)
def update_bar_chart(is_dark_mode):
    return create_bar_chart(is_dark_mode)

# Callback to update the pie chart
@app.callback(
    Output('donut-pie-chart', 'figure'),
    [Input('dark-mode-store', 'data')]
)
def update_pie_chart(is_dark_mode):
    return create_pie_chart(is_dark_mode)

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)