from database_filler import DatabaseFiller

db = DatabaseFiller()
db.create_tickers_table()
db.create_tickers_on_currency_table()
db.refresh_tickers_table()
db.refresh_tickers_on_currency_table()