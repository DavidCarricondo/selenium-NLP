import dash
import dash_html_components as html
import dash_core_components as dcc
import json
import tensorflow as tf
import tensorflow_datasets as tfds
import plotly.express as px
#Using keras directly (from keras import load_model)
#returns an error probably due to a mismatch in the keras version and the keras tensorflow version
from tensorflow import keras

##ALL THIS SHOULD BE IN OTHER SCRIPT
model = keras.models.load_model('./OUTPUT/models/model_2ltsm.h5')

with open('./OUTPUT/data.json') as f:
    data_json = f.read()
data = json.loads(data_json)


#Import the encoder from the tensorflow datasets,
#THis is going to be deprecated, so I have to rerun the model with 
#a non encoded data and encode it myself...
_, info = tfds.load('imdb_reviews/subwords8k', with_info=True,
                          as_supervised=True)
encoder = info.features['text'].encoder

#Function to add the padding at the end of the sentences:
def pad_to_size(vec, size):
  zeros = [0] * (size - len(vec))
  vec.extend(zeros)
  return vec
#Function to get the predictions:
def sample_predict(sample_pred_text, pad):
    predictions = []
    for rev in sample_pred_text:
        rev = rev.replace('\n', '')    
        encoded_sample_pred_text = encoder.encode(rev)
        if pad:
            encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
        encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
        predictions.append(model.predict(tf.expand_dims(encoded_sample_pred_text, 0))[0][0])
    return (predictions)

predictions = sample_predict(data, pad=True)

fig = px.histogram(predictions, marginal='box')

####

### Dashboard
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("My Dash dashboard", style={'text-align': 'center'}),

    dcc.Input(
        placeholder='Enter a book name...',
        type='text',
        value=''),

    dcc.Graph(figure=fig)
])

if __name__=='__main__':
    app.run_server(debug=True)




