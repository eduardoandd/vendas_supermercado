import dash
from dash import html,dcc
from dash.dependencies import Input,Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

app = dash.Dash(
    external_stylesheets=[dbc.themes.CYBORG]
)
server = app.server

#INGESTÃO DE DADOS
df= pd.read_csv('supermarket_sales.csv')


#========= Layout =============
app.layout = html.Div(children=[
    
    dbc.Row([
        
        #MENU LATERAL
            dbc.Col([
                dbc.Card([
                    html.H2('Smart Supermarket:', style={'font-family':'Voltaire','font-size':'30px'}),
                    html.Hr(),
                    
                    html.H5('Cidades:', style={'margin-bottom':'12px'}),
                    dcc.Checklist(df['City'].drop_duplicates(),df['City'].drop_duplicates(),id='check_city',inputStyle={'margin-right':'5px'}),
           
                    html.H5('Variável de análise: ', style={'margin-top':'20px','margin-bottom':'12px'}),
                    dcc.RadioItems(['gross income', 'Rating'],'gross income',id='main-variable',inputStyle={'margin-right':'5px'}),
                    
                
                    
                ], style={'height':'100vh'})
            ], sm=2),
            
      
      #GRÁFICOS
       dbc.Col([
           dbc.Row([
               
               dbc.Col([dcc.Graph(id='city_fig'),]),
               dbc.Col([dcc.Graph(id='gender_fig'),]),
               dbc.Col([dcc.Graph(id='pay_fig'),]),
               
            ]),
           dbc.Row([dcc.Graph(id='income_per_date_fig'),]),
           dbc.Row([dcc.Graph(id='income_per_product_fig'),]),

       ],sm=10)
    ]),
])


#========= Callbacks =============
@app.callback(
    Output('city_fig','figure'),
    Output('pay_fig','figure'),
    Output('gender_fig','figure'),
    Output('income_per_date_fig','figure'),
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
    df_gender = df_filtered.groupby(['Gender','City'])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby('Payment')[main_variable].apply(operation).to_frame().reset_index()
    
    df_product_time= df_filtered.groupby('Date')[main_variable].apply(operation).to_frame().reset_index()
    df_product_income = df_filtered.groupby(['Product line','City'])[main_variable].apply(operation).to_frame().reset_index()
    
    fig_city = px.bar(df_city,x='City',y=main_variable)
    fig_payment = px.bar(df_payment,y='Payment',x=main_variable, orientation='h')
    fig_gender = px.bar(df_gender,y=main_variable,x='Gender', color='City', barmode='group')
    fig_product_income = px.bar(df_product_income,x=main_variable,y='Product line', color='City',orientation='h',barmode='group')
    fig_income_date = px.bar(df_product_time,y=main_variable,x='Date')
    
    for fig in [fig_city,fig_payment,fig_gender,fig_income_date]:
        
        fig.update_layout(margin=dict(l=0,r=0,t=20,b=20), height=200, template='plotly_dark')
        
    fig_product_income.update_layout(margin=dict(l=0,r=0,t=20,b=20), height=500, template='plotly_dark')
        
    
    
    return fig_city,fig_payment,fig_gender,fig_income_date,fig_product_income

    
#========= Run server =============
if __name__ == '__main__':
    app.run_server(port=8083,debug=True)