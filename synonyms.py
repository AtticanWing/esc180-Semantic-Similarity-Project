'''Semantic Similarity: starter code

Author: Vanessa Lu and Erin Stewart. Last modified: Dec. 5, 2022.
'''

import math
import time

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''assuming vec1 and vec2 are of the same length'''
    numerator = 0
    for k, v in vec1.items():
        for k2, v2 in vec2.items():
            if k == k2:
                numerator += (v*v2)
    #print(numerator)
    return numerator/(norm(vec1)*norm(vec2))


def build_semantic_descriptors(sentences):
    d = {}
    for sent in sentences:
        for word in sent:
            if word not in d:
                d.update({word:{}})

    word_list = []
    word_list_2 = []
    for sent in sentences:
        for word in sent:
            if word not in word_list_2:
                word_list_2.append(word)
                for other_word in sent:
                    if other_word != word and other_word not in word_list and other_word in d[word].keys():
                        d[word][other_word] += 1
                        word_list.append(other_word)
                    elif other_word != word and other_word not in word_list:
                        d[word][other_word] = 1
                        word_list.append(other_word)
            word_list = []
        word_list_2 = []

    return d

def build_semantic_descriptors_from_files(filenames):
    ans = []
    for file in filenames:
        f = open(file, "r", encoding="utf-8").read().replace("?", ".")
        sents = f.replace("!", ".")
        sents = sents.split(".")
        if "\n" in sents:
            sents.remove("\n")
        for s in sents:
            s = s.replace(",", " ")
            s = s.replace("-,", " ")
            s = s.replace("--", " ")
            s = s.replace(":", " ")
            s = s.replace(";", " ")
            s = s.lower()
            ans += [s.split()]
    return build_semantic_descriptors(ans)

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_sim = -1          #max similarity initialized as -1
    most_sim = choices[0] #most similar word initialized as first choice
    if word in semantic_descriptors:
        wvec = semantic_descriptors[word]
        for c in choices:
            if c in semantic_descriptors:
                cvec = semantic_descriptors[c]
                sim = similarity_fn(wvec, cvec)
                if sim > max_sim:
                    most_sim = c
                    max_sim = sim
    return most_sim


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    count = 0
    # setting up lists from filename
    questions = []
    answers = []
    f = open(filename, "r", encoding="utf-8")
    options = f.read().split("\n")
    for i in range(len(options)):
        options[i] = options[i].split(" ")
        questions.append(options[i][0])
        del options[i][0]
        answers.append(options[i][0])
        del options[i][0]
    f.close()

    for x in range(len(options)):
        if most_similar_word(questions[x], options[x], semantic_descriptors, similarity_fn) == answers[x]:
            count += 1

    return (count/len(options))*100

if __name__ == "__main__":
    v1 = {"a": 1, "b": 2, "c": 3}
    v2 = {"b": 4, "c": 5, "d": 6}
    print(cosine_similarity(v1, v2))

    # sents = [["i", "am", "a", "sick", "man"],
    # ["i", "am", "a", "spiteful", "man"],
    # ["i", "am", "an", "unattractive", "man"],
    # ["i", "believe", "my", "liver", "is", "diseased"],
    # ["however", "i", "know", "nothing", "at", "all", "about", "my",
    # "disease", "and", "do", "not", "know", "for", "certain", "what", "ails", "me"]]
    # build_semantic_descriptors(sents)
    #sem = build_semantic_descriptors_from_files(["text.txt"])
    sem = build_semantic_descriptors_from_files(["wp.txt", "sw.txt", "text3.txt", "text4.txt", "text5.txt"])
    #sem = build_semantic_descriptors_from_files(["words.txt"])

    print(most_similar_word("rat", ["mouse", "water", "phone"], sem, cosine_similarity))

    # print(run_similarity_test("test.txt", sem, cosine_similarity))
    print(time.process_time())