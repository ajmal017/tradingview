//@version=4
strategy("Random Strategy with 3 TP levels and SL", overlay=true,max_bars_back = 50)

tpx = input(defval = 0.4, title = 'Atr multiplication for TPs?')
slx = input(defval = 0.6, title = 'Atr multiplication for SL?')
isLong = false
isLong := nz(isLong[1])

isShort = false
isShort := nz(isShort[1])

entryPrice = 0.0
entryPrice := nz(entryPrice[1])
tp1 = true
tp1 := nz(tp1[1])
tp2 = true
tp2 := nz(tp2[1])

sl_price = 3213.0
sl_price := nz(sl_price[1])

sl_atr = atr(14)*slx
tp_atr = atr(14)*tpx

rd_number_entry = 1.0
rd_number_entry := (16708 * nz(rd_number_entry[1], 1) % 2147483647)%17

rd_number_exit = 1.0
rd_number_exit := ((16708 * time % 2147483647) %17)


//plot(rd_number_entry)

shortCondition = (rd_number_entry == 13? true:false) and (year >= 2017) and not isLong and not isShort
longCondition = (rd_number_entry == 11 ? true:false) and (year >= 2017) and not isShort and not isShort
//Never exits a trade:
exitLong = (rd_number_exit == 22?true:false) and (year >= 2018) and not isShort
exitShort = (rd_number_exit ==  22?true:false) and (year >= 2018) and not isLong


//shortCondition = crossunder(sma(close, 14), sma(close, 28)) and year >= 2017
//longCondition = crossover(sma(close, 14), sma(close, 28)) and year >= 2017

//exitLong = crossunder(ema(close, 14), ema(close, 28)) and year >= 2017
//exitShort = crossover(ema(close, 14), ema(close, 28)) and year >= 2017

if (longCondition and not isLong)
    strategy.entry('Long1', strategy.long)
    strategy.entry('Long2', strategy.long)
    strategy.entry('Long3', strategy.long)
    isLong := true
    entryPrice := close
    isShort := false
    tp1 := false
    tp2 := false
    sl_price := close-sl_atr

if (shortCondition and not isShort)
    strategy.entry('Short1', strategy.short)
    strategy.entry('Short2', strategy.short)
    strategy.entry('Short3', strategy.short)
    isShort := true
    entryPrice := close
    isLong := false
    tp1 := false
    tp2 := false
    sl_price := close+sl_atr
    
if (exitShort and isShort)
    strategy.close('Short1')
    strategy.close('Short2')
    strategy.close('Short3')
    isShort :=  false

if (exitLong and isLong)
    strategy.close('Long1')
    strategy.close('Long2')
    strategy.close('Long3')
    isLong :=  false

if isLong
    if (close > entryPrice + tp_atr) and not tp1
        strategy.close('Long1')
        tp1 := true
        sl_price := close - tp_atr
    if (close > entryPrice + 2*tp_atr) and not tp2
        strategy.close('Long2')
        tp2 := true
        sl_price := close - tp_atr
    if (close > entryPrice + 3*tp_atr)
        strategy.close('Long3')
        isLong := false
    if (close < sl_price)
        strategy.close('Long1')
        strategy.close('Long2')
        strategy.close('Long3')
        isLong := false

if isShort
    if (close < entryPrice - tp_atr) and not tp1
        strategy.close('Short1')
        sl_price := close + tp_atr
        tp1 := true
    if (close < entryPrice - 2*tp_atr) and not tp2
        strategy.close('Short2')
        sl_price := close + tp_atr
        tp2 := true
    if (close < entryPrice - 3*tp_atr)
        strategy.close('Short3')
        isShort := false
    if (close > sl_price)
        strategy.close('Short1')
        strategy.close('Short2')
        strategy.close('Short3')
        isShort := false
plot(atr(14)*slx)
plot(sl_price)
