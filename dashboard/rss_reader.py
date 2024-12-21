import tkinter as tk
from tkinter import scrolledtext, ttk
import feedparser
from datetime import datetime
import webbrowser
import threading
import copy

# Define RSS feed URLs
BLOOMBERG_RSS_FEED_URL = "https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en"
DOWJONES_RSS_FEED_URL = "https://feeds.content.dowjones.io/public/rss/mw_topstories"
MARKET_PULSE_RSS_FEED_URL = "https://feeds.content.dowjones.io/public/rss/mw_marketpulse"
REUTERS_RSS_FEED_URL = "https://rss.app/feeds/CFdRNLPWqNQpwihP.xml"
DBB_RSS_FEED_URL = "https://www.bundesbank.de/service/rss/de/633290/feed.rss"
ECB_USD_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/fxref-usd.html"
ECB_JPY_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/fxref-jpy.html"
ECB_BLOG_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/blog.html"
ECB_STATPRESS_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/statpress.html"
ECB_PRESS_RSS_FEED_URL = "https://www.ecb.europa.eu/rss/press.html"
EUSTAT_RSS_FEED_URL = "https://ec.europa.eu/eurostat/de/search?p_p_id=estatsearchportlet_WAR_estatsearchportlet&p_p_lifecycle=2&p_p_state=maximized&p_p_mode=view&p_p_resource_id=atom&_estatsearchportlet_WAR_estatsearchportlet_collection=CAT_EURNEW"
YAHOO_FINANCE_RSS = "https://www.yahoo.com/news/rss"
DEUTSCHE_BOERSE_RSS = "https://api.boerse-frankfurt.de/v1/feeds/news.rss"

# Investor's Business Insider feeds (IBD)
IBD_INVESTING_RSS = "https://feeds.feedburner.com/InvestingRss"
IBD_BUSINESS_RSS = "https://feeds.feedburner.com/BusinessRss"
IBD_ECONOMY_RSS = "https://feeds.feedburner.com/EconomyRss"

# Federal Reserve (FED)
FED_RSS = "https://www.federalreserve.gov/feeds/press_all.xml"

# Seeking Alpha (ALPHA)
ALPHA_RSS_1 = "https://seekingalpha.com/article/18-rss-feed-confusion"
ALPHA_RSS_2 = "https://seekingalpha.com/listing/most-popular-articles.xml"
ALPHA_RSS_3 = "https://seekingalpha.com/sector/financial.xml"
ALPHA_RSS_4 = "https://seekingalpha.com/api/sa/combined/TSLA.xml"
ALPHA_RSS_5 = "https://seekingalpha.com/api/sa/combined/AAPL.xml"
ALPHA_RSS_6 = "https://seekingalpha.com/feed.xml"

FEED_SOURCES = {
    "All": [
        BLOOMBERG_RSS_FEED_URL,
        DOWJONES_RSS_FEED_URL,
        MARKET_PULSE_RSS_FEED_URL,
        REUTERS_RSS_FEED_URL,
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
        IBD_ECONOMY_RSS,
        FED_RSS,
        ALPHA_RSS_1,
        ALPHA_RSS_2,
        ALPHA_RSS_3,
        ALPHA_RSS_4,
        ALPHA_RSS_5,
        ALPHA_RSS_6
    ],
    "Bloomberg": [BLOOMBERG_RSS_FEED_URL],
    "Dow Jones": [DOWJONES_RSS_FEED_URL],
    "Dow Jones - Market Pulse": [MARKET_PULSE_RSS_FEED_URL],
    "Reuters": [REUTERS_RSS_FEED_URL],
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
        IBD_ECONOMY_RSS
    ],
    "Federal Reserve": [FED_RSS],
    "Seeking Alpha": [
        ALPHA_RSS_1,
        ALPHA_RSS_2,
        ALPHA_RSS_3,
        ALPHA_RSS_4,
        ALPHA_RSS_5,
        ALPHA_RSS_6
    ],
}

