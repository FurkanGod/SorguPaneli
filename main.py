from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession
import requests
import json


sudo_users = []


api_id = input("API ID GİR: ")
api_hash = input("API HASH GİR: ")
session_string = input("STRING SESSION GİR: ")


while True:
    try:
        num_sudo_users = int(input("Botu Kaç Hesap Yönetecek: "))
        
        for i in range(num_sudo_users):
            sudo_user_id = int(input(f"Yönetici Olarak Eklemek İstediğiniz Kişinin ID'sini Girin: "))
            sudo_users.append(sudo_user_id)

        break  

    except ValueError:
        print("Geçersiz İşlem.")


client = TelegramClient(StringSession(session_string), api_id, api_hash)

oc = "https://teknobash.com/apiservice/tc.php?auth=tekno"
anan = "https://teknobash.com/apiservice/gsmtc.php?auth=tekno"
baban = "https://teknobash.com/apiservice/tcgsm.php?auth=tekno"
bacin = "https://teknobash.com/apiservice/aile.php?tc="
mal = "http://20.25.189.201/apiservice/adsoyad.php?auth_token=tekno"

@client.on(events.NewMessage(pattern=r'\.sorgu (.+)'))
async def handle_sorgu(event):
    try:
        message = event.message

        if message.sender_id not in sudo_users:  
            await client.send_message(message.chat_id, "Siktir Git Piç Bu Komut Sahibime Özel!")
            return

        query = message.text.split(' ', 1)[1]

        isim = None
        soyisim = None
        il = None
        ilce = None

        query_params = query.split()
        i = 0
        while i < len(query_params):
            param = query_params[i]
            if param == '-isim':
                isim = query_params[i + 1]
                i += 2
            elif param == '-soyisim':
                soyisim = query_params[i + 1]
                i += 2
            elif param == '-il':
                il = query_params[i + 1]
                i += 2
            elif param == '-ilce':
                ilce = query_params[i + 1]
                i += 2
            else:
                await client.send_message(message.chat_id, f"Bilinmeyen parametre: {param}")
                return

        if isim is None or soyisim is None:
            await client.send_message(message.chat_id, "Sorgu Başarısız!\n\nÖrnek Sorgu: .sorgu -isim * -soyisim * -il *")
            return

        api_url = f"http://20.25.189.201/apiservice/adsoyad.php?auth_token=tekno&ADI={isim}&SOYADI={soyisim}"
        if il:
            api_url += f"&NUFUSIL={il}"
        if ilce:
            api_url += f"&NUFUSILCE={ilce}"

        response = requests.get(api_url)
        data = json.loads(response.text)

        if data:
            for member in data:
                output_message = "╔═══════════════\n╟ İllegal Checker </>\n╚═══════════════\n\n"
                output_message += (
                    f"\n╔═══════════════\n╟ TC: {member['TC']}\n╟ ADI: {member['ADI']}\n"
                    f"╟ SOY ADI: {member['SOYADI']}\n╟ DOĞUM TARİHİ: {member['DOGUMTARIHI']}\n"
                    f"╟ İL: {member['NUFUSIL']}\n╟ İLÇE: {member['NUFUSILCE']}\n"
                    f"╟ ANNE ADI: {member['ANNEADI']}\n╟ ANNE TC: {member['ANNETC']}\n"
                    f"╟ BABA ADI: {member['BABAADI']}\n╟ BABA TC: {member['BABATC']}\n"
                    "╚═══════════════\n"
                )
                await client.send_message(message.chat_id, output_message)
        else:
            await client.send_message(message.chat_id, "Verilen İnfo Veritabanımda Bulunmadı.")
    except Exception as e:
        error_message = f"bir hata oluştu: {str(e)}"
        await client.send_message(message.chat_id, error_message)

@client.on(events.NewMessage(pattern=r'\.tc \d{11}'))
async def handle_tc(event):
    try:
        message = event.message
        user_id = message.sender_id

        
        if user_id not in sudo_users:
            raise Exception("Siktir Git Piç Bu Komut Sahibime Özel!")

        text = message.text

        
        tc_no = text.split()[1]

        
        response = requests.get(f"{oc}&tc={tc_no}")
        data = json.loads(response.content.decode('utf-8'))

        if len(data) > 0:
            result = data[0]

            
            output_message = (
                f"╔═══════════════\n╟ İllegal Checker </>\n╚═══════════════\n\n"
                f"╔═══════════════\n╟ TC: {result.get('TC', '')}\n"
                f"╟ ADI: {result.get('ADI', '')}\n"
                f"╟ SOY ADI: {result.get('SOYADI', '')}\n"
                f"╟ DOĞUM TARİHİ: {result.get('DOGUMTARIHI', '')}\n"
                f"╟ İL: {result.get('NUFUSIL', '')}\n"
                f"╟ İLÇE: {result.get('NUFUSILCE', '')}\n"
                f"╟ ANNE ADI: {result.get('ANNEADI', '')}\n"
                f"╟ ANNE TC: {result.get('ANNETC', '')}\n"
                f"╟ BABA ADI: {result.get('BABAADI', '')}\n"
                f"╟ BABA TC: {result.get('BABATC', '')}\n"
                f"╚═══════════════"
            )

            await message.reply(output_message)
        else:
            await message.reply("TC Kimlik Numarası bulunamadı.")
    except Exception as e:
        await message.reply(str(e))  


