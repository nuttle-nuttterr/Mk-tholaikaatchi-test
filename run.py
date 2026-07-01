import requests
import re
import time

def main():
    print("Starting playlist generation...")
    
    urls_to_fetch = [
        "https://iptv-org.github.io/iptv/languages/tam.m3u",
        "https://iptv-org.github.io/iptv/languages/eng.m3u"
    ]
    
    categories = {
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
    
    final_channels = {cat: [] for cat in categories.keys()}
    seen_urls = set()
    
    for source_url in urls_to_fetch:
        print(f"Fetching {source_url}...")
        try:
            response = requests.get(source_url, timeout=10)
            response.raise_for_status()
            lines = response.text.splitlines()
            
            current_name = None
            current_attrs = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    current_attrs = dict(re.findall(r'(\S+)="(.*?)"', line))
                    if ',' in line:
                        current_name = line.rsplit(',', 1)[1].strip()
                    else:
                        current_name = None
                elif line and not line.startswith("#") and current_name:
                    url = line
                    if url.startswith("http") and url not in seen_urls:
                        seen_urls.add(url)
                        
                        name_lower = current_name.lower()
                        assigned_cat = None
                        for cat, keywords in categories.items():
                            for kw in keywords:
                                if kw in name_lower:
                                    assigned_cat = cat
                                    break
                            if assigned_cat:
                                break
                                
                        if assigned_cat:
                            clean_name = re.sub(r'\s*\[.*?\]\s*', '', current_name)
                            clean_name = re.sub(r'\s*\(.*?\)\s*', '', clean_name)
                            clean_name = re.sub(r'\s*\b(HD|SD|HEVC|4K|UHD)\b\s*', '', clean_name, flags=re.I).strip()
                            
                            logo = current_attrs.get('tvg-logo', '')
                            final_channels[assigned_cat].append((clean_name, logo, url))
                            
                    current_name = None
                    current_attrs = {}
                    
        except Exception as e:
            print(f"Error fetching {source_url}: {e}")
            continue
            
    with open("master_playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for cat, channels in final_channels.items():
            if channels:
                f.write(f"\n# --- {cat} ---\n")
                for name, logo, url in channels:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{cat}",{name}\n')
                    f.write(f'{url}\n')
                    
    total = sum(len(v) for v in final_channels.values())
    print(f"Success! Generated {total} channels.")
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write("# Tamil IPTV Playlist\n\n")
        f.write(f"Total Channels: {total}\n\n")
        f.write("## Playlist URL\n")
        f.write("https://raw.githubusercontent.com/nuttle-nuttterr/Mk-tholaikaatchi-test/main/master_playlist.m3u\n")

if __name__ == "__main__":
    main()
