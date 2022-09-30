#API scraping POC
#Author: DarkReign

[redacted]AccountAPI = "https://www.[redacted].com.au/api/myaccount/v1/accounts"

import requests
import json
import sys
import os
import time
import datetime
import argparse
import re
import logging
import logging.handlers
import urllib3
import csv
import socket

logger = logging.getLogger('scanAPI')
logger.setLevel(logging.DEBUG)

fh = logging.handlers.RotatingFileHandler('scanAPI.log', maxBytes=1000000, backupCount=5)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
print("Logging to scanAPI.log")
logger.addHandler(fh)
logger.addHandler(ch)
print("Logging initialised")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description='Scan [redacted] API for account details')
parser.add_argument('-u', '--username', help='Username to use for login', required=True)
parser.add_argument('-p', '--password', help='Password to use for login', required=True)
parser.add_argument('-o', '--output', help='Output file name', required=True)
parser.add_argument('-d', '--debug', help='Enable debug logging', action='store_true')
args = parser.parse_args()
print("Command line arguments parsed")

with open(args.output, 'w', newline='') as csvfile:
    csv.writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv.writer.writerow(['Account Number', 'Account Name', 'Account Type', 'Account Status', 'Account Balance', 'Account Credit Limit', 'Account Credit Available', 'Account Credit Expiry', 'Account Credit Expiry Date', 'Account Credit Expiry Days', 'Account Credit Expiry Hours', 'Account Credit Expiry Minutes', 'Account Credit Expiry Seconds'])

print("Setting up session")
session = requests.Session()
session.verify = False
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'})
session.headers.update({'Accept': 'application/json, text/plain, */*'})
session.headers.update({'Accept-Language': 'en-US,en;q=0.9'})
session.headers.update({'Accept-Encoding': 'gzip, deflate, br'})
session.headers.update({'Content-Type': 'application/json;charset=UTF-8'})
session.headers.update({'Origin': 'https://www.[redacted].com.au'})
session.headers.update({'Sec-Fetch-Site': 'same-site'})
session.headers.update({'Sec-Fetch-Mode': 'cors'})
session.headers.update({'Sec-Fetch-Dest': 'empty'})
session.headers.update({'Referer': 'https://www.[redacted].com.au/my-account-login'})
session.headers.update({'Connection': 'keep-alive'})
session.headers.update({'Pragma': 'no-cache'})
session.headers.update({'Cache-Control': 'no-cache'})
print("Session set up")

print("Logging in")
login = session.post('https://www.[redacted].com.au/my-account-login', data=json.dumps({'username': args.username, 'password': args.password, 'rememberMe': False}), headers={'Content-Type': 'application/json;charset=UTF-8'})
print("Login response: " + str(login.status_code))
if login.status_code != 200:
    print("Login failed")
    exit(1)
print("Logged in")

print("Getting API token")
token = session.get('https://www.[redacted].com.au/myaccount/api/v1/token')
print("Token response: " + str(token.status_code))
if token.status_code != 200:
    print("Token request failed")
    exit(1)
print("Got API token")

print("Getting account details")
account = session.get('https://www.[redacted].com.au/myaccount/api/v1/accounts')
print("Account response: " + str(account.status_code))
if account.status_code != 200:
    print("Account request failed")
    exit(1)
print("Got account details")

for account in account.json()['accounts']:
    print("Processing account " + account['accountNumber'])
    print("Getting account details")
    accountDetails = session.get('https://www.[redacted].com.au/myaccount/api/v1/accounts/' + account['accountNumber'])
    print("Account details response: " + str(accountDetails.status_code))
    if accountDetails.status_code != 200:
        print("Account details request failed")
        exit(1)
    print("Got account details")
    print("Getting account balance")
    accountBalance = session.get('https://www.[redacted].com.au/myaccount/api/v1/accounts/' + account['accountNumber'] + '/balance')
    print("Account balance response: " + str(accountBalance.status_code))
    if accountBalance.status_code != 200:
        print("Account balance request failed")
        exit(1)
    print("Got account balance")
    print("Getting account credit")
    accountCredit = session.get('https://www.[redacted].com.au/myaccount/api/v1/accounts/' + account['accountNumber'] + '/credit')
    print("Account credit response: " + str(accountCredit.status_code))
    if accountCredit.status_code != 200:
        print("Account credit request failed")
        exit(1)
    print("Got account credit")
    print("Getting account credit expiry")
    accountCreditExpiry = session.get('https://www.[redacted].com.au/myaccount/api/v1/accounts/' + account['accountNumber'] + '/credit/expiry')
    print("Account credit expiry response: " + str(accountCreditExpiry.status_code))
    if accountCreditExpiry.status_code != 200:
        print("Account credit expiry request failed")
        exit(1)
    print("Got account credit expiry")
    with open(args.output, 'a', newline='') as csvfile:
        csv.writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv.writer.writerow([account['accountNumber'], accountDetails.json()['accountName'], accountDetails.json()['accountType'], accountDetails.json()['']])

csvfile.close()
print("Logging out")
logout = session.get('https://www.[redacted].com.au/myaccount/api/v1/logout')
print("Logout response: " + str(logout.status_code))
if logout.status_code != 200:
    print("Logout failed")
    exit(1)
print("Logged out")

print("Closing session")
session.close()
print("Session closed")

print("Exiting")
exit(0)
