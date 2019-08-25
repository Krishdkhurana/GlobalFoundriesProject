from flask import Flask, redirect, url_for, request, render_template
import csv
import operator 
import math
import urllib2
import sys
import re
import itertools
import string
reload(sys)
sys.setdefaultencoding('iso-8859-1')
app = Flask(__name__)



def NumOfWords(string):
    return len(string.split())
def StringAfterFirstWord(s):
    space  = s.find(' ')
    s = s[space+1:]
    return s
def FirstnNumOfWords(string, n):
    a = string.split()[:n] # first n words
    return ' '.join(a)

def ConsecutiveBagOfWords(complete_string, num_of_words):
    
    #if num_of_words in complete_string > num_of_words
    if NumOfWords(complete_string) > num_of_words:
        # recursion call
        return " ".join(str(x) for x in  [ConsecutiveBagOfWords(StringAfterFirstWord(complete_string), num_of_words),(FirstnNumOfWords(complete_string,num_of_words)),'-'])
        
    else:
        return complete_string+'-'

def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict
def remove_stop_words(lower_case_corpus):
    my_stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    my_stop_words.extend(["Global Foundry View","Foundry View","FoundryView","GlobalFoundryView","foundry view","foundry",'GlobalFoundry View'])
    array_of_sets = []
    for sentence in lower_case_corpus:

        
        sentence = sentence.split(" ")
        sentence_without_stop_words = [x for x in sentence if x not in my_stop_words]
        # sentence_without_stop_words contains the strings as elemenst of a set    
        array_of_sets.append(sentence_without_stop_words)
    return array_of_sets, my_stop_words 


 
def remove_punctuation(lower_case_corpus):

    list_of_strings = []

    for sentence in lower_case_corpus:

        sentence = sentence.rstrip(string.punctuation)
        replace_punctuation = string.maketrans(string.punctuation,' '*len(string.punctuation))
        sentence = sentence.translate(replace_punctuation)
        sentence = re.sub(' +',' ',sentence)
        list_of_strings.append(sentence)

    return list_of_strings   

#Now we have to create the BagOfWords

def BagOfWords(corpus_without_stopwords):
    values = []

    num_of_words_in_sentence_to_search = len(corpus_without_stopwords[0])
    for bowB in corpus_without_stopwords:

        wordSet = list(set().union(bowB,corpus_without_stopwords[0]))
        wordDictA = dict.fromkeys(wordSet, 0)
        wordDictB = dict.fromkeys(wordSet, 0)    


        for word in corpus_without_stopwords[0]:
            wordDictA[word]+=1
        for word in bowB:
            if word in wordSet:
                wordDictB[word]+=1 
        tfBowA = computeTF(wordDictA, corpus_without_stopwords[0])  
        tfBowB = computeTF(wordDictB, bowB)
        
        flag = 0 
        for key,value in tfBowA.iteritems():
            if value > 0 and tfBowB[key] > 0:
                flag = flag + 1
            

        if flag == 0:        
            for key,value in tfBowA.iteritems():
                #value = 0
                tfBowA[key] = 99999
                tfBowB[key] = 99999 

        # fraction is non-zero only if no. of words matched is greater than 51
        
        if flag > 1 :
            fraction =math.log10( float(num_of_words_in_sentence_to_search)/flag ) + 1.0
        else :
            fraction = 0.0  
        
        score = fraction
        values.append(score)
    return values






