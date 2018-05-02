import pandas as pd
import natsort
import numpy as np
import argparse

def dropAndCleanID(df,subj):
    if subj in df.index:
        print "succsessfully removed", subj
        df.drop(subj, inplace=True)
        df.dropna(axis=1,how="all",inplace=True)
    return df

def mergeColumns(df,basename):
    columns=[]
    for i in df.columns.values:
        if(basename in i):
            columns.append(i)
    columns = natsort.natsorted(columns)
    df[basename] = np.nan
    for i in columns:
        if ("Medikament" not in i):
            df[basename].fillna(df[i],inplace=True)
            df.drop(i,axis=1,inplace=True)
    return df

def subjFile2List(in_File):
    with open(in_File) as f:
        out = f.readlines()
    out = [x.rstrip() for x in out]
    #print out
    return out

def main(file,out_file,subj_file,rows):
    df = pd.read_csv(file,sep="\t",skiprows=rows,index_col=0)
    print "Indices: ", df.index.values
    if(subj_file != None):
        subj_list=subjFile2List(subj_file)
        c= len(df.columns.values)
        for i in subj_list:
            print "removing ", i
            if i in df.index:
                print "succsessfully removed", i
                df.drop(i, inplace=True)
                df.dropna(axis=1, how="all", inplace=True)
        print "Removed: ", c-len(df.columns.values), " Columns"
        print "Indices: ", df.index.values
    #df = mergeColumns(df,"WMSRZsv_E7")
    columns = getColumsToMerge(df)
    print len(columns)
    columns = list(set(columns))
    for i in columns:
        df=mergeColumns(df,i)
    cols = df.columns.values
    cols = sorted(cols,key= lambda x: x.split("_")[-1:])
    df=df[cols]
    # convert columns to numeric if possible
    for i in cols:
        try:
            df[i]=pd.to_numeric(df[i],errors="raise")
            print "Converted: ",i
        except:
            pass

    df.to_csv(out_file,header=True,index=True,sep=";",decimal=",")
    #df.to_excel(out_file,header=True,index=True)


def getColumsToMerge(df):
    basenames =[]
    for i in df.columns.values:
        tmp = i.split("_")
        if(len(tmp) > 2):
            if("Medikament" not in i):
                event_ecrf = tmp[-2:]
                tmp=tmp[:len(tmp)-2]
                basenames.append("_".join(tmp)+"_"+event_ecrf[0])
            # else:
            #     print "added basename " + "_".join(tmp) + "_" + event_ecrf[0]
            #     basenames.append(i)

    return basenames

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CleanUp OpenClinica ODM File, TABLES still hardcoded only usable for AgeGain")
    parser.add_argument("-i",metavar="IN_FILE",type=str,help="path/name of the ODM File to clean",required=True)
    parser.add_argument("-o",metavar="OUT_FILE",type=str,help="path/name of the Outfile as csv",required=True)
    parser.add_argument("-s",metavar="subj_file",type=str,help="path/filename of the list of subjects to remove")
    parser.add_argument("-rows",metavar="num_rows",type=int,help="Number of rows to skip in In_File",required=True)
    param = parser.parse_args()
    main(param.i,param.o,param.s,param.rows)