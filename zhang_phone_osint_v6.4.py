import re
import json
import time
import urllib.parse
import urllib.request
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

VERSION = "6.4"

# =========================
# ANSI STYLE
# =========================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
CYAN2 = "\033[36m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"
WHITE = "\033[97m"
GRAY = "\033[90m"
CLEAR = "\033[2J\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"


def clear():
    print(CLEAR, end="")


def width():
    return min(shutil.get_terminal_size((70, 24)).columns, 78)


def line(char="═"):
    return char * width()


def typewrite(text, delay=0.012, color=CYAN):
    print(color, end="")
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(RESET)


def spinner(text="Scanning", seconds=0.7):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + seconds
    i = 0
    print(HIDE_CURSOR, end="")
    try:
        while time.time() < end:
            print(f"\r{CYAN}{frames[i % len(frames)]}{RESET} {text}...", end="", flush=True)
            time.sleep(0.07)
            i += 1
    finally:
        print(SHOW_CURSOR, end="")
        print("\r" + " " * (len(text) + 8) + "\r", end="")


def progress(label="Processing", steps=18, delay=0.025):
    print(f"{CYAN}{label}{RESET}")
    print(HIDE_CURSOR, end="")
    try:
        for i in range(steps + 1):
            filled = "█" * i
            empty = "░" * (steps - i)
            pct = int(i / steps * 100)
            print(f"\r{CYAN}[{filled}{empty}]{RESET} {pct:3d}%", end="", flush=True)
            time.sleep(delay)
    finally:
        print(SHOW_CURSOR, end="")
        print()


def badge(text, color=CYAN):
    return f"{color}{BOLD} {text} {RESET}"


# =========================
# BANNER
# =========================
def banner():
    art = f"""
{CYAN}╔{'═' * 58}╗
║{RESET}{CYAN}              Z H A N G   P H O N E   O S I N T{RESET}{CYAN}              ║
║{RESET}{MAGENTA}                         V {VERSION}{RESET}{CYAN}                         ║
║{RESET}{WHITE}                  Public Intelligence Toolkit{RESET}{CYAN}                  ║
║{RESET}{GRAY}                    By : Muhammad Jeksen{RESET}{CYAN}                    ║
╚{'═' * 58}╝{RESET}
"""
    print(art)


def section(title, icon="◆"):
    print(f"\n{CYAN}{BOLD}{icon} {title.upper()}{RESET}")
    print(f"{CYAN}{line('─')}{RESET}")


# =========================
# PROVIDER
# =========================
PROVIDERS = {
    "Telkomsel": [
        "0811", "0812", "0813", "0821", "0822", "0823",
        "0851", "0852", "0853"
    ],
    "IM3 / Indosat": [
        "0814", "0815", "0816", "0855", "0856", "0857", "0858"
    ],
    "XL": [
        "0817", "0818", "0819", "0859", "0877", "0878", "0879"
    ],
    "AXIS": ["0831", "0832", "0833", "0838"],
    "Tri": ["0895", "0896", "0897", "0898", "0899"],
    "Smartfren": ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"]
}


# =========================
# HLR REFERENCE
# =========================
HLR_RANGES = {
    (10, 14): "Jabodetabek",
    (15, 32): "Jawa Barat",
    (33, 38): "Jawa Tengah",
    (39, 43): "Jawa Timur",
    (44, 47): "Bali",
    (48, 59): "Kalimantan",
    (60, 68): "Sumatera bagian utara",
    (69, 74): "Sumatera bagian tengah",
    (75, 86): "Sumatera bagian selatan",
    (87, 96): "Sulawesi",
    (97, 99): "Papua & Maluku",
}

HLR_SPECIFIC = {
    "081361": "Medan",
    "081370": "Medan",
    "081375": "Medan",
    "081376": "Medan",
    "081368": "Palembang",
    "081369": "Palembang",
}


def get_hlr_reference(local, provider):
    if provider != "Telkomsel":
        return "Tidak tersedia - referensi HLR Telkomsel"
    if len(local) < 6:
        return "Tidak tersedia"
    block6 = local[:6]
    if block6 in HLR_SPECIFIC:
        return f"{block6} - {HLR_SPECIFIC[block6]}"
    try:
        hlr_code = int(local[4:6])
    except ValueError:
        return "Tidak tersedia"
    for (start, end), region in HLR_RANGES.items():
        if start <= hlr_code <= end:
            return f"{hlr_code} - {region}"
    return f"{hlr_code} - Tidak diketahui"


def get_provider(prefix):
    for provider, prefixes in PROVIDERS.items():
        if prefix in prefixes:
            return provider
    return "Tidak diketahui"


def normalize_number(number):
    number = re.sub(r"\D", "", number)
    if number.startswith("62"):
        international = "+" + number
        local = "0" + number[2:]
    elif number.startswith("0"):
        local = number
        international = "+62" + number[1:]
    else:
        local = "0" + number
        international = "+62" + number
    return international, local


