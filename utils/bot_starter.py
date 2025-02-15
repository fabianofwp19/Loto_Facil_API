import time
import requests
from telebot.apihelper import ApiTelegramException

def iniciar_bot(bot):
    while True:
        try:
            bot.polling(timeout=40, long_polling_timeout=40)
        except requests.exceptions.ReadTimeout:
            print("Timeout error. Reconnecting in 5 seconds...")
            time.sleep(5)
        except requests.exceptions.ConnectionError:
            print("Connection error. Reconnecting in 5 seconds...")
            time.sleep(5)
        except ApiTelegramException as e:
            if e.result.status_code == 502:
                print("502 Bad Gateway. Reconnecting in 5 seconds...")
                time.sleep(5)
            else:
                print(f"Telegram API error: {e}. Retrying in 5 seconds...")
                time.sleep(5)
        except KeyboardInterrupt:
            print("Bot stopped by user.")
            bot.stop_polling()
            break
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        else:
            try:
                print("Bot reconnected and is online!")
            except Exception as e:
                print(f"Error sending status: {e}")
            break
