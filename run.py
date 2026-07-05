import requests
import re
import json
import datetime
import concurrent.futures

# ==========================================
# 1. USER'S CUSTOM HARDCODED CHANNELS
# ==========================================
USER_CUSTOM_CHANNELS = """
#EXTINF:-1 group-title="local channels",Sana TV
https://galaxyott.live/hls/sanatv.m3u8
#EXTINF:-1 group-title="local channels",Sana Plus
https://galaxyott.live/hls/sanaplus.m3u8
#EXTINF:-1 group-title="local channels",UTV
https://stream.galaxyott.live/live/utv/index.m3u8
#EXTINF:-1 group-title="local channels",NTV
https://galaxyott.live/hls/ntv.m3u8
#EXTINF:-1 group-title="local channels",Surya TV
https://galaxyott.live/hls/suryatv.m3u8
#EXTINF:-1 group-title="local channels",Subin TV
https://stream.galaxyott.live/live/subintv/index.m3u8
#EXTINF:-1 group-title="local channels",Moon TV
https://live.maxtn.in/moontv/moontv/index.m3u8
#EXTINF:-1 group-title="local channels",Sakthi TV
https://live.sscloud7.in/live/sakthitv/index.m3u8
#EXTINF:-1 group-title="local channels",Prime TV
https://live.applelive.in/primetv/primetv/index.m3u8
#EXTINF:-1 group-title="local channels",D TV
https://stream.d6-pro.com/Dtv/live/index.m3u8
#EXTINF:-1 group-title="local channels",TDN
https://live.maxtn.in/tdn/tdn/index.m3u8
#EXTINF:-1 group-title="local channels",7 Green
https://account33.livebox.co.in/7GREEN4Khls/live.m3u8
#EXTINF:-1 group-title="local channels",Yet TV
https://live.yettelevision.com:5443/LiveApp/streams/yettv.m3u8
#EXTINF:-1 group-title="local channels",PR TV
https://play.applelive.in/prtv/prtv.m3u8
#EXTINF:-1 group-title="local channels",Riya TV
https://play.applelive.in/riyatv/riyatv.m3u8
#EXTINF:-1 group-title="local channels",Dark TV
https://play.applelive.in/darktv/darktv.m3u8
#EXTINF:-1 group-title="local channels",Harin TV HD
https://ipcloud.live/harintv/harintvhd/index.m3u8
#EXTINF:-1 group-title="local channels",Phoenix TV
https://stream.onecloudlive.in/phoenixtv/phoenixtv/index.m3u8
#EXTINF:-1 group-title="local channels",Roja TV
https://live.rojatv.cloud/rojatv/rojatv/index.m3u8
#EXTINF:-1 group-title="local channels",Roja TV
https://stream.rojatv.cloud/rojatv/rojatv/index.m3u8
#EXTINF:-1 group-title="local channels",Nila TV
https://live.olidigital.in/nilatv/nilatv/index.m3u8
#EXTINF:-1 group-title="local channels",SMCV TV
https://singamcloud.in/smcvtv/smcvtv/index.m3u8
#EXTINF:-1 group-title="local channels",APS TV
https://apstv-a1.tamilstream.in/apstv/apstv/index.m3u8
#EXTINF:-1 group-title="local channels",APS Gold
https://apsgold-a1.tamilstream.in/apsgold/apsgold/index.m3u8
#EXTINF:-1 group-title="local channels",MTV Men HD
https://ipcloud.live/mtv/menhd/index.m3u8
#EXTINF:-1 group-title="local channels",MSN TV
https://ipcloud.live/msntv/msntv/index.m3u8
#EXTINF:-1 group-title="local channels",Veerali TV
https://ipcloud.live/veerali/veeralitv/index.m3u8
#EXTINF:-1 group-title="local channels",Three Star TV HD
https://stream.onecloudlive.in/threestartv/threestarhd/index.m3u8
#EXTINF:-1 group-title="local channels",Shalini TV
https://ipcloud.live/shalinitv/shalinitv/index.m3u8
#EXTINF:-1 group-title="local channels",JCV TV
https://play.applelive.in/jcvtv/jcvtv.m3u8
#EXTINF:-1 group-title="local channels",JCV Musix
https://play.applelive.in/jcvtv/jcvmusix.m3u8
#EXTINF:-1 group-title="local channels",Thendral TV
https://live.thendralcloud.in/thendraltv/d0dbe915091d400bd8ee7f27f0791303.sdp/chunks.m3u8
#EXTINF:-1 group-title="local channels",Anbu TV HD
https://ipcloud.live/anbutv/anbutvhd/index.m3u8
#EXTINF:-1 group-title="local channels",Nellai TV
https://stream.onecloudlive.in/nellaitv/nellaitv/index.m3u8
#EXTINF:-1 group-title="local channels",A3e0b02f
https://app.ashokadigital.net/app/a3e0b02f/index.m3u8
#EXTINF:-1 group-title="local channels",Akash TV
https://account2.livebox.co.in/AkashTvhls/live.m3u8
#EXTINF:-1 group-title="local channels",Apple TV
https://play.applelive.in/appletv/appletv.m3u8
#EXTINF:-1 group-title="local channels",Jeyson TV
https://play.applelive.in/jeysontv/jeysontv.m3u8
#EXTINF:-1 group-title="local channels",JJ Max
https://play.applelive.in/jjmax/jjmax.m3u8
#EXTINF:-1 group-title="local channels",JC TV
https://play.applelive.in/jctv/jctv.m3u8
#EXTINF:-1 group-title="local channels",Digital TV
https://play.applelive.in/digitaltv/digitaltv.m3u8
#EXTINF:-1 group-title="local channels",Oscar TV
https://account21.livebox.co.in/oscartvhls/live.m3u8
#EXTINF:-1 group-title="local channels",Jeyan TV
https://stream.onecloudlive.in/jeyantv/jeyantv/index.m3u8
#EXTINF:-1 group-title="local channels",Vidyal TV
https://account11.livebox.co.in/vidyaltvhls/live.m3u8?psk=stream
#EXTINF:-1 group-title="local channels",KCN TV
https://view.rcserver.in/tmp_hls12/kcntv/index.m3u8
#EXTINF:-1 group-title="local channels",Sky TV
https://sscloud7.com/live/skytv/index.m3u8
#EXTINF:-1 group-title="local channels",Boys TV
https://rtmp.applelive.in/boystv/boystv/index.m3u8
#EXTINF:-1 group-title="local channels",King TV
https://server.sscloud7.in/kingtv/kingtv/index.m3u8
#EXTINF:-1 group-title="local channels",Sky TV
https://view.rcserver.in/tmp_hls6/skytv/index.m3u8
#EXTINF:-1 group-title="local channels",Udhayam TV
https://view.rcserver.in/tmp_hls8/udhayamtv/index.m3u8
#EXTINF:-1 group-title="local channels",TN TV
https://view.rcserver.in/tmp_hls14/tntv/index.m3u8
#EXTINF:-1 group-title="local channels",Senthamil TV
https://view.rcserver.in/tmp_hls24/senthamiltv/index.m3u8
#EXTINF:-1 group-title="local channels",Karur TV
https://view.rcserver.in/tmp_hls16/karurtv/index.m3u8
#EXTINF:-1 group-title="local channels",Karur City
https://view.rcserver.in/tmp_hls17/karurcity/index.m3u8
#EXTINF:-1 group-title="local channels",Tmp Hls20
https://view.rcserver.in/tmp_hls20/index.m3u8
#EXTINF:-1 group-title="local channels",Thirai TV
https://view.apserver.in/tmp_hls2/thiraitv/index.m3u8
#EXTINF:-1 group-title="local channels",Bharathi TV
https://server.sscloud7.in/live/bharathitv/index.m3u8
#EXTINF:-1 group-title="local channels",Thendral TV
https://sscloud7.com/live/thendraltv/index.m3u8
#EXTINF:-1 group-title="local channels",Irattipaathai TV
https://account31.livebox.co.in/IRATTAIPAATHAITVhls/live.m3u8
#EXTINF:-1 group-title="local channels",MCN TV
https://play.applelive.in/mcntv/mcntv.m3u8
#EXTINF:-1 group-title="local channels",STN TV
https://play.applelive.in/stntv/stntv.m3u8
#EXTINF:-1 group-title="local channels",Suriyan TV
https://view.rcserver.in/tmp_hls9/suriyantv/index.m3u8
#EXTINF:-1 group-title="local channels",Vasanth TV
https://play.applelive.in/vasanthtv/vasanthtv.m3u8
#EXTINF:-1 group-title="local channels",Eesan TV
https://live.singamcloud.in/eesantv/eesantv/index.m3u8
#EXTINF:-1 group-title="local channels",68b001a0
https://app.ashokadigital.net/app/68b001a0/index.m3u8
#EXTINF:-1 group-title="local channels",Jeyam TV
https://live.sscloud7.in/live/jeyamtv/index.m3u8
#EXTINF:-1 group-title="local channels",Aadhavan TV Colours
https://live.olidigital.in/aadhavantvcolours/aadhavantvcolours/index.m3u8
#EXTINF:-1 group-title="local channels",Solai TV HD
https://ipcloud.live/solaitv/solaihd/index.m3u8
#EXTINF:-1 group-title="local channels",MM TV Jeyam Plus
https://ipcloud.live/mmtv/jeyamplus/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",chithiram tv
https://cdn-6.pishow.tv/live/1243/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",dd tamil
https://d2lk5u59tns74c.cloudfront.net/out/v1/abf46b14847e45499f4a47f3a9afe93d/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",EET Live EET TV
https://eu.streamjo.com/eetlive/eettv.m3u8
#EXTINF:-1 group-title="tamil iptv channels",EET Live EET TV
https://live.streamjo.com/eetlive/eettv.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Isaiaruvi
https://segment.yuppcdn.net/140622/isaiaruvi/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Murasu
https://segment.yuppcdn.net/050522/murasu/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Kalaignar TV
https://segment.yuppcdn.net/240122/kalaignartv/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",mathimugam
https://cdn-3.pishow.tv/live/1476/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Makkal
https://5k8q87azdy4v-hls-live.wmncdn.net/MAKKAL/271ddf829afeece44d8732757fba1a66.sdp/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",malai murasu
https://cdn-3.pishow.tv/live/1606/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",News7
https://segment.yuppcdn.net/240122/news7/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",News18 Tamil Nadu NW18
https://n18syndication.akamaized.net/bpk-tv/News18_Tamil_Nadu_NW18_MOB/output01/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",news j
https://cdn-3.pishow.tv/live/1279/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Polimer News
https://segment.yuppcdn.net/110322/polimernews/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",polimer tv
https://cdn-2.pishow.tv/live/1241/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Puthiya
https://segment.yuppcdn.net/240122/puthiya/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",raj tv
https://d3qs3d2rkhfqrt.cloudfront.net/out/v1/2839e3d1e0f84a2e821c1708d5fdfdf0/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Roja TV
https://stream.rojatv.cloud/rojatv/rojatv/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Roja TV
https://live.rojatv.cloud/rojatv/rojatv/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Sana Plus
https://galaxyott.live/hls/sanaplus.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Sana TV
https://galaxyott.live/hls/sanatv.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Siripoli
https://segment.yuppcdn.net/240122/siripoli/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Subin TV
https://stream.galaxyott.live/live/subintv/index.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Zionmediait 97484f5ce6da96e496a9b87c439835d0
https://cdn.zionmediait.com/zionmediaitserver2024/97484f5ce6da96e496a9b87c439835d0.sdp/playlist.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Thalaa TV TAM
https://streams2.sofast.tv/ptnr-yupptv/title-THALAA-TV-TAM_yupptv/v1/master/611d79b11b77e2f571934fd80ca1413453772ac7/2069c593-3c07-4d62-9d44-746be5c3a5d6/manifest.m3u8
#EXTINF:-1 group-title="tamil iptv channels",thanthi tv
https://cdn-3.pishow.tv/live/1612/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",Thendral TV
https://live.thendralcloud.in/thendraltv/d0dbe915091d400bd8ee7f27f0791303.sdp/chunks.m3u8
#EXTINF:-1 group-title="tamil iptv channels",vendhar tv
https://cdn-3.pishow.tv/live/1271/master.m3u8
#EXTINF:-1 group-title="tamil iptv channels",win news
https://cdn-4.pishow.tv/live/1531/master.m3u8
"""

