import requests
import re
import json
import datetime
import concurrent.futures

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
# 2. BLOCKED LANGUAGES & CATEGORIES
# ==========================================
BLOCKED_LANGUAGES = [
    "telugu", "kannada", "malayalam", "hindi", "bangla", "bengali", 
    "odia", "marathi", "gujarati", "punjabi", "assamese", "urdu",
    "spanish", "french", "german", "italian", "portuguese", "russian",
    "chinese", "japanese", "korean", "arabic", "indonesian"
]

CATEGORIES = {
    # TAMIL CATEGORIES (Must check these first!)
    "Tamil News": ["sun news", "raj news", "thanthi", "puthiya thalaimurai", "news18 tamil", "polimer news", "news7", "news j", "kalaignar seithigal", "win news", "sathiyam", "madhimugam", "captain news", "dina thanthi", "nakkheeran", "lotus news"],
    "Tamil Sports": ["star sports 1 tamil", "star sports 2 tamil", "star sports 3 tamil", "sony ten 1 tamil", "sony ten 2 tamil", "sony ten 3 tamil", "eurosport tamil", "dd sports tamil", "star sports tamil", "sony ten tamil"],
    "Tamil Movies": ["ktv", "zee thirai", "sun life", "raj digital plus", "jaya movie", "mega movies", "vijay super", "raj movies", "kollywood", "tamil movies", "tamil cinemax"],
    "Tamil Music": ["sun music", "raj musix", "isai aruvi", "jaya plus", "g music", "makkal tv", "ktv music", "jcv musix", "tamil music", "mega music", "isai music"],
    "Tamil Kids": ["chutti tv", "chithiram", "cartoon network tamil", "pogo tamil", "discovery kids tamil", "sony yay tamil", "nick tamil", "disney channel tamil", "hungama", "kochu tv", "chutti"],
    "Tamil Devotional": ["angel tv", "sathya tv", "murugan tv", "jeevan tv", "aruloli", "shubhsandesh", "goodness", "nambikkai", "sanskar", "aastha tamil"],
    "Tamil Infotainment": ["discovery channel tamil", "national geographic tamil", "history tv18 tamil", "animal planet tamil", "sony bbc earth tamil", "discovery science tamil", "nat geo wild tamil", "discovery turbo tamil", "discovery tamil"],
    "Tamil Shopping": ["home shop", "india shop", "dd kisan"],
    "Tamil Entertainment": ["sun tv", "star vijay", "zee tamil", "colors tamil", "kalaignar", "raj tv", "polimer tv", "mega tv", "vasanth", "puthuyugam", "captain tv", "adithya", "vendhar", "jaya tv", "d tamil", "maalai malar", "sirippoli", "vijay tv"],

    # ENGLISH CATEGORIES (Specific keywords only to prevent grabbing 3000 junk channels)
    "English News": ["bbc news", "cnn", "al jazeera", "sky news", "fox news", "msnbc", "cnbc", "bloomberg", "wion", "republic tv", "india today", "ndtv 24x7", "times now", "cnn news18"],
    "English Movies": ["hbo", "star movies", "sony pix", "mnx", "movies now", "romedy now", "wb", "zee cafe", "colors infinity", "star world"],
    "English Sports": ["star sports", "sony ten", "eurosport", "ten sports", "sky sports", "bt sport", "espn", "bein sports", "super sport", "willow tv", "dd sports"]
}

# ==========================================
# 3. CORE FUNCTIONS
# ==========================================
def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    name = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', name, flags=re.I)
    return ' '.join(name.split()).strip()

def is_blocked_language(name):
    n = name.lower()
    return any(lang in n for lang in BLOCKED_LANGUAGES)

def get_category(name):
    if not name or is_blocked_language(name): return None
    n = name.lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw in n for kw in keywords): return cat
    return None

