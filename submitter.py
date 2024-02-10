import sys

import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd
import datetime
import openai
import time
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
# import answer_retriever
# import problem_submitter
import pyautogui as pag
import re

url = f"https://codeforces.com/api/contest.list"
response = requests.get(url)
contests = response.json()["result"]
def get_contest_start_time(contest_id,contests):
    for contest in contests:
        if contest["id"] == contest_id:
            start_time = contest["startTimeSeconds"]
            return start_time


def get_contest_date(start_time):
    cd = datetime.datetime.fromtimestamp(start_time)
    contest_date = cd.strftime('%Y-%m-%d')
    return contest_date

def remove_tags(url):
    try:
        return  '\n'.join(
        BeautifulSoup(requests.get("https://"+url).text, "html.parser").find('div',class_="problem-statement").find_all(text=True))
    except:
        return "Nan"



df=pd.read_csv('final_problems.csv')
problems_statement=[]
date=[]
urls=df.hrefs
len=len(urls)
cnt=1
for url in urls:
    print(cnt,"/",len)
    cnt+=1
    contest_id = int(url.split("/")[3])
    start_time = get_contest_start_time(contest_id,contests)
    start_date = get_contest_date(start_time)
    print(start_date)
    date.append(start_date)
    problems_statement.append(remove_tags(url))
new_df=pd.DataFrame({'date':date,'problem_statement':problems_statement})
final_final_df=pd.concat([new_df,df],axis=1)
final_final_df.to_csv("final_final_problems.csv",index=False)



################## asking gpt through api

api_key="################ your api key of openai ################"
openai.api_key=api_key
def chat_with_chatgpt(prompt, model="gpt-3.5-turbo"):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    return message

print(chat_with_chatgpt("hi"))



################################ Data Cleaning #################################


df=pd.read_csv('final_final_problems.csv')
print(len(df))
conditions = (df.problem_statement == 'Nan')|(df.rate=='Nan')
filtered_df = df[~conditions]
print(len(filtered_df))
filtered_df.to_csv('filtered_df.csv',index=False)

#################################################################################




driver = webdriver.Chrome()




def input_the_code():
    lines = []
    cnt=0
    while True:

        user_input = input()

        if user_input == '':
            cnt+=1

            if cnt==3:
                return " ".join(lines)

        else:
            cnt=0
            lines.append(user_input + '\n')


def save_work(lang,serial,code):
    f = open(f"C:\\Users\\DELL\\Desktop\\solutions\\bard\\{lang}\\{serial}.{lang}", "w")
    f.write(code)
    f.close()


# save_work('py','2432C','print("hello World")')


the_length=4657

lang=['c++','java','python']
extensions=['cpp','java','py']

submit_to_gpt=(1559, 923) # position of submit button in my screen
chrome=(1156,1053)        # position of chrome in my task bar
pycharm=(642,1059)        # position of pychar in my task bar
text_area=(1200,923)      # position of text area in gpt interface

df=pd.read_csv('filtered_df.csv')

def remove_new_lines(code):
    return re.sub('\n',' ',code)


# positions of tabs
y=1
x=[1349,1431,1537]



file=open('log.txt','w')



def send(code):

    # take text as ctrl+c
    pag.moveTo(chrome[0],chrome[1])
    pag.click(duration=1)
    new_code=remove_new_lines(code)
    message = f"solve the following problem in C++ : " +new_code+ \
                  ". And please  never explain anything before or after the code nor recommend any thing"
    pag.moveTo(text_area[0],text_area[1],duration=.2)
    pag.click()

    pag.typewrite(message)
    pag.sleep(30)
    pag.press('enter')
    time.sleep(30)
    pag.click(pycharm[0],pycharm[1])
    time.sleep(1)


