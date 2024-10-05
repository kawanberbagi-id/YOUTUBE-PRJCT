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
    return data["items"][0]["statistics"]["likeCount"]

video_likes = {}
page_token = None
while True:
    items, page_token = get_playlist_videos(PLAYLIST_ID, page_token)
    for item in items:
        video_id = item["contentDetails"]["videoId"]
        video_likes[video_id] = get_video_likes(video_id)
    if not page_token:
        break

sorted_videos = sorted(video_likes.items(), key=lambda item: item[1], reverse=True)
for video_id, likes in sorted_videos:
    print(f"Video ID: {video_id}, Likes: {likes}")
