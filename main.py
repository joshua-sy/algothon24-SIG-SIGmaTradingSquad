import numpy as np
import pandas as pd

##### TODO #########################################
### RENAME THIS FILE TO YOUR TEAM NAME #############
### IMPLEMENT 'getMyPosition' FUNCTION #############
### TO RUN, RUN 'eval.py' ##########################

nInst = 50
currentPos = np.zeros(nInst)
numStocksHold = np.zeros(nInst)
lastAction = np.zeros(nInst)
priceBoughtAt = np.zeros(nInst)
hardStopPercent = 0.03
stopLossPt = 0.1
takeProfitPt = 0.1

def stopLoss(currPrice, stockNum, position):
    # Check if position is long 
    if position == 1:
        # Checks if the current price is less than 1 - stoploss percent of the price bought at
        # if so sell it and prevent loss
        if currPrice <= (priceBoughtAt[stockNum] - (stopLossPt * priceBoughtAt[stockNum])):
            return -1
    # Else it is short    
    else:
        # Checks if the current price is greater than 1 + stoploss percent of the price sold at
        # if so buy it and prevent further loss
        if currPrice >= (priceBoughtAt[stockNum] + (stopLossPt*priceBoughtAt[stockNum])):
            return 1
    
    # If the checks are good, then return 0 and do action based on ema wave
    return 0

def takeProfit(currPrice, stockNum, position):
    # Check if position is long 
    if position == 1:
        # Checks if the current price is less than 1 + takeProfit percent of the price bought at
        # if so sell it to get the profit
        if currPrice >= (priceBoughtAt[stockNum] + (takeProfitPt * priceBoughtAt[stockNum])):
            return -1
    # Else it is short    
    else:
        # Checks if the current price is less than 1 - takeProfitPt percent of the price sold at
        # if so buy it and get the profit
        if currPrice <= (priceBoughtAt[stockNum] - (takeProfitPt * priceBoughtAt[stockNum])):
            return 1
    
    # If the checks does not trigger, then return 0 and do action based on ema wave
    return 0

# checks the price after planned to buy/sell and current position
#  if less than the hardStop price then return the planend amount to buy /sell
# else return 0 to buy/sell
#  We can edit this to buy till it reaches maximum price by adding an equation
def checkHardPtStop(currPrice, numToBuySell, stockNum):
    global hardStopPercent
    global currentPos
    global numStocksHold

    # Currently rounding the hard stop price by using int
    # Change to a float, double, etc, if we want more precision

 
    hardStopPrice = int(10000 * hardStopPercent)
    # hardcodedBuy = 100 * currPrice + numStocksHold[stockNum] *currPrice
    # Changce back to currPos - i like numStocksHold -- better meanPL
    totalBuy = numToBuySell * currPrice + numStocksHold[stockNum] *currPrice
    
    # print("stockNum is " + str(stockNum))
    # print("currPrice is " + str(currPrice))
    # print("numToBuySell is " + str(numToBuySell))
    # print("hardStopPrice is " + str(hardStopPrice))
    # print("totalBuy is " + str(totalBuy) + " numToBuySell * currPrice = " + str(numToBuySell * currPrice) + " currentPos[stockNum] *currPrice = " + str(currentPos[stockNum] *currPrice))

    if (totalBuy > hardStopPrice or (-totalBuy) < hardStopPrice):
        return 0
    else:
        return numToBuySell


def getMyPosition(prcSoFar):
    global currentPos
    global lastAction
    global priceBoughtAt
    # rows are days 
    # columns are the stocks
    days, stocks = prcSoFar.shape
    # (nins, nt) = prcSoFar.shape

    # print(type(prcSoFar))
    for col in range(0, 50):
        # print("Stock number " + str(col))
        stock_df = pd.DataFrame({'Close': prcSoFar[col, :]})
        stock_df['ema_short'] = stock_df['Close'].ewm(span=20, adjust=False).mean()
        # stock_df['ema_short'] = stock_df['Close'].rolling(window=20).mean()
        # stock_df['ema_long'] = stock_df['Close'].rolling(window=100).mean()
        stock_df['ema_long'] = stock_df['Close'].ewm(span=100, adjust=False).mean()
        stock_df['bullish'] = 0.0
        stock_df['bullish'] = np.where(stock_df['ema_short'] > stock_df['ema_long'], 1.0, 0.0)
        stock_df['crossover'] = stock_df['bullish'].diff()
        # print(stock_df)
        # Check the last element in 'crossover'
        last_crossover_value = stock_df['crossover'].iloc[-1]
        currPrice = stock_df['Close'].iloc[-1]
        stopTakeSignal = 0
        if (numStocksHold[col] > 0 or numStocksHold[col] < 0):
            stopTakeSignal = stopLoss(currPrice, col, lastAction[col])
            stopTakeSignal = takeProfit(currPrice, col, lastAction[col])

        if stopTakeSignal != 0:
            # print("Stop and take profit kind of works " +str(stopTakeSignal))
            last_crossover_value == stopTakeSignal
        
        plannedBuySell = int(200 /currPrice)
      

        # buy signal == 1
        if last_crossover_value == 1:
            numStocksBuySell = checkHardPtStop(currPrice, 25, col)
            currentPos[col] = numStocksBuySell
            
            # currentPos != 0, that means we are buying
            if (currentPos[col] != 0):
                # If last action was a sell
                if lastAction[col] == -1:
                    # Cancel it out since we are buying back the stock
                    lastAction[col] == 0
                    # Also lets buy everything
                    currentPos[col] = numStocksHold[col]
                else:
                    # Else last action was either 1 or 0
                    lastAction[col] = 1
                    priceBoughtAt[col] = currPrice
                    numStocksHold[col] += currentPos[col]
        # sell signal == -1
        elif last_crossover_value == -1:
            # print("sell signal")
            numStocksBuySell = checkHardPtStop(currPrice, -25, col)
            currentPos[col] = numStocksBuySell
            # if (currentPos[col] == 0):
            #     lastAction[col] = -1
            # else:
            #     lastAction[col] = 0
            if (currentPos[col] != 0):
                # If last action was a buy
                if lastAction[col] == 1:
                    # Cancel it out since we are buying back the stock
                    lastAction[col] == 0
                    # Also lets sell everything
                    currentPos[col] = numStocksHold[col]
                else:
                    # Else last action was either -1 or 0
                    lastAction[col] = -1
                    priceBoughtAt[col] = currPrice
                    numStocksHold[col] += currentPos[col]
        else:
            currentPos[col] = 0
    # print("currentPos")
    # print(currentPos)
    return currentPos
