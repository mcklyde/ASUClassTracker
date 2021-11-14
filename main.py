from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import hashlib
import time
import smtplib
import os

load_dotenv()

def getHashData(url):

    try:

        r = requests.get(url)
        htmlDoc = BeautifulSoup(r.text, 'html.parser')

        nodeTag = "#CatalogList tr[class*='{}'] td.availableSeatsColumnValue".format(classNumber)

        data = (htmlDoc.select(nodeTag)[0].getText(strip=True))
        hashedData = (hashlib.md5(data.encode('utf-8')).hexdigest())
        return hashedData, data
    except:
        print("Could not find class. Please ensure class number exist.")


classNumber = os.getenv("CLASSID")
phoneNumber = os.getenv("PHONE")
url = "https://webapp4.asu.edu/catalog/myclasslistresults?t=2221&k={}&hon=F&promod=F&e=all&page=1".format(classNumber)
refreshTimer = 5 * 60 # in seconds
lastHashData, seats = getHashData(url)

# SMTP setup
email = os.getenv("EMAIL")
emailPass = os.getenv("EMAIL_PASS")
smtpServer = os.getenv("SMTP")
smtpPort = os.getenv("SMTP_PORT")
mail = smtplib.SMTP(smtpServer, smtpPort)
mail.ehlo()
mail.starttls()
mail.login(email, emailPass)
while True:
    newHash, seats = getHashData(url)
    if(lastHashData != newHash):
        mail.sendmail(email, phoneNumber, "\nSeat available! There are currently {}".format(seats))
    else:
        print("No difference")
    lastHashData, seats = newHash, seats
    time.sleep(refreshTimer)

