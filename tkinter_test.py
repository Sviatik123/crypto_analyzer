import tkinter as tk
import tkinter.ttk as ttk
import sqlalchemy as db
from database_filler import DatabaseFiller

engine = db.create_engine("sqlite:///crypto_analyzer.db")
connection = engine.connect()
metadata = db.MetaData()
# dbf = DatabaseFiller()


def generate_request(columns):
    request = 'SELECT '
    for col in columns:
        request += col
        if col == columns[-1]:
            request += ' '
        else:
            request += ', '
    request += 'FROM tickers'
    return request


def fill_table(required_columns=['symbol', 'bid', 'bid_size', 'ask', 'ask_size', 'daily_change', 'daily_change_relative', 'last_price', 'volume', 'high', 'low']):
    for i in table_treeview.get_children():
        table_treeview.delete(i)
    request = generate_request(required_columns)
    result = engine.execute(request)
    table_treeview["columns"] = required_columns
    table_treeview["show"] = "headings"
    for col in required_columns:
        table_treeview.column(col, stretch=False, width=90)
        table_treeview.heading(col, text=col)
    tuples = result.fetchall()
    index = 0
    for row in tuples:
        table_treeview.insert("", index, values=str(row).strip('()').replace(',', ''))
        index += 1


def form_column_list():
    col_list = ['symbol']
    '''form col list'''
    fill_table(col_list)


def refresh_database():
    # dbf.refresh_tickers_table()
    # fill_table()
    pass


def print_info():
    pass


def get_pairs():
    pairs_file = open('pairs.txt', 'r')
    text = pairs_file.read()
    pairs = text.split('\n')
    pairs_file.close()
    return pairs


#preparing root
root = tk.Tk()
root.minsize(1156, 500)
root.title('Crypto Analyzer')
root.resizable(False, False)


#system menus
menubar = tk.Menu(root)
main_menu = tk.Menu(menubar, tearoff=0)
main_menu.add_command(label="Refresh Database", command=refresh_database)
main_menu.add_separator()
main_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Menu", menu=main_menu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=print_info)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


#creating controls
content = ttk.Label(root)

table_treeview = ttk.Treeview(content, height=19)
fill_table()
treeXScroll = ttk.Scrollbar(content, orient=tk.HORIZONTAL)
treeXScroll.configure(command=table_treeview.xview)
table_treeview.configure(xscrollcommand=treeXScroll.set)

refresh_btn = tk.Button(content, text='Refresh', width=10)
pairs_combobox = ttk.Combobox(content, values=get_pairs())
form_btn = tk.Button(content, text='Form Table', width=10, command=form_column_list)


#placing controls
content.pack(side=tk.TOP)
table_treeview.grid(row=0, column=0, rowspan=6, columnspan=6, padx=(10, 5), pady=(10, 0))
treeXScroll.grid(row=7, column=0, columnspan=6, sticky=tk.W + tk.E, padx=(10, 5), pady=(0, 10))
refresh_btn.grid(row=8, column=0, pady=(10, 10))
pairs_combobox.grid(row=0, column=7, padx=(5, 10), pady=(10, 10))
form_btn.grid(row=8, column=7, sticky=tk.W, padx=(5, 10))

root.mainloop()