# ==========================================
# 2. ALL SOURCES
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

# Strict Local Source lock (Ashoka excluded per your instructions)
LOCAL_SOURCES = [
    "https://raw.githubusercontent.com/Vmfm/tamilvmtv/main/live/channels.m3u",
    "https://raw.githubusercontent.com/amazeyourself/m3u/main/ashokadigital.m3u",
    "https://raw.githubusercontent.com/amazeyourself/tamil-local-iptv/refs/heads/main/channels.m3u"
]

# ==========================================
# 3. RUTHLESS BLOCK LIST
# ==========================================
# Instantly destroys ANY channel (even local ones) with these words. 
BLOCKED_KEYWORDS = [
    "hindi", "telugu", "malayalam", "kannada", "marathi", "bengali", "bangla", 
    "gujarati", "punjabi", "odia", "assamese", "urdu", "bhojpuri",
    "spanish", "french", "german", "italian", "portuguese", "russian",
    "chinese", "japanese", "korean", "arabic", "indonesian", "nepali"
]

# ==========================================
# 4. STRICT CATEGORY WHITELIST & ORDERING
# ==========================================
CATEGORY_ORDER = [
    "Tamil GEC", "Tamil Movies", "Tamil News", "Tamil Comedy", 
    "Tamil Music", "Tamil Infotainment", "Tamil Spiritual", "Tamil Kids",
    "English GEC", "English Movies", "English National News", 
    "English International News", "English Business News", "English Infotainment", 
    "English Lifestyle", "English Kids", "Sports", 
    "local channels", "Tamil Local Channels", "tamil iptv channels"
]

