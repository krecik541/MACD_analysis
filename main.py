import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math

# #pobieranie danych
symbol = "CDR.WA"  # Symbol giełdowy CD Projekt Red na giełdzie w Warszawie

data = yf.download(symbol, period="max")

last_1000_data = data.tail(1000)

last_1000_data.to_csv("cd_project_red_historical_data.csv")

#import danych

fsize = (10,6)

def EMA(N, p):
    ema = []
    alfa = 2/(N + 1)
    for i in range(N):
        ema.append(0)
    for i in range(N, len(p)):
        nominator = 0
        denominator = 0
        for j in range(i-N, i):
            nominator += p[j] * (1 - alfa) ** (i-j)
            denominator += (1-alfa) ** (i-j)
        ema.append(nominator/denominator)
    return ema

def cross_points(macd, signal):
    cross = []
    for i in range(1, len(macd)):
        if(macd[i-1] < signal[i-1]) and (macd[i] > signal[i]):
            if(abs(macd[i-1] - signal[i-1]) < abs(macd[i] - signal[i])):
                cross.append((i, "BUY", 0.7))
            else:
                cross.append((i,"BUY", -0.1))
        elif(macd[i-1] > signal[i-1]) and (macd[i] < signal[i]):
            if (abs(macd[i - 1] - signal[i - 1]) < abs(macd[i] - signal[i])):
                cross.append((i, "SELL", 0.7))
            else:
                cross.append((i, "SELL", -0.1))
    return cross

def buy_sell_label(point, buyFlag, sellFlag):
    labels = "Kupno" if point[1] == "BUY" and buyFlag == 0 else None
    labels = "Sprzedaz" if point[1] == "SELL" and sellFlag == 0 else labels
    if labels == "Kupno":
        buyFlag = 1
    elif labels == "Sprzedaz":
        sellFlag = 1
    return labels, buyFlag, sellFlag

def money_value(closePrice, cross):
    shares = []
    shares_money = []
    money = []
    money.append(0)
    shares.append(1000)
    i = 0
    for j in range(len(closePrice)):
        if cross[i][0] == j and i != len(cross)-1:
            i+=1
        point = cross[i]
        if point[1] == "BUY":
            val = (money[-1] / closePrice[point[0]])
            shares.append(val + shares[-1])
            money.append(money[-1] - val * closePrice[point[0]])
        elif point[1] == "SELL":
            money.append(money[-1] + closePrice[point[0]] * shares[-1])
            shares.append(0)
        else:
            money.append(money[-1])
        shares_money.append(closePrice[j] * shares[-1])
    return money[1:], shares_money

def signal_macd_plot(date, macd, signal, title, saveTitle, ticks, start, end):
    buyFlag = 0
    sellFlag = 0
    plt.figure(figsize=fsize)
    plt.plot(date, macd, label='MACD', color='blue')
    plt.plot(date, signal, label='SIGNAL', color='orange')
    for point in cross:
        if start <= point[0] < end:  # Sprawdź, czy indeks jest w zakresie
            labels, buyFlag, sellFlag = buy_sell_label(point, buyFlag, sellFlag)
            plt.scatter(point[0] - start,
                        macd[point[0]-start],
                        color='red' if point[1] == 'SELL' else 'green', marker='^' if point[1] == 'BUY' else 'v', s=30,
                        zorder=3,
                        label=labels)
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(date[start:end:ticks], rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.savefig(saveTitle)
    plt.show()


def buy_sell_price_plot(title, saveTitle, ticks, start, end):
    buyFlag = 0
    sellFlag = 0
    plt.figure(figsize=fsize)
    plt.plot(date[start:end], closePrice[start:end], label='Cena zamknięcia')
    for point in cross:
        if start <= point[0] < end:
            labels, buyFlag, sellFlag = buy_sell_label(point, buyFlag, sellFlag)
            plt.scatter(point[0] - start, closePrice[point[0]], color='green' if point[1] == 'BUY' else 'red',
                        marker='^' if point[1] == 'BUY' else 'v', s=30, zorder=2,
                        label=labels)
    plt.title(title)
    plt.xlabel('Data')
    plt.ylabel('Wartość')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(date[start:end:ticks], rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.savefig(saveTitle)
    plt.show()


def money_shares_plot(title, saveTitle, ticks, start, end):
    plt.figure(figsize=fsize)
    plt.plot(date[start:end], shares[start:end], label='Shares', color='blue')
    plt.plot(date[start:end], money[start:end], label='Money', color='green')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title(title)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(date[start:end:ticks], rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.savefig(saveTitle)
    plt.show()
    print(shares[start] + money[start])
    print(shares[end-1]+money[end-1])

df = pd.read_csv('cd_project_red_historical_data.csv')
closePrice = df['Close']
date = df['Date']

# wyznaczanie macd
ema12 = EMA(12, closePrice)
ema26 = EMA(26, closePrice)
macd = [ema12[i] - ema26[i] for i in range(26, len(closePrice))]

# wyznaczanie signal
signal = EMA(9, macd)

macd = macd[9:]
signal = signal[9:]

# punkty przecięcia signal/macd -> punkty kupna/sprzedaży
cross = cross_points(macd, signal)

# liczenie zysków/strat
money, shares = money_value(closePrice, cross)

# Wykres ceny zamknięcia wraz
plt.figure(figsize=fsize)
plt.plot(date, closePrice, color='green', label='Cena zamknięcia')
plt.title('Wykres 1: Notowania akcji CD Projekt Red')
plt.xlabel('Data')
plt.ylabel('Cena zamknięcia')
plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(date[::80], rotation=45)
plt.tight_layout()
plt.legend()
plt.savefig('notowania_akcji.png')
plt.show()

start = 0
end = len(date)
# Wykres SIGNAL/MACD wraz z znacznikami kupna/sprzedaży
signal_macd_plot(date[35:len(date)], macd, signal, 'Wykres 2: Wskaźnik MACD i SIGNAL wraz z punktami kupna/sprzedaży', 'macd_signal.png', 80, start, end)
# Wykres ceny zamknięcia wraz z znacznikami kupna/sprzedaży
buy_sell_price_plot('Wykres 3:  Notowania akcji CD Projekt Red wraz z markerami kupna/sprzedaży', 'notowania_akcji_kupno_sprzedaz.png', 80, start, end)
# Wykres przedstawiający zmianę w czasie ilości posiadanych akcji i pieniędzy
money_shares_plot('Wykres: zmiana kapitału na przestrzeni czasu', 'money_shares.png', 80, start, end)

starts = [(81, 209), (360, 465), (460, 653), (881, 960)]
for st in starts:
    start = st[0]
    end = st[1]
    ticks = math.floor((end-start)/10)
    signal_macd_plot(date[start:end], macd[start:end], signal[start:end], 'Wykres z sugerowanymi punktami kupna/sprzedaży', 'macd_signal_' + str(st) + '.png', ticks, start, end)
    buy_sell_price_plot('Wykres z sugerowanymi punktami kupna/sprzedaży', 'notowania_akcji_kupno_sprzedaz_' + str(st) + '.png', ticks, start, end)
    money_shares_plot('Wykres zmiany kapitału', 'money_shares_' + str(st) + '.png', ticks, start, end)


#wykres tego jak zmieniają się ilość pieniędzy
#transakcje