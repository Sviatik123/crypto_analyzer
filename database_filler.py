import sqlalchemy as db
from bfxapi import Client
import asyncio


class DatabaseFiller:
    def __init__(self):
        self.bfx = Client()
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

    def create_tickers_on_currency_table(self):
        self.tickers_on_currency = db.Table('tickers_on_currency', self.metadata,
                                            db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
                                            db.Column('symbol', db.String(15)),
                                            db.Column('frr', db.Float()),
                                            db.Column('bid', db.Float()),
                                            db.Column('bid_period', db.Float()),
                                            db.Column('bid_size', db.Float()),
                                            db.Column('ask', db.Float()),
                                            db.Column('ask_period', db.Float()),
                                            db.Column('ask_size', db.Float()),
                                            db.Column('daily_change', db.Float()),
                                            db.Column('daily_change_relative', db.Float()),
                                            db.Column('last_price', db.Float()),
                                            db.Column('volume', db.Float()),
                                            db.Column('high', db.Float()),
                                            db.Column('low', db.Float()),
                                            db.Column('frr_amount_available', db.Float()))

        self.metadata.create_all(self.engine)

    def refresh_tickers_on_currency_table(self):
        delete = self.tickers_on_currency.delete()
        self.connection.execute(delete)
        with open('currencies.txt', 'r+') as file:
            currency = file.read().split(sep='\n')

        async def run():
            tickers = await self.log_mul_tickers(currency)
            for el in tickers:
                ins = self.tickers_on_currency.insert().values(
                    symbol=el[0][1:],
                    frr=el[1],
                    bid=el[2],
                    bid_period=el[3],
                    bid_size=el[4],
                    ask=el[5],
                    ask_period=el[6],
                    ask_size=el[7],
                    daily_change=el[8],
                    daily_change_relative=el[9],
                    last_price=el[10],
                    volume=el[11],
                    high=el[12],
                    low=el[13],
                    frr_amount_available=el[16],
                )
                self.connection.execute(ins)

        # t = asyncio.ensure_future(run())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())
        print("database was successfully updated")

        # loop.close()

    def refresh_tickers_table(self):
        delete = self.tickers.delete()
        self.connection.execute(delete)
        with open('pairs.txt', 'r') as file:
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
