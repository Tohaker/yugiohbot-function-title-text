import os

from textgenrnn import textgenrnn


def generate_from_model(name, length):
    textgen = textgenrnn(weights_path='{}_weights.hdf5'.format(name), vocab_path='{}_vocab.json'.format(name),
                         config_path='{}_config.json'.format(name))
    # this temperature schedule cycles between 1 very unexpected token, 1 unexpected token, 2 expected tokens, repeat.
    # changing the temperature schedule can result in wildly different output!
    temperature = [1.0, 0.5, 0.2, 0.2]
    prefix = None  # if you want each generated text to start with a given seed text
    n = length
    max_gen_length = 60
    gen_file = '{}_gentext.txt'.format(name)

    textgen.generate_to_file(gen_file,
                             temperature=temperature,
                             prefix=prefix,
                             n=n,
                             max_gen_length=max_gen_length)


def generate_single(name, temperature):
    p = os.getenv('TEST_ML', 'resources/model/outputs/{}')
    prefix = p.format(name)
    textgen = textgenrnn(weights_path=prefix + '_weights.hdf5', vocab_path=prefix + '_vocab.json',
                         config_path=prefix + '_config.json')
    return textgen.generate(1, temperature=temperature, return_as_list=True)


def train_model(name):
    model_cfg = {
        'word_level': True,
        # set to True if want to train a word-level model (requires more data and smaller max_length)
        'rnn_size': 128,  # number of LSTM cells of each layer (128/256 recommended)
        'rnn_layers': 3,  # number of LSTM layers (>=2 recommended)
        'rnn_bidirectional': False,  # consider text both forwards and backward, can give a training boost
        'max_length': 5,
        # number of tokens to consider before predicting the next (20-40 for characters, 5-10 for words recommended)
        'max_words': 100000,  # maximum number of words to model; the rest will be ignored (word-level model only)
    }

    train_cfg = {
        'line_delimited': True,  # set to True if each text has its own line in the source file
        'num_epochs': 20,  # set higher to train the model for longer
        'gen_epochs': 10,  # generates sample text from model after given number of epochs
        'train_size': 0.8,  # proportion of input data to train on: setting < 1.0 limits model from learning perfectly
        'dropout': 0.0,  # ignore a random proportion of source tokens each epoch, allowing model to generalize better
        'validation': True,  # If train__size < 1.0, test on holdout dataset; will make overall training slower
        'is_csv': False  # set to True if file is a CSV exported from Excel/BigQuery/pandas
    }

    file_name = "../resources/model/{}.txt".format(name)
    model_name = name  # change to set file name of resulting trained models/texts

    textgen = textgenrnn(name=model_name)
    train_function = textgen.train_from_file

    train_function(
        file_path=file_name,
        new_model=True,
        num_epochs=train_cfg['num_epochs'],
        gen_epochs=train_cfg['gen_epochs'],
        batch_size=1024,
        train_size=train_cfg['train_size'],
        dropout=train_cfg['dropout'],
        validation=train_cfg['validation'],
        is_csv=train_cfg['is_csv'],
        rnn_layers=model_cfg['rnn_layers'],
        rnn_size=model_cfg['rnn_size'],
        rnn_bidirectional=model_cfg['rnn_bidirectional'],
        max_length=model_cfg['max_length'],
        dim_embeddings=100,
        word_level=model_cfg['word_level'])


if __name__ == '__main__':
    train_model('monster')
    generate_from_model('monster', 100)
