# Import required libraries
import tkinter as tk
from tkinter import ttk
from tkinter import *
import urllib.request, urllib.parse, urllib.error
import ssl
import json
import sqlite3
import time

# This connects to the database and creates it if it does not exist and creates a cursor for further communication
conn = sqlite3.connect("favourite_data.db")
cur = conn.cursor()

# If the table doesnt already exist this will force a creation otherwise it will connect
cur.execute("CREATE TABLE IF NOT EXISTS Favourites ( security TEXT, daily_change REAL, weekly_change REAL, monthly_change REAL )")
conn.commit()

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Call on the database and create a list of tuples containing all data from database
cur.execute("select rowid, * FROM Favourites")
List = cur.fetchall()
# Count the length of the list
count = len(List)
# Create a list of the numbers from 0 up to the largest in the count
size = list(range(0, count))
# This creates an empty list and then adds the stock tickrs to that list
list_2 = list()
for items in size:
    items_2 = List[items][1]
    list_2 = list_2 + [items_2]


# Root widget must be created before any other can be put on
root = tk.Tk()
# This defines the overall characteristics of the program
main = root
main.title("Stock favourites with price and trend checker")
# calls on the notebook widget from the ttk library and packs into full window
my_notebook = ttk.Notebook(main)
my_notebook.pack()
# defines the tabs and provides properties
my_frame1 = Frame(my_notebook)
my_frame2 = Frame(my_notebook)
my_frame3 = Frame(my_notebook)
# This adds the tabs created above to the window and names them
my_notebook.add(my_frame1, text="Price Check")
my_notebook.add(my_frame2, text="Favourites")
my_notebook.add(my_frame3, text="Trend Checker")

def clear_function(tabno):
    if tabno == 1:
        Label(my_frame1, text="                                                                                                               ").grid(row=4)
        Label(my_frame1, text="                                                                                                               ").grid(row=5)
        Label(my_frame1, text="                                                                           ").grid(row=6)
        Label(my_frame1, text="                                                                           ").grid(row=7)
        Label(my_frame1, text="                                                                           ").grid(row=8)
        Label(my_frame1, text="                                                                           ").grid(row=9)
    if tabno == 2:
        Label(my_frame2, text="                                                                                                               ").grid(row=4)
        Label(my_frame2, text="                                                                                                               ").grid(row=5)
        Label(my_frame2, text="                                                                                                               ").grid(row=6)
    if tabno == 3:
        Label(my_frame2, text="                                                                 ").grid(column=2, row=2)
        Label(my_frame2, text="                                                                 ").grid(column=2, row=3)
    if tabno == 4:
        Label(my_frame3, text="                                                                        ").grid(column=2)
    if tabno == 5:
        Label(my_frame3, text="                                                                 ").grid(column=1, row=2)


