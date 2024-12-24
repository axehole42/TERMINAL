from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from django.templatetags.static import static
import feedparser
from django.shortcuts import render
from django.utils import timezone
import feedparser
from datetime import datetime
import copy
from django.http import JsonResponse
import re
from django.core.cache import cache
from .synonyms_stocks import STOCK_SYNONYMS

def home(request):
    if request.user.is_authenticated:
        # Show personalized dashboard for logged-in users
        context = {
            'username': request.user.username,
            'description': 'Welcome to your customizable dashboard!',
            'stream_url': static('dashboard/videos/phoenix-us.m3u8'),  # Replace with your stream URL
        }
        return render(request, 'dashboard/home.html', context)
    else:
        # Show registration form for unauthenticated users
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                login(request, user)  # Automatically log in the user
                return redirect('home')  # Redirect to the dashboard
        else:
            form = RegistrationForm()
        
        # Show a general welcome message and the registration form
        context = {
            'welcome_message': 'Welcome to the Tsonevski Terminal.',
            'info_message': (
                "To access the terminal's advanced features, please "
                "<a href='/login/'>log in</a> or "
                "<a href='/register/'>register</a> for an account."
            ),
            'form': form,
        }
        return render(request, 'dashboard/home.html', context)

# Create your views here.
def about_page(request):
    return render(request, 'dashboard/about.html')

# Our login page function.
def register(request):
    print("Register view called")  # Debug statement
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('home')  # Redirect to the home page
    else:
        form = RegistrationForm()
    return render(request, 'dashboard/register.html', {'form': form, 'content_container': False})

def profile(request):
    return render(request, 'dashboard/profile.html')


# ---------------
# Configuration for the RSS Reader
# ---------------
BLOOMBERG_RSS_FEED_URL = "https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en"
DOWJONES_RSS_FEED_URL = "https://feeds.content.dowjones.io/public/rss/mw_topstories"
MARKET_PULSE_RSS_FEED_URL = "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"
DBB_RSS_FEED_URL = "https://www.bundesbank.de/service/rss/de/633290/feed.rss"
ECB_USD_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/fxref-usd.html"
ECB_JPY_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/fxref-jpy.html"
ECB_BLOG_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/blog.html"
ECB_STATPRESS_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/statpress.html"
ECB_PRESS_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/press.html"
EUSTAT_RSS_FEED_URL = "https://ec.europa.eu/eurostat/de/search?p_p_id=estatsearchportlet_WAR_estatsearchportlet&p_p_lifecycle=2&p_p_state=maximized&p_p_mode=view&p_p_resource_id=atom&_estatsearchportlet_WAR_estatsearchportlet_collection=CAT_EURNEW"
YAHOO_FINANCE_RSS = "https://www.yahoo.com/news/rss"
DEUTSCHE_BOERSE_RSS = "https://api.boerse-frankfurt.de/v1/feeds/news.rss"

IBD_INVESTING_RSS = "https://feeds.feedburner.com/InvestingRss"
IBD_BUSINESS_RSS = "https://feeds.feedburner.com/BusinessRss"

FED_RSS = "https://www.federalreserve.gov/feeds/press_all.xml"

ALPHA_RSS_1 = "https://seekingalpha.com/article/18-rss-feed-confusion"
ALPHA_RSS_2 = "https://seekingalpha.com/listing/most-popular-articles.xml"
ALPHA_RSS_3 = "https://seekingalpha.com/sector/financial.xml"
ALPHA_RSS_4 = "https://seekingalpha.com/api/sa/combined/TSLA.xml"
ALPHA_RSS_5 = "https://seekingalpha.com/api/sa/combined/AAPL.xml"
ALPHA_RSS_6 = "https://seekingalpha.com/feed.xml"

# US Stocks---------------------------------------------------

