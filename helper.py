import pandas as pd
import spacy
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet as wn
from string import punctuation
nlp = spacy.load("en_core_web_sm")


def extract_genre(genre_json):
    if len(genre_json) > 0:
        return genre_json[0]["name"]
    else:
        return ""

def extract_cast(cast):
    if len(cast) > 0:
        return cast[0]["name"]
    else:
        return ""

def create_dummies( df, colname ):
    col_dummies = pd.get_dummies(df[colname], prefix=colname)
    df = pd.concat([df, col_dummies], axis=1)
    df.drop( colname, axis = 1, inplace = True )
    return df

def get_hotwords(text):
    result = []
    pos_tag = ['NOUN'] 
    doc = nlp(text.lower()) 
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.text)
    return " ".join(result)


def keywords_inventory(dataframe, colonne ):
    PS = nltk.stem.PorterStemmer()
    keywords_roots  = dict()  # collect the words / root
    keywords_select = dict()  # association: root <-> keyword
    category_keys = []
    icount = 0
    for s in dataframe[colonne]:
        if pd.isnull(s): continue
        for t in s.split(' '):
            t = t.lower() ; racine = PS.stem(t)
            if racine in keywords_roots:                
                keywords_roots[racine].add(t)
            else:
                keywords_roots[racine] = {t}
    
    for s in keywords_roots.keys():
        if len(keywords_roots[s]) > 1:  
            min_length = 1000
            for k in keywords_roots[s]:
                if len(k) < min_length:
                    clef = k ; min_length = len(k)            
            category_keys.append(clef)
            keywords_select[s] = clef
        else:
            category_keys.append(list(keywords_roots[s])[0])
            keywords_select[s] = list(keywords_roots[s])[0]
    print("Nb of keywords in variable '{}': {}".format(colonne,len(category_keys)))
    return category_keys, keywords_roots, keywords_select

def remplacement_df_keywords(df, dico_remplacement, roots = False):
    df_new = df.copy(deep = True)
    PS = nltk.stem.PorterStemmer()
    for index, row in df_new.iterrows():
        chaine = row['overview']
        if pd.isnull(chaine): continue
        nouvelle_liste = []
        for s in chaine.split(' '): 
            clef = PS.stem(s) if roots else s
            if clef in dico_remplacement.keys():
                nouvelle_liste.append(dico_remplacement[clef])
            else:
                nouvelle_liste.append(s)       
        df_new.at[index, 'overview']=  ' '.join(nouvelle_liste)
    return df_new


def get_synonymes(mot_cle):
    lemma = set()
    for ss in wn.synsets(mot_cle):
        for w in ss.lemma_names():
            #_______________________________
            # We just get the 'nouns':
            index = ss.name().find('.')+1
            if ss.name()[index] == 'n': lemma.add(w.lower().replace('_',' '))
    return lemma  

def create_syndict(movies):
    syn_dict ={}
    for index, row in movies.iterrows():
        words = row.overview.split(" ")
        for word in words:
            syns = get_synonymes(word)
            syns.add(word)
            syns = set(syns)
            for syn in syns:
                if syn in syn_dict.keys():
                    syn_dict[syn] =  syn_dict[syn] +1 
                else:
                    syn_dict[syn] = 1
    return syn_dict