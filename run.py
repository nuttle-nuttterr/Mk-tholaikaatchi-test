import requests, re, time
from collections import OrderedDict

OUTPUT_FILE = "master_playlist.m3u"
CATEGORIES = [
    "Tamil Local", "Tamil Entertainment", "Tamil News", "Tamil Movies", 
    "Tamil Music", "Tamil Kids", "Tamil Devotional", "Tamil Infotainment", 
    "Tamil Shopping", "English Entertainment", "English News", 
    "English Movies", "English Kids", "English Infotainment", "Sports"
]
SKIP_URL_CHECK = {"Tamil Local"}

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
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/neotv.m3u"
]

# 1. Local Cable URL Providers
LOCAL_URLS = [
    "galaxyott", "sscloud", "applelive", "ipcloud", "onecloudlive", 
    "bmlive", "phoenixcreations", "singamcloud", "olidigital", 
    "tamilstream", "rojatv", "maxtn", "notvstream", "apserver", 
    "rcserver", "brightmeltech", "mindspell", "7starcloud", 
    "livebox", "yuppcdn", "tangotv", "dailyhunt", "pishow", 
    "streamjo", "massstream", "tatatv", "ranapk", "ashokadigital",
    "103.140.254", "103.87.105", "198.144.149"
]

# 2. Blocked Languages (Strict)
BLOCKED_LANGS = [
    "telugu", "malayalam", "kannada", "hindi", "marathi", "gujarati", 
    "bengali", "punjabi", "odia", "urdu", "maa ", "gemini", "flowers", 
    "asianet", "udaya", "suvarna", "etv ", "zee telugu", "zee kannada", "star maa"
]

# 3. Exact Category Keywords based on your Master List
CAT_KEYWORDS = {
    "Tamil Entertainment": [
        "sun tv", "star vijay", "zee tamil", "colors tamil", "kalaignar tv", 
        "raj tv", "polimer tv", "mega tv", "vasanth tv", "puthuyugam tv", 
        "captain tv", "adithya tv", "vendhar tv", "jaya tv", "d tamil", 
        "maalai malar", "sirippoli"
    ],
    "Tamil News": [
        "sun news", "raj news", "thanthi tv", "puthiya thalaimurai", 
        "news18 tamil nadu", "polimer news", "news7 tamil", "news j", 
        "kalaignar seithigal", "win news", "sathiyam tv", "madhimugam tv", 
        "captain news", "dina thanthi", "nakkheeran", "lotus news"
    ],
    "Tamil Movies": [
        "ktv", "zee thirai", "sun life", "raj digital plus", "jaya movie", 
        "mega movies", "vijay super", "raj movies", "kollywood tv", 
        "tamil movies", "tamil cinemax"
    ],
    "Tamil Music": [
        "sun music", "raj musix", "isai aruvi", "jaya plus", "g music", 
        "makkal tv music", "ktv music", "jcv musix", "tamil music", 
        "mega music", "isai music"
    ],
    "Tamil Kids": [
        "chutti tv", "chithiram tv", "cartoon network tamil", "pogo tamil", 
        "discovery kids tamil", "sony yay tamil", "nick tamil", 
        "disney channel tamil", "hungama tv tamil", "kochu tv tamil"
    ],
    "Tamil Devotional": [
        "angel tv", "sathya tv", "murugan tv", "jeevan tv", "aruloli tv", 
        "shubhsandesh tv", "goodness tv", "nambikkai tv", 
        "sanskar tv tamil", "aastha tamil"
    ],
    "Tamil Infotainment": [
        "discovery channel tamil", "national geographic tamil", 
        "history tv18 tamil", "animal planet tamil", "sony bbc earth tamil", 
        "discovery science tamil", "nat geo wild tamil", "discovery turbo tamil"
    ],
    "Tamil Shopping": [
        "home shop 18 tamil", "india shop tamil", "dd kisan tamil"
    ],
    "Sports": [
        "star sports", "sony ten", "eurosport tamil", "dd sports tamil",
        "sports", "cricket", "football", "tennis"
    ]
}

