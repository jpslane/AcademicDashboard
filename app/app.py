import os

import mongodb_utils
import mysql_utils
import neo4j_utils
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
from dash import dash_table

sql_df_columns = mysql_utils.find_faculty_member('internet').columns
faculty, years, keywords, unis = mysql_utils.get_faculty(), mysql_utils.get_years(), mysql_utils.get_keywords(), mysql_utils.get_uni()


def mod_string(s):
    return '\"' + s + '\"'


app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1('Research Interest Dashboard', style={'text-align': 'center'}),
    html.Div(children=[
        dcc.Dropdown(
            id='keyword-search',
            options=[{'label': val.title(), 'value': val} for val in keywords['name'].unique()],
            value=keywords['name'].iloc[0],
            style={'width': '300px'},
        ),
        dcc.Store(id='keyword'),
        dcc.Graph(
            id='Interest',
            style={'title_font': {'size': 24, 'textAlign': 'center'}, 'width': '60%', 'display': 'inline-block',
                   'height': '400px'}
        ),
        dcc.Graph(
            id='map',
            style={'title_font': {'size': 24, 'textAlign': 'center'}, 'width': '40%', 'display': 'inline-block',
                   'height': '400px'}
        ),
        html.H1(id='title-output', children='Title',
                style={'textAlign': 'center', 'fontSize': '24px'}),
        dash_table.DataTable(
            id='dt',
            columns=[
                {"name": i, "id": i, 'presentation': 'markdown'} if i == 'Google Scholar' else {'id': i, 'name': i} for i in sql_df_columns
            ],
            style_header={
                'textAlign': 'center'
            },
            style_cell={
                'textAlign': 'center'
            },
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            page_current=0,
            page_size=5,
        ),
    ], style={'margin': '15px', 'padding': '15px', 'border': '6px solid #ccc', 'border-radius': '5px'}),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='uni',
                placeholder='Modify University Name...',
                options=[{'label': val, 'value': val} for val in unis['name'].unique()],
                value=keywords['name'].iloc[0],
                style={'width': '300px'},
            ),
            dcc.Input(
                id='uni-input',
                type='text',
                value=''
            ),
            html.Button("Submit", id="submit-button1"),
            dcc.Store(id='result1')
        ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'gap': '20px'}),
        html.Div([
            dcc.Dropdown(
                id='faculty-name',
                placeholder='Modify Faculty Name...',
                options=[{'label': val, 'value': val} for val in faculty['name'].unique()],
                value=keywords['name'].iloc[0],
                style={'width': '300px'},
            ),
            dcc.Input(
                id='faculty-name-input',
                type='text',
                value=''
            ),
            html.Button("Submit", id="submit-button2"),
            dcc.Store(id='result2')
        ], style={'display': 'flex', 'flex-direction': 'row', 'align-items': 'center', 'gap': '20px'}),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
              'margin': '20px', 'padding': '20px', 'border': '1px solid black', 'border-radius': '5px'}),
    html.Div(children=[
        dcc.Dropdown(
            id='year-search',
            options=[{'label': val, 'value': val} for val in years['year'].unique()],
            value=years['year'].iloc[0],
            style={'width': '300px'},
        ),
        dcc.Graph(
            id='Scores',
            style={'height': '400px'}
        )
    ], style={'margin': '15', 'padding': '15px', 'border': '6px solid #ccc', 'border-radius': '5px'}),
])


@app.callback(dash.dependencies.Output('keyword', 'data'),
              [dash.dependencies.Input('keyword-search', 'value')])
def update_store(keyword):
    if keyword is None:
        return None
    return keyword


@app.callback(
    dash.dependencies.Output('result2', 'data'),
    dash.dependencies.Input('submit-button2', 'n_clicks'),
    dash.dependencies.State('faculty-name', 'value'),
    dash.dependencies.State('faculty-name-input', 'value'),
    dash.dependencies.Input('keyword', 'data'),
)
def update_database(n_clicks, faculty_name, input_value, keyword):
    input_value = '\"' + input_value + '\"'
    faculty_name = '\"' + faculty_name + '\"'

    if n_clicks:
        sql_com = f'UPDATE faculty SET name = {input_value} WHERE name = {faculty_name};'
        db = mysql_utils.db
        cursor = db.cursor()
        cursor.execute(sql_com)
        db.commit()
        print(faculty_name, input_value)
    return keyword


@app.callback(
    dash.dependencies.Output('result1', 'data'),
    dash.dependencies.Input('submit-button1', 'n_clicks'),
    dash.dependencies.State('uni', 'value'),
    dash.dependencies.State('uni-input', 'value'),
    dash.dependencies.Input('keyword', 'data'),
)
def update_database(n_clicks, faculty_name, input_value, keyword):
    input_value = '\"' + input_value + '\"'
    faculty_name = '\"' + faculty_name + '\"'

    if n_clicks and input_value and faculty_name:
        sql_com = f'UPDATE university SET university.name = {input_value} WHERE university.name = {faculty_name};'
        db = mysql_utils.db
        cursor = db.cursor()
        cursor.execute(sql_com)
        db.commit()
    return keyword


