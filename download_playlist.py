import yt_dlp
import argparse
from pathlib import Path

def get_best_quality_format():
    return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

def setup_ydl_options(output_dir, browser=None, cookies_file=None):
    opts = {
        'format': get_best_quality_format(),
        'outtmpl': str(Path(output_dir) / '%(playlist_index)s-%(title)s.%(ext)s'),
        'ignoreerrors': True,
        'nocheckcertificate': True,
        'no_warnings': False,
        'quiet': False,
        'extract_flat': False,
        'writethumbnail': False,
        'postprocessors': [{
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        }],
    }
    
    if browser:
        opts['cookiesfrombrowser'] = (browser, None, None, None)
    
    if cookies_file:
        opts['cookiefile'] = cookies_file
        
    return opts

def download_playlist(playlist_url, output_dir='downloads', browser=None, cookies_file=None):
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = setup_ydl_options(output_dir, browser, cookies_file)
    
    # Download the playlist
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\nDownloading playlist: {playlist_url}")
            print(f"Videos will be saved to: {output_dir}\n")
            ydl.download([playlist_url])
            print("\nDownload completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Download YouTube playlist in high quality')
    parser.add_argument('playlist_url', help='URL of the YouTube playlist')
    parser.add_argument('--output-dir', '-o', default='downloads',
                      help='Directory to save the downloaded videos (default: downloads)')
    parser.add_argument('--browser', '-b',
                      help='Browser to load cookies from (e.g. chrome, firefox, safari). Helps avoid 403 errors.')
    parser.add_argument('--cookies-file', '-c',
                      help='Path to a Netscape formatted cookies.txt file (reliable fallback if browser extraction fails).')
    
    args = parser.parse_args()
    download_playlist(args.playlist_url, args.output_dir, args.browser, args.cookies_file)

if __name__ == '__main__':
    main()
