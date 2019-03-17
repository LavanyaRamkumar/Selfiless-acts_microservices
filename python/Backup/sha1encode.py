import hashlib 
import sys
str = sys.argv[1]
result = hashlib.sha1(str.encode()) 
print("")
print(result.hexdigest()) 
print(" ") 