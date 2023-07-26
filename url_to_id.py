from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import csv
import time
import socket
import re
from tkinter import messagebox
import threading
import requests
from selenium.webdriver.common.by import By
import concurrent.futures
import mysql.connector
from fake_useragent import UserAgent

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database='url_to_id_data'
)
cursor = db.cursor()
# cursor.execute("CREATE DATABASE url_to_id_data")
# cursor.execute("DROP TABLE Data_ID")
# cursor.execute("CREATE TABLE Data_ID (id int PRIMARY KEY AUTO_INCREMENT,URL VARCHAR(500),IDSTRING VARCHAR(500))")

urls_list = []
data_dict = []
to_save_in_database = []
window = Tk()
window.geometry("770x600")
window.title('Facebook URL to Id')

window.config(background='white')

label = Label(window, text='Facebook URL to Id', font=('Arial', 18, 'bold'), background='white')
label.place(x=20, y=15)


def on_closing():
    if messagebox.askokcancel("Abort", "Do you want to abort Scrapping ?"):
        for index, xy in enumerate(to_save_in_database):
            cursor.execute("INSERT INTO Data_ID (URL,IDSTRING) VALUES (%s,%s)",
                           (to_save_in_database[index][0], to_save_in_database[index][1]))
            db.commit()
        with open('url_to_id.csv', 'w', newline='') as f:
            fld_name = ['Url', 'ID']
            wrtr = csv.DictWriter(f, fieldnames=fld_name)
            wrtr.writeheader()
            for index, dd in enumerate(data_dict):
                wrtr.writerow({'Url': data_dict[index][0], 'ID': "'"+data_dict[index][1]})
        print('Saved')
        window.destroy()


def fetching(idsx):
    try:
        proxies = {'https': 'http://gate.smartproxy.com:7000', 'http': 'http://gate.smartproxy.com:7000'}
        ids = []
        response = requests.get(idsx, proxies=proxies)
        x = re.findall(
            r'(?:["pageID"|"page_ID"|"selectedID"|"selected_ID"|"user_ID"|"userID"|"id"|"delegate_page_id"|"associated_page_id"]{8}[,:]+.?\d*)',
            response.content.decode('utf-8'))
        for d in x:
            if "pageID" in d or " page_ID" in d or "userID" in d or "user_ID" in d or "selected_ID" in d or "selectedID" in d:
                d = d.replace('"pageID":"', "")
                d = d.replace('"page_ID":"', "")
                d = d.replace('"selectedID":"', "")
                d = d.replace('"selected_ID":"', "")
                d = d.replace('"userID":"', "")
                d = d.replace('"user_ID":"', "")
                d = d.replace('"delegate_page_id":"', "")
                d = d.replace('"associated_page_id":"', "")
                if re.search(r'^[0-9]+$', d):
                    ids.append(d)
        ids = set(ids)
        if (len(ids) > 0):
            resultant_id = list(ids)[0]
        else:
            resultant_id = "0"

        url = re.compile(r"https?://(www\.)?")
        url = url.sub('', idsx).strip().strip('/')
        xyz = url.replace('facebook.com/', '')
        scrap_list.insert(scrap_list.size(), f'{scrap_list.size()} ✔ Scraped id {resultant_id} from {idsx} Link .')
        data_dict.append([idsx, resultant_id])
        to_save_in_database.append([xyz, resultant_id])

    except Exception as d:
        print(d)


def main():
    to_scrap = []
    scrap_list.insert(scrap_list.size(), "---- 🍵 Scrapping Start Now Sit And Relax And Drink Coffee 🍵 ----")
    for dd in urls_list:
        url = re.compile(r"https?://(www\.)?")
        url = url.sub('', dd).strip().strip('/')
        xt = url.replace('facebook.com/', '')
        try:
            sql = "SELECT URL,IDSTRING FROM Data_ID WHERE URL= %s"
            adr = (xt,)
            cursor.execute(sql, adr)
        except Exception as ff:
            print(ff)
        xy = cursor.fetchall()
        if len(xy) > 0:
            data_dict.append([dd, list(xy[0])[1]])
            scrap_list.insert(scrap_list.size(), f'{scrap_list.size()} ✔ Scraped id from {dd} Link From Database.')
        else:
            to_scrap.append(dd)

    with concurrent.futures.ThreadPoolExecutor() as ee:
        ee.map(fetching, to_scrap)

    for index, xy in enumerate(to_save_in_database):
        cursor.execute("INSERT INTO Data_ID (URL,IDSTRING) VALUES (%s,%s)",
                       (to_save_in_database[index][0], to_save_in_database[index][1]))
        db.commit()
    with open('url_to_id.csv', 'w', newline='') as f:
        fld_name = ['Url', 'ID']
        wrtr = csv.DictWriter(f, fieldnames=fld_name)
        wrtr.writeheader()
        for index, dd in enumerate(data_dict):
            wrtr.writerow({'Url': data_dict[index][0], 'ID': "'"+data_dict[index][1]})
    print('Saved')
    window.destroy()


def select_file():
    filetypes = (
        ('text files', '*.txt'),
    )

    filename = fd.askopenfile(
        mode='r',
        filetypes=filetypes)

    labelx = Label(window, text=filename.name, font=('Arial', 10), background='white')
    labelx.place(x=20, y=520)
    scrap_button.config(state=NORMAL)

    global urls_list
    urls_list = filename.read().splitlines()


scrap_list = Listbox(window,
                     bg="#FFFFE0",
                     width=93,
                     height=21, font=('consolas', 11))
scrap_list.place(x=20, y=180)
scrap_list.pack(side="left", fill=X)
# open button

scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=scrap_list.yview)
scrollbar.pack(side=RIGHT, fill=BOTH)

scrap_list.config(yscrollcommand=scrollbar.set)

open_button = Button(
    window,
    text='📁 Select Text Files of URLS',
    command=select_file
)

open_button.place(x=20, y=60)

# scrap_button
scrap_button = Button(window
                      , text='  Start Scrapping ->  '
                      , state=DISABLED
                      , command=threading.Thread(target=main).start)
scrap_button.place(x=20, y=550)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