ALPHA_RSS_7 = "https://seekingalpha.com/api/sa/combined/MSFT.xml"  # Microsoft
ALPHA_RSS_8 = "https://seekingalpha.com/api/sa/combined/GOOGL.xml" # Alphabet (Google)
ALPHA_RSS_9 = "https://seekingalpha.com/api/sa/combined/AMZN.xml"  # Amazon
ALPHA_RSS_10 = "https://seekingalpha.com/api/sa/combined/AMD.xml"  # AMD
ALPHA_RSS_11 = "https://seekingalpha.com/api/sa/combined/NVDA.xml" # NVIDIA
ALPHA_RSS_12 = "https://seekingalpha.com/api/sa/combined/INTC.xml" # Intel
ALPHA_RSS_13 = "https://seekingalpha.com/api/sa/combined/FB.xml"   # Meta Platforms (Facebook)
ALPHA_RSS_14 = "https://seekingalpha.com/api/sa/combined/JPM.xml"  # JPMorgan Chase
ALPHA_RSS_15 = "https://seekingalpha.com/api/sa/combined/GS.xml"   # Goldman Sachs
ALPHA_RSS_16 = "https://seekingalpha.com/api/sa/combined/C.xml"    # Citigroup
ALPHA_RSS_17 = "https://seekingalpha.com/api/sa/combined/BA.xml"   # Boeing (Defense, Aerospace)
ALPHA_RSS_18 = "https://seekingalpha.com/api/sa/combined/LMT.xml"  # Lockheed Martin (Defense)
ALPHA_RSS_19 = "https://seekingalpha.com/api/sa/combined/NOC.xml"  # Northrop Grumman (Defense)
ALPHA_RSS_20 = "https://seekingalpha.com/api/sa/combined/F.xml"    # Ford (Autos)
ALPHA_RSS_21 = "https://seekingalpha.com/api/sa/combined/GM.xml"   # General Motors (Autos)
ALPHA_RSS_22 = "https://seekingalpha.com/api/sa/combined/TSLA.xml" # Tesla (Autos)
ALPHA_RSS_23 = "https://seekingalpha.com/api/sa/combined/COST.xml" # Costco (Consumer)
ALPHA_RSS_24 = "https://seekingalpha.com/api/sa/combined/WMT.xml"  # Walmart (Consumer)
ALPHA_RSS_25 = "https://seekingalpha.com/api/sa/combined/KO.xml"   # Coca-Cola (Consumer)
ALPHA_RSS_26 = "https://seekingalpha.com/api/sa/combined/PG.xml"   # Procter & Gamble (Consumer)
ALPHA_RSS_27 = "https://seekingalpha.com/api/sa/combined/DD.xml"   # DuPont (Chemicals)
ALPHA_RSS_28 = "https://seekingalpha.com/api/sa/combined/DOW.xml"  # Dow (Chemicals)
ALPHA_RSS_29 = "https://seekingalpha.com/api/sa/combined/CLF.xml"  # Cleveland-Cliffs (Materials)
ALPHA_RSS_30 = "https://seekingalpha.com/api/sa/combined/CVX.xml"  # Chevron (Energy)
ALPHA_RSS_31 = "https://seekingalpha.com/api/sa/combined/XOM.xml"  # Exxon Mobil (Energy)
ALPHA_RSS_32 = "https://seekingalpha.com/api/sa/combined/SBUX.xml" # Starbucks (Consumer)
ALPHA_RSS_33 = "https://seekingalpha.com/api/sa/combined/MCD.xml"  # McDonald's (Consumer)
ALPHA_RSS_34 = "https://seekingalpha.com/api/sa/combined/NKE.xml"  # Nike (Consumer)
ALPHA_RSS_35 = "https://seekingalpha.com/api/sa/combined/HD.xml"   # Home Depot (Consumer)


