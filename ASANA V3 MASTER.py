import feather
import pandas as pd
from pandas import DataFrame
import numpy as np
import json
import requests
filename="asana111.csv"
url = "https://app.asana.com/api/1.0/projects/926982266304264/tasks"
payload = "undefined="
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Bearer 0/2c2fb14794fb8e35b5aa8c5fa6209ba0",
    'cache-control': "no-cache",
    'Postman-Token': "18728ed1-8885-4d5f-be50-c39ce3b6b053"
    }
response = requests.request("GET", url, data=payload, headers=headers)
list1= response.text.encode('utf8')
list2=pd.read_json(list1)
## Normalize to split the Json to DataFrame
from pandas.io.json import json_normalize 
dfa1=pd.io.json.json_normalize(list2.data)
# Drop the unwanted columns
dfa1=dfa1.drop(columns=['resource_type'])
#pd.set_option('display.max_rows', dfa1.shape[0]+1)
#dfa1['name'].where(dfa1['name'] == 'The Car Park')
dfaGID=dfa1.gid
listGID=list(dfaGID)

### Asana 2
#Get the fist extended to the url from list
base_url = "https://app.asana.com/api/1.0/tasks/"
url = base_url + listGID[0]
payload = "undefined="
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Bearer 0/2c2fb14794fb8e35b5aa8c5fa6209ba0",
    'cache-control': "no-cache",
    'Postman-Token': "f0ef4da4-d89b-48a0-94bf-7ab96483d783"
}
response = requests.request("GET", url, data=payload, headers=headers)
a1= response.text.encode('utf8')
a2=pd.read_json(a1)
# Normalize and get the given gid of the list parsed to the url
from pandas.io.json import json_normalize 
a2.data.gid
#aa1=pd.io.json.json_normalize(a2.data.assignee)
### GID
#aaGID=aa1[['gid']]
#aaGID
gid=a2.data.gid
aa2=pd.io.json.json_normalize(a2.data.custom_fields)
aa22=aa2[['name','text_value','number_value']]
aaDate=aa22.loc[[1]]
aaDate=aaDate.drop(columns=['number_value'])
### Date
date=aaDate.text_value[1]
aaPhones=aa22.iloc[6:10]
aaPhones=aaPhones.drop(columns=['text_value'])
### Phones carriers dataframe
new_row = {'name':'ShipDate', 'number_value': date }
aaPhones= aaPhones.append(new_row, ignore_index=True)
## insert a new column to dataframe 
aaPhones.insert(2, "gid",0)
#replace it with the gid
aaPhones['gid']=aaPhones.gid.replace(0,gid)
dfg=pd.merge(aaPhones,dfa1,on='gid')
dfg.rename(columns={'name_x':'carrier','name_y':'Location'}, inplace=True)
dfg = dfg[['Location','carrier','number_value','gid']]
dfg.to_csv(filename,index=False,mode='a')
# repeat the process for all the gid's given in the list
for i in range(1,len(listGID)):
    base_url = "https://app.asana.com/api/1.0/tasks/"
    url = base_url + listGID[i]
    payload = "undefined="
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Authorization': "Bearer 0/2c2fb14794fb8e35b5aa8c5fa6209ba0",
        'cache-control': "no-cache",
        'Postman-Token': "f0ef4da4-d89b-48a0-94bf-7ab96483d783"
    }
    response = requests.request("GET", url, data=payload, headers=headers)
    a1= response.text.encode('utf8')
    a2=pd.read_json(a1)
    from pandas.io.json import json_normalize 
    a2.data.gid
    #aa1=pd.io.json.json_normalize(a2.data.assignee)
    ### GID
    #aaGID=aa1[['gid']]
    #aaGID
    gid=a2.data.gid
    aa2=pd.io.json.json_normalize(a2.data.custom_fields)
    aa22=aa2[['name','text_value','number_value']]
    aaDate=aa22.loc[[1]]
    aaDate=aaDate.drop(columns=['number_value'])
    ### Date
    date=aaDate.text_value[1]
    aaPhones=aa22.iloc[6:10]
    aaPhones=aaPhones.drop(columns=['text_value'])
    ### Phones
    new_row = {'name':'ShipDate', 'number_value': date }
    aaPhones= aaPhones.append(new_row, ignore_index=True)
    aaPhones.insert(2, "gid",0)
    aaPhones['gid']=aaPhones.gid.replace(0,gid)
    dfg=pd.merge(aaPhones,dfa1,on='gid')
    dfg.rename(columns={'name_x':'carrier','name_y':'Location'}, inplace=True)
    dfg = dfg[['Location','carrier','number_value','gid']]
    #The code below appends to the same csv file everytime in the loop so that we have one single csv at the end
    dfg.to_csv(filename,index=False, header=False ,mode='a')

data = pd.read_csv(filename)
df1=DataFrame(data,columns=['Location','carrier','number_value'])
#df1['number_value'].replace('', np.nan, inplace=True)
df1=df1.fillna(0)
df2=pd.DataFrame(df1)
pivot = pd.pivot_table(df2,index=['Location'],columns=['carrier'],values=['number_value'] , aggfunc='min')
print(pivot)

