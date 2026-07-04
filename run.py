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
    "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u",
    "https://iptv-org.github.io/iptv/languages/tam.m3u",
    "https://iptv-org.github.io/iptv/languages/eng.m3u"
]

# The ONLY sources allowed to provide Tamil Local Channels
LOCAL_SOURCES = [
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u",
    "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u"
]

# ==========================================
# 2. STRICT CATEGORY WHITELIST
# ==========================================
# If a channel name does not match these keywords, it is INSTANTLY DROPPED.
# This prevents testing Hindi, Telugu, or junk channels, saving immense time.

CATEGORIES = {
    # ---------------- TAMIL ----------------
    "Tamil GEC": ["sun tv", "star vijay", "vijay tv", "zee tamil", "colors tamil", "kalaignar tv", "kalaignar", "jaya tv", "raj tv", "polimer tv", "makkal tv", "vasanth tv", "vasanth", "puthuyugam tv", "puthuyugam", "mega tv", "captain tv", "vendhar tv", "vendhar"],
    "Tamil Movies": ["ktv", "star vijay super", "vijay super", "zee thirai", "j movie", "jaya movie", "raj digital plus", "murasu", "mega 24", "sun action"],
    "Tamil News": ["sun news", "puthiya thalaimurai", "thanthi tv", "news18 tamil", "polimer news", "news7 tamil", "sathiyam", "news j", "jaya plus", "kalaignar seithigal", "raj news", "captain news"],
    "Tamil Comedy": ["adithya tv", "sirippoli"],
    "Tamil Music": ["sun music", "star vijay music", "vijay music", "isaiaruvi", "isai aruvi", "jaya max", "raj musix", "mega musiq"],
    "Tamil Infotainment": ["sun life", "discovery tamil", "nat geo tamil", "sony bbc earth tamil", "bbc earth tamil"],
    "Tamil Spiritual": ["madha tv", "angel tv", "nambikkai", "vaanavil", "jothi tv", "velicham tv", "sankara tv", "sri sankara"],
    "Tamil Kids": ["chutti tv", "etv bal bharat tamil", "cartoon network tamil", "pogo tamil", "discovery kids tamil", "sony yay tamil", "nick tamil", "disney tamil", "kochu tv"],
    
    # ---------------- ENGLISH ----------------
    "English GEC": ["zee cafe", "colors infinity", "comedy central", "disney international"],
    "English Movies": ["star movies", "sony pix", "movies now", "mnx", "mn+", "&flix", "&prive", "romedy now", "hbo", "wb"],
    "English National News": ["times now", "republic tv", "cnn-news18", "india today", "ndtv 24x7", "newsx", "mirror now", "wion"],
    "English International News": ["bbc news", "cnn international", "al jazeera", "rt news", "russia today", "rt "],
    "English Business News": ["cnbc-tv18", "et now", "ndtv profit"],
    "English Infotainment": ["discovery channel", "national geographic", "history tv18", "animal planet", "sony bbc earth"],
    "English Lifestyle": ["tlc", "travelxp", "goodtimes"],
    "English Kids": ["cartoon network", "nickelodeon", "pogo", "disney channel", "disney junior", "sonic", "super hungama", "discovery kids", "babytv"],
    
    # ---------------- SPORTS ----------------
    "Sports": ["star sports 1", "star sports 2", "star sports select 1", "star sports select 2", "sony sports ten 1", "sony sports ten 2", "sony sports ten 5", "sony ten 1", "sony ten 2", "sony ten 5", "eurosport", "sports18", "sports 18"],
    
    # ---------------- LOCAL ----------------
    "Tamil Local Channels": ["local", "cable", "arun", "network"]
}

# ==========================================
# 3. CORE FUNCTIONS
# ==========================================
def clean_name(name):
    """Removes junk tags for a cleaner display name."""
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    return ' '.join(name.split()).strip()

def normalize_name(name):
    """Creates a pure string to perfectly catch duplicates (e.g. 'Sun TV HD' -> 'suntv')."""
    name = re.sub(r'\b(HD|SD|FHD|4K|UHD)\b', '', name, flags=re.I)
    name = re.sub(r'[^a-zA-Z0-9]', '', name)
    return name.lower()

