import sqlite3
import os
import urllib.parse

# Change these as needed
HEADER = "#EXTM3U"
DB_PATH = "vlc_media.db"
OUTPUT_DIR = "vlc_playlists_m3u"
VERBOSE = True

os.makedirs(OUTPUT_DIR, exist_ok=True)

# In my case, this was the absolute path on my phone to my music folder
PREFIX_TO_REMOVE = "file:///storage/emulated/0/Music/library"
# Then I wanted to map it to this folder on my media server for jellyfin
PREFIX_TO_REPLACE = "/media/Music"

# Remove junk
def filename_cleanup(name):
    return "".join(c for c in name if c.isalnum() or c in " _-").rstrip()

# Remap original prefix to new prefix
def map_path(phone_path):
    decoded = urllib.parse.unquote(phone_path)
    if decoded.startswith(PREFIX_TO_REMOVE):
        mapped = decoded.replace(PREFIX_TO_REMOVE, PREFIX_TO_REPLACE, 1)
        # Use forward slashes for Linux paths
        return mapped.replace("\\", "/")
    return decoded.replace("\\", "/")

def export_playlists(db_path, output_dir):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id_playlist, name FROM Playlist")
    playlists = cursor.fetchall()

    for playlist_id, playlist_name in playlists:
        safe_name = filename_cleanup(playlist_name)
        m3u_path = os.path.join(output_dir, f"{safe_name}.m3u")

        # Get media_ids in order
        cursor.execute("""
            SELECT media_id
            FROM PlaylistMediaRelation
            WHERE playlist_id = ?
            ORDER BY position ASC
        """, (playlist_id,))
        media_ids = [row[0] for row in cursor.fetchall()]

        # Get MRLs
        media_paths = []
        for media_id in media_ids:
            cursor.execute("""
                SELECT mrl
                FROM File
                WHERE media_id = ?
                ORDER BY id_file ASC
            """, (media_id,))
            rows = cursor.fetchall()
            for r in rows:
                server_path = map_path(r[0])
                media_paths.append(server_path)
                if VERBOSE:
                    print(f"Remapped: {r[0]} → {server_path}")

        # Write M3U
        if media_paths:
            with open(m3u_path, "w", encoding="utf-8") as f:
                f.write(f"{HEADER}\n")
                for path in media_paths:
                    f.write(f"{path}\n")
            print(f"Exported playlist: \n{playlist_name} → {m3u_path}")
        else:
            print(f"Empty playlist ('{playlist_name}'), skipping.")

    conn.close()
    print("All done, enjoy!")

if __name__ == "__main__":
    export_playlists(DB_PATH, OUTPUT_DIR)
