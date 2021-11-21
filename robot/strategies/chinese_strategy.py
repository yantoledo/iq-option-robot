from finta import TA
from time import time, sleep
from datetime import datetime
import pandas as pd

from robot.config import config


class ChineseStrategy:
    def __init__(self, iq_option):
        self.iq_option = iq_option

    def get_data(self, pair, timeframe, periods=200):
        """Get data from iq options candles"""
        candles = self.iq_option.get_candles(pair, timeframe * 60, periods, time())
        df = pd.DataFrame(candles)
        df.rename(columns={"max": "high", "min": "low"}, inplace=True)
        return df

    def mov_avar_dev(self, df, periods=20):
        """Definition of SSMA from cadles dataset"""
        src = TA.SSMA(df, periods)
        calc = df.iloc[-1]["close"] - src.iloc[-1]  # Move average deviation rate
        return (
            calc,
            "green" if calc >= (df.iloc[-2]["close"] - src.iloc[-2]) else "red",
        )

    def input(self, pair, direction, timeframe):
        """Method to do an iq option input (Call or Put)"""
        print("\n Abrindo operação")
        status, id = self.iq_option.buy_digital_spot_v2(pair, direction, timeframe)

        if status:
            status = False
            while status == False:
                status, gain = self.iq_option.check_win_digital_v2(id)
            if gain > 0:
                print(f"WIN, Lucro de: {gain}")
            else:
                print(f"LOSS, Perda de: {gain}")
        else:
            print("Erro ao abrir informação")

    def run(self):
        """Method to run the strategy"""
        print("\n")
        while True:
            df = self.get_data(config.PAIR, config.TIMEFRAME, 200)

            rate, color = self.mov_avar_dev(df, 20)

            ssma_3 = TA.SSMA(df, 3)
            ssma_50 = TA.SSMA(df, 50)
            if (
                ssma_3.iloc[-1] <= ssma_50.iloc[-1]
                and ssma_3.iloc[-2] > ssma_50.iloc[-2]
                and color == "red"
            ):
                self.input(config.PAIR, direction="put", timeframe=config.TIMEFRAME)
            elif (
                ssma_3.iloc[-1] >= ssma_50.iloc[-1]
                and ssma_3.iloc[-2] < ssma_50.iloc[-2]
                and color == "green"
            ):
                self.input(config.PAIR, direction="call", timeframe=config.TIMEFRAME)

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}]:: Aguardando oportunidade de entrada..",
                end="\r",
            )
