from debug_tools import *
import retrieve_data

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

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.H1("Salary Adjusted by Purchasing Price Parity", style={'text-align': 'center'}),
    html.Div([dcc.Input(
        id="job_title_search",
        type="search",
        placeholder="job title",
        debounce=True,
        style={'text-align':'center'},
        )],
        style={'text-align':'center'},
    ),
    html.H3(id='job_title_label', children=[], style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id='plotly_display_element', figure={})
])

search_box_input_cache = ""

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [
        Output(component_id='job_title_label', component_property='children'),
        Output(component_id='plotly_display_element', component_property='figure'),
     ],
    [
        Input(component_id='job_title_search', component_property='value')
    ],
)
def update_graph(search_box_input):
    dprint(search_box_input)
    dprint(type(search_box_input))
    df = retrieve_data.get_salary_table_for_job_title(search_box_input)
    container = "Showing {} salaries.".format(search_box_input) if search_box_input else "Showing median over all occupations. Enter a job title for specifics."
    if (search_box_input and type(df) != pd.DataFrame):
        container = "No data for {} salaries, showing median salary over all occupations.".format(search_box_input)
    if (type(df) == pd.DataFrame):
        dprint (df.head())
        fig = px.choropleth(
            data_frame=df,
            locationmode='USA-states',
            locations='State Initial',
            scope="usa",
            color='Adjusted Annual Salary',
            hover_data=['State Initial', 'Adjusted Annual Salary'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Adjusted Annual Salary': 'Annual Salary Adjusted for Purchasing Power'},
            template='plotly_dark'
        )
    else:
        fig = px.choropleth(
            data_frame=retrieve_data.get_salary_table_for_job_title('programmer'),
            locationmode='USA-states',
            locations='State Initial',
            scope="usa",
            color='Annual Mean Wage (All Occupations)',
            hover_data=['State Initial', 'Annual Mean Wage (All Occupations)'],
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Adjusted Annual Salary': 'Annual Salary Adjusted for Purchasing Power'},
            template='plotly_dark'
        )
        

    return container, fig, 

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
