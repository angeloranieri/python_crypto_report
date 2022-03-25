import requests
from datetime import datetime
import time
import json


class Bot:  # classe Bot a cui vengono assegnati i valori associati alle istanze
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'USD'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'b9930396-e802-4aa5-89da-8243ab238e56',
        }

    def currenciesData(self):  # funzione per ottenere i dati aggiornati sulle criptovalute
        r = requests.get(url=self.url, headers=self.headers,
                         params=self.params).json()
        return r['data']


impactBot = Bot()
dataJson = {}  # dizionario per la scrittura dei dati in json
while(1):  # ciclo per scaricare le informazioni
    now = datetime.now()
    if now.hour == 18 and now.minute == 30:  # orario di esecuzione del codice
        currencies = impactBot.currenciesData()
        bestCurrency = None  # valuta con valore maggiore
        for currency in currencies:
            if not bestCurrency or currency['quote']['USD']['volume_24h'] > bestCurrency['quote']['USD']['volume_24h']:
                bestCurrency = currency
        bestSymbol = bestCurrency['symbol']
        print(
            f'la criptovaluta con il volume maggiore nelle ultime 24h è {bestSymbol}')
        dataJson['criptovaluta con volume maggiore ultime 24h'] = bestSymbol

        # dizionario con i dati delle valute in base alla variazione percentuale
        changeCurrency = {}
        increaseCurrency = {}  # dizionatio con i dati di solamente le valute in aumento
        for currency in currencies:
            if currency['quote']['USD']['percent_change_24h'] > 0:
                symbol = currency['symbol']
                change = currency['quote']['USD']['percent_change_24h']
                # aggiunge i dati al dizionario
                increaseCurrency[symbol] = change
            else:
                symbol = currency['symbol']
                change = currency['quote']['USD']['percent_change_24h']
                # aggiunge i dati al dizionario
                changeCurrency[symbol] = change
        # dati ordinati dalla variazione peggiore alla migliore
        worstChange = sorted(changeCurrency.items(), key=lambda x: x[1])
        # dati ordinati dalla varizione maggiore di zero più grande alla più piccola
        bestIncrease = sorted(increaseCurrency.items(),
                              key=lambda x: x[1], reverse=True)
        # dati ordinati dalla vazione maggiore di zero più piccola alla più grande
        worstIncrease = sorted(increaseCurrency.items(), key=lambda x: x[1])
        # seleziona le prime 10
        print(
            f' le peggiori 10 criptovalute per variazione percentuale nelle ultime 24 h sono {worstChange[:10]}')
        # seleziona le prime 10
        print(
            f' le migliori 10 criptovalute per variazione percentuale nelle ultime 24 h sono {bestIncrease[:10]}')
        # seleziona le prime 10
        print(
            f' le peggiori 10 criptovalute per incremento percentuale nelle ultime 24 h sono {worstIncrease[:10]}')
        dataJson['peggiori 10 criptovalute per variazione percentuale ultime 24 h'] = worstChange[:10]
        dataJson['migliori 10 criptovalute per variazione percentuale ultime 24 h'] = bestIncrease[:10]
        dataJson['peggiori 10 criptovalute per incremento percentuale ultime 24 h'] = worstIncrease[:10]

        amount = 0  # quantità di denaro per acquistare le criptovalute
        amountVolume = 0  # quantità di denaro per acquistare le criptovalute selezionate per volume
        n = 0  # numero valute
        v = 76000000  # valore volume di riferimento
        for currency in currencies:
            price = currency['quote']['USD']['price']
            volume = currency['quote']['USD']['volume_24h']
            amount += price  # addiziona i prezzi delle criptovalute alla variabile amount
            n += 1
            if n == 20:
                print(
                    f'la quantità di denaro necessario per acquistare le prime 20 criptovalute è {amount:.2f}$')
                dataJson['denaro per acquistare prime 20 criptovalute'] = "{:.2f}".format(
                    amount)
            elif volume > v:
                amountVolume += price  # addiziona i prezzi delle criptovalute alla variabile amountVolume
        print(
            f'la quantità di denaro necessario per acquistare le criptovalute con volume superiore a 76.0000.000 $ è {amountVolume:.2f}$')
        dataJson['denaro per acquistare criptovalute con volume superiore a 76.0000.000 $'] = "{:.2f}".format(
            amountVolume)

        # quantità di denaro per acquistare le criptovalute ai prezzi del giorno precedente
        amountYesterday = 0
        nYesterday = 0  # numero valute al prezzo del giorno precedente
        for currency in currencies:
            price = currency['quote']['USD']['price']
            change = currency['quote']['USD']['percent_change_24h']
            # calcola il prezzo del giorno precedente
            priceYesterday = price / (1 + (change/100))
            # addiziona i prezzi alla variabile amountYesterday
            amountYesterday += priceYesterday
            nYesterday += 1
            if nYesterday == 20:
                print(
                    f'la quantità di denaro necessario per acquistare le prime 20 criptovalute il giorno precedente è {amountYesterday:.2f}$')
                dataJson['denaro per acquistare prime 20 criptovalute giorno precedente'] = "{:.2f}".format(
                    amountYesterday)
        break
# calcola la percentuale di guadagno o perdita
percentageProfit = (amount - amountYesterday) * 100 / amount
print(
    f'la percentuale di guadagno o perdita comprando le prime 20 criptovalute il giorno precedente è {percentageProfit:.2f}%')
dataJson['percentuale guadagno o perdita prime 20 criptovalute giorno precedente'] = "{:.2f}".format(
    percentageProfit)

fileJson = json.dumps(dataJson, indent=1)  # converte i dati in formato json
print(fileJson)
