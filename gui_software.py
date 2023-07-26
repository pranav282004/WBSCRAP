from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from bs4 import BeautifulSoup
import boto3
import os
from datetime import datetime
import csv
from datetime import date
from tkinter import messagebox
import threading
import requests
import concurrent.futures

dynamo_client = boto3.resource(service_name='dynamodb', region_name='ap-south-1',
                               aws_access_key_id='AKIAZE666E7SOS7X2XFO',
                               aws_secret_access_key='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')

URL_TO_COUNT = dynamo_client.Table('URL_TO_COUNT')
ids_list = []
to_databse = []
data_dict = []
ids = []

window = Tk()
window.geometry("770x600")
window.title('Facebook Scrapper')

window.config(background='white')

label = Label(window, text='Facebook Scrapper', font=('Arial', 18, 'bold'), background='white')
label.place(x=20, y=15)


def on_closing():
    if messagebox.askokcancel("Abort", "Do you want to abort Scrapping ?"):
        xv = []
        with open('result.csv', 'w', newline='') as f:
            fld_name = ['URL', 'Count'  ]
            wrtr = csv.DictWriter(f, fieldnames=fld_name)
            wrtr.writeheader()
            for index, dd in enumerate(data_dict):
                wrtr.writerow({'URL': data_dict[index][0], 'Count': data_dict[index][1]})

        print('Saved')
        window.destroy()


def fetching(ln):
    try:
        proxy = "http://f94c8fb3132dcfa8fd5a918aefd0bda1337d10b1:js_render=true&premium_proxy=true@proxy.zenrows.com:8001"
        proxies = {"http": proxy, "https": proxy}
        response = requests.get(ln, proxies=proxies, verify=False)
        soup = BeautifulSoup(response.text.encode('utf-8').strip(), 'lxml')
        contentf = soup.find_all('div', class_='x8t9es0 x1uxerd5 xrohxju x108nfp6 xq9mrsl x1h4wwuj x117nqv4 xeuugli')[0]
        
        URL_TO_COUNT.put_item(Item={'URL': ln, 'Count': contentf.text, 'Date': datetime.today().strftime('%Y-%m-%d')})
        data_dict.append([ln, contentf.text])
        scrap_list.insert(scrap_list.size(),
                          f'{scrap_list.size()} ✔ Successfully Scraped {contentf.text} Ads from {ln}.')
        window.update()
    except Exception as ff:
        print(f'Error {ff}')


def main():
    scrap_list.insert(scrap_list.size(), "---- 🍵 Scrapping Start Now Sit And Relax And Drink Coffee 🍵 ----")
    tv = []
    for ddt in ids_list:
        res = URL_TO_COUNT.get_item(Key={'URL': ddt})

        if len(res) > 1:
            today = date.today().strftime('%Y-%m-%d')
            datetime_object = datetime.strptime(today, '%Y-%m-%d')
            datetime_object2 = datetime.strptime(res['Item']['Date'], '%Y-%m-%d')
            result = (datetime_object - datetime_object2).days / 7
            if result <= 2.0:
                data_dict.append([ddt, res['Item']['Count']])
                scrap_list.insert(scrap_list.size(),
                                  f'{scrap_list.size()} ✔ Successfully Scraped from {ddt} using Online Database .')
            else:
                tv.append(ddt)
        else:
            if len(tv) >= 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=25) as ee:
                    ee.map(fetching, tv)
                tv.clear()
            else:
                tv.append(ddt)

    with open('result.csv', 'w', newline='') as f:
        fld_name = ['URL', 'Count']
        wrtr = csv.DictWriter(f, fieldnames=fld_name)
        wrtr.writeheader()
        for index, dd in enumerate(data_dict):
            wrtr.writerow({'URL': data_dict[index][0], 'Count': data_dict[index][1]})
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

    global ids_list
    ids_list = filename.read().splitlines()
    # ids_list = [s.replace("'", "") for s in ids_list]


scrap_list = Listbox(window,
                     bg="#FFFFE0",
                     width=93,
                     height=21, font=('consolas', 11))
scrap_list.pack()
scrap_list.place(x=20, y=50)
scrap_list.pack(side="left", fill=X)

scrollbar = Scrollbar(window, orient="vertical")
scrollbar.config(command=scrap_list.yview)
scrollbar.pack(side=RIGHT, fill=BOTH)

scrap_list.config(yscrollcommand=scrollbar.set)

# open button
open_button = Button(
    window,
    text='📁 Select Text Files of Ids',
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
