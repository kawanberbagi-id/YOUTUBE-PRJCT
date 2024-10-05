import requests

API_KEY = "AIzaSyCDliV-yGfJplMifa6N5j7QoSI_Ce36H40"  # Ganti dengan API key Anda
PLAYLIST_ID = "PLnIDw5a3YugTbOpcpWpSDPsOQNiH1KMyv"  # Ganti dengan ID playlist Anda

def get_playlist_videos(playlist_id, page_token=None):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&maxResults=50&key={API_KEY}"
    if page_token:
        url += f"&pageToken={page_token}"
    response = requests.get(url)
    data = response.json()
    return data.get("items", []), data.get("nextPageToken", None)

def get_video_details(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    items = data.get("items", [])

    if not items:
        print(f"Video {video_id} tidak ditemukan atau tidak memiliki data.")
        return None, None

    if "snippet" not in items[0]:
        print(f"Video {video_id} tidak memiliki informasi snippet.")
        return None, None

    if "title" not in items[0]["snippet"]:
        print(f"Video {video_id} tidak memiliki judul.")
        return None, None

    if "statistics" not in items[0]:
        print(f"Video {video_id} tidak memiliki data statistik.")
        return None, None

    if "likeCount" not in items[0]["statistics"]:
        print(f"Video {video_id} tidak memiliki data like.")
        return None, None
        
    return items[0]["snippet"]["title"], int(items[0]["statistics"]["likeCount"])

video_details = {}
page_token = None
while True:
    items, page_token = get_playlist_videos(PLAYLIST_ID, page_token)
    for item in items:
        video_id = item["contentDetails"]["videoId"]
        title, likes = get_video_details(video_id)
        if title and likes is not None:  # Hanya tambahkan video dengan data valid
            video_details[title] = likes
    if not page_token:
        break

sorted_videos = sorted(video_details.items(), key=lambda item: item[1], reverse=True)

for title, likes in sorted_videos:
    print(f"Judul: {title}, Likes: {likes}")
