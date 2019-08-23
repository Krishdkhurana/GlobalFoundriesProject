from flask import Flask, redirect, url_for, request, render_template
"""
"""
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
#sys.setdefaultencoding('unicode')
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
    #####print(complete_string)
    #if num_of_words in complete_string > num_of_words
    if NumOfWords(complete_string) > num_of_words:
        # recursion call
        return " ".join(str(x) for x in  [ConsecutiveBagOfWords(StringAfterFirstWord(complete_string), num_of_words),(FirstnNumOfWords(complete_string,num_of_words)),'-'])
        #return " ".join(str(x) for x in  [ConsecutiveBagOfWords(complete_string[1:],num_of_words),(complete_string[:num_of_words])])

    else:
        return complete_string+'-'

def computeTF(wordDict, bow):
    #####print 'bow for TF function'
    #####print bow
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict
def remove_stop_words(lower_case_corpus):
    my_stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
    my_stop_words.extend(["Global Foundry View","Foundry View","FoundryView","GlobalFoundryView","foundry view","foundry",'GlobalFoundry View'])
    array_of_sets = []
    #s = lower_case_corpus[0]
    #########print(s)
    #########print(set([s])-my_stop_words)
    for sentence in lower_case_corpus:

        
        sentence = sentence.split(" ")
        #sentence_without_stop_words = sentence - my_stop_words
        sentence_without_stop_words = [x for x in sentence if x not in my_stop_words]
        # sentence_without_stop_words contains the strings as elemenst of a set    
        array_of_sets.append(sentence_without_stop_words)
    return array_of_sets, my_stop_words 


#corpus_without_punctuation = remove_punctuation(lower_case_corpus)
# return a list of strings
 
def remove_punctuation(lower_case_corpus):

    list_of_strings = []

    for sentence in lower_case_corpus:

        sentence = sentence.rstrip(string.punctuation)
        replace_punctuation = string.maketrans(string.punctuation,' '*len(string.punctuation))
        sentence = sentence.translate(replace_punctuation)
        sentence = re.sub(' +',' ',sentence)
        list_of_strings.append(sentence)

    return list_of_strings   
"""    
def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] +=1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))+1
        #idfDict[word] = 1

    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf    

def calculateEuclidianDistance(listA, listB):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(listA, listB)]))
    return distance


def normalize(lst):
    s = sum(lst)
    n = len(lst)
    mean  = s/n
    return map(lambda x: float(x)/mean, lst)
"""

#Now we have to create the BagOfWords

def BagOfWords(corpus_without_stopwords):
    values = []

    num_of_words_in_sentence_to_search = len(corpus_without_stopwords[0])
    #corpus_without_stopwords = set(corpus_without_stopwords)
    for bowB in corpus_without_stopwords:

        ####print bowB
        wordSet = list(set().union(bowB,corpus_without_stopwords[0]))
        #wordSet = set(corpus_without_stopwords[0])
        #####print'Word set is'
        #####print wordSet
        wordDictA = dict.fromkeys(wordSet, 0)
        wordDictB = dict.fromkeys(wordSet, 0)    


        for word in corpus_without_stopwords[0]:
            wordDictA[word]+=1
        for word in bowB:
            if word in wordSet:
                wordDictB[word]+=1 
        #####print('word dict A')        
        #####print wordDictA
        #####print('word dict B')
        #####print wordDictB  
        #####print'Sentence 2 is down'
        #####print bowB         
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
            #print tfBowB
            #print 'no of words matched'
            #print flag
            ###print 'Score is'
            ###print fraction
            #print '\n --------------'      

        else :
            fraction = 0.0  
        
        """        
        if flag !=0:        
            fraction =math.log10( float(num_of_words_in_sentence_to_search)/flag ) + 1.0        
        else:
            fraction = 0.0 
        """    
        """
        #######print bowB   
        #####print 'Term Frequency'        
        #####print tfBowB          
        ######print '------------------------------'
        idfs = computeIDF([wordDictA, wordDictB])
        ######print 'INVERSE DOC FREQUENCY'
        #######print idfs
        ######print '------------------------------'
        ######print('Inverse Documnet Freq')
        #######print(idfs)
        ######print('\n')
        tfidfBowA = computeTFIDF(tfBowA, idfs)
        tfidfBowB = computeTFIDF(tfBowB, idfs)
    
        #########print('W.r.t tfidf both')
        #########print(pd.DataFrame([tfidfBowA, tfidfBowB]))
        #########print(tfidfBowA)
        #########print(tfidfBowB)
        #########print('\n')
        listA = list(tfidfBowA.values())
        listB = list(tfidfBowB.values())
        a = sum(listA)
        b = sum(listB)
        listA = normalize(listA)
        listB = normalize(listB)
        #########print(listA)
        #########print(listB)
        score = calculateEuclidianDistance(listA, listB)
        #####print bowB
        #####print tfBowB
        #####print idfs
        #####print flag
        #####print num_of_words_in_sentence_to_search
        #####print fraction
        #####print score
        
        #score  = score * fraction
        """
        score = fraction
        #####print score
        #####print'\n'
        #####print'-------------------'

        #####print(score)
        values.append(score)
    #####print values
    return values






