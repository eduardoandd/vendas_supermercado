import dash
from dash import html,dcc
from dash.dependencies import Input,Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__)
server = app.server

#INGESTÃO DE DADOS
df= pd.read_csv('supermarket_sales.csv')


#========= Layout =============
app.layout = html.Div(children=[
    html.H5('Cidades:'),
    dcc.Checklist(df['City'].drop_duplicates(),df['City'].drop_duplicates(),id='check_city'),
    
    html.H5('Variável de análise: '),
    dcc.RadioItems(['gross income', 'Rating'],'gross income',id='main-variable'),
    
    dcc.Graph(id='city_fig'),
    dcc.Graph(id='pay_fig'),
    dcc.Graph(id='income_per_product_fig'),
    
])


#========= Callbacks =============
@app.callback(
    Output('city_fig','figure'),
    Output('pay_fig','figure'),
    Output('income_per_product_fig','figure'),
    Input('check_city', 'value'),
    Input('main-variable', 'value')
)

def render_graphs(cities, main_variable):
    
    # cities = ['Yangon','Mandalay']
    # main_variable='gross income'
    
    operation = np.sum if main_variable == 'gross income' else np.mean
    
    df_filtered = df[df['City'].isin(cities)]
    
    df_city = df_filtered.groupby('City')[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()
    
    fig_city = px.bar(df_city,x='City',y=main_variable)
    fig_payment = px.bar(df_payment,y='Payment',x=main_variable, orientation='h')
    fig_product_income = px.bar(df_product_income,x=main_variable,y='Product line', color='City',orientation='h',barmode='group')
    
    
    return fig_city,fig_payment,fig_product_income

    

#========= Run server =============
if __name__ == '__main__':
    app.run_server(port=8080,debug=True)