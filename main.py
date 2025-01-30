import discord
from discord.ext import commands
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
 
class DiscordBot:
    def __init__(self, token, target_channel_id, telegram_token, telegram_chat_id):
        # Initialisation des intents
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True  # Autorise la lecture du contenu des messages

        # Configuration du bot
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.token = token
        self.target_channel_id = target_channel_id

        # Configuration Telegram
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id

        # Liaison des événements
        self.bot.event(self.on_ready)
        self.bot.event(self.on_message)

    async def on_ready(self):
        logger.info(f"Bot connecté en tant que {self.bot.user}")

    async def on_message(self, message):
        # Vérifie si le message est envoyé dans le channel cible et n'est pas par un bot
        if message.channel.id == self.target_channel_id and not message.author.bot:
            logger.info(f"Message reçu dans le channel cible : {message.content} (de {message.author.name})")
            self.process_message(message)

    def process_message(self, message):
        logger.info(f"Traitement du message : {message.content}")

        # Ajouter une entrée dans le fichier de log
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open("logs.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{timestamp} {message.author.name}: {message.content}\n")

        # Envoi du message sur Telegram
        telegram_message = f"{message.author.name}: {message.content}"
        self.send_telegram_message(telegram_message)

    def send_telegram_message(self, message):
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message
        }

        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info(f"Message envoyé à Telegram : {message}")
        else:
            logger.error(f"Erreur lors de l'envoi : {response.status_code}, {response.text}")

    def run(self):
        self.bot.run(self.token)

# Configuration depuis le fichier .env
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_CHANNEL_ID = int(os.getenv("TARGET_CHANNEL_ID"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
 
# Initialisation et démarrage du bot
if __name__ == "__main__":
    my_bot = DiscordBot(TOKEN, TARGET_CHANNEL_ID, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    my_bot.run()