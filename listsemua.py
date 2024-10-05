import requests

API_KEY = "AIzaSyCDliV-yGfJplMifa6N5j7QoSI_Ce36H40"
PLAYLIST_ID = "PLnIDw5a3YugTbOpcpWpSDPsOQNiH1KMyv"

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
    items = data.get("items", []) # Ambil items, default empty list jika tidak ada

    if not items:
        print(f"Video {video_id} tidak ditemukan atau tidak memiliki data.")
        return None, None

    if "snippet" not in items[0]:
        print(f"Video {video_id} tidak memiliki informasi snippet.")
        return None, None
    
    if "title" not in items[0]["snippet"]:
        print(f"Video {video_id} tidak memiliki judul.")
        return None, None

    return items[0]["snippet"]["title"], int(items[0]["statistics"]["likeCount"])

    if not page_token:
        break

# Filter video dengan like valid atau ubah None menjadi 0
valid_video_details = {k: v for k, v in video_details.items() if v is not None}
# atau
video_details = {k: v if v is not None else 0 for k, v in video_details.items()}

sorted_videos = sorted(valid_video_details.items(), key=lambda item: item[1], reverse=True)

for title, likes in sorted_videos:
    print(f"Judul: {title}, Likes: {likes}")