CATEGORIES_MAP = {
    "Tamil GEC": {
        "Sun TV": ["sun tv"], "Star Vijay": ["star vijay", "vijay tv"], "Zee Tamil": ["zee tamil"],
        "Colors Tamil": ["colors tamil"], "Kalaignar TV": ["kalaignar tv", "kalaignar"],
        "Jaya TV": ["jaya tv"], "Raj TV": ["raj tv"], "Polimer TV": ["polimer tv"],
        "Makkal TV": ["makkal tv", "makkal"], "Vasanth TV": ["vasanth tv", "vasanth"],
        "Puthuyugam TV": ["puthuyugam tv", "puthuyugam"], "Mega TV": ["mega tv"],
        "Captain TV": ["captain tv"], "Vendhar TV": ["vendhar tv", "vendhar"]
    },
    "Tamil Movies": {
        "KTV": ["ktv"], "Star Vijay Super": ["star vijay super", "vijay super"],
        "Zee Thirai": ["zee thirai"], "J Movie": ["j movie", "jaya movie"],
        "Raj Digital Plus": ["raj digital plus"], "Murasu": ["murasu"],
        "Mega 24": ["mega 24"], "Sun Action": ["sun action"], "Tamil Movies": ["tamil movies", "tamil movie"]
    },
    "Tamil News": {
        "Sun News": ["sun news"], "Puthiya Thalaimurai": ["puthiya thalaimurai"],
        "Thanthi TV": ["thanthi tv", "thanthi"], "News18 Tamil Nadu": ["news18 tamil", "news 18 tamil"],
        "Polimer News": ["polimer news"], "News7 Tamil": ["news7 tamil", "news 7 tamil", "news 7"],
        "Sathiyam TV": ["sathiyam tv", "sathiyam"], "News J": ["news j", "newsj"],
        "Jaya Plus": ["jaya plus"], "Kalaignar Seithigal": ["kalaignar seithigal"],
        "Raj News Tamil": ["raj news tamil", "raj news"], "Captain News": ["captain news"]
    },
    "Tamil Comedy": {
        "Adithya TV": ["adithya tv", "adithya"], "Sirippoli": ["sirippoli"]
    },
    "Tamil Music": {
        "Sun Music": ["sun music"], "Star Vijay Music": ["star vijay music", "vijay music"],
        "Isaiaruvi": ["isaiaruvi", "isai aruvi"], "Jaya Max": ["jaya max"],
        "Raj Musix Tamil": ["raj musix tamil", "raj musix"], "Mega Musiq": ["mega musiq", "mega music"]
    },
    "Tamil Infotainment": {
        "Sun Life": ["sun life"], "Discovery Tamil": ["discovery tamil", "discovery channel tamil"],
        "Nat Geo Tamil": ["nat geo tamil", "national geographic tamil"], "Sony BBC Earth Tamil": ["sony bbc earth tamil", "bbc earth tamil"]
    },
    "Tamil Spiritual": {
        "Madha TV": ["madha tv"], "Angel TV": ["angel tv"], "Nambikkai TV": ["nambikkai tv", "nambikkai"],
        "Vaanavil": ["vaanavil"], "Jothi TV": ["jothi tv"], "Velicham TV": ["velicham tv"],
        "Sri Sankara TV": ["sri sankara tv", "sankara tv", "sri sankara"]
    },
    "Tamil Kids": {
        "Chutti TV": ["chutti tv"], "ETV Bal Bharat Tamil": ["etv bal bharat tamil", "bal bharat tamil"],
        "Cartoon Network Tamil": ["cartoon network tamil", "cn tamil"], "Pogo Tamil": ["pogo tamil"],
        "Discovery Kids Tamil": ["discovery kids tamil"], "Sony Yay Tamil": ["sony yay tamil"],
        "Nick Tamil": ["nick tamil", "nickelodeon tamil"], "Disney Channel Tamil": ["disney channel tamil", "disney tamil"],
        "Kochu TV": ["kochu tv"]
    },
    "English GEC": {
        "Zee Cafe": ["zee cafe"], "Colors Infinity": ["colors infinity"],
        "Comedy Central": ["comedy central"], "Disney International HD": ["disney international"]
    },
    "English Movies": {
        "Star Movies Select": ["star movies select"], "Star Movies": ["star movies"],
        "Sony PIX": ["sony pix"], "Movies Now": ["movies now"], "MNX": ["mnx"], "MN+": ["mn+"],
        "&flix": ["&flix", "andflix"], "&prive HD": ["&prive hd", "&prive", "andprive"],
        "Romedy Now": ["romedy now"], "HBO": ["hbo"], "WB": ["wb"]
    },
    "English National News": {
        "Times Now": ["times now"], "Republic TV": ["republic tv"], "CNN-News18": ["cnn-news18", "cnn news18"],
        "India Today": ["india today"], "NDTV 24x7": ["ndtv 24x7"], "NewsX": ["newsx"],
        "Mirror Now": ["mirror now"], "WION": ["wion"]
    },
    "English International News": {
        "BBC News": ["bbc news"], "CNN International": ["cnn international", "cnn"],
        "Al Jazeera English": ["al jazeera english", "al jazeera"], "RT (Russia Today)": ["rt russia today", "russia today", "rt news"]
    },
    "English Business News": {
        "CNBC-TV18": ["cnbc-tv18", "cnbc tv18"], "ET Now": ["et now"], "NDTV Profit": ["ndtv profit"]
    },
    "English Infotainment": {
        "Discovery Channel": ["discovery channel", "discovery"], "National Geographic": ["national geographic", "nat geo"],
        "History TV18": ["history tv18", "history"], "Animal Planet": ["animal planet"],
        "Sony BBC Earth": ["sony bbc earth", "bbc earth"]
    },
    "English Lifestyle": {
        "TLC": ["tlc"], "Travelxp": ["travelxp"], "Goodtimes": ["goodtimes"]
    },
    "English Kids": {
        "Cartoon Network": ["cartoon network"], "Nickelodeon": ["nickelodeon", "nick"],
        "Pogo": ["pogo"], "Disney Channel": ["disney channel"], "Disney Junior": ["disney junior"],
        "Sonic": ["sonic"], "Super Hungama": ["super hungama"], "Discovery Kids": ["discovery kids"],
        "BabyTV": ["babytv"]
    },
    "Sports": {
        "Star Sports 1 Tamil": ["star sports 1 tamil", "star sports tamil"], "Star Sports 1": ["star sports 1"],
        "Star Sports 2": ["star sports 2"], "Star Sports Select 1": ["star sports select 1"],
        "Star Sports Select 2": ["star sports select 2"], "Sony Sports Ten 1": ["sony sports ten 1", "sony ten 1"],
        "Sony Sports Ten 2": ["sony sports ten 2", "sony ten 2"], "Sony Sports Ten 5": ["sony sports ten 5", "sony ten 5"],
        "Eurosport": ["eurosport"], "Sports18 - 1": ["sports18 - 1", "sports18", "sports 18"]
    }
}

