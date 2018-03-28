import pyqrcode
import io


data= '28d21221e263dd03a01f439dd1996904e9252a2e397071f6246e6cda03ccdcd0aa24ed8a46cedc82d771250798c7330b816a379e54172d8ca70295fc30dafcb61ea3ad800bfcbcf5ed351bdb89032fd9ce4bb53a705f16be81155fdcc77a08b44970f6e4c9f9ebc17989a452436d9960d769356329c68f264beb22a99f38e7d1'

url = pyqrcode.create(data, error='L', version=27, mode='binary') 
url.svg('uca-url.svg', scale=8)
url.eps('uca-url.eps', scale=2)
#print(url.terminal(quiet_zone=1))


buffer = io.BytesIO()
url.svg(buffer)
# do whatever you want with buffer.getvalue()
print(list(buffer.getvalue()))

buffer = io.BytesIO()
url.png(buffer)
print(list(buffer.getvalue()))

