import youtube_dl

ydl = youtube_dl.YoutubeDL({'outtmpl': '%(title)s.%(ext)s','format':'best'})
print("URL ?")
url = input()

with ydl:
    result = ydl.extract_info(
        url,
        download=True # We just want to extract the info
    )