from .utils import*


to_ud, morph = load_nlp_engines()
model, index2word_set = load_model()


# make iterative algorithmic mindmap
def make_mindmap_simple(word, model):
    lst = model.most_similar(word, topn=5)
    new_list = []
    for element in lst:
        elmt = element[0]
        new_list.append(elmt)
    lst_final = []
    for el in new_list:
        lst_element = model.most_similar(el, topn=5)
        lst_final.append(lst_element)
    return word, lst, lst_final


# formatter
list_questions = ['зачем', 'причина', 'план', 'исполнение']

# make iterative algorithmic mindmap with formatter
def make_mindmap_formatter(word, model):
    lst = model.most_similar(word, topn=5)
    new_list = []
    for element in lst:
        elmt = element[0]
        new_list.append(elmt)
    lst_final = []
    for el in new_list:
        for i in range(len(list_questions)):
            lst_element = model.most_similar(positive=[el, sentence_tag_pymorphy(list_questions[i])], topn=5)
            lst_final.append(lst_element)
    return word, lst, lst_final