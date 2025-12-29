# VLC Mobile to Jellyfin Playlist Exporter
# This was built for and tested on a DB from "VLC for Android" version 3.6.5

This Python script allows you to export playlists from the VLC Android app and convert them into `.m3u` files ready for import into a Jellyfin server. It handles URI decoding and path remapping. I personally wrote this to translate my VLC playlists into Jellyfin.

---

## Features

- Extracts playlists from VLC’s Android SQLite database (`vlc-media.db`)
- Resolves media URIs (`file://`) to actual file paths
- Normalizes path separators for Linux or Windows
- Maps host paths to paths visible inside the Jellyfin Docker container
- Generates M3U playlists that Jellyfin can import directly

---

## Requirements

- Python 3.8+  
- `vlc_media.db` from your Android device (requires access to VLC app data)  
---

## Step 1: Export VLC Database
1. Open **VLC** on your Android device.
2. Go to **Settings → Advanced → Dump media database** (if available).  
   *this will dump the media database to your home directory*
3. Copy the exported database (`vlc_media.db`) to your PC.

## Step 2: Use the script
1. Adjust the top variables as needed
2. Move the media.db file into the script's root directory or edit the search path for it
3. Run the python script
4. Enjoy your playlists!