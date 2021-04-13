from debug_tools import *
import retrieve_data
from engineer_features import engineer_features

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
    html.H1("Salaries by Profession After Tax", style={'text-align': 'center'}),
    html.Div([
        html.Span(
            [dcc.Input(
                id="job_title_search",
                type="search",
                placeholder="job title",
                debounce=True,
                style={'text-align':'center'},
            )],
        ),
        html.Span(style={'padding-left':'10px'}),
        html.Span(
            [dcc.Input(
                id="exemptions",
                type="number",
                placeholder="exemptions (1 by default)",
                debounce=True,
                style={'text-align':'center'},
            )]
        ),
        html.Span(style={'padding-left':'10px'}),
        html.Span(
            [html.Div(
                [dcc.Dropdown(
                    id='marital_status',
                    options=[
                        {'label': 'Single', 'value': 'single'},
                        {'label': 'Married', 'value': 'married'},
                    ],
                    value='single',
                    clearable=False,
                ),],
                style={'width':'200%'}
            )],
        ),
    ], 
    style={'justify-content':'center', 'align-items':'center','display':'flex'},
    ),
    html.H3(id='job_title_label', children=[], style={'text-align': 'center'}),
    html.Br(),
    dcc.Graph(id='plotly_display_element', figure={})
])

def get_ppp_graph():
    salary_table = retrieve_data.get_salary_table_for_job_title('programmer')
    ppp_table = retrieve_data.get_ppp_table()
    tax_table = retrieve_data.get_tax_all_states(salary_table, 'single', 1) # TODO: replace status/exem with selection
    df = engineer_features(salary_table, ppp_table, tax_table) 
    return px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='State Initial',
        scope="usa",
        color='Annual Mean Wage (All Occupations)',
        hover_data=['State Initial', 'Annual Mean Wage (All Occupations)'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Annual Mean Wage (All Occupations)': 'Annual Mean Wage (All Occupations)'},
        template='plotly_dark'
    )

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
    ppp_table = retrieve_data.get_ppp_table()

    search_is_valid = retrieve_data.check_job_search_term(search_box_input) if search_box_input else False
    if search_is_valid:
        container = "Showing {} salaries.".format(search_box_input)
        salary_table = retrieve_data.get_salary_table_for_job_title(search_box_input)
        tax_table = retrieve_data.get_tax_all_states(salary_table, 'single', 1) # TODO: replace status/exem with selection
        df = engineer_features(salary_table, ppp_table, tax_table) 
        valid_entries.append(search_box_input)
    # empty search box, show ppp map:
    elif not search_box_input:
        valid_entries.append(valid_entries[0])
        container = "Showing median for all occupations. Enter a job title for specifics."
        fig = get_ppp_graph()
        return container, fig
    # search box is invalid and most recent working graph wasn't ppp map:
    elif valid_entries[-1] != valid_entries[0]:
        container = "No data for {} salaries, showing median salary for {}.".format(search_box_input, valid_entries[-1])
        salary_table = retrieve_data.get_salary_table_for_job_title(valid_entries[-1])
        tax_table = retrieve_data.get_tax_all_states(salary_table) #, marital_status, exemptions) TODO: implement with these options
        df = engineer_features(salary_table, ppp_table, tax_table)
    # search box is invalid and most recent working graph *was* ppp map:
    else:
        container = "No data for {} salaries, showing median salary for {}.".format(search_box_input, valid_entries[-1])
        fig = get_ppp_graph()
        return container, fig

    fig = px.choropleth(
        data_frame=df,
        locationmode='USA-states',
        locations='State Initial',
        scope="usa",
        color='Post Tax Annual Salary',
        hover_data=['State Initial', 'Annual Salary Rounded', 'Post Tax Annual Salary'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Post Tax Annual Salary': 'Post Tax Annual Salary'},
        template='plotly_dark'
    )
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    valid_entries = ['all occupations']
    app.run_server(debug=True)