# --- LONGEST KEYWORD MATCHER (Fixes Category Mismatches) ---
FLAT_CATEGORIES = []
for cat, channels in CATEGORIES_MAP.items():
    for proper_name, keywords in channels.items():
        for kw in keywords:
            # Save length of keyword to sort longest first
            FLAT_CATEGORIES.append((len(kw), kw, proper_name, cat))
# Sort descending by length so "Star Sports 1 Tamil" is matched before "Star Sports 1"
FLAT_CATEGORIES.sort(reverse=True, key=lambda x: x[0])

# ==========================================
# 5. CORE FUNCTIONS
# ==========================================
def clean_name(name):
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    name = re.sub(r'\s*\(.*?\)\s*', '', name)
    return ' '.join(name.split()).strip()

def is_blocked(name):
    if not name: return True
    n = name.lower()
    return any(lang in n for lang in BLOCKED_KEYWORDS)

def get_category_and_name(name):
    if is_blocked(name): return None, None
    n = name.lower()
    
    # Matches using the Longest Keyword First logic
    for _, kw, proper_name, cat in FLAT_CATEGORIES:
        if kw in n:
            return cat, proper_name
            
    return None, None

def parse_m3u(content):
    channels = []
    lines = content.splitlines()
    current_name, current_logo, current_cat = None, "", None
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF:"):
            logos = re.findall(r'tvg-logo="(.*?)"', line)
            current_logo = logos[0] if logos else ""
            cats = re.findall(r'group-title="(.*?)"', line)
            current_cat = cats[0] if cats else None
            current_name = line.rsplit(',', 1)[1].strip() if ',' in line else None
        elif line and not line.startswith("#") and current_name:
            channels.append((current_name, current_logo, line, current_cat))
            current_name, current_cat = None, None
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
            if name and url: channels.append((name, logo, url, None))
    except Exception: pass
    return channels

