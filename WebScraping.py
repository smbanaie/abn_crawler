import pandas as pd
import os, shutil, requests, zipfile, io
from datetime import datetime

def get_data(url):
    
    #Get data
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    date=datetime.today().strftime('%Y%m')
    fid='BUSINESS_NAMES_'+date+'.csv'
    print('File:',fid)
    fid = z.extract(fid)
    
    #Read
    date_parser = lambda x: pd.to_datetime(x, format='%d/%m/%Y', errors='coerce')
    date_cols=['BN_REG_DT','BN_CANCEL_DT','BN_RENEW_DT']
    df=pd.read_csv(fid, delimiter='\t', parse_dates=date_cols, date_parser=date_parser)
    
    #Label
    df['New_Registration']=df.apply(lambda x: 'Yes' if (pd.Timestamp.today()-x['BN_REG_DT'])<=pd.Timedelta('7 days') else 'No', axis=1)
    df['New_Cancellation']=df.apply(lambda x: 'Yes' if (pd.Timestamp.today()-x['BN_CANCEL_DT'])<=pd.Timedelta('7 days') else 'No', axis=1)
    
    return df

#Params
url='https://data.gov.au/data/dataset/bc515135-4bb6-4d50-957a-3713709a76d3/resource/839cc783-876f-47a2-a70c-0fe606977517/download/business_names_202001.zip'
df=get_data(url)

#Save
path=r"C:\Users\Behrang.ZadJabbari\Documents\ABN_Downloads"
date=datetime.today().strftime('%Y_%m_%d')
df.to_csv(os.path.join(path,'ABN_download_'+date+'.csv'),index=False)

df