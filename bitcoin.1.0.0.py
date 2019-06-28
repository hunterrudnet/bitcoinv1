import requests
import time
import datetime
import matplotlib.pyplot as plt

x = []
y = []

filename = 'bitcoin_log.txt'
last_price = 0
percent = 0
seconds = 0
formatted_percentage = "{:.1%}".format(percent/100000)

scrape_rate = input("What would you like your refresh rate to be? (in seconds)")
print("Ok...setting the refresh rate to {} seconds".format(scrape_rate))
duration = input("How many seconds would you like the program to run for?")
print("Ok...setting the program to run for {} seconds".format(duration))


while seconds < int(duration):
    url = requests.get('https://index-api.bitcoin.com/api/v0/price/usd').json()
    price = url['price']
    x.append(seconds/10)
    y.append(price)
    if price > last_price:
        try:
            percent = price / last_price
            print("The price of BTC has increased since the last query, up {} percent!".format(formatted_percentage))
        except ZeroDivisionError:
            print("This was the first query since the script started.")
            pass
    elif price < last_price:
        percent = last_price / price
        print("The price of BTC has decreased since the last query, down {} percent!".format(formatted_percentage))
    else:
        print("The price of BTC is unchanged since the last query")
    formatted_price = '${:,.2f}'.format(price/100)
    timestamp = datetime.datetime.now()
    print(formatted_price + "--" + str(timestamp))
    with open(filename, 'a') as file_object:
        file_object.write(formatted_price + "--" + str(timestamp) + "\n")
    last_price = price
    seconds = seconds + int(scrape_rate)
    time.sleep(int(scrape_rate))

plt.plot(x,y)
plt.xlabel('Query')
plt.ylabel('Price (USD)')
plt.title('Bitcoin')
plt.show()    
