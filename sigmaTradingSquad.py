
import numpy as np
import pandas as pd

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)


def getMyPosition(prcSoFar):
    global currentPos
    # rows are days 
    # columns are the stocks
    days, stocks = prcSoFar.shape
    # (nins, nt) = prcSoFar.shape

    print(type(prcSoFar))
    for col in range(0, 50):
        # print("Stock number " + str(col))
        stock_df = pd.DataFrame({'Close': prcSoFar[col, :]})
        stock_df['ema_short'] = stock_df['Close'].ewm(span=20, adjust=False).mean()
        stock_df['ema_long'] = stock_df['Close'].ewm(span=50, adjust=False).mean()
        stock_df['bullish'] = 0.0
        stock_df['bullish'] = np.where(stock_df['ema_short'] > stock_df['ema_long'], 1.0, 0.0)
        stock_df['crossover'] = stock_df['bullish'].diff()
        # print(stock_df)
        # Check the last element in 'crossover'
        last_crossover_value = stock_df['crossover'].iloc[-1]
        # buy signal == 1
        if last_crossover_value == 1:
            currentPos[col] = 500
        # sell signal == -1
        elif last_crossover_value == -1:
            currentPos[col] = -500
        else:
            currentPos[col] = 0
    print("currentPos")
    print(currentPos)
    return currentPos
