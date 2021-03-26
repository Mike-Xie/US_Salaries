from debug_tools import *

import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import urllib
from urllib.error import HTTPError
app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
try:
    df = pd.read_csv("https://raw.githubusercontent.com/Mike-Xie/US_Salaries/main/salaries.csv")
except(urllib.error.HTTPError):
    # "Do something if fails"
    pass
# df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
dprint(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Salary Adjusted by Purchasing Price Parity", style={'text-align': 'center'}),

    # TODO: make this a search box 
    # (https://www.youtube.com/watch?v=VZ6IdRMc0RI&ab_channel=CharmingData) 
    # not dropdown, if we want dropdown for something else, use this: 
    # https://dash.plotly.com/pattern-matching-callbacks

    # dcc.Dropdown(id="select_job_title",
    #              options=[
    #               #   {"label": "2015", "value": 2015},
    #               #   {"label": "2016", "value": 2016},
    #               #   {"label": "2017", "value": 2017},
    #                  {"label": "Data Science", "value": "Data_Science"}],
    #              multi=False,
    #              value="Data_Science",
    #              style={'width': "40%"}
    #              ),
    html.Div([dcc.Input(
        id="job_title_search",
        type="search",
        placeholder="job title",
        debounce=True,
        style={'text-align':'center'},
        )],
        style={'text-align':'center'}),

    html.H3(id='job_title_label', children=[], style={'text-align': 'center'}),
    html.Br(),

    dcc.Graph(id='plotly_display_element', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id='job_title_label', component_property='children'),
        Output(component_id='plotly_display_element', component_property='figure'),
     ],
    # [Input(component_id='select_job_title', component_property='value'),
    [
        Input(component_id='job_title_search', component_property='value')
    ],
)
def update_graph(search_box_input):
    dprint(search_box_input)
    dprint(type(search_box_input))

    container = "Viewing {} salaries".format(search_box_input) if search_box_input else "Enter a job title!"

    dff = df.copy()
   # dff = dff[dff["Year"] == search_box_input]
   # dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state initial',
        scope="usa",
        color='Adjusted Annual Salary',
        hover_data=['State', 'Adjusted Annual Salary'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Adjusted Annual Salary': 'Annual Salary Adjusted for Purchasing Power'},
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig, 


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
