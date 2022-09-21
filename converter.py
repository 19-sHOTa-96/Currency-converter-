from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

h = {'user-agent': 'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',}
NBG_URL = "https://nbg.gov.ge/monetary-policy/currency"
TBC_URL = "https://www.tbcbank.ge/web/ka/web/guest/exchange-rates"

def req(url):
    return requests.get(url, headers = h).text

def soup(request):
    return BeautifulSoup(request, 'html.parser')

#TBC parsing
def tbc_parsing_sell(soup):
    st1 = soup.find('div', id = '_exchangerates_WAR_tbcpwexchangeratesportlet_view')
    st2 = st1.find_all('div', class_ = 'currRate')[1::2][0:2]
    st3 = soup.find_all('div', class_ = 'currCopy')[0::2][0:2]
    ex_rate1 = {name.text[0:3]: float(course.text.strip()) for name, course in zip(st3, st2)}

    return ex_rate1

def tbc_parsing_buy(soup):
    st1 = soup.find('div', id='_exchangerates_WAR_tbcpwexchangeratesportlet_view')
    st4 = soup.find_all('div', class_ = 'currRate')[0::2][0:2]
    st2 = st1.find_all('div', class_='currRate')[0::2][0:2]
    st3 = soup.find_all('div', class_='currCopy')[0::2][0:2]
    return {name.text[0:3]: float(course.text.strip()) for name, course in zip(st3, st2)}
    #return st2



#NBG parsing
def nbg_parsing(soup):
    data = soup.find('div', class_='mt-3-4 border-b-2 border-grey-400 border-solid')
    name = data.find_all('span', class_='text-subtitle2 font-normal font-bd leading-subtitle2 uppercase')
    currency = data.find_all('div', class_='jsx-182984682 flex items-center justify-end')
    ex_rate1 = {name.text: float(course.text) for name, course in zip(name, currency) if name.text == "EUR" or name.text == "USD"}

    return ex_rate1

def buy(soup):
    usd_buy = soup.find_all("div", class_ = "currRate")[1::2][0:2]
    return float(usd_buy[0].text.strip()) / float(usd_buy[1].text.strip()) + 0.03

tbc = tbc_parsing_sell(soup(req(TBC_URL)))
nbg = nbg_parsing(soup(req(NBG_URL)))
tbc_buy = buy(soup(req(TBC_URL)))
tbc1 = tbc_parsing_buy(soup(req(TBC_URL)))

#ასუფთავებს ველებს
def entry_clean():

    inp2.state(["!readonly"])
    inp2.delete(0, 'end')
    inp2.state(["readonly"])

    inp3.state(["!readonly"])
    inp3.delete(0, 'end')
    inp3.state(["readonly"])

    inp4.state(["!readonly"])
    inp4.delete(0, 'end')
    inp4.state(["readonly"])


#TBC ბანკის კონვერტაცია
def TBC_Log():

    value = listbox.get(listbox.curselection())
    amount = inp1.get()

    # USD Convert TBC-BANK
    if value == "U S D" and amount:

        inp3.state(["!readonly"])
        inp3.delete(0, END)
        inp3.insert(0, round((float(amount) * (tbc['USD'] / tbc['EUR'] - 0.0170)), 2))
        inp3.state(["readonly"])

        inp4.state(["!readonly"])
        inp4.delete(0, END)
        inp4.insert(0, round((float(amount) * tbc1["USD"]), 2))
        inp4.state(["readonly"])

    # EUR Convert TBC-BANK
    elif value == "E U R" and amount:

        inp2.state(["!readonly"])
        inp2.delete(0, END)
        inp2.insert(0, round((float(amount) / tbc_buy), 2))
        inp2.state(["readonly"])

        inp4.state(["!readonly"])
        inp4.delete(0, END)
        inp4.insert(0, round((float(amount) * tbc1["EUR"]), 2))
        inp4.state(["readonly"])

    # GEL Convert TBC-BANK
    elif value == "G E L" and amount:

        inp2.state(["!readonly"])
        inp2.delete(0, END)
        inp2.insert(0, round((float(amount)  / tbc['USD']), 2))
        inp2.state(["readonly"])

        inp3.state(["!readonly"])
        inp3.delete(0, END)
        inp3.insert(0, round((float(amount) / tbc["EUR"]), 2))
        inp3.state(["readonly"])


