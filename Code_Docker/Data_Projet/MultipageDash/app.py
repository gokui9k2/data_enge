import dash
from dash import Dash, html, dcc
import pages
import dash
import info

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


#FONCTIONS ET ELASTIC SEARCH











app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Style personnalisé pour améliorer l'apparence
NAV_ITEM_STYLE = {
    "padding": "8px 16px",
    "margin": "5px",
    "background-color": "#000000",  # Fond noir pour les touches
    "color": "white",
    "border-radius": "5px",
    "text-decoration": "none",
}

NAV_STYLE = {
    "padding": "20px",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-top": "20px",
}




# Définition du titre de l'application
app.title = "UFC Analytics: Understand the UFC!"

server = app.server

# Connexion à Elasticsearch
es = Elasticsearch(['http://localhost:9200'])







# Callback pour gérer la recherche
@app.callback(
    Output('search-results', 'children'),
    [Input('search-button', 'n_clicks')],
    [dash.dependencies.State('search-input', 'value')]
)

def update_output(n_clicks, value):
    if value:
        response = es.search(
            index="ufc-index", 
            body={"query": {"match": {"name": value}}},
            _source=["name", "record", "height", "weight", "reach", "Stance"]
        )
        hits = response['hits']['hits']
        
        # Créer un DataFrame à partir des résultats de recherche
        results_df = pd.DataFrame([hit['_source'] for hit in hits])

        # Supprimer les doublons basés sur le champ 'name'
        unique_df = results_df.drop_duplicates(subset=['name'])

        # Convertir les résultats filtrés en un DataFrame pour une manipulation facile
        data = unique_df.to_dict('records')

        # Retourner un DataTable Dash avec les résultats filtrés
        return dash_table.DataTable(
            data=data,
            columns=[
                {"name": "Name", "id": "name"},
                {"name": "Record", "id": "record"},
                {"name": "Height", "id": "height"},
                {"name": "Weight", "id": "weight"},
                {"name": "Reach", "id": "reach"},
                {"name": "Stance", "id": "Stance"},
            ],
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={
                'backgroundColor': 'black',
                'color': 'white',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'padding': '10px'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
            },
        )
    return "Entrez une recherche pour afficher les résultats"



# Définition du layout de l'application avec dash.page_container inclus
app.layout = dbc.Container([
    dbc.Row(
dbc.Col([
    html.H1("UFC Analytics: Understand the UFC!", 
        className="text-center mb-4", 
        style={
            "font-weight": "700",  # Maintient le texte en gras
            "color": "#000000",  # Couleur du texte en noir
            "margin-bottom": "30px",  # Garde un espacement en dessous
            "font-size": "2.5rem",  # Taille de police importante pour l'impact
        }),
], width=12)
),
    dbc.Row(
        dbc.Col(
            html.Div([
                dcc.Link(
                    f"{page['name']} - {page['path']}",
                    href=page["relative_path"],
                    style=NAV_ITEM_STYLE
                ) for page in dash.page_registry.values()
            ], className="d-flex justify-content-center flex-wrap"),
            width=12
        ),
        className="mb-3"
    ),
    dbc.Row(
        dbc.Col([
            
            html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/UFC_Logo.png/800px-UFC_Logo.png?20160112220530',
                     style={"width": '82.5px', 'height': '29.7px', 'margin': 'auto'}),
            html.Img(
    src='https://s.rfi.fr/media/display/c0de7ee2-4fa1-11ee-9464-005056bfb2b6/w:980/p:16x9/AP23253180380469.jpg',
    style={
        "box-shadow": "0 2px 6px 0 rgb(67 89 113 / 20%)",
        "width": "50%",  # Réduisez la largeur à 50% par exemple pour une taille plus petite
        "margin-top": "20px",
        "display": "block",  # Assure que l'image est traitée comme un bloc pour le centrage
        "margin-left": "auto",  # Centre l'image horizontalement
        "margin-right": "auto",
    }
)

            
        ]),
        className="mb-5"
    ),
    
    dbc.Row(
        dbc.Col(html.Div(dash.page_container, style=CONTENT_STYLE), width=12),
    ),
], fluid=True, style={'padding': '20px'})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
