import sqlalchemy as db
from bfxapi import Client
import asyncio

bfx = Client(
    logLevel='DEBUG',
)

async def log_mul_tickers(pairs = []):
    tickers = await bfx.rest.get_public_tickers(pairs)
    print("Tickers:")
    print(tickers)
    return tickers

engine = db.create_engine("sqlite:///test.db")
connection = engine.connect()
metadata = db.MetaData()
test = db.Table('test', metadata,
    db.Column('cookie_id', db.Integer(), primary_key=True, autoincrement = True),
    db.Column('cookie_name', db.String(50), index=True),
    db.Column('cookie_recipe_url', db.String(255)),
    db.Column('cookie_sku', db.String(55)),
    db.Column('quantity', db.Integer()),
    db.Column('unit_cost', db.Numeric(12, 2)))

ins = test.insert().values(
cookie_name="chocolate chip",
cookie_recipe_url="http://some.aweso.me/cookie/recipe.html",
cookie_sku="CC01",
quantity="12",
unit_cost="0.50"
)
#print(str(ins))
metadata.create_all(engine)
connection.execute(ins)
#print(test.columns.keys())

crypto = db.Table('crypto', metadata,
    db.Column('id', db.Integer(), primary_key=True, autoincrement = True),
    db.Column('symbol', db.String(15)),
    db.Column('bid', db.Float()),
    db.Column('bid_size', db.Float()),
    db.Column('ask', db.Float()),
    db.Column('ask_size', db.Float()),
    db.Column('daily_change', db.Float()),
    db.Column('daily_change_relative', db.Float()),
    db.Column('last_price', db.Float()),
    db.Column('volume', db.Float()),
    db.Column('high', db.Float()),
    db.Column('low', db.Float()))

metadata.create_all(engine)

pairs = ['tBTCUSD', 'tBTCEUR', 'tETHUSD', 'tETHEUR']
async def run():
    tickers = await log_mul_tickers(pairs)
    for el in tickers:
        ins = crypto.insert().values(
            symbol = el[0],
            bid = el[1],
            bid_size = el[2],
            ask = el[3],
            ask_size = el[4],
            daily_change = el[5],
            daily_change_relative = el[6],
            last_price = el[7],
            volume = el[8],
            high = el[9],
            low = el[10],
        )
        connection.execute(ins)

t = asyncio.ensure_future(run())
asyncio.get_event_loop().run_until_complete(t)