# European Stocks---------------------------------------------------
ALPHA_RSS_34 = "https://seekingalpha.com/api/sa/combined/SAP.xml"  # SAP (Germany, Tech)
ALPHA_RSS_35 = "https://seekingalpha.com/api/sa/combined/ASML.xml" # ASML (Netherlands, Tech)
ALPHA_RSS_36 = "https://seekingalpha.com/api/sa/combined/UBS.xml"  # UBS (Switzerland, Banking)
ALPHA_RSS_37 = "https://seekingalpha.com/api/sa/combined/CS.xml"   # Credit Suisse (Switzerland, Banking)
ALPHA_RSS_38 = "https://seekingalpha.com/api/sa/combined/BARC.xml" # Barclays (UK, Banking)
ALPHA_RSS_39 = "https://seekingalpha.com/api/sa/combined/RYAAY.xml" # Ryanair (Ireland, Consumer)
ALPHA_RSS_40 = "https://seekingalpha.com/api/sa/combined/DAI.xml"  # Daimler (Germany, Autos)
ALPHA_RSS_41 = "https://seekingalpha.com/api/sa/combined/BMW.xml"  # BMW (Germany, Autos)
ALPHA_RSS_42 = "https://seekingalpha.com/api/sa/combined/VOW3.xml" # Volkswagen (Germany, Autos)
ALPHA_RSS_43 = "https://seekingalpha.com/api/sa/combined/ORCL.xml" # Oracle (France, Consumer)
ALPHA_RSS_44 = "https://seekingalpha.com/api/sa/combined/LVMH.xml" # LVMH (France, Consumer)
ALPHA_RSS_45 = "https://seekingalpha.com/api/sa/combined/RNO.xml"  # Renault (France, Autos)
ALPHA_RSS_46 = "https://seekingalpha.com/api/sa/combined/AIR.xml"  # Airbus (France, Aerospace/Defense)
ALPHA_RSS_47 = "https://seekingalpha.com/api/sa/combined/BNP.xml"  # BNP Paribas (France, Banking)
ALPHA_RSS_48 = "https://seekingalpha.com/api/sa/combined/ING.xml"  # ING (Netherlands, Banking)
ALPHA_RSS_49 = "https://seekingalpha.com/api/sa/combined/GLEN.xml" # Glencore (UK, Materials)
ALPHA_RSS_50 = "https://seekingalpha.com/api/sa/combined/BASF.xml" # BASF (Germany, Chemicals)
ALPHA_RSS_51 = "https://seekingalpha.com/api/sa/combined/BAYN.xml" # Bayer (Germany, Chemicals)
ALPHA_RSS_52 = "https://seekingalpha.com/api/sa/combined/SIEGY.xml" # Siemens (Germany, Industrial)
ALPHA_RSS_53 = "https://seekingalpha.com/api/sa/combined/ADBE.xml"  # Adobe (US, Tech)

