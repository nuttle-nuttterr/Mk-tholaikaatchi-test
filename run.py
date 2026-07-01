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
# 2. BLOCKED LANGUAGES (Non-Tamil/English)
# ==========================================
BLOCKED_LANGUAGES = [
    "telugu", "kannada", "malayalam", "hindi", "bangla", "bengali", 
    "odia", "marathi", "gujarati", "punjabi", "assamese", "urdu",
    "spanish", "french", "german", "italian", "portuguese", "russian",
    "chinese", "japanese", "korean", "arabic", "indonesian"
]

# ==========================================
# 3. CATEGORIES (Ordered by priority)
# ==========================================
CATEGORIES = {
    # Check NEWS first (before Entertainment)
    "Tamil News": [
        "sun news", "raj news", "thanthi", "puthiya thalaimurai", 
        "news18 tamil", "polimer news", "news7", "news j", 
        "kalaignar seithigal", "win news", "sathiyam", "madhimugam", 
        "captain news", "lotus news", "dina thanthi", "nakkheeran",
        "zee tamil news", "kalaignar murasu"
    ],
    
    # Check KIDS before Entertainment
    "Tamil Kids": [
        "chutti tv", "chithiram", "cartoon network tamil", "pogo tamil", 
        "discovery kids tamil", "sony yay tamil", "nick tamil", 
        "disney channel tamil", "hungama tamil", "kochu tv"
    ],
    
    # Check MOVIES before Entertainment
    "Tamil Movies": [
        "ktv", "zee thirai", "sun life", "raj digital plus", 
        "jaya movie", "mega movies", "vijay super", "raj movies", 
        "kollywood", "tamil movies", "tamil cinemax"
    ],
    
    # Check MUSIC before Entertainment
    "Tamil Music": [
        "sun music", "raj musix", "isai aruvi", "jaya plus", 
        "g music", "makkal tv music", "ktv music", "jcv musix", 
        "mega music", "isai music"
    ],
    
    # Check DEVOTIONAL before Entertainment
    "Tamil Devotional": [
        "angel tv", "sathya tv", "murugan tv", "jeevan tv", 
        "aruloli", "shubhsandesh", "goodness", "nambikkai", 
        "sanskar tamil", "aastha tamil"
    ],
    
    # Check INFOTAINMENT before Entertainment
    "Tamil Infotainment": [
        "discovery tamil", "national geographic tamil", 
        "history tv18 tamil", "animal planet tamil", "bbc earth tamil", 
        "nat geo tamil", "discovery science tamil", "nat geo wild tamil", 
        "discovery turbo tamil"
    ],
    
    # Check SHOPPING before Entertainment
    "Tamil Shopping": [
        "home shop tamil", "india shop tamil", "dd kisan tamil"
    ],
    
    # SPORTS (separate category)
    "Sports": [
        "star sports", "sony ten", "eurosport", "dd sports", 
        "sports", "cricket", "football", "tennis"
    ],
    
    # ENTERTAINMENT (last - catch-all for Tamil general channels)
    "Tamil Entertainment": [
        "sun tv", "star vijay", "zee tamil", "colors tamil", 
        "kalaignar tv", "raj tv", "polimer tv", "mega tv", 
        "vasanth tv", "puthuyugam", "captain tv", "adithya tv", 
        "vendhar tv", "jaya tv", "d tamil", "maalai malar", "sirippoli"
    ]
}

def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    name = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', name, flags=re.I)
    return ' '.join(name.split()).strip()

def is_blocked_language(name):
    """Check if channel name contains blocked language keywords"""
    n = name.lower()
    for lang in BLOCKED_LANGUAGES:
        if lang in n:
            return True
    return False

def get_category(name):
    """Get category by checking in priority order"""
    n = name.lower()
    
    # First check if it's a blocked language
    if is_blocked_language(name):
        return None
    
    # Check categories in priority order
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
    """Test if stream is actually alive"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': url,
        'Accept': '*/*'
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout, stream=True)
        if response.status_code != 200:
            return False
            
        chunk = response.raw.read(1024, decode_content=True)
        if not chunk:
            return False
            
        text_chunk = chunk.decode('utf-8', errors='ignore')
        
        # If it's HTML, it's an error page
        if text_chunk.startswith('<'):
            return False
            
        # If it's M3U or binary, it's valid
        return True
        
    except Exception:
        return False

def main():
    print("Starting FIXED playlist builder...")
    print("This version blocks non-Tamil/English languages and fixes categories.")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    seen_urls = set()
    seen_names = set()  # Track channel names to avoid duplicates
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
            blocked = 0
            
            for name, logo, url in parsed:
                url = url.strip()
                if url.startswith("http") and url not in seen_urls:
                    seen_urls.add(url)
                    checked_count += 1
                    
                    # Deep stream check
                    if deep_stream_check(url):
                        # Check category
                        cat = get_category(name)
                        if cat:
                            clean = clean_name(name)
                            
                            # Check for duplicate channel names (allow different URLs)
                            name_key = clean.lower()
                            if name_key not in seen_names:
                                seen_names.add(name_key)
                                final_channels[cat].append((clean, logo, url))
                                added += 1
                        else:
                            blocked += 1
                            
                    if checked_count % 20 == 0:
                        print(f"  -> Tested {checked_count} streams so far...")
                        
            print(f"  -> Added {added} channels, Blocked {blocked} (wrong language/category)")
            
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
    print(f"\n✅ SUCCESS! Total Channels: {total}")
    for cat, channels in final_channels.items():
        if channels:
            print(f"  {cat}: {len(channels)}")
    
    # Write README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write(f"Total Channels: {total}\n\n")
        f.write("## Playlist URL\n")
        f.write("https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n")

if __name__ == "__main__":
    main()    "Tamil Shopping": ["home shop", "india shop", "dd kisan"],
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
