import requests
import re
import json
import time

# ==========================================
# 1. ALL YOUR SOURCES
# ==========================================
SOURCES = [
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u",
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/jio.m3u",
    "https://raw.githubusercontent.com/Tamilwebcast/Tamilwebcast.github.io/main/TWCIPTV.m3u",
    "https://raw.githubusercontent.com/PraveenBojja83/praveentv/main/resource/channels.json",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_iptv.m3u",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_general.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/jtv.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/pishow.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/yupptvfast.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/tangotv.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/neotv.m3u",
    "https://iptv-org.github.io/iptv/languages/tam.m3u",
    "https://iptv-org.github.io/iptv/languages/eng.m3u"
]

# ==========================================
# 2. YOUR EXACT CATEGORIES
# ==========================================
CATEGORIES = {
    "Tamil Entertainment": ["sun tv", "star vijay", "zee tamil", "colors tamil", "kalaignar", "raj tv", "polimer", "mega tv", "vasanth", "puthuyugam", "captain", "adithya", "vendhar", "jaya tv", "d tamil", "maalai malar", "sirippoli"],
    "Tamil News": ["sun news", "raj news", "thanthi", "puthiya thalaimurai", "news18 tamil", "polimer news", "news7", "news j", "kalaignar seithigal", "win news", "sathiyam", "madhimugam", "captain news", "lotus news"],
    "Tamil Movies": ["ktv", "zee thirai", "sun life", "raj digital", "jaya movie", "mega movies", "vijay super", "raj movies", "kollywood", "tamil movies", "tamil cinemax"],
    "Tamil Music": ["sun music", "raj musix", "isai aruvi", "jaya plus", "g music", "makkal tv", "jcv musix", "mega music", "isai music"],
    "Tamil Kids": ["chutti tv", "chithiram", "cartoon network", "pogo", "discovery kids", "sony yay", "nick", "disney channel", "hungama", "kochu"],
    "Tamil Devotional": ["angel tv", "sathya tv", "murugan tv", "jeevan tv", "aruloli", "shubhsandesh", "goodness", "nambikkai", "sanskar", "aastha"],
    "Tamil Infotainment": ["discovery", "national geographic", "history tv", "animal planet", "bbc earth", "nat geo"],
    "Tamil Shopping": ["home shop", "india shop", "dd kisan"],
    "Sports": ["star sports", "sony ten", "eurosport", "dd sports", "sports", "cricket", "football", "tennis"]
}

def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    name = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', name, flags=re.I)
    return ' '.join(name.split()).strip()

def get_category(name):
    n = name.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in n:
                return cat
    return None

def parse_m3u(content):
    channels = []
    lines = content.splitlines()
    current_name = None
    current_logo = ""
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            logos = re.findall(r'tvg-logo="(.*?)"', line)
            current_logo = logos[0] if logos else ""
            if ',' in line:
                current_name = line.rsplit(',', 1)[1].strip()
            else:
                current_name = None
        elif line and not line.startswith("#") and current_name:
            channels.append((current_name, current_logo, line))
            current_name = None
    return channels

def parse_json(content):
    channels = []
    try:
        data = json.loads(content)
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get('channels', data.get('streams', data.get('data', [])))
        else:
            return channels
            
        for item in items:
            name = item.get('name') or item.get('title') or item.get('channel_name')
            url = item.get('url') or item.get('stream') or item.get('link') or item.get('channel_url')
            logo = item.get('logo') or item.get('icon') or item.get('stream_icon') or ""
            if name and url:
                channels.append((name, logo, url))
    except Exception:
        pass
    return channels

def deep_stream_check(url, timeout=10):
    """
    Actually tests if the stream is alive by downloading the first bytes.
    Prevents 2004 errors by ensuring it's not an HTML error page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Referer': url,
        'Accept': '*/*'
    }
    try:
        # GET request with stream=True to read bytes without downloading the whole file
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        if response.status_code != 200:
            return False
            
        # Read the first 1024 bytes
        chunk = response.raw.read(1024, decode_content=True)
        if not chunk:
            return False
            
        # Decode to check for HTML error pages
        text_chunk = chunk.decode('utf-8', errors='ignore')
        
        # If it starts with <, it's an HTML error page (404, 500, etc.)
        if text_chunk.startswith('<'):
            return False
            
        # If it starts with #EXTM3U, it's a valid HLS playlist
        if text_chunk.startswith('#EXTM3U'):
            return True
            
        # If it's binary data (like a TS stream), it's likely valid
        return True
        
    except Exception:
        return False

def main():
    print("Starting DEEP VALIDATION playlist builder...")
    print("Note: This will take 5-10 minutes to thoroughly test every stream.")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    seen_urls = set()
    checked_count = 0

    for src in SOURCES:
        print(f"\nFetching: {src}")
        try:
            resp = requests.get(src, timeout=15)
            resp.raise_for_status()
            content = resp.text
            
            if src.endswith('.json'):
                parsed = parse_json(content)
            else:
                parsed = parse_m3u(content)
                
            print(f"  Found {len(parsed)} raw channels. Testing streams...")
            added = 0
            
            for name, logo, url in parsed:
                url = url.strip()
                if url.startswith("http") and url not in seen_urls:
                    seen_urls.add(url)
                    checked_count += 1
                    
                    # THE DEEP CHECK
                    if deep_stream_check(url):
                        cat = get_category(name)
                        if cat:
                            clean = clean_name(name)
                            final_channels[cat].append((clean, logo, url))
                            added += 1
                            
                    if checked_count % 20 == 0:
                        print(f"  -> Tested {checked_count} streams so far...")
                        
            print(f"  -> Successfully added {added} LIVE channels from this source.")
            
        except Exception as e:
            print(f"  -> ERROR: Skipped source. Continuing...")

    # Write M3U
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat, channels in final_channels.items():
            if channels:
                f.write(f"\n# --- {cat} ---\n")
                for name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{cat}",{name}\n')
                    f.write(f'{url}\n')

    total = sum(len(v) for v in final_channels.values())
    print(f"\nSUCCESS! Total LIVE Channels: {total}")
    
    # Write README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write(f"Total LIVE Channels: {total}\n\n")
        f.write("## Playlist URL\n")
        f.write("https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n")

if __name__ == "__main__":
    main()
