import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output,Input,State

import pandas as pd
import os
import numpy as np
from ipywidgets import widgets, interactive_output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tabulate import tabulate
from tqdm import tqdm
from time import time

app = dash.Dash(__name__)
df = pd.read_csv('./2004-2019.tsv',sep = '\t',index_col = 0)
df.columns = ['fecha_inicial', 'fecha_final','region', 'estado', 'producto', 'num_postes_revisados', 'unidad_medida','precio_medio_reventa','desviacion_estandar_reventa','precio_min_reventa','precio_max_reventa','margen_medio_reventa','coef_variacion_reventa','precio_medio_distribucion','desvia_estand_distribucion','precio_min_distribucion','precio_max_distribucion','coef_variacion_distribucion','mes','ano']
df_ano = list(df.ano.unique())
df_mes = list(df.mes.unique())
#opcion_estados = [{'label':id_1,'value':id_2} for id_1,id_2 in zip(df.estado.unique(),df.index)]

encabezado = html.Div([html.H2(['Precios de la gasolina en Brasil']),
						], className = "encabezado")

banner = html.Div([
                html.Img(id='img-fondo',src = "/assets/fondo1.png"),
                html.Img(id='img-gasolina',src = "/assets/gas.png"),
				encabezado,
                html.Img(id='img-udea',src = "/assets/Logo_UdeA.png"),                
                html.Img(id='img-semillero',src = "/assets/failed_logo_semillero.png"),
                html.Div(className='clear')
        ], className = "banner")
row_1 = html.Div([
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.estado.unique()],
                        value = df.estado.unique()[0],
                        id ='estado',
                    ),className='style_estados'),
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.producto.unique()],
                        value = df.producto.unique()[0],
                        id = 'producto',
                    ),className='style_productos'),
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.ano.unique()],
                        value = df.ano.unique()[0],
                        id ='ano',
                    ),className='style_ano'),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura1')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura3')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura2')]),
                html.Div([dcc.Graph(className = 'style_grafica',id = 'figura4')]),      
                html.Div(className='clear')
        ],className = 'style_row_1')
row_2 = html.Div([
                html.Div(dcc.Dropdown(
                        options=[{'label':i,'value':i} for i in df.region.unique()],
                        value = df.region.unique()[0],
                        id = 'region',
                    ),className='style_F'),
                html.Div([dcc.Graph(id = 'figura5')]),
                html.Div(className='clear')
        ],className = 'style_row_2')

container = html.Div([
                    row_1,
                    row_2
            ])

app.layout = html.Div([banner,row_1,row_2],className = "main")

@app.callback([
    Output(component_id ='figura1', component_property ='figure'),
    Output(component_id ='figura2', component_property ='figure'),
    Output(component_id ='figura3', component_property ='figure'),
    Output(component_id ='figura4', component_property ='figure')
    ],

    [
    Input(component_id='estado', component_property='value'),
    Input(component_id='producto',component_property='value'),
    Input(component_id='ano', component_property='value'),
    ])

def grafica(estado,producto,ano):
    traces = [go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_min_reventa'].agg('sum')),name='Min'),
                  go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_medio_reventa'].agg('sum')),name='Medio'),
                  go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_max_reventa'].agg('sum')),name='Max')
                  ]
    traces2 = [go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_min_distribucion'].agg('sum')),name='Min'),
                  go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_medio_distribucion'].agg('sum')),name='Medio'),
                  go.Scatter(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['precio_max_distribucion'].agg('sum')),name='Max')
                  ]
    traces3 = go.Bar(x=df_ano, y=list(df[(df.producto == producto) & (df.estado == estado)].groupby(['ano','estado'])['num_postes_revisados'].agg('sum')),name='Postes revisados')
    traces4 = go.Bar(x=df_mes, y=list(df[(df.producto == producto) & (df.estado == estado) & (df.ano == ano)].groupby(['mes','estado'])['num_postes_revisados'].agg('sum')),name='Postes revisados')

    fig = go.Figure(data = traces)
    fig2 = go.Figure(data = traces2)
    fig3 = go.Figure(data = traces3)
    fig4 = go.Figure(data = traces4)
    
    fig.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Año",
            ticktext=df_ano,
            tickvals=df_ano
        ),
        yaxis=dict(
            title_text="Precio Reventa",
        ),)
    fig.update_traces(opacity=0.7)
    fig2.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Año",
            ticktext=df_ano,
            tickvals=df_ano
        ),
        yaxis=dict(
            title_text="Precio Distribucion",
        ),)
    fig2.update_traces(opacity=0.7)

    fig3.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Año",
            ticktext=df_ano,
            tickvals=df_ano
        ),
        yaxis=dict(
            title_text="# de estaciones revisadas",
        )
    )
    fig3.update_traces(opacity=0.7)
    fig4.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Año " + ano,
            ticktext=["mayo","junio","julio","agosto","septiembre","octubre","noviembre","diciembre","enero","febrero","marzo","abril"],
            tickvals=df_mes
        ),
        yaxis=dict(
            title_text="# de estaciones revisadas",
        )
    )
    fig4.update_traces(opacity=0.7)
    return(fig,fig2,fig3,fig4)

@app.callback(
            # [
                Output(component_id = 'figura5', component_property = 'figure'),
            # ],
            [
                Input(component_id = 'region', component_property = 'value'),
            ])

def grafica2(region):
    df_temp = df[df.region == region]['estado'].unique()
    productos =['ETANOL HIDRATADO','GASOLINA COMUM','GLP','GNV','ÓLEO DIESEL','ÓLEO DIESEL S10']
    data =[go.Bar(name= prod, x=df_temp, y=df[df.producto == prod].groupby(['ano','estado','producto']).precio_medio_reventa.sum()) for prod in productos]
    fig = go.Figure(data = data)
    fig.update_layout(
        margin = {'l':0,'r':0,'t':0,'b':0},
        xaxis=dict(
            title_text="Estados de " + region,
            ticktext=df_temp,
            tickvals=df_temp
        ),
        yaxis=dict(
            title_text="Precio medio de reventa",
        ))
    
    return(fig)

if __name__ == "__main__":
    app.run_server(debug=True)