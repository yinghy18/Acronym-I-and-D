# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 15:13:18 2021

@author: yinghy
"""

#import xml.etree.ElementTree as ET
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize

stops = set(stopwords.words('english'))
puncts = set(['!',',','.','?','-s','-ly','</s>','-','/'])

def f1(true,pred):
    true = set(true)
    pred = set(pred)
    tp = len(true & pred)
    
    if len(pred) == 0:
        pr = int(len(true) == 0)
    else:
        pr = tp/len(pred)
    if len(true) == 0:
        rec = int(len(pred) == 0)
    else:
        rec = tp/len(true)
    if pr+rec != 0:
        f = 2*pr*rec/(pr+rec)
    else:
        f = 0
    
    return pr,rec,f

def isacronym(token):
    if len(token)<2 or len(token) > 10:
        return False
    count = 0
    count_num = 0
    
    for i in token:
        if i in ['0','1','2','3','4','5','6','7','8','9']:
            count_num += 1
            continue
        count += i.isupper()
    if count+count_num < len(token)/3 or count_num >= 2*len(token)/3 or count == 0:
        return False
    
    return True
    
def findlong_letter(token,tokens):
    for i in range(len(tokens)):
        if token in tokens[i] and '(' in tokens[i]:
            count = i
            break
            
    if count < 1:
        return []
    l = []
    tokens = tokens[:count]
    for length in range(1,min(count,len(token)+5,2*len(token))+1):
        for start in range(count):
            if start + length == count and tokens[start] not in stops and tokens[start+length-1] not in stops:
                longword = tokens[start:start+length]
                if token not in longword:
                    l.append(' '.join(tokens[start:start+length]))
                
    return l            
        

def lettermatch_1to1(sf,lf):
    sindex = len(sf)-1
    lindex = len(lf)-1
    
    for i in range(sindex,0,-1):
        currchar = sf[i]
        if currchar in puncts:
            continue
        currchar = currchar.lower()
        while (lindex >= 0 and lf[lindex].lower()!=currchar):
            lindex += -1
        
        lindex += -1
            
        if lindex < 0:
            return False
        
    return sf[0].lower() == lf[0].lower()

def lettermatch(sf,lf):
    if sf[-1] == '1':
        return (lettermatch_1to1(sf[:-1]+'I',lf) or lettermatch_1to1(sf,lf))
    if sf[-1] == '2':
        return (lettermatch_1to1(sf[:-1]+'II',lf) or lettermatch_1to1(sf,lf))
    if sf[-1] == '3':
        return (lettermatch_1to1(sf[:-1]+'III',lf) or lettermatch_1to1(sf,lf))
    if sf[-1] == 'I':
        return (lettermatch_1to1(sf[:-1]+'1',lf) or lettermatch_1to1(sf,lf))
    if sf[-2:] == 'II':
        return (lettermatch_1to1(sf[:-2]+'2',lf) or lettermatch_1to1(sf,lf))
    if sf[-3:] == 'III':
        return (lettermatch_1to1(sf[:-3]+'3',lf) or lettermatch_1to1(sf,lf))
    return lettermatch_1to1(sf,lf)
    
               
def extract(text):
    m = []
    l = []
    sents = sent_tokenize(text)
    for t in sents:
        tokens = t.split(' ')
        for i in tokens:
            if i[0] == '(':
                if i[-1] == ')':
                    token = i[1:-1]
                elif ')' in i:
                    a = i.find(')')
                    token = i[1:a]
                else:
                    token = i[1:]
                
                if isacronym(token):
                    while token[-1] in puncts:
                        token = token[:-1]
                    m.append(token)
                    long = findlong_letter(token,tokens)
                    l.append(long)
      
    true_l = []              
    for i in range(len(m)):
        true_l_beixuan = []
        for j in range(len(l[i])):
            if lettermatch(m[i],l[i][j]) == True:
                true_l_beixuan.append(l[i][j])
        true_l.append(true_l_beixuan)
                
    return m,l,true_l

def output_sflf_pair(text):
    short_form_candidate,long_form_candidate,true_long_form = extract(text)
    short_long_pair = []
    for i in range(len(short_form_candidate)):
        sf = short_form_candidate[i]
        lf = true_long_form[i]
        if lf != []:
            for lf_candidate in lf:
                short_long_pair.append((sf,lf_candidate))
                
    return short_form_candidate,short_long_pair


if __name__=='__main__':
    #given a sentence or long sentence
    text = 'A specific human lysophospholipase: cDNA cloning, tissue distribution and kinetic characterization. Lysophospholipases are critical enzymes that act on biological membranes to regulate the multifunctional lysophospholipids; increased levels of lysophospholipids are associated with a host of diseases. Herein we report the cDNA cloning of a human brain 25 kDa lysophospholipid-specific lysophospholipase (hLysoPLA). The enzyme (at both mRNA and protein levels) is widely distributed in tissues, but with quite different abundances. The hLysoPLA hydrolyzes lysophosphatidylcholine in both monomeric and micellar forms, and exhibits apparent cooperativity and surface dilution kinetics, but not interfacial activation. Detailed kinetic analysis indicates that the hLysoPLA binds first to the micellar surface and then to the substrate presented on the surface. The kinetic parameters associated with this surface dilution kinetic model are reported, and it is concluded that hLysoPLA has a single substrate binding site and a surface recognition site. The apparent cooperativity observed is likely due to the change of substrate presentation. In contrast to many non-specific lipolytic enzymes that exhibit lysophospholipase activity, hLysoPLA hydrolyzes only lysophospholipids and has no other significant enzymatic activity. Of special interest, hLysoPLA does not act on plasmenylcholine. Of the several inhibitors tested, only methyl arachidonyl fluorophosphonate (MAFP) potently and irreversibly inhibits the enzymatic activity. The inhibition by MAFP is consistent with the catalytic mechanism proposed for the enzyme - a serine hydrolase with a catalytic triad composed of Ser-119, Asp-174 and His-208.'
    short_form,short_long_pair = output_sflf_pair(text)
            


'''
#---------The following are dealing with specific xml file-----------#
tree = ET.parse('bioadi_bioc_gold.xml')

texts = []
loc = []
tags = []

root = tree.getroot()

for i in range(3,len(root)):
    t= []
    l = []
    for child in root[i][1]:
        if child.tag == 'annotation':
            t.append(child[-1].text)
            l.append(child[-2].attrib)
        if child.tag == 'text':
            texts.append(child.text)
            
    tags.append(t)
    loc.append(l)
  
sf_res = []
pair_res = []
      
with open('bioadi_lettermatch.txt','w',encoding = 'utf-8') as f:
    for i in range(len(texts)):
        f.write(texts[i]+'\n')
        sfs = []
        lfs = []
        sflfs = []
        for j in range(len(loc[i])):
            f.write(str(loc[i][j])+'\t'+tags[i][j]+'\n') 
            if j % 2 == 0:
                sfs.append(tags[i][j])
            else:
                lfs.append(tags[i][j])
                sflfs.append((tags[i][j-1],tags[i][j]))
            
        m,l,true_l = extract(texts[i])     
        f.write('sf: '+str(m)+'\n')
        f.write('lf_candidate: '+str(l)+'\n')
        f.write('sf-lf: '+str(true_l)+'\n')
        
        sl = []
        for i in range(len(m)):
            if true_l[i] !=[]:
                for tl in true_l[i]:
                    sl.append((m[i],tl))
        sf_res.append(f1(sfs,m))
        pair_res.append(f1(sflfs,sl))
        
            
        f.write('\n')
   
#-----------end-----------#     
'''      
        
        
        