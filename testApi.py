import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "solve/0/sin(x)")
print(response.json())
'''
response = requests.get(BASE + "solve/x*x-16")
print(response.json()) 
'''