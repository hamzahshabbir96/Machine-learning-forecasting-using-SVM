# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 14:42:30 2021

@author: Hamzah
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 22:21:19 2021

@author: Hamzah
"""
import os
import pathlib
import re
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
#import cufflinks as cf

from app import app

# Initialize app



data=pd.read_excel("data.xlsx")
list_data=data.ISO.tolist()
'''import geopandas as gpd
df = gpd.read_file('globe.geojson')
list_code=df.sov_a3.tolist()
common_list=set(list_code).intersection(list_data)'''
import plotly.express as px

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
df_hist=data_modified.sort_values(by=[2000],ascending=False)
BINS = [
    "0-2",
    "2.1-4",
    "4.1-6",
    "6.1-8",
    "8.1-10",
    "10.1-12",
    "12.1-14",
    "14.1-16",
    "16.1-18",
    "18.1-20",
    "20.1-22",
    "22.1-24",
    "24.1-26",
    "26.1-28",
    "28.1-30",
    ">30",
]
DEFAULT_COLORSCALE=['#ff6a6a',
'#e55f5f',
'#cc5454',
'#b24a4a',
'#993f3f',
'#7f3535',
'#662a2a',
'#4c1f1f',
'#331515',
'#190a0a',
'#000000',
]

DEFAULT_OPACITY = 0.8

df1=data_modified[data_modified['Indicator']=='Population, Persons Millions']
df_hist=df1.sort_values(by=[2000])
#df_hist.sort_values(by=['col1'])
import dash_core_components as dcc
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}
mark_year=[1981,1984,1986,1988,1990,1992,1994,1996,1998,2000,2002,2004,2006,2008,2010,2012,2014,2016,2018,2020,2022,2024,2026]

layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.A([
                    html.Img(src="/assets/github.png", height="30px")],href="https://github.com/hamzahshabbir96",

                ),
                html.A([
                    html.Img(src="/assets/linkedin.png", height="30px")],href="https://www.linkedin.com/in/hamzah-shabbir-108765a5/",

                ),
                html.A([
                    html.Img(src="/assets/stack.png", height="30px")],href="https://stackoverflow.com/users/16555815/hamzah-shabbir",

                ),
                html.A(
                    html.Button("Similar projects", className="link-button"),
                    href="https://github.com/hamzahshabbir96/",
                ),
                html.A(
                    html.Button("Source Code", className="link-button"),
                    href="https://github.com/hamzahshabbir96/Machine-learning-forecasting-using-SVM",
                ),


                html.H1(children="Welcome to Global forecasted database of population and GDP",className="mb-5 mt-5"),
                html.P(
                    id="description",
                    children="In this project Support vector machine method has been used to forecast GDP and Population of countries. Changing the slider will adjust the year and data (population or GDP) can be selected from dropdown menu below. ",
                ),
            ],
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="slider-container",
                            children=[
                                html.P(
                                    id="slider-text",
                                    children="Drag the slider to change the year:",
                                ),
                                dcc.Slider(
                                    id="years-slider",
                                    min=min(years),
                                    max=max(years),
                                    value=min(years),
                                    marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                            #"style": {"color": "#7fafdf", "fontSize": 10,"writing-mode": "vertical-rl","text-orientation": "upright"},

                                        }
                                        for year in mark_year
                                    },
                                ),
                            ],
                        ),
                        html.Div(
                            id="heatmap-container",
                            children=[
                                html.P(
                                    "Heatmap of {0} adjusted mortality rates \
                            from poisonings in year {1}".format(
                                        min(years),'population'
                                    ),
                                    id="heatmap-title",
                                ),
                                dcc.Graph(
                                    id="county-choropleth",
                                    figure=px.choropleth(df1, locations=df1["ISO"],
                    color=2000, # lifeExp is a column of gapminder
                    hover_name="Country",# column to add to hover information
                    color_continuous_scale=DEFAULT_COLORSCALE)
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        html.P(id="chart-selector", children="Select chart:"),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Population Millions",
                                    "value": "Population, Persons Millions",
                                },
                                {
                                    "label": "GDP per capita",
                                    "value": "Gross domestic product per capita, current prices, U.S. dollars Units",
                                }
                            ],
                            value="Population, Persons Millions",
                            id="chart-dropdown",
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=px.bar(x=df_hist.Country.tolist(), y=df_hist[2000].tolist(),color_discrete_sequence=['indianred'])
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("county-choropleth", "figure"),
    Output("selected-data","figure"),
    [Input("years-slider", "value"),
     Input("chart-dropdown","value" )],
    [State("county-choropleth", "figure")],
)
def display_map(year,drop, figure):
    #cm = dict(zip(BINS, DEFAULT_COLORSCALE))
    df2=data_modified[data_modified['Indicator']==drop]
    figure=px.choropleth(df2, locations=df2["ISO"],
                    color=year, # lifeExp is a column of gapminder
                    hover_name="Country", # column to add to hover information
                    color_continuous_scale=DEFAULT_COLORSCALE)
    df_hist1=df2.sort_values(by=[year],ascending=False)
    figure2=px.bar(x=df_hist1.Country.tolist(), y=df_hist1[year].tolist(),color_discrete_sequence=['indianred'])



    #for i, bin in enumerate(reversed(BINS)):
     #   color = cm[bin]
      #  annotations.append(
       #     dict(
        #        arrowcolor=color,
         #       text=bin,
          #      x=0.95,
           #     y=0.85 - (i / 20),
            #    ax=-60,
               # ay=0,
             #   arrowwidth=5,
               # arrowhead=0,
               # bgcolor="#1f2630",
                #font=dict(color="#2cfec1"),
            #)
       # )




    #fig = dict(data=data, layout=layout)
    return figure,figure2

@app.callback(Output("heatmap-title", "children"), [Input("years-slider", "value")],[Input("chart-dropdown", "value")])
def update_map_title(year,demo):
    return "Heatmap of {0} adjusted mortality rates \
				from poisonings in year {1}".format(
        demo,year
    )



'''
@app.callback(
    Output("county-choropleth", "figure"),
    [Input("years-slider", "value"),
     Input("chart-dropdown", "value")],
    [State("county-choropleth", "figure")],
)
def update_acc_drop(slider,drop,figure):
    df=data_modified_data[]

@app.callback(
    Output("selected-data", "figure"),
    [
        Input("county-choropleth", "selectedData"),
        Input("chart-dropdown", "value"),
        Input("years-slider", "value"),
    ],
)
def display_selected_data(selectedData, chart_dropdown, year):
    if selectedData is None:
        return dict(
            data=[dict(x=0, y=0)],
            layout=dict(
                title="Click-drag on the map to select counties",
                paper_bgcolor="#1f2630",
                plot_bgcolor="#1f2630",
                font=dict(color="#2cfec1"),
                margin=dict(t=75, r=50, b=100, l=75),
            ),
        )
    pts = selectedData["points"]
    fips = [str(pt["text"].split("<br>")[-1]) for pt in pts]
    for i in range(len(fips)):
        if len(fips[i]) == 4:
            fips[i] = "0" + fips[i]
    dff = df_full_data[df_full_data["County Code"].isin(fips)]
    dff = dff.sort_values("Year")

    regex_pat = re.compile(r"Unreliable", flags=re.IGNORECASE)
    dff["Age Adjusted Rate"] = dff["Age Adjusted Rate"].replace(regex_pat, 0)

    if chart_dropdown != "death_rate_all_time":
        title = "Absolute deaths per county, <b>1999-2016</b>"
        AGGREGATE_BY = "Deaths"
        if "show_absolute_deaths_single_year" == chart_dropdown:
            dff = dff[dff.Year == year]
            title = "Absolute deaths per county, <b>{0}</b>".format(year)
        elif "show_death_rate_single_year" == chart_dropdown:
            dff = dff[dff.Year == year]
            title = "Age-adjusted death rate per county, <b>{0}</b>".format(year)
            AGGREGATE_BY = "Age Adjusted Rate"

        dff[AGGREGATE_BY] = pd.to_numeric(dff[AGGREGATE_BY], errors="coerce")
        deaths_or_rate_by_fips = dff.groupby("County")[AGGREGATE_BY].sum()
        deaths_or_rate_by_fips = deaths_or_rate_by_fips.sort_values()
        # Only look at non-zero rows:
        deaths_or_rate_by_fips = deaths_or_rate_by_fips[deaths_or_rate_by_fips > 0]
        fig = deaths_or_rate_by_fips.iplot(
            kind="bar", y=AGGREGATE_BY, title=title, asFigure=True
        )

        fig_layout = fig["layout"]
        fig_data = fig["data"]

        fig_data[0]["text"] = deaths_or_rate_by_fips.values.tolist()
        fig_data[0]["marker"]["color"] = "#2cfec1"
        fig_data[0]["marker"]["opacity"] = 1
        fig_data[0]["marker"]["line"]["width"] = 0
        fig_data[0]["textposition"] = "outside"
        fig_layout["paper_bgcolor"] = "#1f2630"
        fig_layout["plot_bgcolor"] = "#1f2630"
        fig_layout["font"]["color"] = "#2cfec1"
        fig_layout["title"]["font"]["color"] = "#2cfec1"
        fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
        fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
        fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"
        fig_layout["margin"]["t"] = 75
        fig_layout["margin"]["r"] = 50
        fig_layout["margin"]["b"] = 100
        fig_layout["margin"]["l"] = 50

        return fig

    fig = dff.iplot(
        kind="area",
        x="Year",
        y="Age Adjusted Rate",
        text="County",
        categories="County",
        colors=[
            "#1b9e77",
            "#d95f02",
            "#7570b3",
            "#e7298a",
            "#66a61e",
            "#e6ab02",
            "#a6761d",
            "#666666",
            "#1b9e77",
        ],
        vline=[year],
        asFigure=True,
    )

    for i, trace in enumerate(fig["data"]):
        trace["mode"] = "lines+markers"
        trace["marker"]["size"] = 4
        trace["marker"]["line"]["width"] = 1
        trace["type"] = "scatter"
        for prop in trace:
            fig["data"][i][prop] = trace[prop]

    # Only show first 500 lines
    fig["data"] = fig["data"][0:500]

    fig_layout = fig["layout"]

    # See plot.ly/python/reference
    fig_layout["yaxis"]["title"] = "Age-adjusted death rate per county per year"
    fig_layout["xaxis"]["title"] = ""
    fig_layout["yaxis"]["fixedrange"] = True
    fig_layout["xaxis"]["fixedrange"] = False
    fig_layout["hovermode"] = "closest"
    fig_layout["title"] = "<b>{0}</b> counties selected".format(len(fips))
    fig_layout["legend"] = dict(orientation="v")
    fig_layout["autosize"] = True
    fig_layout["paper_bgcolor"] = "#1f2630"
    fig_layout["plot_bgcolor"] = "#1f2630"
    fig_layout["font"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["yaxis"]["tickfont"]["color"] = "#2cfec1"
    fig_layout["xaxis"]["gridcolor"] = "#5b5b5b"
    fig_layout["yaxis"]["gridcolor"] = "#5b5b5b"

    if len(fips) > 500:
        fig["layout"][
            "title"
        ] = "Age-adjusted death rate per county per year <br>(only 1st 500 shown)"

    return fig
'''
