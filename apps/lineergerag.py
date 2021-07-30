import os
import pathlib
import re
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import cufflinks as cf
import dash_bootstrap_components as dbc
external_stylesheets = [dbc.themes.LUX]
import plotly.graph_objs as go

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
app.config.suppress_callback_exceptions = True

#from app import app
data=pd.read_excel("data.xlsx")
list_data=data.ISO.tolist()
'''import geopandas as gpd
df = gpd.read_file('globe.geojson')
list_code=df.sov_a3.tolist()
common_list=set(list_code).intersection(list_data)'''
#import plotly.express as px
#
#data1=data[data.ISO.isin(common_list)]
#df1=df[df.sov_a3.isin(common_list)]
#raw_data=pd.read_excel("svm_forest.xlsx")
#list=['Gross domestic product per capita, current prices, U.S. dollars Units','Population, Persons Millions']
#data=raw_data[raw_data.Indicator.isin(list)]
#data.to_excel("data.xlsx")

code=pd.read_csv("lat.csv")
list_code=code.CODE.tolist()

common_list = set(list_code).intersection(list_data)

data_modified=data[data.ISO.isin(common_list)]
years=data_modified.columns.tolist()[3:]
country_list=data_modified.Country.unique().tolist()
dicto=[{'label':i, 'value':i} for i in country_list]

data_selected=data_modified[data_modified['Country']=='India']
data_selected=data_selected[data_selected['Indicator']=='Population, Persons Millions']
df_3=data_selected.T

data_selected.reset_index(inplace=True)
df_3=data_selected.T
df4=df_3[4:]
x=df4.index.tolist()
y=df4[0].tolist()
df_hist=data_modified.sort_values(by=[2000],ascending=False)
app.layout=dbc.Container([
            dbc.Row(
            [
                dbc.Col(html.H1("Line graph to visualize trend in population and GDP per capita of selected country", className="text-center")
                        , className="mb-5 mt-5")
            ]
            ),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.H5("Select Country")

                ),

                dbc.Col(
                html.Div([
                                        dcc.Dropdown(
                        id='dropdown',
                        options=dicto,
                        value='India',style={
                                'height': '3px',
                                'width': '580px',
                                'font-size': "100%",
                                'min-height': '1px',
                                },
                    ),



                    ])

                )



            ]
            ),
            dbc.Row([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br()
            ]

            ),
            dbc.Row([

                        dbc.Col(
                        dcc.RadioItems(
                        id="radio",
                        options=[
                            {'label': 'Population', 'value': 'Population, Persons Millions'},
                            {'label': 'GDP', 'value': 'Gross domestic product per capita, current prices, U.S. dollars Units'},

                        ],
                        value='Population, Persons Millions',
                        style={
                                'height': '3px',
                                'width': '580px',
                                'font-size': "150%",
                                'min-height': '1px',
                                }

                    )),
                    dbc.Col(
                    html.Button('Button 1', id='btn-nclicks-1', n_clicks=0),
                    )



            ]
            ),
            dbc.Row([
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br()
            ]

            ),
            dbc.Row([

            dcc.Graph(
                id="selected_graph",
                figure=go.Figure(data=go.Scatter(x=x, y=y,mode="lines",
                name="Data",
                line=dict(color="rgb(54, 218, 170)"),
                showlegend=False,))


                    )


            ]
            )









]
)

@app.callback(Output("selected_graph", "figure"),
             [Input('dropdown', 'value'),
             Input('radio', 'value')]
             )
def update_columns(drop,radio):
    data_selected=data_modified[data_modified['Country']==drop]
    data_selected=data_selected[data_selected['Indicator']==radio]
    df_3=data_selected.T
    data_selected.reset_index(inplace=True)
    df_3=data_selected.T
    df4=df_3[4:]
    x=df4.index.tolist()
    y=df4[0].tolist()
    data=go.Scatter(x=x, y=y,mode="lines",name="Data",line=dict(color="rgb(54, 218, 170)"),
    showlegend=False,)
    
    figure=go.Figure(data=go.Scatter(x=x, y=y,mode="lines",
    name="Data",
    line=dict(color="rgb(54, 218, 170)"),
    showlegend=False,))
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
