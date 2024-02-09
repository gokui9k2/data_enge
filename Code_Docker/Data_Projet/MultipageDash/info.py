
import dash
from dash import Dash, html, dcc
import pages
import dash
import info
import numpy as np
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



# Connexion à MongoDB

def usecase(data ,fit_json):
    if len(data) == 0:
        df = pd.read_json(fit_json)
    else:
        df= pd.DataFrame(data)
    return df 

client = MongoClient("mongodb://mongodb:27017/")


db = client.ufc_database
collection = db.ufc_fighters

collection_fights = db.ufc_fight

data2 = list(collection_fights.find({}, { 'Date' : 1,'R_CTRL_TIME': 1 ,'B_CTRL_TIME' : 1, 'R_figther': 1 ,'B_figther' : 1 ,'R_SIG_STK_BODY' : 1 ,'B_SIG_STK_BODY':1 ,'R_SIG_POS_GROUND': 1 ,'B_SIG_POS_GROUND' : 1 , '_id': 0}))
df2 = pd.DataFrame(data2)


data = list(collection.find({}, {'height': 1, 'TDDef': 1,'Stance': 1, 'record': 1,'reach':1 ,'StrAcc': 1 , 'StrDef':1 , 'weight' : 1, 'name' : 1, 'DateOfB' : 1 ,'_id': 0}))
df = pd.DataFrame(data)

df = df.drop_duplicates(subset=['name'])

df['Stance'] = df['Stance'].apply(lambda x: np.nan if x == {'$numberDouble': 'NaN'} else x)

df['DateOfB'] = pd.to_datetime(df['DateOfB'], errors='coerce', format='%b %d, %Y')

my_dict = dict(zip(df['name'], df['DateOfB']))
df2["Date_of_R"] = df2['R_figther']
df2["Date_of_B"] = df2['B_figther']
df2["Date_of_R"].replace(my_dict, inplace=True)
df2["Date_of_B"].replace(my_dict, inplace=True)
df2["Date_of_B"] = pd.to_datetime(df2["Date_of_B"], errors='coerce')
df2["Date_of_R"] = pd.to_datetime(df2["Date_of_R"], errors='coerce')

#df2['Date'] = df2['Date'].apply(lambda x: x['$date'])
#df2['Date'] = pd.to_datetime(df2['Date']).dt.strftime('%Y-%m-%d %H:%M:%S')

df2["Date"] = pd.to_datetime(df2["Date"])
df2["Age_of_B"] = ((df2["Date"] - df2["Date_of_B"]).dt.days / 365.25).abs()
df2["Age_of_R"] = ((df2["Date"] - df2["Date_of_R"]).dt.days / 365.25).abs()
df2["Age_of_B"] = np.floor(df2["Age_of_B"].abs())
df2["Age_of_R"] = np.floor(df2["Age_of_R"].abs())


# Combinez les données des combattants rouges et bleus

df_combined = pd.concat([
    df2[['R_figther', 'Age_of_R', 'R_CTRL_TIME']].rename(columns={'R_figther': 'Fighter', 'Age_of_R': 'Age', 'R_CTRL_TIME': 'CTRL_TIME'}),
    df2[['B_figther', 'Age_of_B', 'B_CTRL_TIME']].rename(columns={'B_figther': 'Fighter', 'Age_of_B': 'Age', 'B_CTRL_TIME': 'CTRL_TIME'})
])

# Assurez-vous que l'âge et le temps de contrôle sont numériques

df_combined['Age'] = pd.to_numeric(df_combined['Age'], errors='coerce')
df_combined['CTRL_TIME'] = pd.to_numeric(df_combined['CTRL_TIME'], errors='coerce')

# Vous pourriez vouloir regrouper par âge pour voir l'évolution du temps de contrôle moyen par âge
df_age_ctrl_time = df_combined.groupby('Age').agg({'CTRL_TIME': 'mean'}).reset_index()



# Combinez les données pour les combattants rouges et bleus
df_combined_stk_body = pd.concat([
    df2[['R_figther', 'Age_of_R', 'R_SIG_STK_BODY']].rename(columns={'R_figther': 'Fighter', 'Age_of_R': 'Age', 'R_SIG_STK_BODY': 'SIG_STK_BODY'}),
    df2[['B_figther', 'Age_of_B', 'B_SIG_STK_BODY']].rename(columns={'B_figther': 'Fighter', 'Age_of_B': 'Age', 'B_SIG_STK_BODY': 'SIG_STK_BODY'})
])

# Calculer la moyenne de SIG_STK_BODY par âge
df_age_sig_stk_body = df_combined_stk_body.groupby('Age').agg({'SIG_STK_BODY': 'mean'}).reset_index()




# Combinez les données pour les positions au sol significatives des combattants rouges et bleus
df_combined_sig_pos_ground = pd.concat([
    df2[['R_figther', 'Age_of_R', 'R_SIG_POS_GROUND']].rename(columns={'R_figther': 'Fighter', 'Age_of_R': 'Age', 'R_SIG_POS_GROUND': 'SIG_POS_GROUND'}),
    df2[['B_figther', 'Age_of_B', 'B_SIG_POS_GROUND']].rename(columns={'B_figther': 'Fighter', 'Age_of_B': 'Age', 'B_SIG_POS_GROUND': 'SIG_POS_GROUND'})
])

# Calculer la moyenne de SIG_POS_GROUND par âge
df_age_sig_pos_ground = df_combined_sig_pos_ground.groupby('Age').agg({'SIG_POS_GROUND': 'mean'}).reset_index()