# =========================
# PHONE ANALYSIS
# =========================
def analyze_phone(number):
    international, local = normalize_number(number)
    prefix = local[:4]
    provider = get_provider(prefix)
    hlr = get_hlr_reference(local, provider)
    return {
        "international": international,
        "local": local,
        "country": "Indonesia",
        "prefix": prefix,
        "provider": provider,
        "hlr_reference": hlr
    }


def print_phone_analysis(data):
    section("Phone Analysis", "◈")
    rows = [
        ("International", data["international"]),
        ("Local", data["local"]),
        ("Country", data["country"]),
        ("Prefix", data["prefix"]),
        ("Provider", data["provider"]),
        ("HLR Reference", data["hlr_reference"]),
    ]
    for key, value in rows:
        print(f"{WHITE}{key:<16}{RESET} {CYAN}│{RESET} {GREEN}{value}{RESET}")
    print(f"\n{YELLOW}⚠ HLR hanya referensi area nomor, bukan lokasi real-time.{RESET}")


# =========================
# GOOGLE / SEARCH
# =========================
def google_url(query):
    encoded = urllib.parse.quote(query)
    return f"https://www.google.com/search?q={encoded}"


def build_social_searches(number):
    sites = {
        "Facebook": "facebook.com",
        "Instagram": "instagram.com",
        "TikTok": "tiktok.com",
        "X": "x.com",
        "Telegram": "t.me"
    }
    return {name: google_url(f'site:{site} "{number}"') for name, site in sites.items()}


def build_dorks(number):
    return [
        f'"{number}"',
        f'site:facebook.com "{number}"',
        f'site:instagram.com "{number}"',
        f'site:tiktok.com "{number}"',
        f'site:x.com "{number}"',
        f'site:t.me "{number}"',
        f'site:github.com "{number}"'
    ]


def check_url(name, url):
    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Android) AppleWebKit/537.36 "
                "Chrome/120 Mobile Safari/537.36"
            }
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            code = response.status
        if code == 200:
            return name, "OPEN SEARCH"
        return name, f"HTTP {code}"
    except Exception:
        return name, "TIMEOUT / BLOCKED"


def fast_check(searches):
    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = {
            executor.submit(check_url, name, url): name
            for name, url in searches.items()
        }
        for future in as_completed(tasks):
            name, status = future.result()
            results[name] = status
    return results


def status_color(status):
    if status == "OPEN SEARCH":
        return GREEN
    if "TIMEOUT" in status or "BLOCKED" in status:
        return RED
    return YELLOW


def show_result(name, url, status):
    icon = "✓" if status == "OPEN SEARCH" else "!"
    color = status_color(status)
    print(f"\n{WHITE}{icon} {BOLD}{name}{RESET}")
    print(f"  {GRAY}Status{RESET} {CYAN}│{RESET} {color}{status}{RESET}")
    print(f"  {GRAY}URL   {RESET} {CYAN}│{RESET} {url}")


# =========================
# PUBLIC WEB
# =========================
def public_web(number):
    section("Public Web OSINT", "◎")
    searches = {"Google": google_url(f'"{number}"')}
    spinner("Connecting to Google", 0.55)
    results = fast_check(searches)
    for name, url in searches.items():
        show_result(name, url, results.get(name, "UNKNOWN"))
    return {"urls": searches, "status": results}


# =========================
# SOCIAL
# =========================
def social_osint(number):
    section("Social Public OSINT", "◉")
    searches = build_social_searches(number)
    print(f"{GRAY}Checking public search endpoints in parallel...{RESET}")
    spinner("Scanning public indexes", 0.65)
    results = fast_check(searches)
    for name, url in searches.items():
        show_result(name, url, results.get(name, "UNKNOWN"))
    return {"urls": searches, "status": results}


# =========================
# GITHUB
# =========================
def github_search(number):
    section("GitHub Public Search", "◫")
    url = google_url(f'site:github.com "{number}"')
    spinner("Preparing GitHub public search", 0.45)
    print(f"{GREEN}✓ GitHub search ready{RESET}")
    print(f"{GRAY}URL{RESET} {CYAN}│{RESET} {url}")
    return url


# =========================
# DORK
# =========================
def show_dorks(number):
    section("Google Dork Generator", "⌕")
    dorks = build_dorks(number)
    for i, dork in enumerate(dorks, 1):
        print(f"{CYAN}[{i:02d}]{RESET} {WHITE}{dork}{RESET}")


