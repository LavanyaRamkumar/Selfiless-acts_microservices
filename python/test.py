import re
txt = input()
if(re.search("[A-Za-z0-9+/=]", txt) and len(txt)%4==0):
	print("pass")
else:
	print("fail")