@client.on(events.NewMessage(pattern=r'\.gsmtc \d+'))
async def handle_gsmtc(event):
    try:
        message = event.message
        user_id = message.sender_id

        
        if user_id not in sudo_users:
            raise Exception("Siktir Git Piç Bu Komut Sahibime Özel!")

        text = message.text

        
        gsm_no = text.split()[1]

        
        response = requests.get(f"{anan}&gsm={gsm_no}")
        data = json.loads(response.content.decode('utf-8'))

        if len(data) > 0:
            result = data[0]

            
            output_message = (
                f"╔═══════════════\n╟ İllegal Checker </>\n╚═══════════════\n\n"
                f"╔═══════════════\n╟ GSM: {result.get('GSM', '')}\n"
                f"╟ TC: {result.get('TC', '')}\n"
                f"╚═══════════════"
            )

            await message.reply(output_message)
        else:
            await message.reply("Verilen GSM Veritabanımda Bulunmadı.")
    except Exception as e:
        await message.reply(str(e))  

@client.on(events.NewMessage(pattern=r'\.tcgsm \d{11}'))
async def handle_tcgsm(event):
    try:
        message = event.message
        user_id = message.sender_id

        
        if user_id not in sudo_users:
            raise Exception("Siktir Git Piç Bu Komut Sahibime Özel!")

        text = message.text

        
        tc_no = text.split()[1]

        
        response = requests.get(f"{baban}&tc={tc_no}")
        data = json.loads(response.content.decode('utf-8'))

        if len(data) > 0:
            result = data[0]

            
            output_message = (
                f"╔═══════════════\n╟ İllegal Checker </>\n╚═══════════════\n\n"
                f"╔═══════════════\n╟ TC: {result.get('TC', '')}\n"
                f"╟ GSM: {result.get('GSM', '')}\n"
                f"╚═══════════════"
            )

            await message.reply(output_message)
        else:
            await message.reply("TC Kimlik Numarası bulunamadı.")
    except Exception as e:
        await message.reply(str(e))  


@client.on(events.NewMessage(pattern=r'\.aile \d{11}'))
async def handle_aile(event):
    try:
        message = event.message
        user_id = message.sender_id

        
        if user_id not in sudo_users:
            raise Exception("Siktir Git Piç Bu Komut Sahibime Özel!")

        text = message.text

        
        tc_no = text.split()[1]

        
        response = requests.get(f"{bacin}{tc_no}")

        
        data = json.loads(response.content.decode('utf-8'))

        if len(data) > 0:
            family_members = data

            
            output_message = "╔═══════════════\n╟ İllegal Checker </>\n╚═══════════════\n\n"
            for member in family_members:
                output_message += (
                    f"╔═══════════════\n╟ YAKINLIK: {member['YAKINLIK']}\n"
                    f"╟ TC: {member['TC']}\n"
                    f"╟ ADI: {member['ADI']}\n"
                    f"╟ SOYADI: {member['SOYADI']}\n"
                    f"╟ DOĞUM TARİHİ: {member['DOGUMTARIHI']}\n"
                    f"╟ ANNE ADI: {member['ANNEADI']}\n"
                    f"╟ ANNE TC: {member['ANNETC']}\n"
                    f"╟ BABA ADI: {member['BABAADI']}\n"
                    f"╟ BABA TC: {member['BABATC']}\n╚═══════════════\n\n"
                )

            await message.reply(output_message)
        else:
            await message.reply("TC Kimlik Numarası bulunamadı.")
    except Exception as e:
        error_message = f"İşleme sırasında bir hata oluştu: {str(e)}"
        await message.reply(error_message)


@client.on(events.NewMessage(pattern=r'\.alive'))
async def handle_alive(event):
    try:
        message = event.message

        if message.sender_id not in sudo_users:  
            await client.send_message(message.chat_id, "siktir git piç bu komut Sahibime özel")
            return

        

        help_message = """
╔═══════════════
╟ İllegal Checker Aktif !
╚═══════════════
╔═══════════════
╟ Kanal: @illegalchecker
╚═══════════════
╔═══════════════
╟ Chat: @Majestesohbet
╚═══════════════
╔═══════════════
╟ Dev: @Furkanisyanedior
╚═══════════════
╔═══════════════
╟ Support: @Saygisizbiri
╚═══════════════
╔═══════════════
╟ Admin Mesajı: Sapla Geç :)
╚═══════════════
        """

        await client.send_message(message.chat_id, help_message)

    except Exception as e:
        error_message = f"İşleme sırasında bir hata oluştu: {str(e)}"
        await client.send_message(message.chat_id, error_message)

@client.on(events.NewMessage(pattern=r'\.komutlar'))
async def handle_help(event):
    try:
        message = event.message

        if message.sender_id not in sudo_users:  
            await client.send_message(message.chat_id, "siktir git piç bu komut sahibime özel")
            return

        

        help_message = """
Sorgu Userbot Komutları::
- .sorgu <isim> <soyisim> <il> <ilce>: Ad Soyad Sorgu Atar

- .tcgsm <tc>: TC Den Gsm Sorgu Atar

- .gsmtc <gsm>: Gsm Den TC Sorgu Atar

- .tc <tc>: TC Sorgu Atar

- .aile <tc>: Aile Sorgu Atar
        """

        await client.send_message(message.chat_id, help_message)

    except Exception as e:
        error_message = f"İşleme sırasında bir hata oluştu: {str(e)}"
        await client.send_message(message.chat_id, error_message)

print("\n" * 20)
print("█▀▄▀█ █ █▄░█ █")
print("█░▀░█ █ █░▀█ █")
print("\nillegal checker hesabına kuruldu! herhangi bir Sohbete .alive yaz.\n")

client.start()
client.run_until_disconnected()
