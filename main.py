from iqoptionapi.stable_api import IQ_Option
from robot.config import config
from robot.strategies import ChineseStrategy
import time, json

iq_option = IQ_Option(config.LOGIN, config.PASSWORD)
check, reason = iq_option.connect()

iq_option.change_balance(config.ACCOUNT_TYPE)


if check:
    print("Conectado com sucesso")
else:
    print("Erro ao se conectar")
    input("\n\nAperte ENTER para sair")
    exit()


if check:
    strategy = ChineseStrategy(iq_option)

    strategy.run()
