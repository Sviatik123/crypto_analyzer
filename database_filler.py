import sqlalchemy as db
from bfxapi import Client
import asyncio

class DatabaseFiller:
    def __init__(self):
        self.bfx = Client(logLevel='DEBUG')
        self.engine = db.create_engine("sqlite:///crypto_analyzer.db")
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()

    async def log_mul_tickers(self, pairs=[]):
        tickers = await self.bfx.rest.get_public_tickers(pairs)
        print("Tickers:")
        print(tickers)
        return tickers

    def create_tickers_table(self):
        self.tickers = db.Table('tickers', self.metadata,
                          db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
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

        self.metadata.create_all(self.engine)

    def fill_tickers_table(self):
        delete = self.tickers.delete()
        self.connection.execute(delete)
        with open('pairs.txt', 'r+') as file:
            pairs = file.read().split(sep='\n')


        async def run():
            tickers = await self.log_mul_tickers(pairs)
            for el in tickers:
                ins = self.tickers.insert().values(
                    symbol=el[0][1:],
                    bid=el[1],
                    bid_size=el[2],
                    ask=el[3],
                    ask_size=el[4],
                    daily_change=el[5],
                    daily_change_relative=el[6],
                    last_price=el[7],
                    volume=el[8],
                    high=el[9],
                    low=el[10],
                )
                self.connection.execute(ins)


        # t = asyncio.ensure_future(run())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        print("database was successfully updated")
        # loop.close()

# bfx = Client(
#     logLevel='DEBUG',
# )
#
#
# async def log_mul_tickers(pairs=[]):
#     tickers = await bfx.rest.get_public_tickers(pairs)
#     print("Tickers:")
#     print(tickers)
#     return tickers
#
#
# engine = db.create_engine("sqlite:///test.db")
# connection = engine.connect()
# metadata = db.MetaData()
#
#
# crypto = db.Table('crypto', metadata,
#                   db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
#                   db.Column('symbol', db.String(15)),
#                   db.Column('bid', db.Float()),
#                   db.Column('bid_size', db.Float()),
#                   db.Column('ask', db.Float()),
#                   db.Column('ask_size', db.Float()),
#                   db.Column('daily_change', db.Float()),
#                   db.Column('daily_change_relative', db.Float()),
#                   db.Column('last_price', db.Float()),
#                   db.Column('volume', db.Float()),
#                   db.Column('high', db.Float()),
#                   db.Column('low', db.Float()))
#
# metadata.create_all(engine)
# delete = crypto.delete()
# connection.execute(delete)
# with open('pairs.txt', 'r+') as file:
#     pairs = file.read().split(sep='\n')
#
#
# async def run():
#     tickers = await log_mul_tickers(pairs)
#     for el in tickers:
#         ins = crypto.insert().values(
#             symbol=el[0][1:],
#             bid=el[1],
#             bid_size=el[2],
#             ask=el[3],
#             ask_size=el[4],
#             daily_change=el[5],
#             daily_change_relative=el[6],
#             last_price=el[7],
#             volume=el[8],
#             high=el[9],
#             low=el[10],
#         )
#         connection.execute(ins)
#
#
# # t = asyncio.ensure_future(run())
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
# loop.close()
