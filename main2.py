from cmath import inf
import PiMatrix as p
import os
import math

def servProb(ngram: str):
    return 0.5
    
def sentProb(sparts: str, trans: str):
    result = 0
    ngram = ""
    print(sparts+'|'+trans,':')
    sentp = sparts+" "
    for i in range(1,len(trans)+1):
        if i<3:
            if sparts=="":
                ngram = trans[:i]
            else:
                ngram = sentp[i-3:]+trans[:i]
        else:
            ngram = trans[i-3:i]
        print(i,ngram+'|',)
        result += math.log(servProb(ngram))
    result/=len(trans)
    return result
        

def translate(source:str ,Pi: str):
    result = ""
    words = source.split(' ')
    for word in words:
        ttrans = p.get_top_translations(Pi,word)
        bprob = -inf
        btrans = None
        for (trans,tprob) in ttrans:
            lprob = sentProb(result, trans)
            prob = lprob + tprob
            if bprob<prob:
                bprob = prob
                btrans = trans
        if btrans != None:
            if result == "":
                result = btrans
            else:
                result += " " + btrans
    return result 


if __name__ == "__main__":

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # format wiersza:    slowo;tlum
    corpora = os.path.join(__location__,'korpus.txt')
    
    # format wiersza:     slowo:tlum1,prawd1;tlum2,prawd2;...
    PiMatrixFile = os.path.join(__location__,'pi.txt')
    
    p.init_from_file(corpora,PiMatrixFile)
    # inp = input("Wczytaj polskie zdanie/slowo:\n")
    inp = "lubie chodzic po miescie"
    print(inp)
    print(translate(inp.lower(),PiMatrixFile))