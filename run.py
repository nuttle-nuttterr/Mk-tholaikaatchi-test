import requests
import re
import json
import time
import datetime

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
    "Tamil News": [
        "sun news", "raj news", "thanthi", "puthiya thalaimurai", 
        "news18 tamil", "polimer news", "news7", "news j", 
        "kalaignar seithigal", "win news", "sathiyam", "madhimugam", 
        "captain news", "lotus news", "dina thanthi", "nakkheeran",
        "zee tamil news", "kalaignar murasu"
    ],
    "Tamil Kids": [
        "chutti tv", "chithiram", "cartoon network tamil", "pogo tamil", 
        "discovery kids tamil", "sony yay tamil", "nick tamil", 
        "disney channel tamil", "hungama tamil", "kochu tv", "chutti"
    ],
    "Tamil Movies": [
        "ktv", "zee thirai", "sun life", "raj digital plus", 
        "jaya movie", "mega movies", "vijay super", "raj movies", 
        "kollywood", "tamil movies", "tamil cinemax"
    ],
    "Tamil Music": [
        "sun music", "raj musix", "isai aruvi", "jaya plus", 
        "g music", "makkal tv music", "ktv music", "jcv musix", 
        "mega music", "isai music"
    ],
    "Tamil Devotional": [
        "angel tv", "sathya tv", "murugan tv", "jeevan tv", 
        "aruloli", "shubhsandesh", "goodness", "nambikkai", 
        "sanskar tamil", "aastha tamil"
    ],
    "Tamil Infotainment": [
        "discovery tamil", "national geographic tamil", 
        "history tv18 tamil", "animal planet tamil", "bbc earth tamil", 
        "nat geo tamil", "discovery science tamil", "nat geo wild tamil", 
        "discovery turbo tamil"
    ],
    "Tamil Shopping": [
        "home shop tamil", "india shop tamil", "dd kisan tamil",
        "home shop", "india shop", "dd kisan"
    ],
    "Sports": [
        "star sports", "sony ten", "eurosport", "dd sports", 
        "sports", "cricket", "football", "tennis"
    ],
    "Tamil Entertainment": [
        "sun tv", "star vijay", "zee tamil", "colors tamil", 
        "kalaignar tv", "raj tv", "polimer tv", "mega tv", 
        "vasanth tv", "puthuyugam", "captain tv", "adithya tv", 
        "vendhar tv", "jaya tv", "d tamil", "maalai malar", "sirippoli", "vijay tv"
    ]
}

# ==========================================
# 4. CORE FUNCTIONS
# ==========================================
def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    name = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', name, flags=re.I)
    return ' '.join(name.split()).strip()

def is_blocked_language(name):
    n = name.lower()
    for lang in BLOCKED_LANGUAGES:
        if lang in n:
            return True
    return False

def get_category(name):
    n = name.lower()
    if is_blocked_language(name):
        return None
        
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
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
        
        # HTML error pages masking as HTTP 200
        if text_chunk.startswith('<'):
            return False
            
        return True
    except Exception:
        return False

# ==========================================
# 5. MAIN EXECUTION
# ==========================================
def main():
    print("Starting DEEP VALIDATION playlist builder...")
    print("Note: This will take a few minutes to thoroughly test every stream.")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    seen_urls = set()
    seen_names = set()
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
                    
                    if deep_stream_check(url):
                        cat = get_category(name)
                        if cat:
                            clean = clean_name(name)
                            name_key = clean.lower()
                            
                            if name_key not in seen_names:
                                seen_names.add(name_key)
                                final_channels[cat].append((clean, logo, url))
                                added += 1
                        else:
                            blocked += 1
                            
                    if checked_count % 50 == 0:
                        print(f"  -> Tested {checked_count} unique streams globally so far...")
                        
            print(f"  -> Added {added} live channels, Blocked {blocked} (wrong language/category).")
            
        except Exception as e:
            print(f"  -> ERROR: Skipped source. Continuing...")

    # ==========================================
    # 6. FILE GENERATION
    # ==========================================
    print("\nWriting master_playlist.m3u...")
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat, channels in final_channels.items():
            if channels:
                f.write(f"\n# --- {cat} ---\n")
                for name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{cat}",{name}\n')
                    f.write(f'{url}\n')

    total = sum(len(v) for v in final_channels.values())
    print(f"\n✅ SUCCESS! Total LIVE Channels: {total}")
    for cat, channels in final_channels.items():
        if channels:
            print(f"  {cat}: {len(channels)}")
    
    print("\nWriting README.md...")
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, filtered, and updated every 3 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total}\n")
        f.write(f"**Last Updated:** {timestamp}\n\n")
        f.write("## 📥 Playlist URL\n")
        f.write("Copy and paste this link into your IPTV Player (VLC, TiViMate, etc.):\n")
        f.write("```\n[https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u](https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u)\n```\n\n")
        f.write("## 📊 Channel Breakdown\n")
        f.write("| Category | Count |\n|---|---|\n")
        for cat, channels in final_channels.items():
            if channels:
                f.write(f"| {cat} | {len(channels)} |\n")

if __name__ == "__main__":
    main()
