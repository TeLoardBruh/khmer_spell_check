import os

from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader
import torch
import torch.nn as nn
import torch.nn.utils.rnn
import numpy as np


TRAIN_FILE = "rnn_train_dataset.txt"
MODEL_FILE = "util/rnn.model"

KHCONST = list(u"កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ")
KHVOWEL = list(u"឴឵ាិីឹឺុូួើឿៀេែៃោៅ\u17c6\u17c7\u17c8")
# subscript, diacritics
KHSUB = list(u"្")
KHDIAC = list(
    u"\u17c9\u17ca\u17cb\u17cc\u17cd\u17ce\u17cf\u17d0"
)  # MUUSIKATOAN, TRIISAP, BANTOC,ROBAT,
KHSYM = list("៕។៛ៗ៚៙៘,.? ")  # add space
KHNUMBER = list(u"០១២៣៤៥៦៧៨៩0123456789")  # remove 0123456789
CHARS = ["PADDING"] + ["UNK"] + KHCONST + KHVOWEL + KHSUB + KHDIAC + KHSYM + KHNUMBER

chars2idx = {o: i for i, o in enumerate(CHARS)}
idx2chars = {i: o for i, o in enumerate(CHARS)}

# for gpu
train_on_gpu = False

def one_hot_encode(arr, n_labels):
  arr = arr.numpy()
  # Initialize the the encoded array
  one_hot = np.zeros((arr.size, n_labels), dtype=np.float32)
  # Fill the appropriate elements with ones
  one_hot[np.arange(one_hot.shape[0]), arr.flatten()] = 1.0
  # Finally reshape it to get back to the original array
  one_hot = one_hot.reshape((*arr.shape, n_labels))

  return torch.from_numpy(one_hot)

class WordSegmentRNN(nn.Module):
    def __init__(self, n_input, n_output, n_hidden=100, n_layers=2, drop_prob=0.5):
        super().__init__()
        self.drop_prob = drop_prob
        self.n_layers = n_layers
        self.n_hidden = n_hidden

        ## TODO: define the LSTM
        self.lstm = nn.LSTM(
            n_input, n_hidden, n_layers, dropout=drop_prob, batch_first=True
        )

        ## TODO: define a dropout layer
        self.dropout = nn.Dropout(drop_prob)

        ## TODO: define the final, fully-connected output layer
        self.fc = nn.Linear(n_hidden, n_output)

    def forward(self, x, hidden):
        """Forward pass through the network.
        These inputs are x, and the hidden/cell state `hidden`."""

        ## TODO: Get the outputs and the new hidden state from the lstm
        r_output, hidden = self.lstm(x, hidden)

        ## TODO: pass through a dropout layer
        out = self.dropout(r_output)

        # Stack up LSTM outputs using view
        # you may need to use contiguous to reshape the output
        out = out.contiguous().view(-1, self.n_hidden)

        ## TODO: put x through the fully-connected layer
        out = self.fc(out)

        # return the final output and the hidden state
        return out, hidden

    def init_hidden(self, batch_size):
        """Initializes hidden state"""
        # Create two new tensors with sizes n_layers x batch_size x n_hidden,
        # initialized to zero, for hidden state and cell state of LSTM
        weight = next(self.parameters()).data

        if train_on_gpu:
            hidden = (
                weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda(),
                weight.new(self.n_layers, batch_size, self.n_hidden).zero_().cuda(),
            )
        else:
            hidden = (
                weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
                weight.new(self.n_layers, batch_size, self.n_hidden).zero_(),
            )

        return hidden

def segment(str):
  model = torch.load(MODEL_FILE)

  model.eval()

  list_of_chars = list(str)
  # print(CHARS)
  # print(list_of_chars)

  index_of_chars = [(chars2idx[x] if (x in CHARS) else 1) for x in list_of_chars]
  # print(index_of_chars)

  tensor_chars = torch.from_numpy(np.array(index_of_chars)).unsqueeze(0)
  encoded_chars = one_hot_encode(tensor_chars, len(CHARS))

  if train_on_gpu:
    encoded_chars = encoded_chars.cuda()

  h = model.init_hidden(1)
  h = tuple([each.data for each in h])

  outputs, _ = model(encoded_chars, h)

  if train_on_gpu:
    outputs = outputs.detach().cpu().numpy()
  else:
    outputs = outputs.detach().numpy()

  segmented_chars_idx = np.argmax(outputs, axis=1)

  result = ""

  for idx, char in enumerate(list_of_chars):
    if segmented_chars_idx[idx] == 1 and result != "":
      result += " " + char
    else:
      result += char

  space = ' '
  return list(
    filter(
      lambda x: x != "",
      result.strip()
      .replace("   ", space)
      .replace(" ", space)
      .replace("\u200b", space)
      .split(space),
    )
  )