FEED_SOURCES = {
    "All": [
        BLOOMBERG_RSS_FEED_URL,
        DOWJONES_RSS_FEED_URL,
        MARKET_PULSE_RSS_FEED_URL,
        DBB_RSS_FEED_URL,
        ECB_USD_RSS_FEED_URL,
        ECB_JPY_RSS_FEED_URL,
        ECB_BLOG_RSS_FEED_URL,
        ECB_STATPRESS_RSS_FEED_URL,
        ECB_PRESS_RSS_FEED_URL,
        EUSTAT_RSS_FEED_URL,
        YAHOO_FINANCE_RSS,
        DEUTSCHE_BOERSE_RSS,
        IBD_INVESTING_RSS,
        IBD_BUSINESS_RSS,
        FED_RSS,
        
        ALPHA_RSS_1,
        ALPHA_RSS_2,
        ALPHA_RSS_3,
        ALPHA_RSS_4,
        ALPHA_RSS_5,
        ALPHA_RSS_6,
        ALPHA_RSS_3,
        ALPHA_RSS_4,
        ALPHA_RSS_5,
        ALPHA_RSS_6,
        ALPHA_RSS_7,

        #US STOCKS---------------------------------------------------

        ALPHA_RSS_8,
        ALPHA_RSS_9,
        ALPHA_RSS_10,
        ALPHA_RSS_11,
        ALPHA_RSS_12,
        ALPHA_RSS_13,
        ALPHA_RSS_14,
        ALPHA_RSS_15,
        ALPHA_RSS_16,
        ALPHA_RSS_17,
        ALPHA_RSS_18,
        ALPHA_RSS_19,
        ALPHA_RSS_20,
        ALPHA_RSS_21,
        ALPHA_RSS_22,
        ALPHA_RSS_23,
        ALPHA_RSS_24,
        ALPHA_RSS_25,
        ALPHA_RSS_26,
        ALPHA_RSS_27,
        ALPHA_RSS_28,
        ALPHA_RSS_29,
        ALPHA_RSS_30,
        ALPHA_RSS_31,
        ALPHA_RSS_32,
        ALPHA_RSS_33,

        #EUROPEAN STOCKS---------------------------------------------------

        ALPHA_RSS_34,
        ALPHA_RSS_35,
        ALPHA_RSS_36,
        ALPHA_RSS_37,
        ALPHA_RSS_38,
        ALPHA_RSS_39,
        ALPHA_RSS_40,
        ALPHA_RSS_41,
        ALPHA_RSS_42,
        ALPHA_RSS_43,
        ALPHA_RSS_44,
        ALPHA_RSS_45,
        ALPHA_RSS_46,
        ALPHA_RSS_47,
        ALPHA_RSS_48,
        ALPHA_RSS_49,
        ALPHA_RSS_50,
        ALPHA_RSS_51,
        ALPHA_RSS_52,
        ALPHA_RSS_53



    ],
    "Bloomberg": [BLOOMBERG_RSS_FEED_URL],
    "Dow Jones": [DOWJONES_RSS_FEED_URL],
    "Dow Jones - Market Pulse": [MARKET_PULSE_RSS_FEED_URL],
    "Deutsche Bundesbank": [DBB_RSS_FEED_URL],
    "European Central Bank": [
        ECB_USD_RSS_FEED_URL,
        ECB_JPY_RSS_FEED_URL,
        ECB_BLOG_RSS_FEED_URL,
        ECB_STATPRESS_RSS_FEED_URL,
        ECB_PRESS_RSS_FEED_URL
    ],
    "EUROSTAT": [EUSTAT_RSS_FEED_URL],
    "Yahoo Finance": [YAHOO_FINANCE_RSS],
    "Deutsche Boerse": [DEUTSCHE_BOERSE_RSS],
    "Investor's Business Insider": [
        IBD_INVESTING_RSS,
        IBD_BUSINESS_RSS,
    ],
    "Federal Reserve": [FED_RSS],
    "Seeking Alpha": [
        ALPHA_RSS_3,
        ALPHA_RSS_4,
        ALPHA_RSS_5,
        ALPHA_RSS_6,
        ALPHA_RSS_7,
        ALPHA_RSS_8,
        ALPHA_RSS_9,
        ALPHA_RSS_10,
        ALPHA_RSS_11,
        ALPHA_RSS_12,
        ALPHA_RSS_13,
        ALPHA_RSS_14,
        ALPHA_RSS_15,
        ALPHA_RSS_16,
        ALPHA_RSS_17,
        ALPHA_RSS_18,
        ALPHA_RSS_19,
        ALPHA_RSS_20,
        ALPHA_RSS_21,
        ALPHA_RSS_22,
        ALPHA_RSS_23,
        ALPHA_RSS_24,
        ALPHA_RSS_25,
        ALPHA_RSS_26,
        ALPHA_RSS_27,
        ALPHA_RSS_28,
        ALPHA_RSS_29,
        ALPHA_RSS_30,
        ALPHA_RSS_31,
        ALPHA_RSS_32,
        ALPHA_RSS_33,
        ALPHA_RSS_34,
        ALPHA_RSS_35,
        ALPHA_RSS_36,
        ALPHA_RSS_37,
        ALPHA_RSS_38,
        ALPHA_RSS_39,
        ALPHA_RSS_40,
        ALPHA_RSS_41,
        ALPHA_RSS_42,
        ALPHA_RSS_43,
        ALPHA_RSS_44,
        ALPHA_RSS_45,
        ALPHA_RSS_46,
        ALPHA_RSS_47,
        ALPHA_RSS_48,
        ALPHA_RSS_49,
        ALPHA_RSS_50,
        ALPHA_RSS_51,
        ALPHA_RSS_52,
        ALPHA_RSS_53

    ],
}

HIGHLIGHT_KEYWORDS = [
    'Breaking', 'Bitcoin', 'Ethereum', 'Breaking News',
    'Sharply', 'Steep Drop', 'Interest Rate', 'Hike', 'Jerome', 'Powell', 'Interest Rates'
]
HIGHLIGHT_SYNONYMS = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'Powell': 'Jerome Powell',
    'XET': 'Ethereum',
    'XBT': 'Bitcoin',
    'btc': 'Bitcoin',
    'DE': 'Germany',
    'GER': 'Germany',
    'US': 'United States',
    'USA': 'United States',
    'United States': 'USA',
}