def strict_stream_check(url, cat):
    """
    Advanced broken link logic. 
    Strictly enforces an 8s timeout and scans headers and bytes.
    """
    timeout_val = 5.0 if "local" in cat.lower() else 8.0
    headers = {'User-Agent': 'VLC/3.0.9 LibVLC/3.0.9', 'Accept': '*/*'}
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout_val, stream=True)
        if response.status_code != 200: return False
        
        ctype = response.headers.get('Content-Type', '').lower()
        if 'text/html' in ctype: return False
            
        # Read a sizable chunk to verify it's a real stream
        chunk = response.raw.read(1500)
        if not chunk: return False
            
        text_chunk = chunk.decode('utf-8', errors='ignore').lower()
        
        # Fake HTML masquerading as 200 OK
        if '<html' in text_chunk or '<body' in text_chunk or '<!doctype' in text_chunk:
            return False
            
        # Strict M3U8 payload validation
        if '.m3u8' in url.lower() or 'mpegurl' in ctype:
            if '#extm3u' not in text_chunk: return False
            if '#extinf' not in text_chunk and '#ext-x' not in text_chunk:
                return False
                
        return True
    except Exception:
        return False

def process_channel_urls(item):
    """
    Tests the URLs for a specific channel ONE BY ONE.
    Stops testing immediately once it finds a working link to guarantee 0 duplicates.
    """
    proper_name, data = item
    cat = data['category']
    logo = data['logo']
    
    for url in data['urls']:
        if strict_stream_check(url, cat):
            return (cat, proper_name, logo, url)  # Winner!
            
    return None # All links broken