def current_price_checker(e):
    # Try to remove rate limit error
    try:
        # r is input from radio button
        if r.get() == 1:
            Tickr = e
            # import data
            # send request to api
            x = urllib.request.urlopen(
                "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
            # read, convert the data from json to utf-8 and then load
            data_x = x.read().decode()
            try:
                js = json.loads(data_x)
            except:
                js = None
            # Additional code for pulling the date on the file and if it includes a time, removing the time
            date = str(js["Meta Data"]["3. Last Refreshed"])
            if len(date) > 10:
                list = date.split(" ")
                date = list[0]

            # Parse json file to open selected data
            open = js["Time Series (Daily)"][date]["1. open"]
            open = float(open)
            high = js["Time Series (Daily)"][date]["2. high"]
            high = float(high)
            low = js["Time Series (Daily)"][date]["3. low"]
            low = float(low)
            close = js["Time Series (Daily)"][date]["4. close"]
            close = float(close)
            volume = js["Time Series (Daily)"][date]["5. volume"]
            volume = float(volume)

            # Creates output onto GUI
            label_date = Label(my_frame1, text="Date:  " + str(date)).grid(row=4)
            label_open = Label(my_frame1, text="Open:  " + str(open)).grid(row=5)
            label_high = Label(my_frame1, text="High:  " + str(high)).grid(row=6)
            label_low = Label(my_frame1, text="Low:  " + str(low)).grid(row=7)
            label_close = Label(my_frame1, text="Close:  " + str(close)).grid(row=8)
            label_volume = Label(my_frame1, text="Volume:  " + str(volume)).grid(row=9)

        # code for FX pairs
        if r.get() == 2:
            # Takes input with a - between currencies, splits the data into list and then pulls corresponding from index
            e_split = e.split("-")
            From = e_split[0]
            To = e_split[1]
            y = urllib.request.urlopen(
                "https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=" + From + "&to_symbol=" + To + "&apikey=O0NEY0ZPDX1XZ2BT")
            # read, convert the data from json to utf-8 and then load
            data_y = y.read().decode()
            try:
                js = json.loads(data_y)
            except:
                js = None
            # Additional code for pulling the date on the file and if it includes a time, removing the time
            date = str(js["Meta Data"]["5. Last Refreshed"])
            if len(date) > 10:
                list = date.split(" ")
                date = list[0]

                # Parse json file to open selected data
                open = js["Time Series FX (Daily)"][date]["1. open"]
                open = float(open)
                high = js["Time Series FX (Daily)"][date]["2. high"]
                high = float(high)
                low = js["Time Series FX (Daily)"][date]["3. low"]
                low = float(low)
                close = js["Time Series FX (Daily)"][date]["4. close"]
                close = float(close)

                # Creates output onto GUI
                label_date = Label(my_frame1, text="Date:  " + str(date)).grid(column=0, row=4)
                label_open = Label(my_frame1, text="Open:  " + str(open)).grid(column=0, row=5)
                label_high = Label(my_frame1, text="High:  " + str(high)).grid(column=0, row=6)
                label_low = Label(my_frame1, text="Low:  " + str(low)).grid(column=0, row=7)
                label_close = Label(my_frame1, text="Close:  " + str(close)).grid(column=0, row=8)
    except:
        # Error message for when connection doesnt go through or input incorrect
        label_error = Label(my_frame1, text="An error has occurred please check your input").grid(column=0, row=4)
        label_error = Label(my_frame1, text="otherwise wait 1min to allow for  server rate limit").grid(column=0, row=5)

def add_fucntion(Tickr):
    # import data and send request to api
    x = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and then load
    data_x = x.read().decode()
    try:
        js = json.loads(data_x)
    except:
        js = None
    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_d = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_d) > 10:
        list = date_d.split(" ")
        date_d = list[0]

    # Parse json file to open selected data and calculate percentage change
    open_d = js["Time Series (Daily)"][date_d]["1. open"]
    open_d = float(open_d)
    close_d = js["Time Series (Daily)"][date_d]["4. close"]
    close_d = float(close_d)
    percentage_change_d = ((close_d - open_d)*100)/close_d

    # import weekly data and send request to api
    y = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and load data
    data_y = y.read().decode()
    try:
        js = json.loads(data_y)
    except:
        js = None
    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_w = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_w) > 10:
        list = date_w.split(" ")
        date_w = list[0]
    # Parse json file to open selected data and calculate percentage change
    open_w = js["Weekly Time Series"][date_w]["1. open"]
    open_w = float(open_w)
    close_w = js["Weekly Time Series"][date_w]["4. close"]
    close_w = float(close_w)
    percentage_change_w = ((close_w - open_w)*100)/close_w

    # import monthly data and send request to api
    z = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and load data
    data_z = z.read().decode()
    try:
        js = json.loads(data_z)
    except:
        js = None
    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_m = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_m) > 10:
        list = date_m.split(" ")
        date_m = list[0]
    # Parse json file to open selected data and calculate percentage change
    open_m = js["Monthly Time Series"][date_m]["1. open"]
    open_m = float(open_m)
    close_m = js["Monthly Time Series"][date_m]["4. close"]
    close_m = float(close_m)
    percentage_change_m = ((close_m - open_m)*100)/close_m

    # Database insert function
    def insert_data(Tickr,daily, weekly, monthly):
        # enter data through this function, using placeholders so variables can be inserted later
        cur.execute("INSERT INTO Favourites VALUES (?,?,?,?)", (Tickr, daily, weekly, monthly))
        # Commit data to database
        conn.commit()
    insert_data(Tickr, percentage_change_d, percentage_change_w, percentage_change_m)

