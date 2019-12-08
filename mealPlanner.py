import random
import os
import smtplib
from django.utils.encoding import smart_str

CWD = os.getcwd()

f = open(CWD+"\\credentials.txt","r")
LOGIN_INFO = f.read().splitlines()

FROM = LOGIN_INFO[0]
TO = LOGIN_INFO[1]
USER = LOGIN_INFO[0]
PASSW = LOGIN_INFO[2]


server = smtplib.SMTP("smtp.gmail.com:587")
server.starttls()
server.login(USER,PASSW)




NUMBER_OF_MEALS = 7
NUMBER_OF_DAYS = 2
SUBJECT = "THIS WEEKS PLAN"
OUTPUT_FILE = open("toSend.txt", "w")
SHOPPING_LIST = []

def getShoppingList(fileLoc):
    file = open(fileLoc, "r")
    lines = file.readlines()

    print(lines)

    index = 3
    while not lines[index].startswith("..."):
        if lines[index] not in SHOPPING_LIST:
            SHOPPING_LIST.append(lines[index])
        index+=1

    file.close()



def getRandomMeals():
    numbers = []

    while len(numbers) < NUMBER_OF_DAYS:
        x = random.randint(1,NUMBER_OF_MEALS)
        while x in numbers:
            x = random.randint(1,NUMBER_OF_MEALS)
        numbers.append(x)

    return numbers


#######

fileList = getRandomMeals()

info = ""

for file in fileList:
    f = CWD+"\\dishes\\"+str(file)+".txt"
    getShoppingList(f)
    actFile = open(f)
    info+=actFile.read()
    info+="\n\n**************\n\n"
    actFile.close()

OUTPUT_FILE.write("SHOPPING LIST: \n")
for item in SHOPPING_LIST:
    OUTPUT_FILE.write(item)

OUTPUT_FILE.write("\n\n#####\n\n")
OUTPUT_FILE.write(info)
OUTPUT_FILE.close()

f = open("toSend.txt", "r")

MSG = f.read().encode('utf-8')

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (FROM, TO, SUBJECT, smart_str(MSG))





server.sendmail(FROM,TO,email_text.encode('utf-8'))
server.quit()

