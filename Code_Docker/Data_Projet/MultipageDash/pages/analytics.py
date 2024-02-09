import dash
from dash import html, dcc, callback, Input, Output
import info
import dash
from dash import Dash, html, dcc
import pages
import dash

import app
from pymongo import MongoClient
from dash.dependencies import Input, Output
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
import re
import dash_bootstrap_components as dbc
from elasticsearch import Elasticsearch
from plotly.subplots import make_subplots
from dash import dash_table
#from elasticsearch_dsl import Search# 
import elasticsearch





dash.register_page(__name__)


# Préparation des figures Plotly Express
fig_tddef_height = px.scatter(
    info.df, 
    x='height', 
    y='TDDef', 
    labels={'height': 'Taille (cm)', 'TDDef': 'Défense de Takedown'},
    title='TDDef par Taille des Combattants'
)

fig_strike_accuracy_defense = px.scatter(
    info.df, 
    x='StrAcc', 
    y='StrDef',  
    title='Comparaison de la Précision des Frappes et de la Défense contre les Frappes',
    labels={'StrAcc': 'Précision des Frappes (Striking Accuracy)', 'StrDef': 'Défense contre les Frappes (Striking Defense)'},
    size_max=60
)

fig_weight_distribution = px.histogram(
    info.df, 
    x='weight', 
    nbins=20,  
    title='Distribution des Poids des Combattants',
    labels={'weight': 'Poids (lbs)'}
)



layout = html.Div([
    html.H1('UFC en Vrac : Les Combats et Classes dans les grandes lignes', className="text-center"),
    html.Br(),
    html.H2("TDDef par Taille des Combattants", className="text-center"),
    dcc.Graph(
        id='tddef-height-graph',
        figure=fig_tddef_height
    ),
    html.H2("Comparaison de la Précision des Frappes et de la Défense contre les Frappes", className="text-center"),
    dcc.Graph(
        id='strike-accuracy-defense-graph',
        figure=fig_strike_accuracy_defense
    ),
    html.H2("Distribution des Poids des Combattants", className="text-center"),
    dcc.Graph(
        id='weight-distribution-graph',
        figure=fig_weight_distribution
    ),
    
])