import requests

API_KEY = "AIzaSyCDliV-yGfJplMifa6N5j7QoSI_Ce36H40"  # Ganti dengan API key Anda
VIDEO_ID = "v88U0orqzTI"  # Ganti dengan ID video YouTube

url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={VIDEO_ID}&key={API_KEY}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    like_count = data["items"][0]["statistics"]["likeCount"]
    print(f"Jumlah like video: {like_count}")
else:
    print("Gagal mendapatkan data")
