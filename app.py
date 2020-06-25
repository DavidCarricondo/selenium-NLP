import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
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

'''
reviews = GR_scrapping(DRIVER, GR_PASS, GR_USER, 'lord of the flies')
predictions = sample_predict(reviews, model, encoder, pad=True)
print(predictions)
fig = px.histogram(predictions, marginal='box')
fig
'''
### Dashboard
app = dash.Dash(__name__)

app.layout = html.Div(children=
[
    html.H1("My Dash dashboard", style={'text-align': 'center'}),

    dcc.Input(id='book_input',
        placeholder='Enter a book name...',
        type='text',
        value='Lord of the flies'),
    html.Div(id='output'),
    
    #dcc.Graph(figure=fig),
    #dcc.Graph(figure={
    #    'data': [{'x':predictions, 'type':'bar', 'name':'PREDICTIONS'}], #type: line, histogram, bar
    #    'layout': {'title':'Sentiment predictions'}
    #})
    
])

@app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='book_input', component_property='value')])
def update_value(input_data):
    reviews = GR_scrapping(DRIVER, GR_PASS, GR_USER, input_data)
    predictions = sample_predict(reviews, model, encoder, pad=True)
    fig = px.histogram(predictions, marginal='box')
    return dcc.Graph(figure=fig)



if __name__=='__main__':
    app.run_server(debug=True)



