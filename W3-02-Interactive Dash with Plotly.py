# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Read the SpaceX data into pandas dataframe
spacex_df =  pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# App layout & graph components
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                            style={'textAlign': 'center',
                                            'color': '#503D36',
                                            'font-size': 40}),
                                
                                # TASK 1: Add a Launch Site Drop-down Input Component
                                 dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a launch site here",
                                            searchable=True
                                            ),
                                html.Br(),
                                
                                #TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
                                html.Div(dcc.Graph(id='success-pie-chart')),  
                                html.Br(),

                                #TASK 3: Add a Range Slider to Select Payload
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                        min=0,
                                        max=10000,
                                        step=1000,
                                        value=[min_payload, max_payload]),
                                html.Br(),

                                #TASK 4: Add scatter plot
                                dcc.Graph(id="success-payload-scatter-chart"),
                                html.P("Correlation between payload and success for all sites:"),




                                               
                    ])

# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == "ALL":
        fig = px.pie(filtered_df, values="class", 
        names="Launch Site", 
        title="Success count for all launch sites")
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        filtered_df = filtered_df.groupby(["Launch Site", "class"]).size().reset_index(name="class count")
        # create a pie chart for the selected launch site
        fig = px.pie(filtered_df, values="class count", names='class', title="Total success launches for site")
        return fig

# TASK 4: Add a callback function to render the scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value"))

def scatter(entered_site, payload):
        filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(payload[0],payload[1])]
        if entered_site=="ALL":
            fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title="Success count on payload mass for all sites")
            return fig
        else:
            fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],x='Payload Mass (kg)',y='class',color='Booster Version Category',title="Success count on payload mass for selected site")
            return fig

# Run the application                   
if __name__ == '__main__':
    app.run_server()