@app.callback(
    dash.dependencies.Output('title-output', 'children'),  # Output component and property to update
    [dash.dependencies.Input('keyword-search', 'value')]  # Input component to get value from
)
def update_actual_title(title):
    title = f'Top Faculty for {title.title()} by Publication Output'
    return title


@app.callback(
    dash.dependencies.Output('faculty-name', 'options'),
    dash.dependencies.Input('submit-button2', 'n_clicks'),
    dash.dependencies.State('faculty-name', 'value'),
    dash.dependencies.State('faculty-name-input', 'value'),
)
def update_dropdown(n_clicks, old, new):
    if n_clicks and old and new:
        faculty.loc[faculty['name'] == old, 'name'] = new
        options = [{'label': val, 'value': val} for val in faculty['name'].unique()]
        return options
    return [{'label': val, 'value': val} for val in faculty['name'].unique()]


@app.callback(
    dash.dependencies.Output('uni', 'options'),
    dash.dependencies.Input('submit-button1', 'n_clicks'),
    dash.dependencies.State('uni', 'value'),
    dash.dependencies.State('uni-input', 'value'),
)
def update_dropdown(n_clicks, old, new):
    if n_clicks and old and new:
        unis.loc[unis['name'] == old, 'name'] = new
        options = [{'label': val, 'value': val} for val in unis['name'].unique()]
        return options
    return [{'label': val, 'value': val} for val in unis['name'].unique()]


@app.callback(
    dash.dependencies.Output('dt', 'data'),
    [dash.dependencies.Input('keyword-search', 'value'),
     dash.dependencies.Input('result2', 'data'),
     dash.dependencies.Input('result1', 'data')]
)
def update_graph(keyword, value2, value1):
    context = dash.callback_context
    val = keyword
    if context.triggered:
        prop_id = context.triggered[0]['prop_id'].split('.')[0]
        if prop_id == 'keyword-search':
            val = keyword
        elif prop_id == 'result2':
            val = value2
        elif prop_id == 'result1':
            val = value1
        df = mysql_utils.find_faculty_member(val)
        data = df.to_dict('records')
        return data


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('keyword-search', 'value'),
     dash.dependencies.Input('result1', 'data')])
def update_bubble_map(keyword, value):
    use = keyword
    context = dash.callback_context
    if context.triggered:
        trigger_id = context.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'keyword-search':
            use = keyword
        elif trigger_id == 'result1':
            use = value
        filtered_df = neo4j_utils.return_university_interest('\"' + use + '\"')

        fig = px.scatter_geo(filtered_df, lat='latitude', lon='longitude',
                             hover_name='university', hover_data=['count'],
                             size='count', size_max=20,
                             locationmode='USA-states')

        fig.update_layout(
            title_text=f'<b>Top Universities for {use.title()} by Publication Output</b>',
            title_x=0.5,
            title_y=0.93,
            showlegend=True,
            geo=dict(
                scope='usa',
                landcolor='rgb(217, 217, 217)',
            ),
            title_font=dict(
                size=24,
                family='Times New Roman',
            )
        )
        return fig


@app.callback(
    dash.dependencies.Output('Interest', 'figure'),
    [dash.dependencies.Input('keyword-search', 'value')]
)
def update_graph(keyword):
    df1, df2 = neo4j_utils.return_faculty_count('\"' + keyword + '\"')
    data = [go.Bar(x=df2['year'], y=df2['publication_count'], name='Publications'),
            go.Bar(x=df1['year'], y=df1['faculty_count'],
                   name='Faculty')]  # , {'x': x, 'y': y, 'type': 'scatter', 'mode': 'lines', 'name': 'Hype Curve'}]
    layout = {
        'barmode': 'group',
        'xaxis': {'tickmode': 'linear', 'tick0': 0, 'dtick': 1, 'title': 'Year'},
        'yaxis': {'title': 'Count'},
        'title':
            {
                'text': f'<b>Count of Publications and Faculty Who Worked on Publications Involving {keyword.title()} by Year</b>',
                'font': {'family': 'Times New Roman', 'size': 24},
                'x': .5
            }
    }
    fig = go.Figure(data=data, layout=layout)
    return fig


@app.callback(
    dash.dependencies.Output('Scores', 'figure'),
    [dash.dependencies.Input('year-search', 'value')]
)
def update_mongo(year):
    year = int(year)
    mongodf = mongodb_utils.most_popular_keywords_in_year(year)
    data = [go.Scatter(x=mongodf['count'], y=mongodf['total'], mode='markers', marker=dict(
        size=10), text=mongodf['_id'], hoverinfo='text')]
    layout = {
        'barmode': 'stack',
        'xaxis': {'title': 'Count of Publications'},
        'yaxis': {'title': 'Sum of Keyword Scores in Publications'},
        'title':
            {
                'text': f'<b>Most Popular Keywords in {year}</b>',
                'font': {'family': 'Times New Roman', 'size': 24},
                'x': .5
            }
    }
    fig = go.Figure(data=data, layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