TICKER_TO_SOURCE = {
    "BBG": "Bloomberg",
    "DOWJ": "Dow Jones",
    "Dow Jones - Market Pulse": "Dow Jones - Market Pulse",
    "Reuters": "Reuters",
    "DBB": "Deutsche Bundesbank",
    "ECB": "European Central Bank",
    "EUSTAT": "EUROSTAT",
    "YF": "Yahoo Finance",
    "DB": "Deutsche Boerse",
    "IBD": "Investor's Business Insider",
    "FED": "Federal Reserve",
    "ALPHA": "Seeking Alpha"
}

SOURCE_COLORS = {
    "BBG": "#B22222",               # Bloomberg (FireBrick)
    "DOWJ": "#FF4500",              # Dow Jones (OrangeRed)
    "Dow Jones - Market Pulse": "#D2691E",
    "Reuters": "#0071B6",
    "DBB": "#8A2BE2",               # Deutsche Bundesbank (BlueViolet)
    "ECB": "#32CD32",               # European Central Bank (LimeGreen)
    "EUSTAT": "#FFD700",
    "YF": "#1E90FF",                # Yahoo Finance (DodgerBlue)
    "DB": "#2F4F4F",                # Deutsche Boerse (DarkSlateGray)
    "IBD": "#FF69B4",               # Investor's Business Daily (HotPink)
    "FED": "#800000",               # Federal Reserve (Maroon)
    "ALPHA": "#228B22",             # Seeking Alpha (SaddleBrown)
}


# A simple module-level cache to store feed entries (you may replace with Redis, database, etc.)
ALL_ENTRIES_CACHE = []
LAST_FETCH_TIME = None

def parse_date(date_str):
    """
    Convert 'mm/dd' to a Python datetime date for sorting.
    Fallback to current date/time if parse fails.
    """
    try:
        return datetime.strptime(date_str, "%m/%d")
    except ValueError:
        return datetime.now()

def get_feed_entries(url):
    """
    Parse a single RSS feed URL and return a list of normalized entries.
    Similar logic to your Tkinter code.
    """
    feed = feedparser.parse(url)
    entries = []

    for entry in feed.entries:
        published_struct = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
        if published_struct:
            published_time = datetime(*published_struct[:6]).strftime("%H:%M:%S")
            published_date = datetime(*published_struct[:6]).strftime("%m/%d")
        else:
            # fallback if no structured date is found
            published_str = getattr(entry, "published", None) or getattr(entry, "updated", None)
            if published_str:
                # try to parse as ISO8601
                try:
                    iso_time = datetime.strptime(published_str, "%Y-%m-%dT%H:%M:%SZ")
                    published_time = iso_time.strftime("%H:%M:%S")
                    published_date = iso_time.strftime("%m/%d")
                except ValueError:
                    published_time = datetime.now().strftime("%H:%M:%S")
                    published_date = datetime.now().strftime("%m/%d")
            else:
                published_time = datetime.now().strftime("%H:%M:%S")
                published_date = datetime.now().strftime("%m/%d")

        # Determine ticker based on URL
        if "yahoo.com" in url:
            ticker_name = "YF"
        elif "boerse-frankfurt.de" in url:
            ticker_name = "DB"
        elif "bundesbank" in url:
            ticker_name = "DBB"
        elif "ecb.europa.eu" in url:
            ticker_name = "ECB"
        elif "eurostat" in url:
            ticker_name = "EUSTAT"
        elif "bloomberg" in url:
            ticker_name = "BBG"
        elif "dowjones" in url and "marketpulse" not in url:
            ticker_name = "DOWJ"
        elif "marketpulse" in url:
            ticker_name = "Dow Jones - Market Pulse"
        elif "feedburner.com" in url:
            ticker_name = "IBD"
        elif "federalreserve.gov" in url:
            ticker_name = "FED"
        elif "seekingalpha.com" in url:
            ticker_name = "ALPHA"
        else:
            ticker_name = "Reuters"  # fallback

        friendly_source = TICKER_TO_SOURCE.get(ticker_name, ticker_name)

        entries.append({
            "title": entry.title,
            "link": entry.link,
            "published": published_time,
            "date": published_date,
            "source": friendly_source,
            "ticker": ticker_name
        })

    return entries