def parse_m3u(content):
    channels = []
    lines = content.splitlines()
    current_name, current_logo = None, ""
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            logos = re.findall(r'tvg-logo="(.*?)"', line)
            current_logo = logos[0] if logos else ""
            current_name = line.rsplit(',', 1)[1].strip() if ',' in line else None
        elif line and not line.startswith("#") and current_name:
            channels.append((current_name, current_logo, line))
            current_name = None
    return channels

def parse_json(content):
    channels = []
    try:
        data = json.loads(content)
        items = data if isinstance(data, list) else data.get('channels', data.get('streams', data.get('data', [])))
        for item in items:
            name = item.get('name') or item.get('title') or item.get('channel_name')
            url = item.get('url') or item.get('stream') or item.get('link') or item.get('channel_url')
            logo = item.get('logo') or item.get('icon') or item.get('stream_icon') or ""
            if name and url: channels.append((name, logo, url))
    except Exception: pass
    return channels

def deep_stream_check(item):
    """Uses a strict 3-second connection and 5-second read timeout to completely prevent hanging."""
    name, logo, url, cat, clean = item
    headers = {'User-Agent': 'VLC/3.0.9 LibVLC/3.0.9'}
    try:
        # Tuple Timeout: (Connect Timeout, Read Timeout)
        response = requests.get(url, headers=headers, timeout=(3.0, 5.0), stream=True)
        if response.status_code == 200:
            # Read a tiny 256 byte chunk just to verify it isn't an HTML error page
            chunk = response.raw.read(256, decode_content=True).decode('utf-8', errors='ignore')
            if not chunk.strip().startswith('<'):  
                return item
    except Exception:
        pass
    return None

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
def main():
    print("Starting HYPER-FAST Playlist Builder...")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    seen_urls = set()  # Only filtering Duplicate URLs, multiple identical Channel Names are allowed!
    total_added = 0

    for src in SOURCES:
        print(f"\nFetching: {src}")
        try:
            resp = requests.get(src, timeout=15)
            resp.raise_for_status()
            parsed = parse_json(resp.text) if src.endswith('.json') else parse_m3u(resp.text)
            
            # 1. FILTER FIRST (Super Fast)
            to_check = []
            for name, logo, url in parsed:
                url = url.strip()
                if not url.startswith("http") or url in seen_urls: continue
                
                cat = get_category(name)
                if not cat: continue  # Skip invalid/blocked channels immediately
                
                clean = clean_name(name)
                
                to_check.append((name, logo, url, cat, clean))
                seen_urls.add(url)

            if not to_check:
                print("  -> No matching channels found in this source.")
                continue
                
            print(f"  -> Found {len(to_check)} potential channels. Testing streams (50 at a time)...")
            
            # 2. CHECK MULTITHREADED (50 concurrent connections to blast through the checks)
            added_this_src = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(deep_stream_check, to_check)
                for res in results:
                    if res:
                        # Append the original name to allow duplicate channel backups
                        final_channels[res[3]].append((res[0], res[1], res[2]))
                        added_this_src += 1
                        total_added += 1
            
            print(f"  -> {added_this_src} channels are LIVE and added.")
            
        except Exception as e:
            print(f"  -> ERROR: Skipped source.")

    # ==========================================
    # 5. FILE GENERATION
    # ==========================================
    print("\nWriting master_playlist.m3u...")
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat, channels in final_channels.items():
            if channels:
                f.write(f"\n# --- {cat} ---\n")
                for name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{cat}",{name}\n{url}\n')

    print(f"\n✅ SUCCESS! Total LIVE Channels: {total_added}")
    
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, filtered, and updated every 3 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total_added}\n**Last Updated:** {timestamp}\n\n")
        f.write("## 📥 Playlist URL\n```\n[https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u](https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u)\n```\n\n")
        f.write("## 📊 Channel Breakdown\n| Category | Count |\n|---|---|\n")
        for cat, channels in final_channels.items():
            if channels: f.write(f"| {cat} | {len(channels)} |\n")

if __name__ == "__main__":
    main()
