import requests
import re
import json
import datetime
import concurrent.futures

# ==========================================
# 1. ALL YOUR SOURCES & TAGS
# ==========================================
# Mapping sources to a short name so we can tag duplicate channels!
SOURCES = {
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u": "TamilVM",
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/jio.m3u": "Jio",
    "https://raw.githubusercontent.com/Tamilwebcast/Tamilwebcast.github.io/main/TWCIPTV.m3u": "TWC",
    "https://raw.githubusercontent.com/PraveenBojja83/praveentv/main/resource/channels.json": "Praveen",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_iptv.m3u": "IndiaIPTV",
    "https://raw.githubusercontent.com/Indiblog/india-iptv/main/output/india_general.m3u": "IndiaGen",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/jtv.m3u": "Amaze-JTV",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/pishow.m3u": "Amaze-Pi",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/yupptvfast.m3u": "Amaze-Yupp",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/tangotv.m3u": "Amaze-Tango",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u": "Amaze-Ashoka",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/neotv.m3u": "Amaze-Neo",
    "https://iptv-org.github.io/iptv/languages/tam.m3u": "IPTV-Org-Tam",
    "https://iptv-org.github.io/iptv/languages/eng.m3u": "IPTV-Org-Eng"
}

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
    "Tamil Local Channels": ["local", "cable", "arun", "network"],
    "Tamil News": ["sun news", "raj news", "thanthi", "puthiya thalaimurai", "news18 tamil", "polimer news", "news7", "news j", "kalaignar seithigal", "win news", "sathiyam", "madhimugam", "captain news", "dina thanthi", "nakkheeran", "lotus news"],
    "Tamil Sports": ["star sports 1 tamil", "star sports 2 tamil", "star sports 3 tamil", "sony ten 1 tamil", "sony ten 2 tamil", "sony ten 3 tamil", "eurosport tamil", "dd sports tamil", "star sports tamil", "sony ten tamil"],
    "Tamil Movies": ["ktv", "zee thirai", "sun life", "raj digital plus", "jaya movie", "mega movies", "vijay super", "raj movies", "kollywood", "tamil movies", "tamil cinemax"],
    "Tamil Music": ["sun music", "raj musix", "isai aruvi", "jaya plus", "g music", "makkal tv", "ktv music", "jcv musix", "tamil music", "mega music", "isai music"],
    "Tamil Kids": ["chutti tv", "chithiram", "cartoon network tamil", "pogo tamil", "discovery kids tamil", "sony yay tamil", "nick tamil", "disney channel tamil", "hungama", "kochu tv", "chutti"],
    "Tamil Devotional": ["angel tv", "sathya tv", "murugan tv", "jeevan tv", "aruloli", "shubhsandesh", "goodness", "nambikkai", "sanskar", "aastha tamil"],
    "Tamil Infotainment": ["discovery channel tamil", "national geographic tamil", "history tv18 tamil", "animal planet tamil", "sony bbc earth tamil", "discovery science tamil", "nat geo wild tamil", "discovery turbo tamil", "discovery tamil"],
    "Tamil Shopping": ["home shop", "india shop", "dd kisan"],
    "Tamil Entertainment": ["sun tv", "star vijay", "zee tamil", "colors tamil", "kalaignar", "raj tv", "polimer tv", "mega tv", "vasanth", "puthuyugam", "captain tv", "adithya", "vendhar", "jaya tv", "d tamil", "maalai malar", "sirippoli", "vijay tv"],

    # ENGLISH CATEGORIES
    "English News": ["bbc news", "cnn", "al jazeera", "sky news", "fox news", "msnbc", "cnbc", "bloomberg", "wion", "republic tv", "india today", "ndtv 24x7", "times now", "cnn news18"],
    "English Movies": ["hbo", "star movies", "sony pix", "mnx", "movies now", "romedy now", "wb", "zee cafe", "colors infinity", "star world"],
    "English Sports": ["star sports", "sony ten", "eurosport", "ten sports", "sky sports", "bt sport", "espn", "bein sports", "super sport", "willow tv", "dd sports"]
}

# ==========================================
# 3. CORE FUNCTIONS
# ==========================================
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
    """
    Validates stream health.
    - 3s Connect Timeout, 5s Read Timeout.
    - Bypasses check completely for 'Tamil Local Channels'.
    - Strictly checks HLS/M3U8 headers to drop fake 200 OK links.
    """
    name, logo, url, cat, source_tag = item
    
    # RULE: Skip validation entirely for Tamil Local Channels
    if cat == "Tamil Local Channels":
        return item

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=(3.0, 5.0), stream=True)
        if response.status_code == 200:
            # Read first 512 bytes
            chunk = response.raw.read(512, decode_content=True).decode('utf-8', errors='ignore')
            chunk_lower = chunk.lower()
            
            # 1. Kill fake HTML error pages masquerading as valid streams
            if '<html' in chunk_lower or '<!doctype' in chunk_lower:
                return None
                
            # 2. Strict M3U8 validation (If it's an m3u8, it MUST have standard HLS tags)
            if '.m3u8' in url.lower():
                if '#extm3u' not in chunk_lower and '#ext-x' not in chunk_lower:
                    return None
                    
            return item
    except Exception:
        pass
    return None

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
def main():
    print("Starting HYPER-FAST Playlist Builder with Tagging...")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    seen_urls = set()  
    total_added = 0

    # Iterate over dictionary items (URL and its Tag)
    for src_url, source_tag in SOURCES.items():
        print(f"\nFetching from [{source_tag}]: {src_url}")
        try:
            resp = requests.get(src_url, timeout=15)
            resp.raise_for_status()
            parsed = parse_json(resp.text) if src_url.endswith('.json') else parse_m3u(resp.text)
            
            # 1. FILTER FIRST 
            to_check = []
            for name, logo, url in parsed:
                url = url.strip()
                if not url.startswith("http") or url in seen_urls: continue
                
                cat = get_category(name)
                if not cat: continue  
                
                to_check.append((name, logo, url, cat, source_tag))
                seen_urls.add(url)

            if not to_check:
                print("  -> No matching channels found in this source.")
                continue
                
            print(f"  -> Found {len(to_check)} potential channels. Testing streams (50 at a time)...")
            
            # 2. CHECK MULTITHREADED
            added_this_src = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(deep_stream_check, to_check)
                for res in results:
                    if res:
                        # Unpack the result
                        r_name, r_logo, r_url, r_cat, r_tag = res
                        
                        # Add the Source Tag to the display name
                        display_name = f"{r_name} [{r_tag}]"
                        
                        final_channels[r_cat].append((display_name, r_logo, r_url))
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
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

    print(f"\n✅ SUCCESS! Total LIVE Channels: {total_added}")
    
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ---------------------------------------------------------
    # README UPDATE - Formatting raw text to avoid Markdown links
    # ---------------------------------------------------------
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, filtered, and updated every 3 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total_added}\n**Last Updated:** {timestamp}\n\n")
        f.write("## 📥 Playlist URL\n")
        f.write("Copy the pure text link below and paste it directly into your IPTV Player:\n\n")
        
        # Uses strict code block so GitHub doesn't create a clickable [link](link) output
        f.write("```text\n")
        f.write("[https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u](https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u)\n")
        f.write("```\n\n")
        
        f.write("## 📊 Channel Breakdown\n| Category | Count |\n|---|---|\n")
        for cat, channels in final_channels.items():
            if channels: f.write(f"| {cat} | {len(channels)} |\n")

if __name__ == "__main__":
    main()
