import pandas as pd
import re
import numpy as np
df=pd.read_csv("data/simplified.csv",sep=";",decimal=",")
#print df
#print df.columns
class Variable:
    def __init__(self,input):
        self.name=input
        components=input.split("_")
        if len(components) > 0:
            self.basename=components[0]
        self.event=components[len(components)-1]
        self.n_name=self.basename+"_"+self.event

    def __str__(self):
        return "Basename: "+self.basename+" Event: "+self.event

    def __eq__(self, other):
        if self.n_name==other.n_name:
            return True
        else:
            return False



colums=df.columns.values

nomeds=[s for s in colums if "REAL" in s or "STRING" in s]
vars=[Variable(s) for s in nomeds]
def printasline(tmp):
    for i in tmp:
        print i

def reduceNames(tmp):
    l=[Variable(s).n_name for s in tmp]
    l=list(set(l))
    return l
print len(nomeds)
basenames=reduceNames(nomeds)
print len(basenames)
vars=[Variable(s) for s in nomeds]
for i in basenames:
    print "Basename: ",i
    t_vars=[s for s in vars if s.n_name == i]
    print "Found Variables: ", t_vars
    df[i]=np.nan
    for t in t_vars:
        if t.name != i:
            print "deleted: " ,t.name, "Merged with ",i
            df[i].fillna(df[t.name], inplace=True)
            df.drop(t.name,axis=1,inplace=True)

#print df
print len(df[" paseS_E5"])
print len(df[" paseS_E5"] != None)
df.to_csv("data/finished.csv",sep=";",decimal=",",index=False)
printasline(df.columns.values)
printasline(df["Study Subject ID"])
print len(df[" paseS_E5"])
subs=pd.DataFrame(sorted(list(df["Study Subject ID"].values)))
subs.to_csv("data/keepSubs.txt",header=False,index=False)



#printasline(nomeds)