def clean_name(raw):
    raw = re.sub(r'\s*\[.*?\]\s*', '', raw)
    raw = re.sub(r'\s*\(.*?\)\s*', '', raw)
    raw = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', raw, flags=re.I)
    return ' '.join(raw.split()).strip()

def detect_cat(name, url=""):
    n = name.lower()
    u = url.lower()
    
    # 1. Check URL for Local Cable providers
    if any(p in u for p in LOCAL_URLS):
        return "Tamil Local"

    # 2. Block other languages
    if any(lang in n for lang in BLOCKED_LANGS):
        return None

    # 3. Match against the Master List Categories
    for category, keywords in CAT_KEYWORDS.items():
        for kw in keywords:
            if kw in n:
                return category

    # 4. Fallback for English channels (if not blocked and not matched above)
    english_kws = ["english", "hbo", "cnn", "bbc", "disney", "discovery", "nat geo", "sony pix", "star movies", "comedy central", "axn", "tlc", "animal planet", "history", "bloomberg", "cnbc", "sky news", "ndtv", "wion"]
    if any(kw in n for kw in english_kws):
        if any(w in n for w in ["news", "cnn", "bbc", "ndtv", "wion", "sky news"]): return "English News"
        if any(w in n for w in ["movie", "hbo", "star movies", "sony pix", "comedy central"]): return "English Movies"
        if any(w in n for w in ["discovery", "nat geo", "history", "animal planet", "science"]): return "English Infotainment"
        if any(w in n for w in ["kids", "cartoon", "disney", "nick", "pogo"]): return "English Kids"
        return "English Entertainment"

    return None

def check_url(url, timeout=3):
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        return r.status_code == 200
    except: 
        return False

def parse_m3u(content):
    lines = content.splitlines()
    attrs = {}
    name = None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            attrs = {}
            for match in re.finditer(r'(\S+)="(.*?)"', line):
                attrs[match.group(1)] = match.group(2)
            if ',' in line:
                name = line.rsplit(',', 1)[-1].strip()
            else:
                name = None
        elif line and not line.startswith("#") and name:
            yield attrs, name, line
            name = None