@app.route('/handle_data', methods=['POST'])
def handle_data():
    string_to_search = request.form['searchstring']
    file_path = request.form['filepath']
    x_percentage = request.form['xpercentage']
    column_numbers = request.form['column_numbers']
    column_numbers = map(int, column_numbers.split(','))
    x_percentage=float(x_percentage)
    c=0
    corpus=[]

    response = urllib2.urlopen(file_path)

    reader = csv.reader(response, dialect=csv.excel_tab, skipinitialspace=True, delimiter=',', quotechar='"')
    header =[]
    for row in reader:
        
        st=''
        
        if c!=0:
                if  row[column_numbers[0]].startswith('INC') :
                    i=0
                    while( i< len(column_numbers)):
                        st = st + row[column_numbers[i]]+';;;' 
                        i +=1
                    corpus.append(st)
        else:
            header = row            

        c = c+1  


    
        
    st = string_to_search
    corpus.insert(0,st) 

    # Removing special characters 
    new_header=[]
    for i in column_numbers:
        element = header[i]
        new_header.append(element)
    lower_case_corpus=[]
    for sentence in corpus:
        lower_case_corpus.append(sentence.lower())
  
    corpus_without_stopwords = [] 
    i=0
    l=len(lower_case_corpus)
    while i < l:
        lower_case_corpus[i] = lower_case_corpus[i].encode('utf-8')
        i+=1

    corpus_without_punctuation = remove_punctuation(lower_case_corpus)
    
    corpus_without_stopwords, my_stop_words = remove_stop_words(corpus_without_punctuation)
    my_stop_words = set(my_stop_words)
    # corpus_without_stopwords is corpus without punctuation also
    # corpus_without_stopwords is Array Of Sets
    # Add to every set their own 2 and 3 every subsets.
    new_corpus_without_stopwords = []

    for word, word_with_stopwords in itertools.izip_longest( corpus_without_stopwords, corpus_without_punctuation ):
        # s in notebook is now word in our proj
        

        #lower_case_corpus is a list of strings
        #and word_with_stopwords is a string
        word_to_string = word_with_stopwords   
        # Replacing punctuation marks with whitespace

        #word_to_string is a string    
        
        BagOf2words = ConsecutiveBagOfWords(word_to_string, 2)
        BagOf3words = ConsecutiveBagOfWords(word_to_string, 3)
        BagOf2words =  '-' + BagOf2words
        BagOf3words =  '-' + BagOf3words
        
        pat = r'(?<=\-).+?(?=\-)' 
        Array2 = re.findall(pat, BagOf2words)
        Array3 = re.findall(pat, BagOf3words)

        for word2,word3 in itertools.izip_longest(Array2,Array3):
            
            if word2 !=None:
                word2=word2.strip()
                setWord2 = set(word2.split(' '))
                if len(setWord2 & my_stop_words) == 0:
                    word.append(word2)

            if word3 !=None and len(word_to_string.split(' '))!=2:    
                word3 = word3.strip()
                setWord3 = set(word3.split(' '))
                if len(setWord3 & my_stop_words) == 0:
                    word.append(word3)
                    
        new_corpus_without_stopwords.append(word)
           
    if not new_corpus_without_stopwords[0]:
        return render_template('NotFound.html')
    
    values =  BagOfWords(new_corpus_without_stopwords)
    
    final_output_dict = FinalOutput(values, corpus, x_percentage, st )  

    dict_copy_list = list(final_output_dict)
    dict_new_copy_list = []
    for item in dict_copy_list:
        arr = item.split(';;;')
        dict_new_copy_list.append(arr)
    if not dict_copy_list:
        return render_template('NotFound.html')

    else:
        return render_template('print.html',dict_copy_list = dict_new_copy_list,st=st,header = new_header,column_numbers=column_numbers)
    






def FinalOutput(values, corpus, x_percentage, st):
    l = {}
    l = {k:v for (k,v) in zip(corpus,values)}
    import operator
    sorted_d = sorted(l.items(), key=lambda x: x[1])
    d = dict(sorted_d)
    
    x1 = sorted(l.iteritems(), key=lambda (k,v): (v,k))
    
    dict_to_list = list(d.values())
    len_l=len(l)
    if not any(dict_to_list):
            return []
    min_val = min([n for n in dict_to_list  if n>0])
    
    max_val = max([n for n in dict_to_list  if n<99999])
    
    range_uniq = float(max_val - min_val)
    half_range = (x_percentage * range_uniq/100.0)
    threshold = min_val + half_range 
    d_copy = dict(d)
    
    final_list=[]
    
    for pair in x1:
        (key,value) = pair
       
        if value <= threshold  and value > 0:
            final_list.append(key)
    final_list.remove(st)
    return final_list    


if __name__ == '__main__':
   app.run()
