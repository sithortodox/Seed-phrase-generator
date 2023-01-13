import mnemonic
import bitcoin
import requests
import time
from telegram.bot import Bot

# Add proxy support
proxies = {}
with open("proxy.txt") as f:
    proxy = f.readline().strip()
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }

bot = Bot(token="YOUR_TOKEN")
chat_id = your_chat_id

try:
    bot.send_message(chat_id=chat_id, text="Начинаем майнить бабло)")
except TelegramError as e:
    print("Error sending message to Telegram: ", e)
    # You can add any additional error handling here

address_count = 0
while address_count < 1000000:
    # Generate a random mnemonic phrase
    mnemo = mnemonic.Mnemonic("english")
    secret_phrase = mnemo.generate(strength=256)

    # Convert the mnemonic phrase to a seed
    seed = mnemonic.Mnemonic.to_seed(secret_phrase)

    # Generate the private key from seed
    priv = bitcoin.sha256(seed)

    # Generate the public key from private key
    pub = bitcoin.privtopub(priv)

    # Generate the address from public key
    address = bitcoin.pubtoaddr(pub)

    # check balance and number of transactions
    response = requests.get("https://blockchain.info/rawaddr/" + address)
    if response.status_code == 200:
        data = response.json()
        balance = data["final_balance"]
        transactions = data["n_tx"]
        print("Checking address: ", address)
        print("Balance: ", balance)
        print("Number of transactions: ", transactions)
        
        if balance > 0 or transactions > 0:
            with open("good.txt", "w") as f:
                f.write(address + " : " + secret_phrase)
                message = address + " : " + secret_phrase
                bot.send_message(chat_id=chat_id, text=message)
            break
                        
    elif response.status_code == 404:
        print(f"Address {address} not found")
    else:
        print(f"Request failed with status code {response.status_code}")
    time.sleep(5)
    address_count += 1
