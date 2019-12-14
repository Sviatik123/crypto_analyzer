from database_filler import DatabaseFiller

db = DatabaseFiller()
db.create_tickers_table()
db.fill_tickers_table()
db.fill_tickers_table()