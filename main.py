from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
import re
import requests
import asyncio

# === API da tua conta pessoal ===
api_id = 28188675
api_hash = 'f502f13e43a95b51d686798cee94b764'
session_name = 'coringa_session'

# === Bot e canais ===
bot_token = '7422554030:AAFqcUFnyWrGz5Zy2yUMMpgw8_0nA61uv6k'
canal_origem = -1002058333477
canal_destino = -1002391988849
contador_mensagens = 0

# === Iniciar cliente do Telethon ===
client = TelegramClient(session_name, api_id, api_hash)

# === Flask para manter o serviço ativo ===
app = Flask('')

@app.route('/')
def home():
    return "✅ Bot online via Render!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === Processar mensagens ===
@client.on(events.NewMessage(chats=canal_origem))
async def reenviar(event):
    global contador_mensagens
    texto = event.raw_text

    if texto:
        try:
            # Substituir trecho específico
            if "⚠️ EVITE RED E O DELAY NOS SINAIS ⚠️" in texto:
                texto = texto.replace(
                    "🔴 [[CADASTRE-SE E JOGUE SOMENTE AQUI PARA NÃO PERDER DINHEIRO]](",
                    "🐘 Jogue na Elephant Bet para melhor experiência!"
                )

            # Remover links e menções
            texto = re.sub(r'https?://t\.me/\S+', '', texto)
            texto = re.sub(r'https?://\S+', '', texto)
            texto = re.sub(r'@\w+', '', texto)

            contador_mensagens += 1
            rodape = ""

            if contador_mensagens % 5 == 0:
                rodape += "\n📞 Contacte Bac Bo Estratégico no WhatsApp: https://wa.me/244921130838"

            if "entra na cor" in texto.lower():
                rodape += "\n🎲 Jogue com responsabilidade."

            if rodape:
                texto += "\n\n" + rodape.strip()

            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': canal_destino,
                'text': texto,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                print(f"✅ Mensagem #{contador_mensagens} enviada")
            else:
                print("❌ Erro:", response.text)

        except Exception as e:
            print("❌ Erro ao processar:", e)

# === Executar o bot ===
async def main():
    print("🔄 Bot escutando...")
    keep_alive()
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())