def fetch_all_feeds():
    """
    Rebuilds the ALL_ENTRIES_CACHE by fetching all enabled RSS sources except "All".
    """
    new_cache = {}
    # For each source and URL
    for source, urls in FEED_SOURCES.items():
        if source == "All":
            continue
        for url in urls:
            feed_items = get_feed_entries(url)
            for item in feed_items:
                # Use 'link' as a unique key
                new_cache[item["link"]] = item
    return list(new_cache.values())

def highlight_text(text):
    """
    Insert <span> for highlight keywords.
    DOES NOT rewrite synonyms; headlines remain as-is.
    """
    # e.g. from your existing code
    all_words = set(HIGHLIGHT_KEYWORDS + list(HIGHLIGHT_SYNONYMS.values()))
    highlighted = text
    for kw in sorted(all_words, key=len, reverse=True):
        highlighted = highlighted.replace(
            kw, f"<span class='highlight'>{kw}</span>"
        )
    return highlighted


def get_feed_entries(url):
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        published_struct = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
        if published_struct:
            pub_time = datetime(*published_struct[:6]).strftime("%H:%M:%S")
            pub_date = datetime(*published_struct[:6]).strftime("%m/%d")
        else:
            pub_str = getattr(entry, "published", None) or getattr(entry, "updated", None)
            if pub_str:
                try:
                    iso_time = datetime.strptime(pub_str, "%Y-%m-%dT%H:%M:%SZ")
                    pub_time = iso_time.strftime("%H:%M:%S")
                    pub_date = iso_time.strftime("%m/%d")
                except ValueError:
                    pub_time = datetime.now().strftime("%H:%M:%S")
                    pub_date = datetime.now().strftime("%m/%d")
            else:
                pub_time = datetime.now().strftime("%H:%M:%S")
                pub_date = datetime.now().strftime("%m/%d")

        # Determine ticker
        if "yahoo.com" in url:
            ticker = "YF"
        elif "boerse-frankfurt.de" in url:
            ticker = "DB"
        elif "bundesbank" in url:
            ticker = "DBB"
        elif "ecb.europa.eu" in url:
            ticker = "ECB"
        elif "eurostat" in url:
            ticker = "EUSTAT"
        elif "bloomberg" in url:
            ticker = "BBG"
        elif "dowjones" in url and "marketpulse" not in url:
            ticker = "DOWJ"
        elif "marketpulse" in url:
            ticker = "Dow Jones - Market Pulse"
        elif "feedburner.com" in url:
            ticker = "IBD"
        elif "federalreserve.gov" in url:
            ticker = "FED"
        elif "seekingalpha.com" in url:
            ticker = "ALPHA"
        else:
            ticker = "Reuters"

        friendly_source = TICKER_TO_SOURCE.get(ticker, ticker)

        items.append({
            "title": entry.title,
            "link": entry.link,
            "published": pub_time,
            "date": pub_date,
            "source": friendly_source,
            "ticker": ticker
        })
    return items

def fetch_all_feeds():
    """
    Build the ALL_ENTRIES_CACHE by fetching all FEED_SOURCES (except 'All') 
    and merging them into a single list.
    """
    new_cache = {}
    for source, urls in FEED_SOURCES.items():
        if source == "All":
            continue
        for url in urls:
            for item in get_feed_entries(url):
                new_cache[item["link"]] = item
    return list(new_cache.values())

