import json
import requests
import gzip

url = "http://api.syosetu.com/novelapi/api/?out=json&gzip=5"

#Responce オブジェクトを生成
response = requests.get(url)

#エンコーディングを指定する
response.encoding = 'gzip'

# デコードされていないレスポンスの内容（バイト列）
r = response.content

# gzipの展開，UTF-8
res_content = gzip.decompress(r).decode("utf-8")

# JSONのデコーディング
response_json = json.loads(res_content)

print(response_json)
