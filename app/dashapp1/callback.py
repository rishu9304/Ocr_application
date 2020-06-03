import base64
import datetime
import io
from dash.dependencies import Input
from dash.dependencies import Output,State
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_table


df =  pd.DataFrame()

def parse_contents(contents, filename, date):
    global df
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            id='datatable'
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

def parse_content1(filename):
    global df
    df =  df.describe()
    return html.Div([
        html.H5(filename),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns],
            id='datatable1'
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
    ])


def register_callback(dashapp):
    @dashapp.callback([Output('output-data-upload', 'children'),
                    Output('output-data-upload1', 'children')],
                  [Input('upload-data', 'contents'),
                  Input('submit-button-state','n_clicks')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
    def update_output(list_of_contents,n_clicks ,list_of_names, list_of_dates):
        print("n_clicks",n_clicks)
        if n_clicks>0:
            if list_of_contents is not None:
                children = [
                    parse_contents(c, n, d) for c, n, d in
                    zip(list_of_contents, list_of_names, list_of_dates)]
                children1 = parse_content1(list_of_names[0])
                return children,children1
        if list_of_contents is not None:
            children = [
                parse_contents(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]
            return children,''