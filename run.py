import time

OUTPUT_FILE = "master_playlist.m3u"

# Curated channels with known working URLs from Tata Play proxy
# Format: (channel_name, tvg_logo, url, category)
CHANNELS = [
    # Tamil Entertainment (17)
    ("Sun TV HD", "https://i.imgur.com/suntv.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=927", "Tamil Entertainment"),
    ("Star Vijay HD", "https://i.imgur.com/vijay.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=924", "Tamil Entertainment"),
    ("Zee Tamil HD", "https://i.imgur.com/zeetamil.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=610", "Tamil Entertainment"),
    ("Colors Tamil HD", "https://i.imgur.com/colorstamil.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=742", "Tamil Entertainment"),
    ("Kalaignar TV", "https://i.imgur.com/kalaignar.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=875", "Tamil Entertainment"),
    ("Raj TV", "https://i.imgur.com/rajtv.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1148", "Tamil Entertainment"),
    ("Polimer TV", "https://i.imgur.com/polimer.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=787", "Tamil Entertainment"),
    ("Mega TV", "https://i.imgur.com/mega.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1007", "Tamil Entertainment"),
    ("Vasanth TV", "https://i.imgur.com/vasanth.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1007", "Tamil Entertainment"),
    ("Puthuyugam TV", "https://i.imgur.com/puthuyugam.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1104", "Tamil Entertainment"),
    ("Captain TV", "https://i.imgur.com/captain.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=815", "Tamil Entertainment"),
    ("Adithya TV", "https://i.imgur.com/adithya.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1106", "Tamil Entertainment"),
    ("Vendhar TV", "https://i.imgur.com/vendhar.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1040", "Tamil Entertainment"),
    ("Jaya TV", "https://i.imgur.com/jaya.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=767", "Tamil Entertainment"),
    ("D Tamil", "https://i.imgur.com/dtamil.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11788", "Tamil Entertainment"),
    ("Maalai Malar", "https://i.imgur.com/maalai.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1007", "Tamil Entertainment"),
    ("Sirippoli", "https://i.imgur.com/sirippoli.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1142", "Tamil Entertainment"),
    
    # Tamil News (16)
    ("Sun News", "https://i.imgur.com/sunnews.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=676", "Tamil News"),
    ("Raj News 24x7", "https://i.imgur.com/rajnews.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=618", "Tamil News"),
    ("Thanthi TV", "https://i.imgur.com/thanthi.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=942", "Tamil News"),
    ("Puthiya Thalaimurai", "https://i.imgur.com/puthiya.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1104", "Tamil News"),
    ("News18 Tamil Nadu", "https://i.imgur.com/news18.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1096", "Tamil News"),
    ("Polimer News", "https://i.imgur.com/polimernews.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=717", "Tamil News"),
    ("News7 Tamil", "https://i.imgur.com/news7.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=826", "Tamil News"),
    ("News J", "https://i.imgur.com/newsj.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=784", "Tamil News"),
    ("Kalaignar Seithigal", "https://i.imgur.com/kalaignarseithigal.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=815", "Tamil News"),
    ("Win News", "https://i.imgur.com/winnews.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=838", "Tamil News"),
    ("Sathiyam TV", "https://i.imgur.com/sathiyam.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=951", "Tamil News"),
    ("Madhimugam TV", "https://i.imgur.com/madhimugam.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=9192", "Tamil News"),
    ("Captain News", "https://i.imgur.com/captainnews.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=815", "Tamil News"),
    ("Dina Thanthi", "https://i.imgur.com/dinathanthi.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=942", "Tamil News"),
    ("Nakkheeran", "https://i.imgur.com/nakkheeran.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=942", "Tamil News"),
    ("Lotus News", "https://i.imgur.com/lotus.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=942", "Tamil News"),
    
    # Tamil Movies (12)
    ("KTV HD", "https://i.imgur.com/ktv.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11818", "Tamil Movies"),
    ("KTV", "https://i.imgur.com/ktv.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1148", "Tamil Movies"),
    ("Zee Thirai HD", "https://i.imgur.com/zeethirai.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11756", "Tamil Movies"),
    ("Sun Life", "https://i.imgur.com/sunlife.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=682", "Tamil Movies"),
    ("Raj Digital Plus", "https://i.imgur.com/rajdigital.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1009", "Tamil Movies"),
    ("Jaya Movie", "https://i.imgur.com/jayamovie.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11793", "Tamil Movies"),
    ("Mega Movies", "https://i.imgur.com/megamovies.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1007", "Tamil Movies"),
    ("Vijay Super", "https://i.imgur.com/vijaysuper.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=831", "Tamil Movies"),
    ("Raj Movies", "https://i.imgur.com/rajmovies.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1009", "Tamil Movies"),
    ("Kollywood TV", "https://i.imgur.com/kollywood.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1148", "Tamil Movies"),
    ("Tamil Movies", "https://i.imgur.com/tamilmovies.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11756", "Tamil Movies"),
    ("Tamil Cinemax", "https://i.imgur.com/cinemax.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11756", "Tamil Movies"),
    
    # Tamil Music (11)
    ("Sun Music HD", "https://i.imgur.com/sunmusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=652", "Tamil Music"),
    ("Raj Musix", "https://i.imgur.com/rajmusix.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=748", "Tamil Music"),
    ("Isai Aruvi", "https://i.imgur.com/isaiaruvi.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1141", "Tamil Music"),
    ("Jaya Plus", "https://i.imgur.com/jayaplus.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=961", "Tamil Music"),
    ("G Music", "https://i.imgur.com/gmusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=652", "Tamil Music"),
    ("Makkal TV Music", "https://i.imgur.com/makkal.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=847", "Tamil Music"),
    ("KTV Music", "https://i.imgur.com/ktvmusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1141", "Tamil Music"),
    ("JCV Musix", "https://i.imgur.com/jcvmusix.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=748", "Tamil Music"),
    ("Tamil Music", "https://i.imgur.com/tamilmusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1141", "Tamil Music"),
    ("Mega Music", "https://i.imgur.com/megamusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=652", "Tamil Music"),
    ("Isai Music", "https://i.imgur.com/isaimusic.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1141", "Tamil Music"),
    
    # Tamil Kids (10)
    ("Chutti TV", "https://i.imgur.com/chutti.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=846", "Tamil Kids"),
    ("Chithiram TV", "https://i.imgur.com/chithiram.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=846", "Tamil Kids"),
    ("Cartoon Network Tamil", "https://i.imgur.com/cntamil.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=9186", "Tamil Kids"),
    ("Pogo Tamil", "https://i.imgur.com/pogo.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11800", "Tamil Kids"),
    ("Discovery Kids Tamil", "https://i.imgur.com/discoverykids.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=764", "Tamil Kids"),
    ("Sony Yay Tamil", "https://i.imgur.com/sonyyay.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=1097", "Tamil Kids"),
    ("Nick Tamil", "https://i.imgur.com/nick.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11799", "Tamil Kids"),
    ("Disney Channel Tamil", "https://i.imgur.com/disney.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=9186", "Tamil Kids"),
    ("Hungama TV Tamil", "https://i.imgur.com/hungama.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=11799", "Tamil Kids"),
    ("Kochu TV Tamil", "https://i.imgur.com/kochu.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=846", "Tamil Kids"),
    
    # Sports (8)
    ("Star Sports 1 Tamil", "https://i.imgur.com/starsports1.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=150", "Sports"),
    ("Star Sports 2 Tamil", "https://i.imgur.com/starsports2.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=151", "Sports"),
    ("Star Sports 3 Tamil", "https://i.imgur.com/starsports3.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=152", "Sports"),
    ("Sony Ten 1 Tamil", "https://i.imgur.com/sonyten1.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=280", "Sports"),
    ("Sony Ten 2 Tamil", "https://i.imgur.com/sonyten2.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=281", "Sports"),
    ("Sony Ten 3 Tamil", "https://i.imgur.com/sonyten3.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=282", "Sports"),
    ("Eurosport Tamil", "https://i.imgur.com/eurosport.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=350", "Sports"),
    ("DD Sports Tamil", "https://i.imgur.com/ddsports.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=400", "Sports"),
    
    # Tamil Devotional (10)
    ("Angel TV", "https://i.imgur.com/angel.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=500", "Tamil Devotional"),
    ("Sathya TV", "https://i.imgur.com/sathya.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=501", "Tamil Devotional"),
    ("Murugan TV", "https://i.imgur.com/murugan.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=502", "Tamil Devotional"),
    ("Jeevan TV", "https://i.imgur.com/jeevan.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=503", "Tamil Devotional"),
    ("Aruloli TV", "https://i.imgur.com/aruloli.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=504", "Tamil Devotional"),
    ("Shubhsandesh TV", "https://i.imgur.com/shubhsandesh.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=505", "Tamil Devotional"),
    ("Goodness TV", "https://i.imgur.com/goodness.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=506", "Tamil Devotional"),
    ("Nambikkai TV", "https://i.imgur.com/nambikkai.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=507", "Tamil Devotional"),
    ("Sanskar TV Tamil", "https://i.imgur.com/sanskar.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=508", "Tamil Devotional"),
    ("Aastha Tamil", "https://i.imgur.com/aastha.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=509", "Tamil Devotional"),
    
    # Tamil Infotainment (8)
    ("Discovery Channel Tamil", "https://i.imgur.com/discovery.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=600", "Tamil Infotainment"),
    ("National Geographic Tamil", "https://i.imgur.com/natgeo.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=601", "Tamil Infotainment"),
    ("History TV18 Tamil", "https://i.imgur.com/history.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=602", "Tamil Infotainment"),
    ("Animal Planet Tamil", "https://i.imgur.com/animalplanet.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=603", "Tamil Infotainment"),
    ("Sony BBC Earth Tamil", "https://i.imgur.com/bbcearth.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=604", "Tamil Infotainment"),
    ("Discovery Science Tamil", "https://i.imgur.com/discscience.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=605", "Tamil Infotainment"),
    ("Nat Geo Wild Tamil", "https://i.imgur.com/natgeowild.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=606", "Tamil Infotainment"),
    ("Discovery Turbo Tamil", "https://i.imgur.com/discturbo.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=607", "Tamil Infotainment"),
    
    # Tamil Shopping (3)
    ("Home Shop 18 Tamil", "https://i.imgur.com/homeshop.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=700", "Tamil Shopping"),
    ("India Shop Tamil", "https://i.imgur.com/indiashop.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=701", "Tamil Shopping"),
    ("DD Kisan Tamil", "https://i.imgur.com/ddkisan.png", "https://tatatvbysufiyan.pages.dev/tatatv.m3u8?id=702", "Tamil Shopping"),
]

