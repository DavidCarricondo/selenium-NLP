import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
import tensorflow as tf
import tensorflow_datasets as tfds
import plotly.express as px
from src.app_utils import *
from src.goodreads_scrapping import GR_scrapping
#Using keras directly (from keras import load_model)
#returns an error probably due to a mismatch in the keras version and the keras tensorflow version
from tensorflow import keras

model = keras.models.load_model('./OUTPUT/models/model_2ltsm.h5')
#Import the encoder from the tensorflow datasets,
#THis is going to be deprecated, so I have to rerun the model with 
#a non encoded data and encode it myself...
_, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
encoder = info.features['text'].encoder


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")


# CSS EXTERNAL FILE
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

###CARDS
wordcloud_card = dbc.Card(
    [
        dbc.CardBody(
            html.Div(id='wordcloud')
        ),
    ],
    #style={"width": "18rem"},
)

freqplot_card = dbc.Card(
    [
        dbc.CardBody(
            html.Div(id='freqplot')
        ),
    ],
    #style={"width": "18rem"},
)

cards = dbc.Row(
    [dbc.Col(wordcloud_card, width="auto"), dbc.Col(freqplot_card, width="auto")],
)

### Dashboard
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

    dcc.Input(id='book_input',
        placeholder='Enter a book name...',
        type='text',
        value=''),
    html.Button(id='submit_button', n_clicks=0, children='Submit'),
    dcc.Store(id='reviews_store'),
    html.Div(id='prediction_store', style={'display': 'none'}),
    html.Div(id='output1'),
    html.Div(id='output2'),
    html.Div(children=cards)
])



@app.callback(
    [Output(component_id='prediction_store', component_property='children'),
    Output('reviews_store', 'data')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='book_input', component_property='value')])
def update_book(n_clicks, input_data):
    if input_data=='':
        return None, None
    reviews = GR_scrapping(DRIVER, input_data)
    predictions = sample_predict(reviews, model, encoder, pad=True)
    return predictions, reviews

@app.callback(
    Output(component_id='output1', component_property='children'),
    [Input(component_id='prediction_store', component_property='children')])
def create_boxplot(predictions):
    if predictions=='':
        return None
    fig = px.histogram(predictions, marginal='box')
    fig.update_layout(height=500, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return dcc.Graph(figure=fig)

@app.callback(
    Output(component_id='output2', component_property='children'),
    [Input(component_id='prediction_store', component_property='children')])
def create_barplot(predictions):
    if predictions=='':
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
    Output(component_id='freqplot', component_property='children'),
    [Input('reviews_store', 'data')])
def create_wordcloud(reviews):
    if reviews==None:
        return None
    _, fig, _ = plotly_wordcloud(reviews)
    return dcc.Graph(figure=fig)

if __name__=='__main__':
    app.run_server(debug=True)



