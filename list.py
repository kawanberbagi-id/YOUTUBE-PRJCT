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

def get_video_likes(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
    response = requests.get(url)
    data = response.json()  

    items = data.get("items", []) # Ambil items, default empty list jika tidak ada
    if items and "statistics" in items[0] and "likeCount" in items[0]["statistics"]:
        return items[0]["statistics"]["likeCount"]
    else:
        print(f"Video {video_id} tidak ditemukan atau tidak memiliki data like.")
        return None  # Atau nilai default yang sesuai

video_likes = {}
page_token = None
while True:
    items, page_token = get_playlist_videos(PLAYLIST_ID, page_token)
    for item in items:
        video_id = item["contentDetails"]["videoId"]
        likes = get_video_likes(video_id)
        if likes is not None:  # Hanya tambahkan video dengan like valid
            video_likes[video_id] = likes

    if not page_token:
        break

# Filter video dengan like valid atau ubah None menjadi 0
valid_video_likes = {k: v for k, v in video_likes.items() if v is not None}
# atau
video_likes = {k: v if v is not None else 0 for k, v in video_likes.items()}

sorted_videos = sorted(valid_video_likes.items(), key=lambda item: item[1], reverse=True)

for video_id, likes in sorted_videos:
    print(f"Video ID: {video_id}, Likes: {likes}")