def remove_function(Tickr):
    # Connects to database and removes entry
    cur.execute("DELETE from Favourites WHERE security LIKE (?) ", (Tickr,))
    conn.commit()

def update_function(Tickr):
    # import data and send request to api
    x = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and load data
    data_x = x.read().decode()
    try:
        js = json.loads(data_x)
    except:
        js = None

    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_d = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_d) > 10:
        list = date_d.split(" ")
        date_d = list[0]

    # Parse json file to open selected data and calculate percentage change
    open_d = js["Time Series (Daily)"][date_d]["1. open"]
    open_d = float(open_d)
    close_d = js["Time Series (Daily)"][date_d]["4. close"]
    close_d = float(close_d)
    percentage_change_d = ((close_d - open_d) * 100) / close_d

    # import data and send request to api
    y = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and load data
    data_y = y.read().decode()
    try:
        js = json.loads(data_y)
    except:
        js = None

    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_w = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_w) > 10:
        list = date_w.split(" ")
        date_w = list[0]

    # Parse json file to open selected data and calculate percentage change
    open_w = js["Weekly Time Series"][date_w]["1. open"]
    open_w = float(open_w)
    close_w = js["Weekly Time Series"][date_w]["4. close"]
    close_w = float(close_w)
    percentage_change_w = ((close_w - open_w) * 100) / close_w

    # import data and send request to api
    z = urllib.request.urlopen(
        "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
    # read and then convert the data from json to utf-8 and load data
    data_z = z.read().decode()
    try:
        js = json.loads(data_z)
    except:
        js = None

    # Additional code for pulling the date on the file and if it includes a time, removing the time
    date_m = str(js["Meta Data"]["3. Last Refreshed"])
    if len(date_m) > 10:
        list = date_m.split(" ")
        date_m = list[0]

    # Parse json file to open selected data and calculate percentage change
    open_m = js["Monthly Time Series"][date_m]["1. open"]
    open_m = float(open_m)
    close_m = js["Monthly Time Series"][date_m]["4. close"]
    close_m = float(close_m)
    percentage_change_m = ((close_m - open_m) * 100) / close_m

    # Database update function
    def update_data(Tickr, daily, weekly, monthly):
        # enter data through this function, using placeholders so variables can be inserted later
        cur.execute("UPDATE Favourites SET daily_change = ? WHERE security = ? ", (daily, Tickr, ))
        cur.execute("UPDATE Favourites SET weekly_change = ? WHERE security = ?", (weekly, Tickr, ))
        cur.execute("UPDATE Favourites SET monthly_change = ? WHERE security = ?", (monthly, Tickr, ))
        conn.commit()
    update_data(Tickr, percentage_change_d, percentage_change_w, percentage_change_m)

# command for button click on tab 1
def button_click():
    clear_function(1)
    # retrieves user selections
    x1 = e.get()
    r1 = r.get()
    # Runs previous function
    current_price_checker(x1)

# Command for refreshing list button on tab 2
def refresh_list():
    clear_function(3)
    # This calls on the database and creates a list of tuples containing all data from database
    cur.execute("select rowid, * FROM Favourites")
    L = cur.fetchall()
    # This counts the length of the list
    countB = len(L)
    # This creates a list of the numbers from 0 up to the largest in the count
    sizeB = list(range(0, countB))
    # This creates a list and then adds the stock tickrs to that list
    global list_B
    list_B = list()
    for things in sizeB:
        items_B = L[things][1]
        list_B =list_B + [items_B]
    list_label = Label(my_frame2, text="favourites list").grid(column=2, row=1)
    list_label = Label(my_frame2, text=list_B).grid(column=2, row=2)

# Command for multiple choice entry on tab 2
def button_click_2():
    clear_function(2)
    # retrieves user selections
    x2 = e2.get()
    f2 = f.get()
    # try and except to provide error message for incorrect input and exceeding rate limit
    try:
        # Choice 1 - adding new fav
        if f2 == 1:
            # to prevent repeats in database
            if x2 not in list_B:
                add_fucntion(x2)
                dpc_ = Label(my_frame2, text=x2 + " added").grid(column=0, row=4)
                wpc_ = Label(my_frame2, text="                                    ").grid(column=0, row=5)
                mpc_ = Label(my_frame2, text="                                    ").grid(column=0, row=6)
            else:
                dpc_ = Label(my_frame2, text="stock already in favourites").grid(column=0, row=4)

        # Choice 2 - removing fav
        if f2 == 2:
            # incase not in list
            if x2 in list_B:
                remove_function(x2)
                dpc_ = Label(my_frame2, text=x2 + " removed").grid(column=0, row=4)
                wpc_ = Label(my_frame2, text="                                    ").grid(column=0, row=5)
                mpc_ = Label(my_frame2, text="                                    ").grid(column=0, row=6)
            else:
                dpc_ = Label(my_frame2, text="stock not in favourites").grid(column=0, row=4)
        # Choice 3 - viewing d/w/m data
        if f2 == 3:
            # to ensure only favs are selected
            if x2 in list_B:
                update_function(x2)
                # This calls on the database and creates a list of tuples containing all data from database
                cur.execute("SELECT daily_change, weekly_change, monthly_change FROM Favourites WHERE security = (?) ",
                            (x2,))
                List = cur.fetchall()
                dpc_ = Label(my_frame2, text="Daily percentage change: " + str(List[0][0])).grid(column=0, row=4)
                wpc_ = Label(my_frame2, text="Weekly percentage change: " + str(List[0][1])).grid(column=0, row=5)
                mpc_ = Label(my_frame2, text="Monthly percentage change: " + str(List[0][2])).grid(column=0, row=6)
            else:
                dpc_ = Label(my_frame2, text="please add to favourites first").grid(column=0, row=4)
    except:
        # Error message for when connection doesnt go through or input incorrect
        label_error = Label(my_frame2, text="An error has occurred please check your input").grid(column=0, row=4)
        label_error = Label(my_frame2, text="otherwise wait 1min to allow for  server rate limit").grid(column=0, row=5)
    # updates favs list if any changes have been made
    refresh_list()

# update all button
def update_all():
    clear_function(5)
    # incase of exceeding rate limit
    try:
        # updates everything in the list with pause between to not overload server and stay within rate limit
        for stuff in list_B:
            update_function(stuff)
            time.sleep(60)
        Label(my_frame3, text="Done").grid(column=1, row=2)
    except:
        label_error = Label(my_frame3, text="""Rate limit exceeded wait 1min and try again""").grid(column=1, row=2)

# command for trend checker
def trend_check():
    clear_function(4)
    try:
        # loops through list and checks each favourite
        for stuff in list_B:
            # pause to prevent rate limit exceeded
            time.sleep(10)
            Tickr = stuff
            Label(my_frame3, text=Tickr).grid(column=2)
            # This calls on the database and creates a list of tuples containing all data from database
            cur.execute("SELECT daily_change, weekly_change, monthly_change FROM Favourites WHERE security = (?) ",
                        (Tickr,))
            List = cur.fetchall()
            # creates variables for daily weekly and monthly percentage change
            dpc = List[0][0]
            wpc = List[0][1]
            mpc = List[0][2]
            # checks if all are negative
            x = dpc < 0
            y = wpc < 0
            z = mpc < 0
            # if they are all negative or all postive - it suspects a trend and continues
            xyz = x == y == z
            if xyz == True:
                # it pulls the most recent close price and compares it to the 200 day moving average
                url = urllib.request.urlopen(
                    "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + Tickr + "&apikey=O0NEY0ZPDX1XZ2BT")
                data_url = url.read().decode()
                url_1 = urllib.request.urlopen(
                    "https://www.alphavantage.co/query?function=SMA&symbol=" + Tickr + "&interval=weekly&time_period=200&series_type=open&apikey=O0NEY0ZPDX1XZ2BT")
                data_url_1 = url_1.read().decode()
                try:
                    js = json.loads(data_url)
                except:
                    js = None
                try:
                    js2 = json.loads(data_url_1)
                except:
                    js2 = None
                # Additional code for pulling the date on the file and if it includes a time, removing the time
                date = str(js["Meta Data"]["3. Last Refreshed"])
                if len(date) > 10:
                    list = date.split(" ")
                    date = list[0]
                date_m = str(js2["Meta Data"]["3: Last Refreshed"])
                # Creates variables for moving average and close
                MA = js2["Technical Analysis: SMA"][date_m]["SMA"]
                MA = float(MA)
                close = js["Time Series (Daily)"][date]["4. close"]
                close = float(close)
                # Defines the trend based on nested if statments, ie all positive % change + above 200Ma = strong uptrend
                if x == True:
                    if MA > close:
                        Label(my_frame3, text="Strong downtrend \n").grid(column=2)
                    else:
                        Label(my_frame3, text="possible downtrend \n").grid(column=2)
                else:
                    if MA < close:
                        Label(my_frame3, text="Strong uptrend \n").grid(column=2)
                    else:
                        Label(my_frame3, text="possible uptrend \n").grid(column=2)
            else:
                # If the 3 % did not match
                Label(my_frame3, text="trend not very clear \n").grid(column=2)
    except:
        label_error = Label(my_frame3, text="""Rate limit exceeded wait 1min and try again""").grid(column=2)


# Tab 1 - price check
# sets r, variable for radiobutton as a variable and pre selects choice 1
r = IntVar()
r.set(1)
# creates multiple choice
Radiobutton(my_frame1, text="Stock", variable=r, value=1).grid(row=0)
Radiobutton(my_frame1, text="Forex pair", variable=r, value=2).grid(row=1)
# provides guidence for entering forex pairs
Label(my_frame1, text="for forex pairs please input primary-secondary as such ").grid(row=2)
# creates entry input
e = tk.Entry(my_frame1, width=50)
e.grid(column=0, row=3)
# creates entry trigger
myButton = tk.Button(my_frame1, text="Enter Tickr/Pair", command=button_click).grid(column=1, row=3)



# Tab 2 - Favourites
# starts by refreshing list and displaying it
refresh_list()
# sets f, variable for radiobutton as variable and pre selects choice 1
f = IntVar()
f.set(1)
# creates multiple choice
Radiobutton(my_frame2, text="Add new favourite", variable=f, value=1).grid(column=0, row=0)
Radiobutton(my_frame2, text="Remove current favourite", variable=f, value=2).grid(column=0, row=1)
Radiobutton(my_frame2, text="View D/W/M % Change", variable=f, value=3).grid(column=0, row=2)
# creates entry input
e2 = tk.Entry(my_frame2, width=50)
e2.grid(column=0, row=3)
# creates entry trigger
myButton = tk.Button(my_frame2, text="Enter Tickr", command=button_click_2).grid(column=1, row=3)
# trigger for refreshing list manually
update_list_button = tk.Button(my_frame2, text="refresh list", command=refresh_list).grid(column=2, row=0)



# Tab 3 - Trend Checker
# to center the other 2 buttons while leaving space on the sides
Label(my_frame3, text="                                    ").grid(column=0, row=0)
Label(my_frame3, text="                                    ").grid(column=4, row=0)
# creates trigger for updating all stocks in favs
updateButton = tk.Button(my_frame3, text="Update all", command=update_all, width=30).grid(column=1, row=0)
# Creates trigger to check all favs for trends
trendButton = tk.Button(my_frame3, text="check for trends", command=trend_check, width=30).grid(column=2, row=0)


# This needs to be at the end as it puts the computer in a wait and hold for response
root.mainloop()
