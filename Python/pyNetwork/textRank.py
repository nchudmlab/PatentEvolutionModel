"""
From this paper: https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
External dependencies: nltk, numpy, networkx
Based on https://gist.github.com/voidfiles/1646117
"""

import nltk
import itertools
import networkx as nx


#apply syntactic filters based on POS tags
def filter_for_tags(tagged, tags=['NN', 'JJ', 'NNP','NNS','NNPS']):
    return [item for item in tagged if item[1] in tags]


def normalize(tagged):
    return [(item[0].replace('.', ''), item[1]) for item in tagged]

def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in itertools.filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element

def lDistance(firstString, secondString):
    "Function to find the Levenshtein distance between two words/sentences - gotten from http://rosettacode.org/wiki/Levenshtein_distance#Python"
    if len(firstString) > len(secondString):
        firstString, secondString = secondString, firstString
    distances = range(len(firstString) + 1)
    for index2, char2 in enumerate(secondString):
        newDistances = [index2 + 1]
        for index1, char1 in enumerate(firstString):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]

def buildGraph(nodes):
    "nodes - list of hashables that represents the nodes of the graph"
    gr = nx.Graph() #initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    #add edges to the graph (weighted by Levenshtein distance)
    for pair in nodePairs:
        firstString = pair[0]
        secondString = pair[1]
        levDistance = lDistance(firstString, secondString)
        gr.add_edge(firstString, secondString, weight=levDistance)

    return gr

def extractKeyphrases(text):
    #tokenize the text using nltk
    wordTokens = nltk.word_tokenize(text)

    #assign POS tags to the words in the text
    tagged = nltk.pos_tag(wordTokens)
    textlist = [x[0] for x in tagged]
    
    tagged = filter_for_tags(tagged)
    tagged = normalize(tagged)

    unique_word_set = unique_everseen([x[0] for x in tagged])
    word_set_list = list(unique_word_set)

   #this will be used to determine adjacent words in order to construct keyphrases with two words

    graph = buildGraph(word_set_list)

    #pageRank - initial value of 1.0, error tolerance of 0,0001, 
    calculated_page_rank = nx.pagerank(graph, weight='weight')

    #most important words in ascending order of importance
    keyphrases = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=True)

    #the number of keyphrases returned will be relative to the size of the text (a third of the number of vertices)
    aThird = int(len(word_set_list) / 3)
    keyphrases = keyphrases[0:aThird+1]

    #take keyphrases with multiple words into consideration as done in the paper - if two words are adjacent in the text and are selected as keywords, join them
    #together
    modifiedKeyphrases = set([])
    dealtWith = set([]) #keeps track of individual keywords that have been joined to form a keyphrase
    i = 0
    j = 1
    while j < len(textlist):
        firstWord = textlist[i]
        secondWord = textlist[j]
        if firstWord in keyphrases and secondWord in keyphrases:
            keyphrase = firstWord + ' ' + secondWord
            modifiedKeyphrases.add(keyphrase.lower())
            dealtWith.add(firstWord)
            dealtWith.add(secondWord)
        else:
            if firstWord in keyphrases and firstWord not in dealtWith: 
                modifiedKeyphrases.add(firstWord.lower())

            #if this is the last word in the text, and it is a keyword,
            #it definitely has no chance of being a keyphrase at this point    
            if j == len(textlist)-1 and secondWord in keyphrases and secondWord not in dealtWith:
                modifiedKeyphrases.add(secondWord.lower())
        
        i = i + 1
        j = j + 1
        
    return modifiedKeyphrases



if __name__ == '__main__':
    text = """
    LINCOLNSHIRE, IL With next-generation video game systems such as the Xbox One and the Playstation 4 hitting stores later this month, the console wars got even hotter today as electronics manufacturer Zenith announced the release of its own console, the Gamespace Pro, which arrives in stores Nov. 19. “With its sleek silver-and-gray box, double-analog-stick controllers, ability to play CDs, and starting price of $374.99, the Gamespace Pro is our way of saying, ‘Move over, Sony and Microsoft, Zenith is now officially a player in the console game,’” said Zenith CEO Michael Ahn at a Gamespace Pro press event, showcasing the system’s launch titles MoonChaser: Radiation, Cris Collinsworth’s Pigskin 2013, and survival-horror thriller InZomnia. “With over nine launch titles, 3D graphics, and the ability to log on to the internet using our Z-Connect technology, Zenith is finally poised to make some big waves in the video game world.” According to Zenith representatives, over 650 units have already been preordered.
    
    """
    
    keyphrases = extractKeyphrases(text)
    print(keyphrases)


    