@app.route('/handle_data', methods=['POST'])
def handle_data():
    #projectpath = request.form['projectFilepath']
    string_to_search = request.form['searchstring']
    file_path = request.form['filepath']
    x_percentage = request.form['xpercentage']
    #a = request.form['inciddent_num'] 
    #b = request.form['incident_des']
    column_numbers = request.form['column_numbers']
    column_numbers = map(int, column_numbers.split(','))
    #args = [a,b]
    #args[0] = int(args[0])
    #args[1] = int(args[1])
    #a = args[0]
    #b = args[1]
    x_percentage=float(x_percentage)
    #return type(string_to_search),type(file_path),type(x_percentage),type(a) 
    #gdd.download_file_from_google_drive(file_id=file_path,dest_path='./data/mnist.zip',unzip=True)
    #s = requests.get(file_path).content
    c=0
    corpus=[]


     
    #result = urllib2.urlopen(file_path)
    #cr = csv.reader(response)
    #result = parts(result,"\n")
    response = urllib2.urlopen(file_path)

    #Reading a single file
    #reader = csv.reader(iter(gcs_file.readline, ''), dialect=csv.excel_tab,skipinitialspace=True, delimiter=',', quotechar='"')
    reader = csv.reader(response, dialect=csv.excel_tab, skipinitialspace=True, delimiter=',', quotechar='"')
    header =[]
    for row in reader:
        
        st=''
        
        if c!=0:
                if  row[column_numbers[0]].startswith('INC') :
                    i=0
                    while( i< len(column_numbers)):
                        #if i == 0:
                        #st = row[column_numbers[0]]+' '     
                        #else:    
                        st = st + row[column_numbers[i]]+';;;' 
                        i +=1
                    #st = row[args[0]]+' '+row[args[1]]
                    ########print row
                    ########print st
                    corpus.append(st)
        else:
            header = row            

        c = c+1  


    
    #df=pd.read_csv( file_path , sep=',', engine='python')
    #df = pd.read_csv(file_path)
    
    #df[args[0]]=df[args[0]].astype(str)
    #row = df[args[0]]+' '+df[args[1]]
    
    st = string_to_search
    #corpus = row
    #corpus = corpus.tolist()
    corpus.insert(0,st) 

    # Removing special characters 

    

    new_header=[]
    for i in column_numbers:
        element = header[i]
        new_header.append(element)

    #print new_header
    lower_case_corpus=[]
    #return (corpus[0].lower)
    for sentence in corpus:
        lower_case_corpus.append(sentence.lower())
    #########print(lower_case_corpus)    
    corpus_without_stopwords = [] 
    i=0
    l=len(lower_case_corpus)
    while i < l:
        lower_case_corpus[i] = lower_case_corpus[i].encode('utf-8')
        i+=1
    ####print lower_case_corpus
    corpus_without_punctuation = remove_punctuation(lower_case_corpus)
    ####print corpus_without_punctuation
    
    corpus_without_stopwords, my_stop_words = remove_stop_words(corpus_without_punctuation)
    my_stop_words = set(my_stop_words)
    # corpus_without_stopwords is corpus without punctuation also
    # corpus_without_stopwords is Array Of Sets
    #####print corpus_without_stopwords
    # Add to every set their own 2 and 3 every subsets.
    ####print corpus_without_stopwords
    ####print corpus_without_stopwords
    ####print type(corpus_without_stopwords)
    new_corpus_without_stopwords = []
    #print corpus_without_stopwords
    #print ' ------------------'
    #print lower_case_corpus
    for word, word_with_stopwords in itertools.izip_longest( corpus_without_stopwords, corpus_without_punctuation ):
        # s in notebook is now word in our proj
        

        #lower_case_corpus is a list of strings
        #and word_with_stopwords is a string
        #word_to_string = ' '.join(word_with_stopwords)
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
        #print new_corpus_without_stopwords     
        ##print word
    """   
    for w in new_corpus_without_stopwords:     
        print w
        print '\n'            
    """    
    if not new_corpus_without_stopwords[0]:
        return render_template('NotFound.html')
    
    #print new_corpus_without_stopwords[0]
    values =  BagOfWords(new_corpus_without_stopwords)
    #########print(values)
    final_output_dict = FinalOutput(values, corpus, x_percentage, st )  

    dict_copy_list = list(final_output_dict)
    dict_new_copy_list = []
    for item in dict_copy_list:
        arr = item.split(';;;')
        dict_new_copy_list.append(arr)
    #dict_copy_list.remove(st)

    #print(dict_copy_list)
    #print dict_new_copy_list
    if not dict_copy_list:
        return render_template('NotFound.html')

    else:
        return render_template('print.html',dict_copy_list = dict_new_copy_list,st=st,header = new_header,column_numbers=column_numbers)
    #return render_template("index.html", user_image = full_filename)