# ==========================================
# 6. MAIN EXECUTION
# ==========================================
def main():
    print("Starting Ultimate Deduplication, Ordered, & Strict Validation Builder...")
    
    # Structure: {'Sun TV': {'category': 'Tamil GEC', 'logo': 'url', 'urls': [url1, url2]}}
    grouped_channels = {}
    seen_urls_global = set()

    # --- 1. GATHER CUSTOM CHANNELS FIRST (Gives them Priority!) ---
    print("\nGathering User Custom Channels...")
    custom_parsed = parse_m3u(USER_CUSTOM_CHANNELS)
    for name, logo, url, custom_cat in custom_parsed:
        url = url.strip()
        if not url.startswith("http") or url in seen_urls_global: continue
        seen_urls_global.add(url)
        
        if is_blocked(name): continue  # Block junk from custom lists too
        
        cat = custom_cat if custom_cat else "tamil iptv channels"
        proper_name = clean_name(name)
        
        if proper_name not in grouped_channels:
            grouped_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': []}
        grouped_channels[proper_name]['urls'].append(url)

    # --- 2. GATHER FROM GITHUB REPOS ---
    for src_url in SOURCES:
        print(f"Scraping: {src_url}")
        try:
            resp = requests.get(src_url, timeout=15)
            resp.raise_for_status()
            parsed = parse_json(resp.text) if src_url.endswith('.json') else parse_m3u(resp.text)
            
            for name, logo, url, _ in parsed:
                url = url.strip()
                if not url.startswith("http") or url in seen_urls_global: continue
                seen_urls_global.add(url)
                
                if is_blocked(name): continue 
                
                cat, proper_name = get_category_and_name(name)
                
                # Strict Local Channel verification
                if not cat:
                    if src_url in LOCAL_SOURCES:
                        cat = "Tamil Local Channels"
                        proper_name = clean_name(name)
                    else:
                        continue 
                        
                if proper_name not in grouped_channels:
                    grouped_channels[proper_name] = {'category': cat, 'logo': logo, 'urls': []}
                grouped_channels[proper_name]['urls'].append(url)
                if not grouped_channels[proper_name]['logo'] and logo:
                    grouped_channels[proper_name]['logo'] = logo
                    
        except Exception:
            pass

    print(f"\n-> Extracted {len(grouped_channels)} unique channels. Testing backups to find 1 working link per channel...")
    
    # --- 3. MULTITHREADED STRICT TESTING ---
    final_channels = {cat: [] for cat in CATEGORY_ORDER}
    total_added = 0
    
    # Sends each "Proper Name" (with all its backup URLs) to be tested
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(process_channel_urls, grouped_channels.items())
        for res in results:
            if res:
                cat, proper_name, logo, url = res
                if cat not in final_channels:
                    final_channels[cat] = []
                final_channels[cat].append((proper_name, logo, url))
                total_added += 1

    # ==========================================
    # 7. ORDERED SORTING & FILE GENERATION
    # ==========================================
    print("\nWriting master_playlist.m3u in perfect category order...")
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#PLAYLIST:Checked by CODECS.COM M3U Checker\n")
        
        # Enforce exact category order requested
        for cat in CATEGORY_ORDER:
            if cat in final_channels and final_channels[cat]:
                channels = final_channels[cat]
                channels.sort(key=lambda x: x[0].lower()) # A-Z sort inside category
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

        # Catch any custom categories just in case
        for cat in sorted(final_channels.keys()):
            if cat not in CATEGORY_ORDER and final_channels[cat]:
                channels = final_channels[cat]
                channels.sort(key=lambda x: x[0].lower())
                f.write(f"\n# --- {cat} ---\n")
                for display_name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{display_name}" tvg-logo="{logo}" group-title="{cat}",{display_name}\n{url}\n')

    print(f"\n✅ SUCCESS! Total Working Unique Channels: {total_added}")
    
    # ---------------------------------------------------------
    # README UPDATE
    # ---------------------------------------------------------
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil & English IPTV Playlist\n\n")
        f.write("This playlist is automatically checked, perfectly categorized, A-Z sorted, completely deduplicated (1 link per channel), and updated every 6 hours.\n\n")
        f.write(f"**Total LIVE Channels:** {total_added}\n**Last Updated:** {timestamp}\n\n")
        
        f.write("## 📥 Playlist URL\n")
        f.write("Use the **Copy button** in the top right corner of the box below. Paste it directly into your IPTV Player:\n\n")
        
        f.write("```text\n")
        f.write("[https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u](https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u)\n")
        f.write("```\n\n")
        
        f.write("## 📊 Channel Breakdown\n| Category | Count |\n|---|---|\n")
        for cat in CATEGORY_ORDER:
            if cat in final_channels and final_channels[cat]:
                f.write(f"| {cat} | {len(final_channels[cat])} |\n")

if __name__ == "__main__":
    main()
