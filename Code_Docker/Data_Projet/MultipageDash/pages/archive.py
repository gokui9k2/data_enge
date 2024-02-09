import dash
from dash import html
import plotly.express as px
import info
import dash_core_components as dcc

dash.register_page(__name__)



# Création du graphique avec Plotly Express
fig = px.line(info.df_age_ctrl_time, x='Age', y='CTRL_TIME', title='Evolution du Temps de Contrôle par Âge des Combattants',
              labels={'CTRL_TIME': 'Temps de Contrôle Moyen (secondes)', 'Age': 'Âge des Combattants'})
fig.update_layout(xaxis_title='Âge des Combattants', yaxis_title='Temps de Contrôle Moyen (secondes)', xaxis=dict(tickmode='linear'))

fig2 = px.line(info.df_age_sig_stk_body, x='Age', y='SIG_STK_BODY', title='Evolution des Coups Significatifs au Corps par Âge',
              labels={'SIG_STK_BODY': 'Pourcentage Moyen de Coups Significatifs au Corps', 'Age': 'Âge des Combattants'})
fig2.update_layout(xaxis_title='Âge des Combattants', yaxis_title='Pourcentage Moyen de Coups Significatifs au Corps', xaxis=dict(tickmode='linear'))

fig3 = px.line(info.df_age_sig_pos_ground, x='Age', y='SIG_POS_GROUND', title='Evolution de la Position au Sol Significative par Âge',
              labels={'SIG_POS_GROUND': 'Pourcentage Moyen de Position au Sol Significative', 'Age': 'Âge des Combattants'})
fig.update_layout(xaxis_title='Âge des Combattants', yaxis_title='Pourcentage Moyen de Position au Sol Significative', xaxis=dict(tickmode='linear'))

layout = html.Div(children=[
    html.H1('Analyse Succinte des performances des combattants selon leurs ages.'),
    html.Div('On se concentre sur les temps de controles, les positionnements au sol, et pourcentages de coups significatifs'),
    dcc.Graph(
        id='ctrl-time-by-age',
        figure=fig  # Ici, vous passez votre figure Plotly directement
    ),
    dcc.Graph(figure=fig2),
    
    dcc.Graph(figure=fig3),



])