import os

import aiohttp
from pyrogram import filters
from pytube import YouTube
from youtubesearchpython import VideosSearch

from DaisyX import LOGGER, pbot
from DaisyX.utils.ut import get_arg


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@pbot.on_message(filters.command("song"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Masukan Nama Lagu. Check /help")
        return ""
    status = await message.reply("Memproses...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Lagu Tidak Ditemukan.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")


__help__ = """
 *Silakan Masukan Judul Lagu Atau Nama Artis Lagu. *

Holla Welcome to help menu ✨

📌BAGAIMANA CARA MENGGUNAKAN RIO MANAGER MUSIC ?

1. pertama tambahkan saya ke grup mu.
2. promote me as admin and give all permission.
3. kemudian, tambahkan @Riomusicasistant ke grupmu atau bisa ketik /userbotjoin.
3. nyalakan dulu VCG sebelum memutar musik.

📌perintan untuk semua anggota grup:

/play (judul lagu) - memutar musik melalui youtube
/stream (balas ke audio) - memutar musik melalui balas audio
/playlist - kenunjukan daftar putar
/current - menunjukan yang sedang diputar saat ini
/song (judul lagu) - mengunduh musik melalui youtube
/search (nama video) - mencari video dari youtube secara rinci
/vsong (nama video) - mengunduh video dari youtube secara rinci
/vk (judul lagu) - unduh melalui mode inline

📌 perintah untuk admin:

/player - membuka panel oengaturan musik
/pause - jeda pemutaran musik
/resume - melanjutkan pemutaran musik
/skip - melompati lagu yang sedang diputar
/end - menghentikan musik
/userbotjoin - mengundang assisten ke grup anda
/reload - untuk memperbarui daftar admin
/cache - untuk membersihkan cache admin
/musicplayer (on / off) - mematikan/menghidupkan pemutar musik di grupmu

🎧 channel streaming commands:

/cplay - mendengarkan musik lewat channel
/cplayer - melihat daftar putar
/cpause - jeda pemutar musik
/cresume - melajutkan musik yang di jeda
/cskip - melompati lagu yang sedang diputar
/cend - menghentikan lagu
/admincache - memperbarui cache admin

🧙‍♂️ command for sudo users:

/userbotleaveall - mengeluarkan asisten dari semua grup
/gcast - mengirim pesan siaran

📌 commands for fun:

/lyric - (judul lagu) melihat lirik
"""

__mod_name__ = "Music Player"
