# ライブラリの読み込み
from bs4 import BeautifulSoup
import pandas as pd
import requests
from datetime import datetime

def get_dfs(stock_number):
    dfs = []
    year = [2018,2019] #2017〜2019年までの株価データを取得
    for y in year:
        try:
            print(y)
            url = 'https://kabuoji3.com/stock/{}/{}/'.format(stock_number,y)
            soup = BeautifulSoup(requests.get(url).content,'html.parser')
            tag_tr = soup.find_all('tr')
            head = [h.text for h in tag_tr[0].find_all('th')]
            data = []
            for i in range(1,len(tag_tr)):
                data.append([d.text for d in tag_tr[i].find_all('td')])
            df = pd.DataFrame(data, columns = head)

            col = ['始値','高値','安値','終値','出来高','終値調整']
            for c in col:
                df[c] = df[c].astype(float)
            df['日付'] = [datetime.strptime(i,'%Y-%m-%d') for i in df['日付']]
            dfs.append(df)
        except IndexError:
            print('No data')
    return dfs

def concatenate(dfs):
    data = pd.concat(dfs,axis=0)
    data = data.reset_index(drop=True)
    col = ['始値','高値','安値','終値','出来高','終値調整']
    for c in col:
        data[c] = data[c].astype(float)
    return data

#作成したコードリストを読み込む
code_list = pd.read_csv('code_list.csv')
print(code_list)

#複数のデータフレームをcsvで保存
for i in range(len(code_list)):
    k = code_list.loc[i,'code']
    v = code_list.loc[i,'name']
    print(k,v)
    dfs = get_dfs(k)
    data = concatenate(dfs) 
    data.to_csv('{}-{}.csv'.format(k,v))



