"""Build index.html for Cabaña 28. Run: python _src/build.py"""
import html
import json
from pathlib import Path

from menu import MENU

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://samirawad24.github.io/cabana28-site/"
PICKUP = "https://food.orders.co/cabaa28"
DOORDASH = "https://www.doordash.com/store/cabana28-fort-lauderdale-25130447/"
UBER = "https://www.ubereats.com/store/cabana-28/YuIAFhCmWMiQWB06PUECMw"
GOOGLE = "https://www.google.com/maps/search/?api=1&query=Caba%C3%B1a+28+6351+N+Andrews+Ave+Fort+Lauderdale"
TEL = "tel:+19545305123"
PHONE = "(954) 530-5123"

HOURS = [  # (label, days for schema, open, close)
    ("Monday to Friday", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "10:30", "21:00"),
    ("Saturday", ["Saturday"], "10:15", "21:00"),
    ("Sunday", ["Sunday"], "10:15", "20:00"),
]

e = html.escape


def money(p):
    return f"${p:,.2f}"


def build_menu():
    tabs, sections = [], []
    for slug, es, en, note, items in MENU:
        tabs.append(f'<a href="#m-{slug}" data-tab="{slug}">{e(en)}</a>')
        rows = []
        for name, desc, price, popular in items:
            fav = '<span class="fav">House favorite</span>' if popular else ""
            p = money(price) if price is not None else f'<a href="{PICKUP}" class="opts">Options</a>'
            d = f'<p class="dish-desc">{e(desc)}</p>' if desc else ""
            rows.append(
                f'<li class="dish" data-search="{e((name + " " + desc).lower())}">'
                f'<div class="dish-line"><h4 class="dish-name">{e(name)}</h4>'
                f'<span class="leader" aria-hidden="true"></span><span class="dish-price">{p}</span></div>'
                f'{fav}{d}</li>'
            )
        n = f'<p class="cat-note">{e(note)}</p>' if note else ""
        sections.append(
            f'<section class="cat" id="m-{slug}" data-cat="{slug}">'
            f'<header class="cat-head"><h3>{e(es)}</h3><span class="cat-en">{e(en)}</span>{n}</header>'
            f'<ul class="dishes">{"".join(rows)}</ul></section>'
        )
    return "\n".join(tabs), "\n".join(sections)


def schema():
    restaurant = {
        "@context": "https://schema.org",
        "@type": "Restaurant",
        "name": "Cabaña 28",
        "alternateName": "Cabana 28",
        "description": "Family-run Peruvian restaurant in Fort Lauderdale serving pollo a la brasa, lomo saltado, ceviche, chaufa and family meals for dine-in, pickup and delivery.",
        "servesCuisine": ["Peruvian", "Rotisserie Chicken", "Seafood"],
        "url": SITE,
        "telephone": "+19545305123",
        "priceRange": "$10-20",
        "image": SITE + "images/cabana28-og.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": "6351 N Andrews Ave",
                    "addressLocality": "Fort Lauderdale", "addressRegion": "FL",
                    "postalCode": "33309", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 26.2065, "longitude": -80.1420},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": days, "opens": o, "closes": c}
            for _, days, o, c in HOURS
        ],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.7", "reviewCount": "370", "bestRating": "5"},
        "hasMenu": SITE + "#menu",
        "acceptsReservations": "False",
        "potentialAction": {"@type": "OrderAction", "target": [PICKUP, DOORDASH, UBER]},
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    return json.dumps(restaurant, ensure_ascii=False, indent=2), json.dumps(faq, ensure_ascii=False, indent=2)


FAQS = [
    ("Where is Cabaña 28?", "6351 N Andrews Ave, Fort Lauderdale, FL 33309. There is parking in front of the restaurant."),
    ("What are your hours?", "Monday to Friday 10:30am to 9pm, Saturday 10:15am to 9pm, Sunday 10:15am to 8pm."),
    ("Can I order pickup or delivery?", "Yes. Order pickup on our online ordering site or by phone at (954) 530-5123. We deliver through DoorDash and Uber Eats."),
    ("What should I order the first time?", "Start with pollo a la brasa and our green ají, then add lomo saltado or a ceviche for the table. Chaufa de pollo a la brasa is a good pick if you are eating alone."),
    ("Do you have meals for families and groups?", "Yes. Our family meals start at $26.99 for a whole rotisserie chicken with two sides. For catering, call us or use the catering option on our ordering site."),
]


def faq_html():
    return "\n".join(
        f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in FAQS
    )


def hours_html():
    return "\n".join(
        f'<div class="hrow" data-days="{",".join(d[:3] for d in days)}"><dt>{e(label)}</dt>'
        f'<dd>{fmt(o)} to {fmt(c)}</dd></div>'
        for label, days, o, c in HOURS
    )


def fmt(t):
    h, m = map(int, t.split(":"))
    suf = "am" if h < 12 else "pm"
    h = h % 12 or 12
    return f"{h}:{m:02d}{suf}" if m else f"{h}{suf}"


def main():
    tabs, sections = build_menu()
    rjson, fjson = schema()
    count = sum(len(c[4]) for c in MENU)
    tpl = (ROOT / "_src" / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{MENU_TABS}}", tabs)
              .replace("{{MENU_SECTIONS}}", sections)
              .replace("{{SCHEMA_RESTAURANT}}", rjson)
              .replace("{{SCHEMA_FAQ}}", fjson)
              .replace("{{FAQ}}", faq_html())
              .replace("{{HOURS}}", hours_html())
              .replace("{{PICKUP}}", PICKUP).replace("{{DOORDASH}}", DOORDASH)
              .replace("{{UBER}}", UBER).replace("{{GOOGLE}}", GOOGLE)
              .replace("{{TEL}}", TEL).replace("{{PHONE}}", PHONE)
              .replace("{{SITE}}", SITE))
    assert "{{" not in out, "unreplaced placeholder"
    (ROOT / "index.html").write_text(out, encoding="utf-8")
    print(f"built index.html: {len(MENU)} categories, {count} dishes")


if __name__ == "__main__":
    main()