def FinalOutput(values, corpus, x_percentage, st):
    l = {}
    l = {k:v for (k,v) in zip(corpus,values)}
    import operator
    sorted_d = sorted(l.items(), key=lambda x: x[1])
    #########print(sorted_d) 
    d = dict(sorted_d)
    #########print(d)
    x1 = sorted(l.iteritems(), key=lambda (k,v): (v,k))
    #####print('-------------')
    #####print(x1)
    dict_to_list = list(d.values())
    ######print dict_to_list
    #len_uniq_val = len(dict_to_list)
    #########print(dict_to_list)
    len_l=len(l)
    #print l
    if not any(dict_to_list):
            return []
    min_val = min([n for n in dict_to_list  if n>0])
    ########print min_val
    max_val = max([n for n in dict_to_list  if n<99999])
    ########print(max_val)
    #min_val = dict_to_list[1]
    
    #max_val = dict_to_list[len_uniq_val-1]
    range_uniq = float(max_val - min_val)
    half_range = (x_percentage * range_uniq/100.0)
    threshold = min_val + half_range 
    d_copy = dict(d)
    #d_copy = pd.Series(d_copy)
    #dict_copy=d_copy.to_frame()
    #dict_copy.columns = ['score']
    #dict_copy = dict_copy.drop(dict_copy[dict_copy.score > threshold].index)                
    #return dict_copy

    final_list=[]
    """
    for key,value in sorted(d.iteritems(), key=lambda (k,v): (v,k)):
        if value > threshold :
            final_list.append(key)
    """
    for pair in x1:
        (key,value) = pair
        ######print key
        ######print value
        ######print threshold
        if value <= threshold  and value > 0:
            final_list.append(key)
    final_list.remove(st)
    return final_list    


if __name__ == '__main__':
   app.run()
