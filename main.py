import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerChannel
from telethon import events

# API bilgilerinizi buraya girin
api_id = 'api_id'
api_hash = 'api_hash'
phone_number = 'phone_number'

# Telegram istemcisini oluştur
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Telegram'a oturum aç
    await client.start(phone_number)

    # media_channel kanalından medyayı al
    media_channel = 'mediachannel'
    target_channel = 'targetchannel'
    
    message_count = 0
    spamming = True
    
    async for message in client.iter_messages(target_channel):
        if not spamming:
            break
        
        # Mesajda medya var mı kontrol et
        if message.media:
            # Mesajın medya içeriğini indir
            media = await message.download_media()

            # Medyayı hedef kanala gönder
            await client.send_file(target_channel, media, caption="media description")

        message_count += 1
        if message_count >= 10:
            message_count = 0
            # Mesaj atmayı durdur ve 45 saniye bekleyip devam et
            await client.send_message(target_channel, "🤩 Tool 45 saniyeliğine durduruluyor & Spam Protected # 2024")
            await asyncio.sleep(45)
            await client.send_message(target_channel, "45 saniye bitti, devam ediyor...")

# /stop komutunu dinleme
@client.on(events.NewMessage(pattern='/stop'))
async def stop_spam(event):
    global spamming
    spamming = False
    await event.respond('Spam işlemi durduruldu.')

# Ana işlevi çalıştır
with client:
    client.loop.run_until_complete(main())
