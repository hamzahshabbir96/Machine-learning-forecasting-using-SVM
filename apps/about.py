import dash_html_components as html
import dash_bootstrap_components as dbc

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("ABOUT THIS PROJECT", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This application is not for commercial purpose but only for educational purpose'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Support Vector Machine (SVM) is a machine learning algorithm which is mostly used for classification. '
                                     'In this project, SVM has been used for the purpose of regression'
                                     'Aim of regression is to find a function that fits all the features of training set with certain weight.'
                                     'Data for this project has been taken from open source database of International Monetary Fund(IMF).'
                                     'Description and approach of this project can be understood from chart below.')
                    , className="mb-5")
        ]),

        dbc.Row([
        html.Img(src="/assets/project.jpg"),
        html.Hr(),


               html.Hr(),
               html.H5("If you find any bug or abnormalities in this project, please report me on hamzahshabbir7@gmail.com"
                      ),
                      html.A("Special Thanks to IMF for providing open source data which were used in this project",
                             href="https://www.imf.org/"),

    ])

])
])
# needed only if running this as a single page app
# if __name__ == '__main__':
# app.run_server(host='127.0.0.1', debug=True)
