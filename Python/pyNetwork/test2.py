import nltk

from nltk.collocations import BigramAssocMeasures,BigramCollocationFinder
from main import preprocessing


text = """

A computer system provides a plug-in architecture for creation of a dynamic font. The computer system can incorporate a new filter function into a filtering layer of a font program. The filtering layer includes pre-defined filter functions to transform a base font into a new font. The computer system applies one or more font rules in the filtering layer to the base font. The font rules are implemented by the new filter function and at least one of the pre-defined filter functions to randomize an appearance of each character in a character string. The character string rendered with the new font has a dynamic and randomized appearance.

"""

bigram_measures = BigramAssocMeasures()
#trigram_measures = TrigramAssocMeasures()
 
# change this to read in your data
 
finder = BigramCollocationFinder.from_words(preprocessing(text))


 
# only bigrams that appear 3+ times
#finder.apply_freq_filter(2)
 
# return the 10 n-grams with the highest PMI
print(finder.nbest(bigram_measures.pmi,-1))
print(finder.nbest(bigram_measures.likelihood_ratio, -1))
print(finder.nbest(bigram_measures.poisson_stirling, -1))


""" 
d = ['09-2012', '04-2007', '11-2012', '05-2013', '12-2006', '05-2006', '08-2007']
sort_index = sorted(d, key=lambda x: datetime.datetime.strptime(x, '%m-%Y'))
        
for i,j in enumerate(sort_index[:-1]):
    print(sort_index[i],sort_index[i+1])
    

t = [(('vector', 'art'), 0.03571428571428571), (('graphics', 'hardware'), 0.023809523809523808),(('graphics'), 0.023809523809523808)]

for term,freq in t:
    print(term)
    

hash = {'a':1,'b':2,'c':.2}


s = 'line.21 method basis.3 image'
print(re.sub('(\S+)\.\d+', '\g<1>', s))
"""

"""
1. A computer for generating hair comprising: a processor;  a memory including a hair pipeline comprising:  a surface definition module to define a surface;  an optimization module to determine whether a hair is to be rendered upon the surface, the optimization module to: determine a size metric for the hair, wherein determining the size metric for the hair includes calculating a length of the hair;  apply a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;  apply a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;  based upon the density multiplier value, determine whether to render the hair; and   a display device module to display the rendered hair on a display device. a processor;a memory including a hair pipeline comprising:a surface definition module to define a surface;an optimization module to determine whether a hair is to be rendered upon the surface, the optimization module to: determine a size metric for the hair, wherein determining the size metric for the hair includes calculating a length of the hair;  apply a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;  apply a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;  based upon the density multiplier value, determine whether to render the hair; and determine a size metric for the hair, wherein determining the size metric for the hair includes calculating a length of the hair;apply a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;apply a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;based upon the density multiplier value, determine whether to render the hair; anda display device module to display the rendered hair on a display device.2. The hair pipeline of  claim 1 , wherein the density multiplier value is further compared to a random number to determine whether to render the hair.3. The hair pipeline of  claim 1 , wherein determining the size metric for the hair including calculating the length of the hair is calculated in a normalized device coordinate (NDC) space.4. The hair pipeline of  claim 1 , wherein the optimization module further determines a speed space metric based upon a distance traveled by a hair root position of the hair from a first frame to a second frame.5. The hair pipeline of  claim 4 , wherein a second density curve is applied to the speed space metric for the hair to generate the density multiplier value.6. The hair pipeline of  claim 5 , wherein a first width curve is applied to the size metric for the hair and a second width curve is applied to the speed space metric for the hair to generate a width multiplier value to adjust the width of the hair.7. A method implemented by a computer system having a memory and processor to determine whether a hair is to be rendered comprising: determining a size metric for a hair, wherein determining the size metric for the hair includes calculating a length of the hair;  applying a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;  applying a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;  determining whether to render the hair based upon the density multiplier value; and  displaying the rendered hair on a display device, wherein the steps of determining, applying, determining, and displaying are performed by the computer system. determining a size metric for a hair, wherein determining the size metric for the hair includes calculating a length of the hair;applying a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;applying a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;determining whether to render the hair based upon the density multiplier value; anddisplaying the rendered hair on a display device, wherein the steps of determining, applying, determining, and displaying are performed by the computer system.8. The method of  claim 7 , further comprising comparing the density multiplier value to a random number to determine whether to render the hair.9. The method of  claim 7 , wherein determining the size metric for the hair including calculating the length of the hair is calculated in a normalized device coordinate (NDC) space.10. The method of  claim 7 , further comprising determining a speed space metric based upon a distance traveled by a hair root position of the hair from a first frame to a second frame.11. The method of  claim 10 , further comprising applying a second density curve to the speed space metric for the hair to generate the density multiplier value.12. The method of  claim 11 , further comprising applying a first width curve to the size metric for the hair and applying a second width curve to the speed space metric for the hair to generate a width multiplier value that is used to adjust the width of the hair.13. A non-transitory computer-readable storage medium containing executable instructions tangibly stored thereon which, when executed in a computer processing system, cause the computer processing system to perform a method for determining whether a hair is to be rendered comprising: determining a size metric for a hair, wherein determining the size metric for the hair includes calculating a length of the hair;  applying a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;  applying a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;  determining whether to render the hair based upon the density multiplier value; and  displaying the rendered hair on a display device. determining a size metric for a hair, wherein determining the size metric for the hair includes calculating a length of the hair;applying a first user-defined functional density curve to the size metric determined for the hair to generate a density multiplier value;applying a first user-defined functional width curve to the size metric for the hair to adjust the width of the hair;determining whether to render the hair based upon the density multiplier value; anddisplaying the rendered hair on a display device.14. The computer-readable storage medium of  claim 13 , further comprising comparing the density multiplier value to a random number to determine whether to render the hair.15. The computer-readable storage medium of  claim 13 , wherein determining the size metric for the hair including calculating the length of the hair is calculated in a normalized device coordinate (NDC) space.16. The computer-readable storage medium of  claim 13 , further comprising determining a speed space metric based upon a distance traveled by a hair root position of the hair from a first frame to a second frame.17. The computer-readable storage medium of  claim 16 , further comprising applying a second density curve to the speed space metric for the hair to generate the density multiplier value.18. The computer-readable storage medium of  claim 17 , further comprising applying a first width curve to the size metric for the hair and applying a second width curve to the speed space metric for the hair to generate a width multiplier value that is used to adjust the width of the hair.

"""
"""
text = nltk.word_tokenize('generating 2D texture coordinates')
bi = nltk.bigrams(text)

tmp = []
for i,(term,pos) in enumerate(nltk.pos_tag(text)):
    print(term,pos)
    if pos in ['NN']:
        tmp.append(term)
        del text[i]
         
    
print(text)
print(tmp)

#dict={'1':4,'2':3,'3':2,'4':1}
dict={'1':1,'2':2,'3':3,'4':4}

for key, value in sorted(dict.items(), key=lambda x: x[1], reverse=True):
    print ('%s: %s' % (key, value))
"""

    

    