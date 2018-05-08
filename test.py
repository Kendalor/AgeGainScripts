import pandas as pd
import itertools
import operator

if __name__ == "__main__":
    f=open("data/complete.tsv")
    column=[]
    for i in range(0,100):
        column.append(len(f.readline().split("\t")))
    test=[[i for i,value in it] for key,it in itertools.groupby(enumerate(column), key=operator.itemgetter(1)) if key !=0]
    print test[-1][0]
    print column