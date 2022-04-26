from cmath import pi
import math

def init_from_file(src: str, pipath: str): 
    ''' 
        T: 
            klucze: słowa polskie (s)
            wartości:
                klucze: tłumaczenia (t) słów (s) w formie ngramów angielskich słów
                wartości: liczby wystąpień (t) jako tłumaczeń (s) w korpusie równoległym
        N:
            klucze: ngramy (t) angielskich słów w korpusie równoległym (tym samym w T)
            wartości: liczby wystąpień (t) w korpusie równoległym    
    '''
    T = {}
    N = {}
    with open(src,mode="r") as f:
        line = ' '
        while line:
            line = f.readline()
            pair = line.split(';')
            if len(pair)<2:
                break
            s = pair[0]
            t = pair[1].rstrip()
            if t in N.keys():
                N[t]+=1
            else:
                N[t]=1
            if s not in T.keys():
                T[s]={t:0}
            if t in T[s].keys():
                T[s][t]+=1
            else:
                T[s][t]=1
    
    with open(pipath,mode="w") as w:
        for s in T.keys():
            l = [[ngram,numb] for ngram,numb in T[s].items()]
            for i in range(len(l)):
                t = l[i][0]
                p = l[i][1]
                l[i][1] = math.log(p)-math.log(N[t])
            sSorted = sorted(l, key=lambda tup: tup[1], reverse=True)
            line = s+":"
            for trans in sSorted:
                line+=f'{trans[0]},{trans[1]};'
            line+="\n"
            w.write(line)
    

def get_top_translations(pipath: str, word: str, n = 10):
    topTr = []
    with open(pipath) as f:
        line = ' '
        while line:
            line = f.readline()
            pair = line.split(':')
            if len(pair)<2:
                break
            pl = pair[0]
            if pl==word:
                ts = pair[1].rstrip().split(';')
                for i in range(min(n,len(ts))):
                    pair = ts[i]
                    if len(pair)<2:
                        break
                    p = pair.split(',')
                    prob = float(p[1])
                    # en = p[0].split(' ')
                    en = p[0]
                    topTr.append((en,prob))    
    return topTr

