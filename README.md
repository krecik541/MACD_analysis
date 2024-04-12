## Analiza wskaźnika MACD dla akcji CD Projekt Red
# Opis:
Program ten analizuje wskaźnik MACD (Moving Average Convergence Divergence) dla akcji CD Projekt Red na giełdzie w Warszawie (symbol: CDR.WA). Wykorzystuje dane historyczne pobrane za pomocą biblioteki yfinance oraz oblicza średnie kroczące wykładnicze (EMA) oraz punkty przecięcia MACD z linią sygnału, sugerujące momenty kupna i sprzedaży akcji.

# Dane wejściowe:
Symbol giełdowy: "CDR.WA"
Okres analizy: maksymalny dostępny

# Funkcje:
EMA(N, p): Oblicza średnie kroczące wykładnicze (Exponential Moving Averages) dla danych wejściowych.
cross_points(macd, signal): Określa punkty przecięcia między MACD a linią sygnału.
buy_sell_label(point, buyFlag, sellFlag): Przypisuje etykiety punktom kupna i sprzedaży.
money_value(closePrice, cross): Oblicza wartość pieniężną transakcji na podstawie punktów przecięcia.

# Wykresy generowane przez program:
Notowania akcji CD Projekt Red: Wykres przedstawiający zmianę cen zamknięcia w czasie.
Wskaźnik MACD i SIGNAL z punktami kupna/sprzedaży: Wykres obrazujący wskaźnik MACD oraz linię sygnału wraz z zaznaczonymi punktami kupna i sprzedaży.
Notowania akcji CD Projekt Red z markerami kupna/sprzedaży: Wykres cen zamknięcia z zaznaczonymi punktami kupna i sprzedaży.
Zmiana kapitału w czasie: Wykres przedstawiający zmianę ilości posiadanych akcji oraz pieniędzy w czasie.

# Generowanie dodatkowych wykresów:
Program generuje również dodatkowe wykresy dla wybranych przedziałów czasowych, z zaznaczonymi punktami sugerującymi kupno i sprzedaż akcji.
