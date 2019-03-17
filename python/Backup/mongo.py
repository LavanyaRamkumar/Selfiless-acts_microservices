from flask import Flask, render_template, request, jsonify
from pymongo import *
from random import randint

client = MongoClient(port=27017)
db=client.cc_assignment
result = db.profiles.create_index([('userId' , ASCENDING)], unique=True)
f = open("users.txt","r")
k = f.readline()
x = 0

def getNextSequence(collection,name):
	return collection.find_and_modify(query= { '_id': name },update= { '$inc': {'seq': 1}}, new=True ).get('seq');



while(k is not ""): 
	result=db.users.insert_one({'userId': getNextSequence(db.orgid_counter,"userId"), 'name': k.split(":")[1], 'password' : k.split(":")[2] })
	print('Created {0} entry as {1}'.format(x,result.inserted_id))
	x = x+1
	k = f.readline()
print('finished creating entries')

