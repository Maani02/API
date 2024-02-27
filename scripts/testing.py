import pandas as pd
import requests
import json
import os


stri= 'gh api repos/'+collector+ '/traffic/popular/paths --method GET > ../jsonRefOutput/' +collector+ '.json'
os.system(stri)

#create csv files from the Json files
f=open('../jsonRefOutput/'+collector+ '.json')
JsonData=json.load(f)
   # print(JsonData)
   # temp=enumerate(JsonData)
for i, value in (enumerate(JsonData)):
    df= pd.DataFrame(JsonData)
    df.to_csv("../csvRefOutput/" +collector+".csv", mode='a', index=False, header=False)
f.close()
username='muneeb-mbytes'
path='/home/aniruddh/API/collector/csvRefOutput/'
request=requests.get('https://api.github.com/users/'+muneeb-mbytes+'/repos?per_page=1000')
JsonData=request.json()

