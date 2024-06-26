import discord
from discord.ext import commands
import os


# library pesan random
import random

# library keperluan enkripsi
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import base64

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

rand_respon = [
    "Hai beb!",
    "Manggil aja, udah belajar belom?",
    "Kenapa nichh?",
    "Ada masalah kawan?",
    "Hai aku disini aja kok!",
    "Ya?",
    "Apa kabar?",
    "Ada yang bisa dibantu?",
    "Senang melihatmu!",
    "Butuh bantuan?",
    "Halo! Ada yang bisa aku lakukan?",
    "Bagaimana harimu?",
    "Apa yang sedang kamu kerjakan?",
    "Ada yang menarik?",
    "Hai! Ada kabar apa?",
    "Butuh bantuan belajar?",
    "Ada yang ingin dibahas?",
    "Halo! Apa kabar?",
    "Selamat datang!",
    "Hai! Semoga harimu menyenangkan!"
]

respon_terbaru = set()

def get_unique_response():
    global respon_terbaru

# reset set kalau udah kepakai 
    if len(respon_terbaru) == len(rand_respon):
        respon_terbaru.clear()

# bikin respon baru, tanpa ada yang sebelumnya tadi
    respon = random.choice(rand_respon)
    while respon in respon_terbaru:
        respon = random.choice(rand_respon)

# masukkan respon baru ke variabel set
    respon_terbaru.add(respon)

    return respon

bot = commands.Bot(command_prefix="!", intents=intents)

TARGET_CATEGORY_ID = 1203968516320006206  # ganti id-nya sesuai kategori yang ingin di announcement perubahannya
LOG_CHANNEL_ID = 1255226641739943986      # tempat untuk menyampaikan update yang ada di forum channelnya
DEFAULT_IMAGE_BANNER_URL = 'https://media.discordapp.net/attachments/1220780067311845547/1255248536845680811/Sayangnya_tidak_ada_banner_.png?ex=667c70cc&is=667b1f4c&hm=6d54b1b9f8a5cc7734bbd129d8281cb15abed837fa857b2ebfb7d6f7b8d1433d&=&format=webp&quality=lossless&width=687&height=343'

# tempat nyimpan data sementara embed yang dikirim biar bisa diedit lebih mudah dan terstruktur.
message_log = {}

def encrypt_message(message, key):
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()
    
    encrypted_message = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_message).decode('utf-8')

def decrypt_message(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
    iv = encrypted_message[:16]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_message = decryptor.update(encrypted_message[16:]) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_message = unpadder.update(decrypted_padded_message) + unpadder.finalize()
    
    return decrypted_message.decode('utf-8')

# kunci unutk AES encryption/decryption 32 bytes AES-25
AES_KEY = b'rahasia_nihkak_hehe_maafya_KAKA!'[:32]

@bot.event
async def on_ready():
    print(f'bot nyala nama bot : {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user.mentioned_in(message):
        respon = get_unique_response()
        await message.reply(respon)

@bot.event
async def on_thread_create(thread):
    parent_channel = thread.parent
    if parent_channel and parent_channel.category_id == TARGET_CATEGORY_ID:
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            try:
                pesan_awal = await thread.fetch_message(thread.id)
                author = pesan_awal.author if pesan_awal else None
                deskripsi = pesan_awal.content if pesan_awal else 'Tidak ada konten'
            except discord.errors.NotFound:
                pesan_awal = None
                author = None
                deskripsi = 'Tidak ada konten'

            embed = discord.Embed(
                title="Post Baru di Forum",
                description=f"Hai! **Akademikus** ada post baru nih teman teman.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Material", value=parent_channel.mention, inline=False)
            embed.add_field(name="Judul Post", value=thread.mention, inline=False)
            embed.add_field(name="Deskripsi Post", value=deskripsi, inline=False)
            embed.add_field(name="Author", value=author.mention if author else 'Unknown', inline=False)
            embed.add_field(name="Status", value="Sedang Aktif😊", inline=False)
            if hasattr(thread, 'applied_tags'):
                tags = [tag.name for tag in thread.applied_tags]
                embed.add_field(name="Tags", value=', '.join(tags) if tags else 'Tidak ada kategori', inline=False)
            else:
                embed.add_field(name="Tags", value='Tidak ada kategori', inline=False)

            if pesan_awal and pesan_awal.attachments:
                image_url = pesan_awal.attachments[0].url
            else:
                image_url = DEFAULT_IMAGE_BANNER_URL
            embed.set_image(url=image_url)
            embed.set_footer(text="Yuk langsung cuss cekkk!")

            log_message = await log_channel.send(embed=embed)
            message_log[thread.id] = log_message

@bot.event
async def on_thread_delete(thread):
    parent_channel = thread.parent
    if parent_channel and parent_channel.category_id == TARGET_CATEGORY_ID:
        if thread.id in message_log:
            log_message = message_log[thread.id]
            embed = log_message.embeds[0]
            embed.title = "[DELETED POST]"
            embed.color = discord.Color.red()
            encrypted_description = encrypt_message(embed.fields[2].value, AES_KEY)
            embed.set_field_at(1, name="Judul Post", value=thread.name, inline=False)
            embed.set_field_at(2, name="Deskripsi Post", value=f"||{encrypted_description}||", inline=False)
            embed.set_field_at(4, name="Status", value="Post telah dihapus😥", inline=False)
            await log_message.edit(embed=embed)

bot.run('bot_token_kalian')

