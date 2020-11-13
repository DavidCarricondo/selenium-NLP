import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import json
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import plotly.express as px
import plotly.graph_objects as go
from src.app_utils import *
from src.goodreads_scrapping import GR_scrapping
#Using keras directly (from keras import load_model)
#returns an error probably due to a mismatch in the keras version and the keras tensorflow version
from tensorflow import keras

model = keras.models.load_model('./OUTPUT/models/model_custom_rnn.h5')
#Loads the vocabulary to use:
#Load vocabulary file and create the statictable:
with open('OUTPUT/vocabulary', 'rb') as f:
    vocab = pickle.load(f)
f.close()
table = load_vocabulary(vocab, num_oov_buckets = 1000)


DRIVER = os.getenv("DRIVER")
GR_PASS = os.getenv("GR_PASS")
GR_USER = os.getenv("GR_USER")


###STYLE

external_stylesheets = external_stylesheets = [dbc.themes.DARKLY]

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

tab1 = html.Div(id='output1_1')
tab2 = html.Div(id='output1')

def sentiment_paragraph():
    paragraph = html.Div([html.H3('Sentiment prediction of the reviews', className='card-header', style={'color': colors['text'], 'text-align': 'center'}), 
    html.Div('A bidirectional recursive neural network with LSTM blocks is used to conduct an analysis\
         of the last thirty reviews of the book from goodreads.com. The model predicts a value from -5 to +5 \
             (-5 being very negative, 0 being neutral and +5 being very positive). The left figure is a boxplot \
                 showing the distribution of the predictions, and the right figure is a barplot showing the individual\
                      sentiment prediction of the reviews.', className='card-text')], className="card border-success mb-3")
    return paragraph
    
def frequency_paragraph():
    paragraph = html.Div([html.H3('Word frequency in the reviews', className='card-header', style={'color': colors['text'], 'text-align': 'center'}), 
    html.Div('The most frequent words in the reviews are calculated and visualized using three different visualization methods. \
        The first figure is a WordCloud with the most frequent words represented with a bigger size. The figure to the right \
            is a WordTree, with the most frequent words having a larger area in the figure. Finally, there is a simple barplot \
                with the most frequent words having larger bars.', className='card-text')], className="card border-success mb-3")
    return paragraph

cards = dbc.Container([
    dbc.Row(input_card, align='center'),

    dbc.Row([dbc.CardBody(
        dbc.Row([
            dbc.Col([dbc.Row(html.Div(id='title')),
                    dbc.Row(html.Div(id='author'))], width=6),
            dbc.Col(html.Div(id='bookcover'), width=6),
        ])
    )]),

    dbc.Row(dbc.Col(sentiment_paragraph())),

    dbc.Row([dbc.Col([
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dbc.Tabs([dbc.Tab(tab1, label='Pie chart'),
                                    dbc.Tab(tab2, label='Bar plot')]), width=6), 
                    dbc.Col(html.Div(id='output2'), width=6),
                ])
            ]),
        ])
    ])]),

    dbc.Row(dbc.Col(frequency_paragraph())),

    dbc.Row([dbc.Col(
        dbc.Card([
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
    html.H1("GOODREAD REVIEWS ANALYZER", style={'color': colors['text'], 'text-align': 'center'}),
    html.Div(id='prediction_store', style={'display': 'none'}),
    dcc.Store(id='reviews_store'),
    html.Div(children=cards)
    
])




##CALLBACKS

@app.callback(
    [Output(component_id='prediction_store', component_property='children'),
    Output('reviews_store', 'data'),
    Output(component_id='title', component_property='children'),
    Output(component_id='author', component_property='children'),
    Output(component_id='bookcover', component_property='children')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='book_input', component_property='value')])
def update_book(n_clicks, input_data):
    if input_data=='':
        return None, None, None, None, None
    reviews, title, author, pic = GR_scrapping(DRIVER, input_data)
    preprocess = sample_predict(reviews, table)
    pred = model.predict(preprocess)
    predictions = decode(pred)
    return predictions, reviews, html.H3(title, style={'color': colors['text'], 'text-align': 'left'}), html.H3(author, style={'color': colors['text'], 'text-align': 'left'}), html.Img(src=pic, style={'height':'50%', 'width':'50%', 'text-align':'right'})

@app.callback(
    Output(component_id='output1_1', component_property='children'),
    [Input(component_id='prediction_store', component_property='children')])
def create_piechart(predictions):
    if predictions==None:
        return None
    values = [predictions.count('Neutral'), predictions.count('Positive'), predictions.count('Negative')]
    pull = [0, 0, 0]
    pull[np.argmax(values)] = 0.2
    fig = go.Figure(data=[go.Pie(labels=['Neutral', 'Positive', 'Negative'], values=values, pull=pull)])
    fig.update_layout(height=500, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return dcc.Graph(figure=fig)

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



