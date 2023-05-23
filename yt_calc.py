from googleapiclient.discovery import build
from iso8601 import parse_duration

# Enter your Google API key here
API_KEY = "YOUR_API_KEY"

# Enter the ID of the YouTube playlist here
PLAYLIST_ID = "YOUR_PLAYLIST_ID"

# Create a YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Get the first page of playlist items
playlist_items = youtube.playlistItems().list(
    part="contentDetails",
    playlistId=PLAYLIST_ID,
    maxResults=50
).execute()

# Initialize variables to store the total duration
total_duration_seconds = 0
total_duration_iso8601 = "PT0S"

# Loop through each page of playlist items
while playlist_items:

    # Loop through each video in the page
    for item in playlist_items["items"]:
        video_duration = item["contentDetails"]["duration"]
        duration_seconds = parse_duration(video_duration).total_seconds()
        total_duration_seconds += duration_seconds

    # Check if there are more pages of playlist items
    if "nextPageToken" in playlist_items:
        next_page_token = playlist_items["nextPageToken"]
        playlist_items = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=PLAYLIST_ID,
            maxResults=50,
            pageToken=next_page_token
        ).execute()
    else:
        break

# Format the total duration as an ISO 8601 duration
total_duration_iso8601 = "PT{}S".format(int(total_duration_seconds))

# Print the total duration
print("Total duration:", total_duration_iso8601)
