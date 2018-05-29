import pandas as pd
import numpy as np
import argparse

def main(param):
    df=pd.read_csv(param.i,sep=param.delimiter,decimal=param.decimal)
    cols=df.columns.values
    print cols
    print "Total Cols: ",len(cols)
    n_cols= df.select_dtypes(include=[np.number]).columns.values
    o_cols= df.select_dtypes(include=[np.object]).columns.values
    print "Numeric Cols: ",len(n_cols)
    print "Object Cols: ",len(o_cols)
    outlier_cols=[]
    df_out=pd.DataFrame()
    for i in n_cols:
        #print "Column: ",i
        temp=df.loc[np.abs(df[i]-df[i].mean()) > (param.d*df[i].std()),['Study Subject ID',i]]
        if len(temp > 0):
            #print "Temp: \n ",temp
            for index,row in temp.iterrows():
                #print temp.loc[index,:]
                df_out=df_out.append({'Study Subject ID':temp.loc[index,'Study Subject ID'],"Outlier In": i,"Value": temp.loc[index,i]},ignore_index=True)

    print df_out
    df_out=df_out.sort_values("Study Subject ID")
    df_out.to_csv(param.o,header=True,index=False,decimal=param.decimal,sep=param.delimiter)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finds Outliers in a csv file per column")
    parser.add_argument("-i",metavar="in_file",type=str,help="path/name of the CSV File to clean",required=True)
    parser.add_argument("-o",metavar="out_file",type=str,default="outliers.csv",help="path/name of the Outfile as csv",required=False)
    parser.add_argument("-d",metavar="x",type=float,default=3,help="Outliers if abs(x-mean)> d*std")
    parser.add_argument("-delimiter", metavar="delimiter", type=str,default=";", help="delimiter used in CSV File", required=False)
    parser.add_argument("-decimal", metavar="decimal", type=str,default=",", help="decimal separator used in CSV File", required=False)

    param = parser.parse_args()
    print param
    main(param)