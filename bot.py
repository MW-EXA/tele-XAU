import requesta
from telegram.ext import Updater, CommandHandler

def get_gold_price_usd():
    api_KEY = 'r96fdt8q12jnv1zrqs4jshgv9zknaf1e1f58ypbl0v4mja8vae68omfxfq19'
    url = f'https://metals-api.com/api/latest?access_key={api_KEY}&base=USD&symbols=XAU'
    response = requests.get(url)
    data = response.json()
    if 'rates' in data and 'XAU' in data['rates']:
        return data['rates']['XAU']
    else:
        return None

def get_usd_to_myr_rate():
    exchange_rate_api_key = 'd236ae9d168da396762388aa'  # Replace with your actual Exchange Rate API key
    url = f'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    if 'rates' in data and 'MYR' in data['rates']:
        return data['rates']['MYR']
    else:
        return None

def get_gold_price_myr_per_gram():
    gold_price_usd_per_ounce = get_gold_price_usd()
    usd_to_myr_rate = get_usd_to_myr_rate()
    if gold_price_usd_per_ounce and usd_to_myr_rate:
        gold_price_usd_per_gram = gold_price_usd_per_ounce / 31.1035
        gold_price_myr_per_gram = gold_price_usd_per_gram * usd_to_myr_rate
        return gold_price_myr_per_gram
    else:
        return None

# Function to handle the /goldprice command
def goldprice(update, context):
    price = get_gold_price_myr_per_gram()
    if price:
        message = f"The current price of gold is RM{price:.2f}/g."
    else:
        message = "Sorry, I couldn't fetch the gold price at the moment."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    # Telegram bot token
    token = '7380623356:AAG_eNOwby6D0_PMW3tmyitrJkU_U1xB4qY'

    # Create Updater object and attach dispatcher to it
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handler to dispatcher
    dispatcher.add_handler(CommandHandler('goldprice', goldprice))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
