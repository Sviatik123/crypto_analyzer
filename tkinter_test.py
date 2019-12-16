import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import sqlalchemy as db
# from database_filler import DatabaseFiller

engine = db.create_engine("sqlite:///crypto_analyzer.db")
connection = engine.connect()
metadata = db.MetaData()
# dbf = DatabaseFiller()


def generate_request(columns, db_table):
    request = 'SELECT '
    for col in columns:
        request += col
        if col == columns[-1]:
            request += ' '
        else:
            request += ', '
    request += 'FROM ' + db_table
    if currencies_combobox.get() != 'All':
        request += " WHERE symbol='" + currencies_combobox.get()[1:] + "'"
    return request


def fill_table():
    for i in table_treeview.get_children():
        table_treeview.delete(i)
    required_columns = form_column_list()
    request = generate_request(required_columns, radio.get())
    result = engine.execute(request)
    table_treeview["columns"] = required_columns
    for col in required_columns:
        table_treeview.column(col, stretch=False, width=64)
        table_treeview.heading(col, text=col)
    table_treeview["show"] = "headings"
    tuples = result.fetchall()
    index = 0
    for row in tuples:
        table_treeview.insert("", index, values=str(row).strip('()').replace(',', '').replace("'", ''))
        index += 1


def form_column_list():
    col_list = ['symbol']
    if check1.get() != '':
        col_list.append(check1.get())
    if check2.get() != '':
        col_list.append(check2.get())
    if check3.get() != '':
        col_list.append(check3.get())
    if check4.get() != '':
        col_list.append(check4.get())
    if check5.get() != '':
        col_list.append(check5.get())
    if check6.get() != '':
        col_list.append(check6.get())
    if check7.get() != '':
        col_list.append(check7.get())
    if check8.get() != '':
        col_list.append(check8.get())
    if check9.get() != '':
        col_list.append(check9.get())
    if check10.get() != '':
        col_list.append(check10.get())
    if check11.get() != '' and radio.get() != 'tickers':
        col_list.append(check11.get())
    if check12.get() != '' and radio.get() != 'tickers':
        col_list.append(check12.get())
    if check13.get() != '' and radio.get() != 'tickers':
        col_list.append(check13.get())
    if check14.get() != '' and radio.get() != 'tickers':
        col_list.append(check14.get())
    return col_list


def print_info():
    messagebox.showinfo("About", "We just wanted to do something normal.\n:)")


# not working
def refresh_database():
    # dbf.refresh_tickers_table()
    # fill_table()
    pass


def get_currencies(currencies_type):
    if not currencies_type:
        pairs_file = open('pairs.txt', 'r')
        text = pairs_file.read()
        pairs = text.split('\n')
        pairs_file.close()
        pairs.insert(0, 'All')
        return pairs
    else:
        pairs_file = open('currencies.txt', 'r')
        text = pairs_file.read()
        pairs = text.split('\n')
        pairs_file.close()
        pairs.insert(0, 'All')
        return pairs


def change_checkboxes():
    if radio.get() == 'tickers':
        check_btn11.config(state=tk.DISABLED)
        check_btn12.config(state=tk.DISABLED)
        check_btn13.config(state=tk.DISABLED)
        check_btn14.config(state=tk.DISABLED)

        currencies_combobox.configure(values=get_currencies(0))
    else:
        check_btn11.config(state=tk.ACTIVE)
        check_btn12.config(state=tk.ACTIVE)
        check_btn13.config(state=tk.ACTIVE)
        check_btn14.config(state=tk.ACTIVE)
        currencies_combobox.configure(values=get_currencies(1))
    fill_table()


# preparing root
root = tk.Tk()
root.minsize(1360, 570)
root.title('Crypto Analyzer')
root.resizable(False, False)


# system menus
menubar = tk.Menu(root)
main_menu = tk.Menu(menubar, tearoff=0)
main_menu.add_command(label="Form Table", command=fill_table)
main_menu.add_separator()
main_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=main_menu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=print_info)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


# creating controls
content = tk.Frame(root)
instrument = tk.Frame(root)

table_treeview = ttk.Treeview(content, height=25)
treeXScroll = ttk.Scrollbar(content, orient=tk.HORIZONTAL)
treeXScroll.configure(command=table_treeview.xview)
table_treeview.configure(xscrollcommand=treeXScroll.set)
treeYScroll = ttk.Scrollbar(content, orient=tk.VERTICAL)
treeYScroll.configure(command=table_treeview.yview)
table_treeview.configure(yscrollcommand=treeYScroll.set)

currencies_combobox = ttk.Combobox(instrument, values=get_currencies(0))
currencies_combobox.current(0)
form_btn = tk.Button(instrument, text='Form Table', width=10, command=fill_table)
label_checkboxes = tk.Label(instrument, text='Select columns:')
label_radio = tk.Label(instrument, text='Select tickers:')

