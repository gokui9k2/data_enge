import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
import app
import plotly.express as px

dash.register_page(__name__, path='/')





layout = dbc.Container([
    html.H1('Find The Record of your favorite Fighter with Elastic-Search', className='text-center mb-4'),
    html.Div('For example: enter Jon Jones', className='text-center mb-4'),
    dbc.Row([
        dbc.Col(dcc.Input(id='search-input', type='text', placeholder='Recherche...', 
                          className="form-control form-control-lg mb-2", style={"maxWidth": "100%"}), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Button('Recherche', id='search-button', 
                            className="btn btn-dark btn-lg mb-2", style={"width": "100%"}), width=12)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='search-results'), width=12)
    ], justify="center"),
], fluid=True, style={"maxWidth": "600px", "margin": "auto"})