def parse_date_mmdd(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d")
    except ValueError:
        return datetime.now()

def entry_datetime(e):
    d = parse_date_mmdd(e["date"])
    try:
        t = datetime.strptime(e["published"], "%H:%M:%S").time()
        return datetime(d.year, d.month, d.day, t.hour, t.minute, t.second)
    except ValueError:
        return d

# ========== NEW: A cached version of fetch_all_feeds ==========
def fetch_all_feeds_cached():
    """
    Check if we have 'rss_data' in cache. If so, return it.
    Otherwise, call fetch_all_feeds() and cache it for 60 seconds (1 minute).
    """
    cached_data = cache.get("rss_data")
    if cached_data is not None:
        return cached_data
    
    # Not in cache -> do the full fetch
    new_data = fetch_all_feeds()
    # store in cache for 60s
    cache.set("rss_data", new_data, 60)
    return new_data

# ------------------------------
# The main RSS feed view
# ------------------------------
def rss_feed(request):
    global ALL_ENTRIES_CACHE, LAST_FETCH_TIME

    # Instead of fetch_all_feeds(), we use our cached version
    ALL_ENTRIES_CACHE = fetch_all_feeds_cached()
    LAST_FETCH_TIME = timezone.now()

    filtered_entries = ALL_ENTRIES_CACHE
    filtered_entries.sort(key=lambda e: entry_datetime(e), reverse=True)

    for e in filtered_entries:
        e["title_highlighted"] = highlight_text(e["title"])
        e["source_color"] = SOURCE_COLORS.get(e["ticker"], "#FF9900")

    unique_dates = sorted(
        {x["date"] for x in ALL_ENTRIES_CACHE},
        key=lambda d: parse_date_mmdd(d),
        reverse=True
    )

    context = {
        "entries": filtered_entries,
        "feed_sources": list(FEED_SOURCES.keys()),  
        "unique_dates": ["All Dates"] + unique_dates,
        "selected_source": "All",
        "selected_date": "All Dates",
        "keyword": "",
        "last_fetch_time": LAST_FETCH_TIME,
    }
    return render(request, "dashboard/rss_feed.html", context)

# ------------------------------
# The JSON endpoint for filtering
# ------------------------------
def rss_feed_json(request):
    global ALL_ENTRIES_CACHE, LAST_FETCH_TIME

    ALL_ENTRIES_CACHE = fetch_all_feeds_cached()
    LAST_FETCH_TIME = timezone.now()

    selected_source = request.GET.get("source", "All")
    keyword = request.GET.get("keyword", "").strip()
    date_filter = request.GET.get("date", "All Dates")
    enabled_sources_str = request.GET.get("enabled_sources", "")

    # parse ribbon sources
    if enabled_sources_str:
        enabled_sources_list = enabled_sources_str.split("|")
    else:
        enabled_sources_list = [
            "Bloomberg", "Dow Jones", "Dow Jones - Market Pulse",
            "Reuters", "Deutsche Bundesbank", "European Central Bank",
            "EUROSTAT", "Yahoo Finance", "Deutsche Boerse",
            "Investor's Business Insider", "Federal Reserve", "Seeking Alpha"
        ]

    filtered_entries = ALL_ENTRIES_CACHE
    # 1) Filter by enabled
    filtered_entries = [x for x in filtered_entries if x["source"] in enabled_sources_list]

    # 2) Source
    if selected_source != "All":
        filtered_entries = [x for x in filtered_entries if x["source"] == selected_source]

    # 3) Date
    if date_filter != "All Dates":
        filtered_entries = [x for x in filtered_entries if x["date"] == date_filter]

    # 4) Synonym logic for searching
    # if the user typed e.g. 'tsla', we want to match articles containing
    # 'tsla' OR 'tesla'
    if keyword:
        # e.g. user typed 'TSLA'
        upper_kw = keyword.upper()
        # We check if the user-typed string is in STOCK_SYNONYMS
        # If yes, we do a 2-way search:
        #   (a) the original typed string (like "tsla")
        #   (b) the synonyms library result (like "Tesla")
        # e.g. synonyms_stocks["TSLA"] = "Tesla"
        alt_syn = None
        if upper_kw in STOCK_SYNONYMS:
            alt_syn = STOCK_SYNONYMS[upper_kw]

        # We'll filter if e["title"].lower() contains kw_lower OR alt_syn
        kw_lower = keyword.lower()

        def match_article(article_title):
            t = article_title.lower()
            if kw_lower in t:
                return True
            if alt_syn:
                # alt_syn might be "Tesla" -> we also check "tesla" in t
                if alt_syn.lower() in t:
                    return True
            return False

        filtered_entries = [x for x in filtered_entries if match_article(x["title"])]

    # 5) sort
    filtered_entries.sort(key=lambda e: entry_datetime(e), reverse=True)

    # 6) highlight & color
    for e in filtered_entries:
        e["title_highlighted"] = highlight_text(e["title"])
        e["source_color"] = SOURCE_COLORS.get(e["ticker"], "#FF9900")

    data = {
        "last_fetch_time": LAST_FETCH_TIME.strftime("%Y-%m-%d %H:%M:%S"),
        "entries": filtered_entries,
    }
    return JsonResponse(data, safe=False)