import grequests
import tqdm
import os, time
from kwik_token import get_dl_link
import pahe  # Import animepahe module
from colorama import Fore
from utils import progress_message, humanbytes
from pyrogram import Client,filters,enums

app = Client("Bot", api_id=24541704,api_hash="7b1b63a5c5a2e53233a0e78727c068d3",bot_token="6344846447:AAGw1C34OXF8YLp80newmf9chnUnQuxnTtE")

thumb = "Thumb.jpg"

script_directory = os.path.dirname(os.path.realpath(__file__))

# Set the CWD to the script directory
os.chdir(script_directory)

# Function to replace special characters in a string
def replace_special_characters(input_string, replacement="_"):
    special_characters = "!@#$%^&*()_+{}[]|\\:;<>,.?/~`"
    for char in special_characters:
        input_string = input_string.replace(char, replacement)
    return input_string

# Input: Search for anime
query = input("Enter the anime to Download: ")
list_of_anime = pahe.search_apahe(query)

# Display search results
print("Search Results:")
count = 0
for i in list_of_anime:
    count += 1
    print(
        count, ":",
        Fore.MAGENTA + i[0],
        "Type:", i[1],
        Fore.CYAN +"Episodes:",Fore.CYAN + str(i[2]),
        "Airing?", i[3],
        "Year Aired:", i[4],
        Fore.GREEN + "Rating:", Fore.GREEN + str(i[5])
    )

# Input: Choose an anime
choice = int(input("\nEnter the Anime of Choice: ")) - 1
anime_id = list_of_anime[choice][6]

# Input: Choose episode range
episode_range = input("Enter Range of Episode: ").split("-")
episode_range = (
    [int(episode_range[0]), int(episode_range[1]) + 1]
    if len(episode_range) == 2
    else [int(episode_range[0]), int(episode_range[0]) + 1]
)

# Fetch episode IDs
episode_ids = pahe.mid_apahe(session_id=anime_id, episode_range=episode_range)

# Fetch episode download links
episodes_data = pahe.dl_apahe1(anime_id=anime_id, episode_ids=episode_ids)


# Organize episode data
episodes = {}
index = episode_range[0]
for key, value in episodes_data.items():
    sorted_links = {}
    for link_info in value:
        link, size, lang = link_info
        size = int(size.split('p')[0])
        if lang == '':
            lang = 'jpn'
        if lang not in sorted_links:
            sorted_links[lang] = {}
        if size not in sorted_links[lang]:
            sorted_links[lang][size] = []
        sorted_links[lang][size].append(link)
    episodes[index] = sorted_links
    index += 1

# Input: Choose language and quality
lang = input("Languages Available " + str(list(episodes[episode_range[0]].keys())) + ": ")
quality = int(input("Quality Available (*integer) " + str(list(episodes[episode_range[0]][lang])) + ": "))

# Update episodes dictionary to contain selected download link
for key, items in episodes.items():
    backup_quality=list(episodes[key][lang])[-1]
    try:
        episodes[key] = episodes[key][lang][quality][0]
    except:
        try:
            episodes[key] = episodes[key][lang][backup_quality][0]
        except:
            pass
# Fetch video links
for key, value in tqdm.tqdm(episodes.items(), desc="Parsing links"):
    episodes[key] = pahe.dl_apahe2(value)
    print(episodes[key])

# Confirmation and download initiation

# Create a directory for the anime
title = replace_special_characters(list_of_anime[choice][0])
if not os.path.exists("Anime"):
    os.makedirs("Anime")

# Download episodes
for key, value in tqdm.tqdm(episodes.items(), desc="Downloading Episodes"):
    destination = os.path.join("Anime",f"{key} - {title} [{quality}p] @AnimeFiles.mkv") 
    download_link = get_dl_link(value)
    print("download_link")
    pahe.download_file(url=download_link, destination=destination)
    async def main():
      await app.start()
      sts = await app.send_message("activ3","ᴛʀʏɪɴɢ ᴛᴏ Upload.....")
      c_time = time.time()
      await app.send_document("activ3", document=destination,thumb=thumb,progress=progress_message, progress_args=("Uploade Started.....", sts, c_time))
      await sts.delete()
      await app.stop()
    app.run(main())
    os.remove(destination)

