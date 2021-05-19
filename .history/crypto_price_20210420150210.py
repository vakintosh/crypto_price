from urllib.request import urlopen
import ast,time,sys,os

which_crypto = str(sys.argv[1]).lower()
which_currency = str(sys.argv[2]).lower()
telegram_bot = 'your_telegran_bot_token'
telegram_id = 'your_telegran_bot_id'
min_threshold = int(sys.argv[3])
max_threshold = int(sys.argv[4])
time_interval = 9 * 60 # in seconds
track_currency = f"https://api.kraken.com/0/public/Ticker?pair={(which_crypto+which_currency)}"


print("This process has the PID", os.getpid())

def convert_to_dict(link):
    """CONVERT TO DICT THE DATA FROM @KRAKEN"""
    f = urlopen(link)
    data_link = f.read()
    data_decode = data_link.decode("UTF-8")
    currency = ast.literal_eval(data_decode)
    return currency

def get_price(letter,number):
    """GET THE PRICE OF THE CHOOSEN CURRENCY"""
    currency_choosen = convert_to_dict(track_currency)
    currency_name = currency_choosen["result"]
    coin_name = list(currency_name.keys())[0]
    price = currency_name[f"{coin_name}"]["a"][0]
    return price.split('.')[0]

def telegram_message(telegram_id, msg):
    """Send message to telegram"""
    url = f"https://api.telegram.org/bot{telegram_bot}/sendMessage?chat_id={telegram_id}&text={msg}"

    # send the msg
    urlopen(url).read()

def main ():
    last_price_list = []

    while True:
        currency_last_price = int(get_price("a",0))
        last_price_list.append(currency_last_price)

        if currency_last_price < min_threshold:
            telegram_message(telegram_id=telegram_id, msg=f'/!\%20DUMP%20ALERT,%20{which_crypto.upper()}:%20{currency_last_price}')
        elif currency_last_price > max_threshold:
            telegram_message(telegram_id=telegram_id, msg=f'/!\%20PUMP%20ALERT,%20{which_crypto.upper()}:%20{currency_last_price}')

        if len(last_price_list) >= 10:
            # empty the price_list
            last_price_list = []
        
        time.sleep(time_interval)
        print(last_price_list)

if __name__ == '__main__':
    main()

#TO DO : CHECK SINCE WHEN THE PRICE IS LOW 
