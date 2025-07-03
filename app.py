from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Baca file CSV dan parse kolom Date
df = pd.read_csv("automobile_sales_dataset.csv", parse_dates=['Date'])

# Filter data saat terjadi resesi
recession_df = df[df["Recession"] == 1]

# Group data penjualan mobil per tahun
yearly_sales = df.groupby("Year")["Automobile_Sales"].sum().reset_index()

# Grafik awal (statik) total penjualan per tahun
fig_yearly = px.line(
    yearly_sales,
    x="Year",
    y="Automobile_Sales",
    title="Total Automobile Sales per Year",
    markers=True
)

# Inisialisasi aplikasi Dash
app = Dash(__name__)

# Layout web dashboard
app.layout = html.Div([
    html.H1("Automotive Sales Report during Recession Periods", style={'textAlign': 'center'}),
    
    html.Label("Select Vehicle Type:"),
    dcc.Dropdown(
        id='vehicle-type-dropdown',
        options=[{'label': vt, 'value': vt} for vt in df['Vehicle_Type'].unique()],
        value='Sports'  # nilai default
    ),

    html.Div(id='output-container'),
    dcc.Graph(id='sales-graph', figure=fig_yearly)  # tampilkan grafik default
])

# Callback interaktif berdasarkan dropdown
@app.callback(
    [Output('output-container', 'children'),
     Output('sales-graph', 'figure')],
    Input('vehicle-type-dropdown', 'value')
)
def update_output(selected_type):
    text = f"You selected vehicle type: {selected_type}"
    filtered = recession_df[recession_df['Vehicle_Type'] == selected_type]

    fig = px.line(
        filtered,
        x='Year',
        y='Automobile_Sales',
        title=f'Sales Trend for {selected_type} During Recession',
        markers=True
    )
    return text, fig

# Jalankan aplikasi
if __name__ == '__main__':
    
