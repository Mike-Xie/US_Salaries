from debug_tools import *
import scraper
import data_io
import clean_data

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
# try:
#     df = pd.read_csv("https://raw.githubusercontent.com/Mike-Xie/US_Salaries/main/salaries.csv")
# except(urllib.error.HTTPError):
#     pass
# df.reset_index(inplace=True)
# dprint(df[:5])

def get_salary_table_for_job_title(job_title: str):
    salary_data = scraper.get_salary_table_for_job_title(job_title)
    if (type(salary_data) == pd.DataFrame):
        ppp = scraper.get_ppp_table()
        return clean_data.engineer_features(salary_data, ppp)
    else:
        return None

# salary_graph = False

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
        style={'text-align':'center'},
    ),

    html.H3(id='job_title_label', children=[], style={'text-align': 'center'}),
    html.Br(),

    # dcc.Graph(id='plotly_display_element', figure={}) if salary_graph else html.H2("Enter a job title!", style={'text-align': 'center'}),
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

    container = "Showing {} salaries.".format(search_box_input) if search_box_input else "Showing median over all occupations. Enter a job title for specifics."

    df = get_salary_table_for_job_title(search_box_input)

    if (type(df) == pd.DataFrame):
        dprint (df.head())
        # Plotly Express
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
            data_frame=get_salary_table_for_job_title('programmer'),
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
