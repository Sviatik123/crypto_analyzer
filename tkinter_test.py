import tkinter as tk
import tkinter.ttk as ttk
import sqlalchemy as db

engine = db.create_engine("sqlite:///crypto_analyzer.db")
connection = engine.connect()
metadata = db.MetaData()


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
        table_treeview.column(col, width=90)
        table_treeview.heading(col, text=col)
    tuples = result.fetchall()
    index = 0
    for row in tuples:
        table_treeview.insert("", index, values=str(row).strip('()').replace(',', ''))
        index += 1


def form_column_list():
    col_list = []
    '''form col list'''
    fill_table(col_list)


def refresh_database():
    pass


def print_info():
    pass


def get_pairs():
    pairs_file = open('pairs.txt', 'r')
    text = pairs_file.read()
    pairs = text.split('\n')
    pairs_file.close()
    return pairs


root = tk.Tk()
root.minsize(1000, 500)
root.title('Crypto Analyzer')
root.resizable(False, False)

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


table_frame = tk.LabelFrame(root, text='Frame1', padx=10, pady=10)

table_frame.grid(row=0, column=0, padx=10)


table_treeview = ttk.Treeview(table_frame, height=19)
fill_table()
scbV = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=table_treeview.yview)#not working
table_treeview.configure(yscrollcommand=scbV.set)#not working
table_treeview.pack(pady=5)

refresh_btn = tk.Button(table_frame, text='Refresh', width=10)
refresh_btn.pack(pady=5)


controls_frame = tk.LabelFrame(root, text='Search Options', padx=10, pady=10)
controls_frame.grid(row=0, column=1, padx=10)

pairs_combobox = ttk.Combobox(controls_frame, values=get_pairs())
pairs_combobox.pack()

form_btn = tk.Button(controls_frame, text='Form Table', width=10, command=form_column_list)
form_btn.pack(pady=5)

root.mainloop()
