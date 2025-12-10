import yt_dlp
import json
import argparse
from pathlib import Path
import sys

def download_comments(video_url, output_file=None, limit=None, no_playlist=False):
    """
    Downloads comments from a YouTube video or playlist and saves them to a JSON file.
    """
    ydl_opts = {
        'getcomments': True,
        'skip_download': True,
        'quiet': False,
        'no_warnings': True,
        'extract_flat': False,
        'noplaylist': no_playlist,
    }
    
    if limit:
        ydl_opts['max_comments'] = int(limit)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching comments for: {video_url}")
            info = ydl.extract_info(video_url, download=False)
            
            comments_data = []
            
            if 'entries' in info:
                # It's a playlist
                print(f"Playlist detected: {info.get('title', 'Unknown Playlist')}")
                for entry in info['entries']:
                    if not entry:
                        continue
                    video_id = entry.get('id')
                    title = entry.get('title')
                    entry_comments = entry.get('comments')
                    
                    if entry_comments:
                        print(f"Found {len(entry_comments)} comments for video: {title}")
                        comments_data.append({
                            'video_id': video_id,
                            'title': title,
                            'comments': entry_comments
                        })
                    else:
                        print(f"No comments found for video: {title}")
            
            elif 'comments' in info:
                # It's a single video
                comments = info['comments']
                print(f"Found {len(comments)} comments.")
                comments_data = comments # For single video, keep original structure or wrap it? 
                # To maintain backward compatibility with the previous structure for single videos, 
                # we should probably just save the list of comments directly if it's a single video.
                # But if we want a consistent format, we might want to wrap it. 
                # However, the user asked for "download all comments of a youtube video", so a list of comments is expected.
                # Let's keep it as list of comments for single video, and list of video-objects for playlist.
                pass 
            else:
                print("No comments found or comments are disabled.")
                return

            if not comments_data:
                print("No comments collected.")
                return

            if not output_file:
                if 'entries' in info:
                    playlist_title = info.get('title', 'playlist').replace(' ', '_')
                    output_file = f"{playlist_title}_comments.json"
                else:
                    video_id = info.get('id', 'video')
                    output_file = f"{video_id}_comments.json"

            output_path = Path(output_file)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(comments_data, f, indent=4, ensure_ascii=False)
            
            print(f"Comments saved to: {output_path.absolute()}")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video comments to JSON')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', help='Output JSON filename')
    parser.add_argument('-l', '--limit', type=int, help='Maximum number of comments to download')
    parser.add_argument('--no-playlist', action='store_true', help='Download only the video, if the URL is a playlist')
    
    args = parser.parse_args()
    
    download_comments(args.url, args.output, args.limit, args.no_playlist)

if __name__ == '__main__':
    main()
