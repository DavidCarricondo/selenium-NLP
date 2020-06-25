import tensorflow as tf

def pad_to_size(vec, size):
    '''
    Zero pad the model input
    '''
    zeros = [0] * (size - len(vec))
    vec.extend(zeros)
    return vec

#Function to get the predictions:
def sample_predict(sample_pred_text, model, encoder,  pad):
    '''
    Get the prediction of the sample from the model after preprocessing
    '''
    predictions = []
    for k, v in sample_pred_text.items():
        rev = v.replace('\n', '')
        encoded_sample_pred_text = encoder.encode(rev)
        if pad:
            encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
        encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
        predictions.append(model.predict(tf.expand_dims(encoded_sample_pred_text, 0))[0][0])
    return predictions