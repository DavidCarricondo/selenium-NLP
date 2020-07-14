import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
from src.app_utils import *
from src.goodreads_scrapping import GR_scrapping
from src.model_utils import SentimentCLassifier
import torch
from transformers import BertTokenizer

#Get the PyTorch model
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')

model = SentimentCLassifier(3)
model.load_state_dict(torch.load('OUTPUT/models/best_model_custom.bin', map_location=torch.device('cpu')))


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")


###STYLE

external_stylesheets = external_stylesheets = [dbc.themes.BOOTSTRAP]

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

###CARDS

input_card = dbc.Card([
    dbc.CardBody(
        [dcc.Input(id='book_input',
        placeholder='Enter a book name...',
        type='text',
        value='',
        style={'text-align': 'center'}),
        html.Button(id='submit_button', n_clicks=0, children='Submit')],
    ),
])

cards = dbc.Container([
    dbc.Row([dbc.Col(input_card, align='center')]),
    dbc.Row([dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5("Sentiment analysis of the reviews", style={'color': colors['text'], 'text-align': 'center'})),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col( html.Div(id='output1'), width=6), 
                    dbc.Col(html.Div(id='output2'), width=6),
                ])
            )
        ])
    )]),
    dbc.Row([dbc.Col(
        dbc.Card([
            dbc.CardHeader(html.H5("Word frequency of the reviews", style={'color': colors['text'], 'text-align': 'center'})),
            dbc.CardBody(
                dbc.Row([
                    dbc.Col(html.Div(id='wordcloud'), width=6), 
                    dbc.Col(html.Div(id='treeplot'), width=6)
                ]),
            )
        ])
    )]),
    dbc.Row([dbc.Col(
        dbc.Card([
            dbc.CardBody(
                html.Div(id='freqplot')
            )
        ])
        )
    ]),
])

### DASHBOARD

app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[

                    {

                        "name": "viewport",

                        "content": "width=device-width, initial-scale=1, maximum-scale=1",

                    },

                ],)


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=
[
    html.H1("Book reviews analysis", style={'color': colors['text'], 'text-align': 'center'}),
    html.Div(id='prediction_store', style={'display': 'none'}),
    dcc.Store(id='reviews_store'),
    html.Div(children=cards)
    
])




##CALLBACKS

@app.callback(
    [Output(component_id='prediction_store', component_property='children'),
    Output('reviews_store', 'data')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='book_input', component_property='value')])
def update_book(n_clicks, input_data):
    if input_data=='':
        return None, None
    reviews = GR_scrapping(DRIVER, input_data)
    predictions = sample_predict(reviews, model, tokenizer)
    return predictions, reviews

@app.callback(
    Output(component_id='output1', component_property='children'),
    [Input(component_id='prediction_store', component_property='children')])
def create_boxplot(predictions):
    if predictions==None:
        return None
    fig = px.histogram(predictions, marginal='box')
    fig.update_layout(height=500, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='output2', component_property='children'),
    [Input(component_id='prediction_store', component_property='children')])
def create_barplot(predictions):
    if predictions==None:
        return None
    return dcc.Graph(figure={
        'data': [{'x':predictions, 'type':'bar', 'name':'PREDICTIONS'}], #type: line, histogram, bar
        'layout': {'title':'Sentiment predictions'}
        })

@app.callback(
    Output(component_id='wordcloud', component_property='children'),
    [Input('reviews_store', 'data')])
def create_wordcloud(reviews):
    if reviews==None:
        return None
    fig, _, _ = plotly_wordcloud(reviews)
    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='treeplot', component_property='children'),
    [Input('reviews_store', 'data')])
def create_treemap(reviews):
    if reviews==None:
        return None
    _, _, fig = plotly_wordcloud(reviews)
    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='freqplot', component_property='children'),
    [Input('reviews_store', 'data')])
def create_wordcloud(reviews):
    if reviews==None:
        return None
    _, fig, _ = plotly_wordcloud(reviews)
    return dcc.Graph(figure=fig)

if __name__=='__main__':
    app.run_server(debug=True)



