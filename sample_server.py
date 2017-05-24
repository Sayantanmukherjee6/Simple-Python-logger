import requests
import time

while True:
    r=requests.post('http://192.168.0.101:8000/RFID/data1', data = {'key':'value'})
    time.sleep(2)