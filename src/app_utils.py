import tensorflow as tf
from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go
import pickle
import numpy as np

def load_vocabulary(vocab_file, num_oov_buckets = 5000):
    '''
    Creates a StaticTable vocabulary from the vocabulary list 
    '''
    words = tf.constant(vocab_file)
    word_ids = tf.range(len(vocab_file), dtype=tf.int64)
    vocab_init = tf.lookup.KeyValueTensorInitializer(words, word_ids)
    return tf.lookup.StaticVocabularyTable(vocab_init, num_oov_buckets)

def sample_predict(sample_pred_texts, table):
    reviews = [rev for key, rev in sample_pred_texts.items()]
    rev_tensor = tf.convert_to_tensor(reviews)
    X = tf.strings.substr(rev_tensor, 0, 2000)
    X = tf.strings.regex_replace(X, b"<br\\s*/?>", b" ")
    X = tf.strings.regex_replace(X, b"[^a-zA-Z']", b" ")
    X = tf.strings.split(X)
    X = X.to_tensor(default_value=b"<pad>")
    return table.lookup(X)

def decode(predictions):
    codex = {'0':'Negative', '1':'Neutral', '2':'Positive'}
    return [codex[str(np.argmax(e))] for e in predictions]  



##Graphs


def plotly_wordcloud(reviews):
    #Adapted from: https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-nlp/app.py
    """A wonderful function that returns figure data for three equally
    wonderful plots: wordcloud, frequency histogram and treemap"""
    text = [v for k,v in reviews.items()]

    if len(text) < 1:
        return {}, {}, {}

    # join all documents in corpus
    text = " ".join(list(text))

    word_cloud = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    word_cloud.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x_arr = []
    y_arr = []
    for i in position_list:
        x_arr.append(i[0])
        y_arr.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x_arr,
        y=y_arr,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
            "hovermode": "closest",
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}
    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "550", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }
    treemap_trace = go.Treemap(
        labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
    )
    treemap_layout = go.Layout({"margin": dict(t=10, b=10, l=5, r=5, pad=4)})
    treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
    return wordcloud_figure_data, frequency_figure_data, treemap_figure