# =========================
# REPORT
# =========================
def save_report(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    txt_file = "phone_osint_report.txt"
    json_file = "phone_osint_report.json"

    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"ZHANG PHONE OSINT V{VERSION}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Timestamp : {timestamp}\n\n")
        f.write("PHONE ANALYSIS\n" + "-" * 50 + "\n")
        for key, value in data["phone"].items():
            f.write(f"{key}: {value}\n")
        f.write("\nPUBLIC WEB\n" + "-" * 50 + "\n")
        for name, url in data["public_web"]["urls"].items():
            f.write(f"{name}: {data['public_web']['status'].get(name)}\n{url}\n\n")
        f.write("\nSOCIAL PUBLIC OSINT\n" + "-" * 50 + "\n")
        for name, url in data["social"]["urls"].items():
            f.write(f"{name}: {data['social']['status'].get(name)}\n{url}\n\n")
        f.write("\nDISCLAIMER\n" + "-" * 50 + "\n")
        f.write(
            "Tool ini hanya menggunakan pencarian dan informasi publik.\n"
            "Status OPEN SEARCH tidak berarti nomor ditemukan atau dimiliki\n"
            "oleh seseorang tertentu.\n"
            "HLR adalah referensi area nomor, bukan lokasi real-time.\n"
        )

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n{GREEN}✓ TXT report : {txt_file}{RESET}")
    print(f"{GREEN}✓ JSON report: {json_file}{RESET}")


# =========================
# ABOUT
# =========================
def about():
    clear()
    banner()
    section("About ZHANG", "ⓘ")
    print(f"{WHITE}ZHANG Phone OSINT{RESET} {CYAN}V{VERSION}{RESET}")
    print(f"{GRAY}Public-information search toolkit for Termux.{RESET}\n")
    features = [
        "Phone number analysis",
        "Provider reference",
        "HLR area reference",
        "Google public search",
        "Facebook / Instagram / TikTok / X / Telegram public search",
        "GitHub public search",
        "Google dork generator",
        "TXT + JSON report",
        "Parallel endpoint checks"
    ]
    for item in features:
        print(f"  {GREEN}✓{RESET} {item}")
    print(f"\n{YELLOW}⚠ Public OSINT only. No private accounts, leaked databases,\n  credentials, stalking, or real-time location tracking.{RESET}")
    input(f"\n{GRAY}Press Enter to return...{RESET}")


# =========================
# MENU
# =========================
def menu():
    print(f"{CYAN}{BOLD}┌──────────────────────────────────────────────┐{RESET}")
    items = [
        ("1", "Phone Analysis", "Analyze"),
        ("2", "Public Web OSINT", "Google"),
        ("3", "Social Public OSINT", "Social"),
        ("4", "Search All", "Full Scan"),
        ("5", "Google Dork Generator", "Dorks"),
        ("6", "GitHub Public Search", "GitHub"),
        ("7", "About", "Info"),
        ("0", "Exit", "Quit"),
    ]
    for key, label, tag in items:
        print(f"{CYAN}│{RESET} {MAGENTA}[{key}]{RESET} {WHITE}{label:<24}{RESET} {GRAY}{tag:<10}{RESET} {CYAN}│{RESET}")
    print(f"{CYAN}└──────────────────────────────────────────────┘{RESET}")


def main():
    try:
        clear()
        banner()
        progress("Initializing ZHANG engine", 16, 0.018)
        time.sleep(0.15)

        while True:
            clear()
            banner()
            print(f"{GRAY}Termux Edition  •  Public OSINT  •  Fast Scan{RESET}\n")
            menu()
            choice = input(f"\n{CYAN}{BOLD}ZHANG{RESET} {MAGENTA}›{RESET} ").strip()

            if choice == "0":
                print(f"\n{CYAN}╭─{RESET} {GREEN}Session closed. Stay ethical, Kayzen.{RESET} {CYAN}─╮{RESET}\n")
                break

            if choice == "7":
                about()
                continue

            if choice not in {"1", "2", "3", "4", "5", "6"}:
                print(f"{RED}✗ Pilihan tidak tersedia.{RESET}")
                time.sleep(0.8)
                continue

            number = input(f"\n{WHITE}Target number{RESET} {CYAN}›{RESET} ").strip()
            if not number:
                print(f"{RED}✗ Nomor tidak boleh kosong.{RESET}")
                time.sleep(0.8)
                continue

            spinner("Normalizing phone number", 0.35)
            phone = analyze_phone(number)
            print_phone_analysis(phone)

            public_result = None
            social_result = None

            if choice == "1":
                pass
            elif choice == "2":
                public_result = public_web(phone["international"])
            elif choice == "3":
                social_result = social_osint(phone["international"])
            elif choice == "4":
                public_result = public_web(phone["international"])
                social_result = social_osint(phone["international"])
            elif choice == "5":
                show_dorks(phone["international"])
            elif choice == "6":
                github_search(phone["international"])

            if choice in {"1", "2", "3", "4"}:
                print(f"\n{CYAN}{line('─')}{RESET}")
                save = input(f"{YELLOW}Save report? {RESET}{GREEN}(y){RESET}/{RED}(n){RESET} › ").strip().lower()
                if save == "y":
                    data = {
                        "timestamp": datetime.now().isoformat(),
                        "phone": phone,
                        "public_web": public_result or {"urls": {}, "status": {}},
                        "social": social_result or {"urls": {}, "status": {}}
                    }
                    save_report(data)

            input(f"\n{GRAY}Press Enter to return to main menu...{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Interrupted. Bye, Kayzen.{RESET}")


if __name__ == "__main__":
    main()
