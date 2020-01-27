import pandas as pd
import json
import requests
filename="postb.csv"
url = "https://api.sosinventory.com/api/v2/serial/?start=0"
payload = {}
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
  'Host': 'api.sosinventory.com',
  'Authorization': 'Bearer pNndLVLqGLIZPiyRrRPlPljrP0Fi6MZR50XJJaK4RZtaBysBt2TkSnsigWIWh07Nsbz5CRS6OoSRdUesOQNMyekGj4dRnqY4kbZSe4QYed6qGpEInwqLs018a15MX8qx4Koqn76zHsRDHH09vVEP0owgxBs397sGjI2P3IaPiEXkceEBkmlcJq3M3Wl05UxbOp_u6PdndzE0ROmo06dEOUeJ7ymjEl-9kr4IwXBOh5fSUndHsx39i2kN3r6akn-rsQ3DBPTv0f4qWzJKaUT1t7bdjU7sa4djGmQnvttBxrCaqPmU',
  'User-Agent': 'PostmanRuntime/7.22.0',
  'Accept': '*/*',
  'Cache-Control': 'no-cache',
  'Postman-Token': '34a6c8c7-eb46-440c-800d-cf1971f29854',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}
response = requests.request("GET", url, headers=headers, data = payload)
df= response.text.encode('utf8')
df1=pd.read_json(df)
TotalCount=df1.totalCount[0]
Count=df1['count'][0]
loop=int(TotalCount/Count)
df1=df1.drop(columns=['count','totalCount','status','message'])
from pandas.io.json import json_normalize 
df1=pd.io.json.json_normalize(df1.data)
df2=df1[['item.name','location.name']]
df2.to_csv(filename,index=False,mode='a')

ini=201
for i in range(loop): # 56 times to get 11366
    base_url = "https://api.sosinventory.com/api/v2/serial/?start="   
    url = base_url + str(ini)
    payload = {}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'api.sosinventory.com',
        'Authorization': 'Bearer pNndLVLqGLIZPiyRrRPlPljrP0Fi6MZR50XJJaK4RZtaBysBt2TkSnsigWIWh07Nsbz5CRS6OoSRdUesOQNMyekGj4dRnqY4kbZSe4QYed6qGpEInwqLs018a15MX8qx4Koqn76zHsRDHH09vVEP0owgxBs397sGjI2P3IaPiEXkceEBkmlcJq3M3Wl05UxbOp_u6PdndzE0ROmo06dEOUeJ7ymjEl-9kr4IwXBOh5fSUndHsx39i2kN3r6akn-rsQ3DBPTv0f4qWzJKaUT1t7bdjU7sa4djGmQnvttBxrCaqPmU',
        'User-Agent': 'PostmanRuntime/7.22.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': '34a6c8c7-eb46-440c-800d-cf1971f29854',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers, data = payload)
    df= response.text.encode('utf8')
    df1=pd.read_json(df)
    df1=df1.drop(columns=['count','totalCount','status','message'])
    from pandas.io.json import json_normalize 
    df1=pd.io.json.json_normalize(df1.data)
    df2=df1[['item.name','location.name']]
    df2.to_csv(filename,index=False,header=False,mode='a')
    ini +=200
