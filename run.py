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

LOCAL_URLS = [
    "galaxyott", "sscloud", "applelive", "ipcloud", "onecloudlive", 
    "bmlive", "phoenixcreations", "singamcloud", "olidigital", 
    "tamilstream", "rojatv", "maxtn", "notvstream", "apserver", 
    "rcserver", "brightmeltech", "mindspell", "7starcloud", 
    "livebox", "yuppcdn", "tangotv", "dailyhunt", "pishow", 
    "streamjo", "massstream", "tatatv", "ranapk", "ashokadigital",
    "103.140.254", "103.87.105", "198.144.149"
]

BLOCKED_LANGS = [
    "telugu", "malayalam", "kannada", "hindi", "marathi", "gujarati", 
    "bengali", "punjabi", "odia", "urdu", "maa ", "gemini", "flowers", 
    "asianet", "udaya", "suvarna", "etv ", "zee telugu", "zee kannada", "star maa"
]

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
    
    if any(p in u for p in LOCAL_URLS):
        return "Tamil Local"

    if any(lang in n for lang in BLOCKED_LANGS):
        return None

    for category, keywords in CAT_KEYWORDS.items():
        for kw in keywords:
            if kw in n:
                return category

    english_kws = ["english", "hbo", "cnn", "bbc", "disney", "discovery", "nat geo", "sony pix", "star movies", "comedy central", "axn", "tlc", "animal planet", "history", "bloomberg", "cnbc", "sky news", "ndtv", "wion"]
    if any(kw in n for kw in english_kws):
        if any(w in n for w in ["news", "cnn", "bbc", "ndtv", "wion", "sky news"]):
            return "English News"
        if any(w in n for w in ["movie", "hbo", "star movies", "sony pix", "comedy central"]):
            return "English Movies"
        if any(w in n for w in ["discovery", "nat geo", "history", "animal planet", "science"]):
            return "English Infotainment"
        if any(w in n for w in ["kids", "cartoon", "disney", "nick", "pogo"]):
            return "English Kids"
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
    main()
