import requests
from flask import Flask, request, jsonify

# на страницу отправляем текст
res = requests.post('http://127.0.0.1:5000/api/add_message/1234', json={"mytext":[39, 28.0, 1, 0, 0, 3]})

print(res)
if res.ok:
    print(res.json())