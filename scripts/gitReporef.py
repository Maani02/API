import requests
import json
import os
import pandas as pd
from datetime import date,timedelta
import time
import math

def zeroesToEmptyFile(reponame,flag):
    a=[]
    today=date.today()
    for i in range(15,0,-1):
        b=[]
        newdate=str(today-timedelta(i))
        b.append(newdate)
        b.append(0)
        b.append(0)
        a.append(b)
    zeroes=pd.DataFrame(columns=['Date', 'views','unique'])
    for i in range(len(a)):
        zeroes.loc[len(zeroes)]=a[i]


    if(flag==0):
        #fresh data
        if(os.path.exists(old_csv_name)):
            removePath="rm "+old_csv_name
            os.system(removePath)
        zeroes.to_csv("../csvRefOutput/" +reponame+".csv", mode='a', index=False, header=True)
    else:
        #update data
        zeroes.to_csv("../csvRefOutput/csvRefUpdateData/" +reponame+".csv", mode='a', index=False, header=True)

def merge_csv(reponame):
    
    data = pd.read_csv(csv_name,header=None)
    oldData = pd.read_csv(old_csv_name,header=None)
    newdata=pd.concat([oldData,data])
    newCleanData=newdata.drop_duplicates(keep='last')
    removePath="rm "+old_csv_name
    os.system(removePath)
    newCleanData.to_csv("../csvOutput/" +reponame+".csv", mode='a', index=False, header=False)
    
def updateRefData(reponame):
    flag=1
    print("Project Name:",reponame)
    stri= 'gh api repos/' +username+ '/' +reponame+ '/traffic/popular/paths --method GET > ../jsonRefOutput/' +reponame+ '.json'
    os.system(stri)

#create csv files from the Json files
    f=open('../jsonRefOutput/' +reponame+ '.json')
    JsonData=json.load(f)
   # print(JsonData)
    temp=enumerate(JsonData)
       # print(i)
    df= pd.DataFrame(list(temp))
        #print(df)
    df.to_csv("../csvRefOutput/csvRefUpdateData" +reponame+".csv", mode='a', index=False, header=False)
   # print(df)
    f.close()
    
    if(os.stat(old_csv_name).st_size == 0):
        print("empty file",reponame)
        zeroesToEmptyFile(reponame,flag)
   # time.sleep(10)
    df=pd.read_csv(old_csv_name,header=None)
    #df=removeTimestamp(df) 
    removePath="rm "+csv_name
    os.system(removePath)
    df.to_csv("../csvRefOutput/csvRefUpdateData/" +reponame+".csv", mode='a', index=False, header=False)
   # print("removed timestamp")
    merge_csv(reponame)
    #print("after merge")
    

def freshRefData(reponame):
    print("Project Name:",reponame)
    stri= 'gh api repos/' +username+ '/' +reponame+ '/traffic/popular/paths --method GET > ../jsonRefOutput/' +reponame+ '.json'
    os.system(stri)

#create csv files from the Json files
    f=open('../jsonRefOutput/' +reponame+ '.json')
    JsonData=json.load(f)
   # print(JsonData)
    temp=enumerate(JsonData)
    
    df= pd.DataFrame(list(temp))
    df.to_csv("../csvRefOutput/" +reponame+".csv", mode='a', index=False, header=False)
    f.close()
#user data
username='muneeb-mbytes'
path='/home/aniruddh/API/collector/csvRefOutput/'
request=requests.get('https://api.github.com/users/'+username+'/repos?per_page=1000')
JsonData=request.json()

#store various repo names into an array
repoName=[]
for i in range (0,len(JsonData)):
    if(JsonData[i]['name']=='.github'):
        continue
    if(JsonData[i]['name']=='mbits-mirafra.github.io'):
        continue
    repoName.append(JsonData[i]['name'])

for i in range(0,len(repoName)):
    path_to_csv=f'{path}{repoName[i]}.csv'
    reponame=repoName[i]
    csv_name="../csvRefOutput/csvRefUpdateData/"+reponame+".csv"
    old_csv_name = "../csvRefOutput/"+reponame+".csv"
    if(os.path.exists(path_to_csv)):
        updateRefData(reponame);
    else:   
        freshRefData(reponame);

