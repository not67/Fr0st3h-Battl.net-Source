from readsettings import ReadSettings
import requests
import json
import time

config = ReadSettings("Config.json")

token = config['api_key']
country = config["country"]
operator = config['operator']

count = 1
while count <= 100:
    time.sleep(1)
    print(count)
    count += 1

def request5SimNumber():
    headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
    #5sim Part
    print("[+] Requesting phone number..")
    response = requests.get('https://5sim.net/v1/user/buy/activation/' + country + '/' + operator + '/' + "blizzard", headers=headers)
    try:
        data = json.loads(response.text)
        id = data['id']
        phoneNumberr = data['phone']
        print("Phone Request Info:")
        print('Phone Number: ' + str(phoneNumberr))
        print('Phone Price: ' + str(data['price']))
        return data
    except:
        if(response.status_code == 401):
            raise Exception("[5Sim.net] API Key Invalid!")
        else:
            raise Exception("[Exception] Caught Exception while requesting 5Sim Number: {}".format(response.text))

def waitFor5SimCode(id):
    headers = {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
        }
    codeInp = ""
    while(requests.get('https://5sim.net/v1/user/check/' + str(id), headers=headers)):
        response = requests.get('https://5sim.net/v1/user/check/' + str(id), headers=headers)
        data = json.loads(response.text)
        if(data['status'] == "RECEIVED"):
            print("[!] Waiting for code")
            if(data['sms']):
                codeInp = data['sms'][0]['code']
                break
        elif(data['status'] == "PENDING"):
            print("[!] Waiting for phone setup..")
            time.sleep(2)
        else:
            print("Something went wrong: STATUS: " + data['status'])
    print("[+] Got SMS Code: " + codeInp)
    return codeInp

data = request5SimNumber()
id = data['id']
phoneNumberr = data['phone']
if(id):
    code = waitFor5SimCode(id)
    if(code):
        print(code)