#NBG ეროვნული ბანკის კონვერტაცია
def NBG_Log():

    value = listbox.get(listbox.curselection())
    amount = inp1.get()

    # USD Convert NBG-BANK
    if value == "U S D" and amount:

        inp3.state(["!readonly"])
        inp3.delete(0, END)
        inp3.insert(0, round((float(amount) * (nbg['USD'] / nbg['EUR'])), 2))
        inp3.state(["readonly"])

        inp4.state(["!readonly"])
        inp4.delete(0, END)
        inp4.insert(0, round((float(amount) * nbg["USD"]), 2))
        inp4.state(["readonly"])

    # EUR Convert NBG-BANK
    elif value == "E U R" and amount:

        inp2.state(["!readonly"])
        inp2.delete(0, END)
        inp2.insert(0, round((float(amount) / (nbg['USD'] / nbg['EUR'])), 2))
        inp2.state(["readonly"])

        inp4.state(["!readonly"])
        inp4.delete(0, END)
        inp4.insert(0, round((float(amount) * nbg["EUR"]), 2))
        inp4.state(["readonly"])

    # GEL Convert NBG-BANK
    elif value == "G E L" and amount:
        inp2.state(["!readonly"])
        inp2.delete(0, END)
        inp2.insert(0, round((float(amount) / nbg["USD"]), 2))
        inp2.state(["readonly"])

        inp3.state(["!readonly"])
        inp3.delete(0, END)
        inp3.insert(0, round((float(amount) / nbg["EUR"]), 2))
        inp3.state(["readonly"])

def option(event):
    entry_clean()
    try:
        if combobox.get() == "T B C":
            TBC_Log()
        elif combobox.get() == "N B G":
            NBG_Log()
    except:
       pass



#Interface
window = Tk()

window.config(padx = 25, pady = 25)
main_label = Label(text = "Currency Converter", fg = "red", font = ("Verdana", 12, "bold"))
main_label.pack()

units = StringVar()

lb1 = Label(text = "Chose Bank", font = ("Verdana", 10, "bold"))
lb1.pack()

combobox = ttk.Combobox(window, textvariable = units)
combobox.pack()

#Combobox
combobox.config(values = ("T B C", "N B G"))
combobox.get()

lb1 = Label(text = "Choose Unit", font = ("Verdana", 10, "bold"))
lb1.pack()

#Listbox ერთეული არჩევა
listbox = Listbox(height=3, width=5)
units = ["U S D", "E U R", "G E L"]
for item in units:
    listbox.insert(units.index(item), item)
listbox.bind("<<ListboxSelect>>", option)
listbox.pack()

lb1 = Label(text = "Chose Amount ", font = ("Verdana", 10, "bold"))
lb1.pack()
inp1 = ttk.Entry(width = 23)
inp1.pack()


#USD label
lb2 = Label(text = "USD", font = ("Verdana", 10, "bold"))
lb2.pack()

#USD entry
inp2 = ttk.Entry(width = 23)
inp2.state(["readonly"])
inp2.pack()

#EUR label
lb3 = Label(text = "EUR", font = ("Verdana", 10, "bold"))
lb3.pack()

#EUR entry
inp3 = ttk.Entry(width = 23)
inp3.state(["readonly"])
inp3.pack()

#GEL label
lb4 = Label(text = "GEL", font = ("Verdana", 10, "bold"))
lb4.pack()

#GEL entry
inp4 = ttk.Entry(width = 23)
inp4.state(["readonly"])
inp4.pack()

#ციფრების დაჭერა
for key in range(0, 9):
    window.bind(key, option)


#BackSpace ით წაშლა
window.bind("<BackSpace>", option)


combobox.set("T B C")
window.mainloop()