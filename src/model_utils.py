from transformers import BertModel
from torch import nn
import torch

class SentimentCLassifier(nn.Module):

  def __init__(self, n_classes):
    super(SentimentCLassifier, self).__init__()
    self.bert = BertModel.from_pretrained('bert-base-cased')
    self.drop = nn.Dropout(p=0.4)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
        input_ids=input_ids, 
        attention_mask=attention_mask
    )
    output = self.drop(pooled_output)
    return self.out(output)

def encoder(tokenizer, review_text):
    return tokenizer.encode_plus(
                review_text,
                max_length=400,
                truncation=True,
                add_special_tokens=True,
                return_token_type_ids=False,
                pad_to_max_length=True,
                return_attention_mask=True,
                return_tensors='pt',
                )

def prediction(encoded_review, model):
    input_ids = encoded_review['input_ids']
    attention_mask = encoded_review['attention_mask']
    output = model(input_ids, attention_mask)
    _, prediction = torch.max(output, dim=1)
    return prediction