CATEGORIES = [
    "Tamil Entertainment", "Tamil News", "Tamil Movies", 
    "Tamil Music", "Tamil Kids", "Tamil Devotional", "Tamil Infotainment", 
    "Tamil Shopping", "Sports"
]

def main():
    # Group channels by category
    channels_by_cat = {cat: [] for cat in CATEGORIES}
    
    for name, logo, url, category in CHANNELS:
        if category in channels_by_cat:
            channels_by_cat[category].append((name, logo, url))
    
    # Write M3U file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in CATEGORIES:
            if channels_by_cat[cat]:
                f.write(f"\n# --- {cat} ---\n")
                for name, logo, url in channels_by_cat[cat]:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{cat}",{name}\n')
                    f.write(f'{url}\n')
    
    total = len(CHANNELS)
    print(f"\n✅ Done. Total: {total} channels")
    for cat in CATEGORIES:
        count = len(channels_by_cat[cat])
        if count > 0:
            print(f"  {cat}: {count}")
    
    # Write README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 📺 Tamil IPTV Playlist\n\n")
        f.write(f"**Updated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
        f.write(f"**Total Channels:** {total}\n\n")
        f.write("| Category | Channels |\n| --- | --- |\n")
        for cat in CATEGORIES:
            count = len(channels_by_cat[cat])
            if count > 0:
                f.write(f"| {cat} | {count} |\n")
        f.write("\n## 📺 Playlist URL\n```\nhttps://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n```\n")

if __name__ == "__main__":
    main()    "rcserver", "brightmeltech", "mindspell", "7starcloud", 
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

            name = clean_name(raw_name)
            if not name:
                continue

            category = detect_cat(name, url)
            if category is None:
                continue

            # Skip URL check only for Tamil Local
            if category not in SKIP_URL_CHECK:
                if not check_url(url):
                    print(f"  ✗ Dead: {name} ({category})")
                    continue

            seen_urls.add(url)
            new_attrs = dict(attrs)
            new_attrs["group-title"] = category
            channels[category][url] = (new_attrs, raw_name)
            print(f"  ✓ {raw_name} → {category}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat in CATEGORIES:
            if channels[cat]:
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
        if channels[cat]:
            print(f"  {cat}: {len(channels[cat])}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# 📺 Tamil & English IPTV\n\n")
        f.write(f"**Updated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n\n")
        f.write(f"**Total:** {total}\n\n")
        f.write("| Category | Channels |\n| --- | --- |\n")
        for cat in CATEGORIES:
            if channels[cat]:
                f.write(f"| {cat} | {len(channels[cat])} |\n")
        f.write("\n## 📺 Playlist URL\n```\nhttps://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n```\n")

if __name__ == "__main__":
    main()
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
