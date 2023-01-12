import mnemonic
import bitcoin
import requests
import time

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
            break
                        
    else:
        print("Request failed")
    time.sleep(5)
    address_count += 1