def get_category(name):
    """STRICT WHITELIST CHECK: Only returns a category if the exact channel keyword is found."""
    if not name: return None
    n = name.lower()
    for cat, keywords in CATEGORIES.items():
        if any(kw in n for kw in keywords): 
            return cat
    return None  # Rejects non-matching channels instantly

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
    Validates stream health:
    - Strict 6.0s timeout.
    - Checks 1024 bytes to drop fake HTML error pages.
    """
    orig_name, logo, url, cat, norm_name = item
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=6.0, stream=True)
        if response.status_code == 200:
            chunk = response.raw.read(1024, decode_content=True)
            if not chunk:
                return None
                
            text_chunk = chunk.decode('utf-8', errors='ignore').lower()
            
            # Reject HTML error pages masking as 200 OK
            if '<html' in text_chunk or '<!doctype' in text_chunk:
                return None
                
            # Strict validation for .m3u8 files
            if '.m3u8' in url.lower():
                if '#extm3u' not in text_chunk and '#ext-x' not in text_chunk:
                    return None
                    
            return item
    except Exception:
        pass
    return None

# ==========================================
# 4. MAIN EXECUTION
# ==========================================
def main():
    print("Starting Strictly Categorized, Sorted, & Fast Playlist Builder...")
    
    final_channels = {cat: [] for cat in CATEGORIES.keys()}
    final_seen_names = set() # Prevents duplicate channels
    seen_urls = set()
    total_added = 0

    for src_url in SOURCES:
        print(f"\nFetching from: {src_url}")
        try:
            resp = requests.get(src_url, timeout=15)
            resp.raise_for_status()
            parsed = parse_json(resp.text) if src_url.endswith('.json') else parse_m3u(resp.text)
            
            # 1. WHITELIST FILTERING (Ultra Fast)
            to_check = []
            for name, logo, url in parsed:
                url = url.strip()
                if not url.startswith("http") or url in seen_urls: continue
                seen_urls.add(url)
                
                cat = get_category(name)
                if not cat: continue  # Skips unlisted channels instantly
                
                # STRICT LOCAL SOURCE CHECK
                if cat == "Tamil Local Channels" and src_url not in LOCAL_SOURCES:
                    continue
                
                clean_n = clean_name(name)
                norm_name = normalize_name(name)
                
                # Deduplication check
                if norm_name in final_seen_names: 
                    continue
                
                to_check.append((clean_n, logo, url, cat, norm_name))

            if not to_check:
                print("  -> No new matching channels found here.")
                continue
                
            print(f"  -> Testing {len(to_check)} streams (Max 6s timeout)...")
            
            # 2. CHECK MULTITHREADED (Fast concurrent checks)
            added_this_src = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(deep_stream_check, to_check)
                for res in results:
                    if res:
                        orig_name, logo, url, cat, norm_name = res
                        
                        if norm_name not in final_seen_names:
                            final_seen_names.add(norm_name)
                            final_channels[cat].append((orig_name, logo, url))
                            added_this_src += 1
                            total_added += 1
            
            print(f"  -> {added_this_src} working unique channels added.")
            
        except Exception as e:
            print(f"  -> ERROR: Skipped source.")

    # ==========================================
    # 5. SORTING A-Z & FILE GENERATION
    # ==========================================
    print("\nSorting channels A-Z and writing master_playlist.m3u...")
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for cat in CATEGORIES.keys():
            channels = final_channels[cat]
            if channels:
                # SORTING A-Z perfectly
                channels.sort(key=lambda x: x[0].lower())
                
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

    print(f"\n✅ SUCCESS! Total Working Unique Channels: {total_added}")
    
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # ---------------------------------------------------------
    # README UPDATE - Pure Text URL Fix
    # ---------------------------------------------------------
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil & English IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, filtered, A-Z sorted, deduplicated, and updated every 3 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total_added}\n**Last Updated:** {timestamp}\n\n")
        f.write("## 📥 Playlist URL\n")
        f.write("Copy the pure text link below and paste it directly into your IPTV Player:\n\n")
        
        # Raw block prevents Markdown hyperlink parsing
        f.write("```text\n")
        f.write("[https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u](https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u)\n")
        f.write("```\n\n")
        
        f.write("## 📊 Channel Breakdown\n| Category | Count |\n|---|---|\n")
        for cat in CATEGORIES.keys():
            channels = final_channels[cat]
            if channels:
                f.write(f"| {cat} | {len(channels)} |\n")

if __name__ == "__main__":
    main()