ICON_PATH = r"C:\Users\Coneff\Desktop\images.ico"

HIGHLIGHT_KEYWORDS = ['Breaking', 'Bitcoin', 'Ethereum', 'Breaking News', 'Sharply', 'Steep Drop', 'Interest Rate', 'Hike', 'Jerome', 'Powell', 'Interest Rates']
HIGHLIGHT_SYNONYMS = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'Powell': 'Jerome Powell',
    'XET':'Ethereum',
    'XBT':'Bitcoin',
    'btc':'Bitcoin',
    'DE':'Germany',
    'GER':'Germany',
    'US':'United States',
    'USA':'United States',
    'United States':'USA',
    'US':'United States',
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

class RSSFeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSS News Feed Aggregator - TSONEVSKI TERMINAL")
        self.root.configure(bg="black")
        self.root.iconbitmap(ICON_PATH)

        self.original_feeds = copy.deepcopy(FEED_SOURCES)
        self.enabled_sources = copy.deepcopy(FEED_SOURCES)

        self.all_entries_cache = []

        self.timestamp_label = tk.Label(root, text="Last Refresh: Not updated yet", bg="black", fg="#FF9900", font=("Helvetica", 12))
        self.timestamp_label.pack(fill=tk.X, padx=10, pady=5)

        self.search_frame = tk.Frame(root, bg="black")
        self.search_frame.pack(fill=tk.X, padx=10, pady=5)

        # Define a custom style for comboboxes
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.TCombobox",
                        fieldbackground="#333333",
                        background="#333333",
                        foreground="#333333",
                        arrowcolor="#FF9900")

        tk.Label(self.search_frame, text="Keyword:", fg="#FF9900", bg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=30, font=("Helvetica", 12), bg="#333333", fg="#FF9900", insertbackground="#FF9900")
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.debounce(self.apply_filters, delay=300))
        self.search_entry.bind("<Control-BackSpace>", self.clear_search_field)

        tk.Label(self.search_frame, text="Source:", fg="#FF9900", bg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)

        self.source_var = tk.StringVar(value="All")
        self.source_dropdown = ttk.Combobox(self.search_frame, textvariable=self.source_var, values=list(self.enabled_sources.keys()),
                                            state="readonly", font=("Helvetica", 12), style="Custom.TCombobox")
        self.source_dropdown.pack(side=tk.LEFT)
        self.source_dropdown.bind("<<ComboboxSelected>>", lambda event: self.apply_filters())

        tk.Label(self.search_frame, text="Date:", fg="#FF9900", bg="black", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=10)
        self.date_var = tk.StringVar(value="All Dates")
        self.date_dropdown = ttk.Combobox(self.search_frame, textvariable=self.date_var, state="readonly", font=("Helvetica", 12),
                                          style="Custom.TCombobox")
        self.date_dropdown.pack(side=tk.LEFT)
        self.date_dropdown.bind("<<ComboboxSelected>>", lambda event: self.apply_filters())

        self.clear_button = tk.Button(self.search_frame, text="Clear All Filters", command=self.clear_filters, bg="black", fg="#FF9900", font=("Helvetica", 12))
        self.clear_button.pack(side=tk.LEFT, padx=10)

        self.sources_frame = tk.Frame(root, bg="black")
        self.sources_frame.pack(fill=tk.X, padx=10, pady=5)

        self.reset_sources_button = tk.Button(self.sources_frame, text="Reset Sources", command=self.reset_sources, bg="black", fg="#FF9900", font=("Helvetica", 12))
        self.reset_sources_button.pack(side=tk.LEFT, padx=5)

        self.bubbles_frame = tk.Frame(self.sources_frame, bg="black")
        self.bubbles_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.update_source_bubbles()

        self.feed_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=90, bg="black", fg="#FF9900", font=("Helvetica", 12), cursor="arrow")
        self.feed_display.pack(padx=10, pady=10)
        self.configure_tags()

        threading.Thread(target=self._background_load_feeds).start()
        self.auto_refresh()

    def configure_tags(self):
        self.feed_display.tag_configure("timestamp", foreground="#F0C04B", font=("Helvetica", 10))
        self.feed_display.tag_configure("date", foreground="#FFFFFF", font=("Helvetica", 10, "italic"))
        self.feed_display.tag_configure("headline", foreground="#FF9900", font=("Helvetica", 12))
        self.feed_display.tag_configure("clicked", foreground="gray", font=("Helvetica", 12))
        self.feed_display.tag_configure("source_bbg", foreground="#B22222", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_dowj", foreground="#FF4500", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_djpulse", foreground="#D2691E", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_reuters", foreground="#0071B6", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_dbb", foreground="#8A2BE2", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_ecb", foreground="#32CD32", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_eustat", foreground="#FFD700", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_yf", foreground="#1E90FF", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_db", foreground="#2F4F4F", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_ibd", foreground="#FF69B4", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_fed", foreground="#800000", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("source_alpha", foreground="#8B4513", font=("Helvetica", 10, "bold"))
        self.feed_display.tag_configure("highlight", foreground="yellow", font=("Helvetica", 12, "bold"))

    def update_source_bubbles(self):
        for widget in self.bubbles_frame.winfo_children():
            widget.destroy()

        for src in self.enabled_sources:
            if src == "All":
                continue
            bubble = tk.Frame(self.bubbles_frame, bg="gray", bd=1, relief="solid")
            bubble.pack(side=tk.LEFT, padx=2)
            tk.Label(bubble, text=src, font=("Helvetica", 10), bg="gray", fg="black").pack(side=tk.LEFT, padx=5)
            tk.Button(bubble, text="X", command=lambda s=src: self.remove_source(s), font=("Helvetica", 8), fg="black").pack(side=tk.RIGHT, padx=2)

    def remove_source(self, source_name):
        if source_name in self.enabled_sources:
            del self.enabled_sources[source_name]
            self.rebuild_all_source()
            self.source_dropdown["values"] = list(self.enabled_sources.keys())
            if self.source_var.get() not in self.enabled_sources:
                self.source_var.set("All")
            self.update_source_bubbles()
            self.apply_filters()

    def rebuild_all_source(self):
        all_urls = []
        for k, v in self.enabled_sources.items():
            if k != "All":
                all_urls.extend(v)
        self.enabled_sources["All"] = all_urls

    def reset_sources(self):
        self.enabled_sources = copy.deepcopy(self.original_feeds)
        self.update_source_bubbles()
        self.source_dropdown["values"] = list(self.enabled_sources.keys())
        self.source_var.set("All")
        self.apply_filters()

    def clear_search_field(self, event):
        self.search_entry.delete(0, tk.END)
        self.apply_filters()

    def auto_refresh(self):
        self.root.after(5000, self.refresh_feeds)

    def refresh_feeds(self):
        threading.Thread(target=self._background_load_feeds).start()
        self.auto_refresh()

    def _background_load_feeds(self):
        new_cache = {}
        for source, urls in self.enabled_sources.items():
            if source == "All":
                continue
            for url in urls:
                for entry in self.get_feed_entries(url):
                    new_cache[entry["link"]] = entry
        self.all_entries_cache = list(new_cache.values())
        self.root.after(0, self._update_ui_after_load)

    def _update_ui_after_load(self):
        self.update_refresh_timestamp()
        self.apply_filters()

    def debounce(self, func, delay):
        def debounced(event=None):
            if hasattr(self, "_debounce_id"):
                self.root.after_cancel(self._debounce_id)
            self._debounce_id = self.root.after(delay, func)
        return debounced

    def update_refresh_timestamp(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Last Refresh: {current_time}")

    def clear_filters(self):
        self.search_entry.delete(0, tk.END)
        self.source_var.set("All")
        self.date_var.set("All Dates")
        self.apply_filters()

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%m/%d")
        except ValueError:
            return datetime.now()

    def apply_filters(self):
        keyword = self.search_entry.get().lower()
        if keyword.upper() in HIGHLIGHT_SYNONYMS:
            keyword = HIGHLIGHT_SYNONYMS[keyword.upper()]

        selected_source = self.source_var.get()
        selected_date = self.date_var.get()

        filtered_entries = self.all_entries_cache
        if selected_source != "All":
            filtered_entries = [entry for entry in filtered_entries if entry["source"] == selected_source]

        if selected_date != "All Dates":
            filtered_entries = [entry for entry in filtered_entries if entry["date"] == selected_date]

        if keyword:
            filtered_entries = [entry for entry in filtered_entries if keyword.lower() in entry["title"].lower()]

        # Always sort newest first (descending)
        filtered_entries.sort(key=lambda x: (
            self.parse_date(x["date"]),
            datetime.strptime(x["published"], "%H:%M:%S")
        ), reverse=True)

        unique_dates = sorted({entry["date"] for entry in self.all_entries_cache}, key=lambda d: self.parse_date(d), reverse=True)
        self.date_dropdown["values"] = ["All Dates"] + unique_dates

        self.display_feed(filtered_entries)

    def get_feed_entries(self, url):
        feed = feedparser.parse(url)
        entries = []
        for entry in feed.entries:
            published_struct = getattr(entry, "published_parsed", None) or getattr(entry, "updated_parsed", None)
            if published_struct:
                published_time = datetime(*published_struct[:6]).strftime("%H:%M:%S")
                published_date = datetime(*published_struct[:6]).strftime("%m/%d")
            else:
                published_str = getattr(entry, "published", None) or getattr(entry, "updated", None)
                if published_str:
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

            # Determine ticker
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
                ticker_name = "Reuters"

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

    def display_feed(self, entries):
        old_view = self.feed_display.yview()
        at_top = (old_view[0] == 0.0)

        self.feed_display.delete(1.0, tk.END)
        for entry in entries:
            tag_name = f"source_{entry['ticker'].lower().replace(' ', '_')}"
            self.feed_display.insert(tk.END, f"{entry['date']} ", "date")
            self.feed_display.insert(tk.END, f"[{entry['published']}] ", "timestamp")
            self.feed_display.insert(tk.END, f"{entry['ticker']} ", tag_name)

            headline_start = self.feed_display.index(tk.INSERT)
            self.feed_display.insert(tk.END, f"{entry['title']}\n", "headline")
            self.apply_highlight(headline_start, entry['title'])

            self.feed_display.tag_add(entry["link"], headline_start, self.feed_display.index(tk.INSERT))
            self.feed_display.tag_bind(entry["link"], "<Enter>", lambda e: self.on_mouseover())
            self.feed_display.tag_bind(entry["link"], "<Leave>", lambda e: self.on_mouseleave())
            self.feed_display.tag_bind(entry["link"], "<ButtonRelease-1>", lambda e, url=entry["link"], tag=entry["link"]: self.open_link(url, tag))
            self.feed_display.insert(tk.END, "-" * 80 + "\n", "default")

        if at_top:
            self.feed_display.see("1.0")
        else:
            self.feed_display.yview_moveto(old_view[0])

    def apply_highlight(self, start_index, text):
        keywords = HIGHLIGHT_KEYWORDS + list(HIGHLIGHT_SYNONYMS.values())
        for keyword in keywords:
            start_pos = text.lower().find(keyword.lower())
            while start_pos != -1:
                end_pos = start_pos + len(keyword)
                start = f"{start_index}+{start_pos}c"
                end = f"{start_index}+{end_pos}c"
                self.feed_display.tag_add("highlight", start, end)
                start_pos = text.lower().find(keyword.lower(), end_pos)

    def open_link(self, url, tag):
        webbrowser.open(url)
        self.feed_display.tag_configure(tag, foreground="gray", underline=False)

    def on_mouseover(self):
        self.feed_display.config(cursor="hand2")

    def on_mouseleave(self):
        self.feed_display.config(cursor="arrow")

def main():
    root = tk.Tk()
    app = RSSFeedApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