def main():
    channels = {cat: OrderedDict() for cat in CATEGORIES}
    seen_urls = set()

    for src in SOURCES:
        print(f"Fetching {src} ... ", end="")
        try:
            resp = requests.get(src, timeout=15)
            resp.raise_for_status()
            print("OK")
        except Exception as e:
            print(f"FAIL ({e})")
            continue

        for attrs, raw_name, url in parse_m3u(resp.text):
            url = url.strip()
            if not url.startswith("http") or url in seen_urls: 
                continue
            seen_urls.add(url)

            name = clean_name(raw_name)
            if not name: 
                continue

            category = detect_cat(name, url)
            if category is None: 
                continue

            if category not in SKIP_URL_CHECK:
                if not check_url(url):
                    print(f"  ✗ Dead: {name} ({category})")
                    continue

            new_attrs = dict(attrs)
            new_attrs["group-title"] = category
            channels[category][url] = (new_attrs, raw_name)
            print(f"  ✓ {raw_name} → {category}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in CATEGORIES:
            f.write(f"\n# --- {cat} ---\n")
            for url, (attrs, ch_name) in channels[cat].items():
                extinf = '#EXTINF:-1'
                for k, v in attrs.items(): 
                    extinf += f' {k}="{v}"'
                extinf += f',{ch_name}'
                f.write(extinf + '\n')
                f.write(url + '\n')

    total = sum(len(v) for v in channels.values())
    print(f"\n✅ Done. Total: {total}")
    for cat in CATEGORIES: 
        print(f"  {cat}: {len(channels[cat])}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 📺 Tamil & English IPTV\n\n")
        f.write(f"**Updated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
        f.write(f"**Total:** {total}\n\n")
        f.write("| Category | Channels |\n| --- | --- |\n")
        for cat in CATEGORIES: 
            f.write(f"| {cat} | {len(channels[cat])} |\n")
        f.write("\n## 📺 Playlist URL\n```\nhttps://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n```\n")

if __name__ == "__main__":
    main()    if any(lang in n for lang in blocked): return "other"
    
    tamil_kws = ["tamil", "sun ", "vijay", "kalaignar", "jaya ", "raj ", "captain", "polimer", "mega ", "pudhiya", "thanthi", "vasanth", "isaiaruvi", "k tv", "ktv", "adithya", "chutti", "chithiram", "makkal", "sirippoli", "vendhar", "peppers", "angel", "murugan", "madha", "velicham", "seithigal", "zee tamil", "colors tamil", "d tamil", "maalai malar"]
    if any(kw in n for kw in tamil_kws): return "tamil"
    
    english_kws = ["english", "hbo", "cnn", "bbc", "disney", "discovery", "nat geo", "sony pix", "star movies", "mn+", "hits", "romedy", "comedy central", "axn", "colors infinity", "zee cafe", "flix", "prive", "star world", "fox", "fyi", "tlc", "animal planet", "history tv18", "bloomberg", "cnbc", "sky news", "ndtv", "republic", "wion", "times now"]
    if any(kw in n for kw in english_kws): return "english"
    
    return None

def detect_cat(name, url=""):
    n = name.lower()
    u = url.lower()
    local_providers = ["galaxyott", "sscloud", "applelive", "ipcloud", "onecloudlive", "bmlive", "phoenixcreations", "singamcloud", "olidigital", "tamilstream", "rojatv", "maxtn", "notvstream", "apserver", "rcserver", "brightmeltech", "mindspell", "7starcloud", "livebox", "yuppcdn", "tangotv", "dailyhunt", "pishow", "streamjo", "massstream", "tatatv", "ranapk", "ashokadigital", "103.140.254", "103.87.105", "198.144.149"]
    if any(p in u for p in local_providers): return "Tamil Local"

    lang = detect_lang(name)
    if lang == "other" or lang is None: return None

    manual_map = {"sun tv": "Tamil Entertainment", "vijay tv": "Tamil Entertainment", "zee tamil": "Tamil Entertainment", "colors tamil": "Tamil Entertainment", "raj tv": "Tamil Entertainment", "polimer tv": "Tamil Entertainment", "jaya tv": "Tamil Entertainment", "vasanth tv": "Tamil Entertainment", "kalaignar tv": "Tamil Entertainment", "sun music": "Tamil Music", "raj musix": "Tamil Music", "ktv": "Tamil Movies", "sun life": "Tamil Movies", "zee thirai": "Tamil Movies", "sun news": "Tamil News", "raj news": "Tamil News", "thanthi tv": "Tamil News", "chutti tv": "Tamil Kids", "star movies": "English Movies", "hbo": "English Movies", "cnn": "English News", "bbc": "English News"}
    for key, cat in manual_map.items():
        if key in n: 
            if lang == "tamil" and "tamil" in cat.lower(): return cat
            if lang == "english" and "english" in cat.lower(): return cat

    if any(w in n for w in ["kids", "chutti", "chithiram", "cartoon", "disney", "nick", "pogo", "motu patlu", "chhota bheem", "scooby", "mr bean", "vir the robot", "hungama", "sony yay"]):
        return "Tamil Kids" if lang == "tamil" else "English Kids"

    if any(kw in n for kw in ["sports", "star sports", "sony ten", "eurosport", "dsport", "olympics", "cricket", "football", "tennis", "f1", "nba", "wwe"]): return "Sports"

    if lang == "tamil":
        if any(w in n for w in ["news", "seithigal", "pudhiya", "polimer news", "sun news", "thanthi tv", "news18", "win news", "sathiyam", "madhimugam", "captain news", "lotus news", "nakkheeran"]): return "Tamil News"
        if any(w in n for w in ["movie", "cinema", "ktv", "megahit", "thirai", "sun life", "jaya movie", "raj digital", "vijay super", "kollywood"]): return "Tamil Movies"
        if any(w in n for w in ["music", "isai", "isaiaruvi", "sun music", "mega music", "raj musix", "jcv musix"]): return "Tamil Music"
        if any(w in n for w in ["devotional", "bhakti", "angel", "sathya tv", "murugan", "jeevan", "aruloli", "shubhsandesh", "goodness", "nambikkai", "sanskar", "aastha"]): return "Tamil Devotional"
        if any(w in n for w in ["discovery", "nat geo", "national geographic", "history", "animal planet", "bbc earth", "science", "infotainment", "turbo", "wild"]): return "Tamil Infotainment"
        return "Tamil Entertainment"

    if lang == "english":
        if any(w in n for w in ["news", "cnn", "bbc", "ndtv", "times now", "republic", "wion", "sky news", "bloomberg", "fox news", "cnbc", "aljazeera"]): return "English News"
        if any(w in n for w in ["movie", "hbo", "star movies", "sony pix", "mn+", "hits", "romedy", "comedy central", "&flix", "zee cafe", "studio", "paramount", "universal"]): return "English Movies"
        if any(w in n for w in ["discovery", "nat geo", "national geographic", "history", "animal planet", "bbc earth", "science", "infotainment", "turbo", "wild"]): return "English Infotainment"
        return "English Entertainment"
    return None

def check_url(url, timeout=3):
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True)
        return r.status_code == 200
    except: return False

def parse_m3u(content):
    lines = content.splitlines()
    attrs = {}
    name = None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            attrs = {}
            for match in re.finditer(r'(\S+)="(.*?)"', line): attrs[match.group(1)] = match.group(2)
            if ',' in line: name = line.rsplit(',', 1)[-1].strip()
            else: name = None
        elif line and not line.startswith("#") and name:
            yield attrs, name, line
            name = None

def main():
    channels = {cat: OrderedDict() for cat in CATEGORIES}
    seen_urls = set()
    for src in SOURCES:
        print(f"Fetching {src} ... ", end="")
        try:
            resp = requests.get(src, timeout=15)
            resp.raise_for_status()
            print("OK")
        except Exception as e:
            print(f"FAIL ({e})")
            continue
        for attrs, raw_name, url in parse_m3u(resp.text):
            url = url.strip()
            if not url.startswith("http") or url in seen_urls: continue
            seen_urls.add(url)
            name = clean_name(raw_name)
            if not name: continue
            category = detect_cat(name, url)
            if category is None: continue
            if category not in SKIP_URL_CHECK:
                if not check_url(url):
                    print(f"  ✗ Dead: {name} ({category})")
                    continue
            new_attrs = dict(attrs)
            new_attrs["group-title"] = category
            channels[category][url] = (new_attrs, raw_name)
            print(f"  ✓ {raw_name} → {category}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in CATEGORIES:
            f.write(f"\n# --- {cat} ---\n")
            for url, (attrs, ch_name) in channels[cat].items():
                extinf = '#EXTINF:-1'
                for k, v in attrs.items(): extinf += f' {k}="{v}"'
                extinf += f',{ch_name}'
                f.write(extinf + '\n')
                f.write(url + '\n')

    total = sum(len(v) for v in channels.values())
    print(f"\n✅ Done. Total: {total}")
    for cat in CATEGORIES: print(f"  {cat}: {len(channels[cat])}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 📺 Tamil & English IPTV\n\n")
        f.write(f"**Updated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
        f.write(f"**Total:** {total}\n\n")
        f.write("| Category | Channels |\n| --- | --- |\n")
        for cat in CATEGORIES: f.write(f"| {cat} | {len(channels[cat])} |\n")
        f.write("\n##  Playlist URL\n```\nhttps://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n```\n")

if __name__ == "__main__":
    main()
