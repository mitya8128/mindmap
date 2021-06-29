from gensim.models import KeyedVectors
import numpy as np
import nltk
from russian_tagsets import converters
from pymorphy2 import MorphAnalyzer
from collections import Counter
from config import Configuration


config = Configuration()


def load_nlp_engines():
    to_ud = converters.converter('opencorpora-int', 'ud20')
    morph = MorphAnalyzer()
    return to_ud, morph


def load_model():
    model_path = config.MODEL_PATH
    model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    return model


def avg_feature_vectorizer(sentence, model, num_features, index2word_set):
    if type(sentence) == str:
        words = sentence.split()
    else:
        words = sentence
    total = len(words)
    feature_vec = np.zeros((num_features,), dtype='float32')
    n_words = 0
    counter = Counter(words)

    for word in words:
        if word in index2word_set:
            n_words += 1
            # feature_vec = np.add(feature_vec, model[word])
            feature_vec = np.add(feature_vec, model[word]) * (counter[word] / total)
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return np.array(feature_vec)


def cosine(a, b):
    dot = np.dot(a, b.T)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    return cos


def sentence_tag_pymorphy(sentence: str) -> str:
    sentence = nltk.word_tokenize(sentence)
    parsed = []
    for word in sentence:
        lemma = str(morph.parse(word)[0].normal_form)
        pos = to_ud(str(morph.parse(word)[0].tag.POS)).split()[0]
        word_with_tag = lemma + '_' + pos
        parsed.append(word_with_tag)
    parsed = ' '.join(parsed)
    parsed = parsed.replace('[', '').replace(']', '')
    return parsed