# checkboxes and radiobuttons
check1 = tk.StringVar()
check2 = tk.StringVar()
check3 = tk.StringVar()
check4 = tk.StringVar()
check5 = tk.StringVar()
check6 = tk.StringVar()
check7 = tk.StringVar()
check8 = tk.StringVar()
check9 = tk.StringVar()
check10 = tk.StringVar()
check11 = tk.StringVar()
check12 = tk.StringVar()
check13 = tk.StringVar()
check14 = tk.StringVar()

check_btn1 = tk.Checkbutton(instrument, text='bid', variable=check1, onvalue='bid', offvalue='')
check_btn2 = tk.Checkbutton(instrument, text='bid_size', variable=check2, onvalue='bid_size', offvalue='')
check_btn3 = tk.Checkbutton(instrument, text='ask', variable=check3, onvalue='ask', offvalue='')
check_btn4 = tk.Checkbutton(instrument, text='ask_size', variable=check4, onvalue='ask_size', offvalue='')
check_btn5 = tk.Checkbutton(instrument, text='daily_change', variable=check5, onvalue='daily_change', offvalue='')
check_btn6 = tk.Checkbutton(instrument, text='daily_change_relative', variable=check6, onvalue='daily_change_relative', offvalue='')
check_btn7 = tk.Checkbutton(instrument, text='last_price', variable=check7, onvalue='last_price', offvalue='')
check_btn8 = tk.Checkbutton(instrument, text='volume', variable=check8, onvalue='volume', offvalue='')
check_btn9 = tk.Checkbutton(instrument, text='high', variable=check9, onvalue='high', offvalue='')
check_btn10 = tk.Checkbutton(instrument, text='low', variable=check10, onvalue='low', offvalue='')
check_btn11 = tk.Checkbutton(instrument, text='frr', variable=check11, onvalue='frr', offvalue='')
check_btn12 = tk.Checkbutton(instrument, text='bid_period', variable=check12, onvalue='bid_period', offvalue='')
check_btn13 = tk.Checkbutton(instrument, text='ask_period', variable=check13, onvalue='ask_period', offvalue='')
check_btn14 = tk.Checkbutton(instrument, text='frr_amount_available', variable=check14, onvalue='frr_amount_available', offvalue='')

check_btn1.grid(row=2, column=0, sticky=tk.W)
check_btn2.grid(row=2, column=1, sticky=tk.W, padx=(0, 10))
check_btn3.grid(row=3, column=0, sticky=tk.W)
check_btn4.grid(row=3, column=1, sticky=tk.W, padx=(0, 10))
check_btn5.grid(row=4, column=0, sticky=tk.W)
check_btn6.grid(row=4, column=1, sticky=tk.W, padx=(0, 10))
check_btn7.grid(row=5, column=0, sticky=tk.W)
check_btn8.grid(row=5, column=1, sticky=tk.W, padx=(0, 10))
check_btn9.grid(row=6, column=0, sticky=tk.W)
check_btn10.grid(row=6, column=1, sticky=tk.W, padx=(0, 10))
check_btn11.grid(row=7, column=0, sticky=tk.W)
check_btn12.grid(row=7, column=1, sticky=tk.W, padx=(0, 10))
check_btn13.grid(row=8, column=0, sticky=tk.W)
check_btn14.grid(row=8, column=1, sticky=tk.W, padx=(0, 10))

radio = tk.StringVar()

radio_btn1 = tk.Radiobutton(instrument, text='Pair', variable=radio, value='tickers', command=change_checkboxes)
radio_btn2 = tk.Radiobutton(instrument, text='Currency', variable=radio, value='tickers_on_currency', command=change_checkboxes)
radio_btn1.select()
radio_btn2.deselect()
radio_btn1.grid(row=10, column=0, sticky=tk.W)
radio_btn2.grid(row=10, column=1, sticky=tk.W)

change_checkboxes()

# placing controls
content.grid(row=0, column=0, sticky=tk.W)
table_treeview.grid(row=0, column=0, rowspan=6, columnspan=6, padx=(10, 0), pady=(10, 0))
treeXScroll.grid(row=7, column=0, columnspan=6, sticky=tk.W + tk.E, padx=(10, 5), pady=(0, 10))
treeYScroll.grid(row=0, column=7, rowspan=6, sticky=tk.N + tk.S, padx=(0, 5), pady=(10, 0))

instrument.grid(row=0, column=1, sticky=tk.NE)
currencies_combobox.grid(row=0, column=0, padx=(5, 10), pady=(10, 10))
form_btn.grid(row=11, column=1, sticky=tk.E, padx=(5, 10), pady=(10, 0))
label_checkboxes.grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
label_radio.grid(row=9, column=0, sticky=tk.W, pady=(10, 0))

fill_table()

root.mainloop()
