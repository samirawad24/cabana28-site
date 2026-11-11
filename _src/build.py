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

# Dishes with raw or undercooked fish (Florida / FDA Food Code consumer advisory)
RAW = {"Causa Acevichada", "Leche de Tigre Cabaña", "Vuelve a la Vida", "Ceviche Tradicional",
       "Ceviche de Ají Amarillo", "Ceviche de Rocoto", "Ceviche Mixto", "Ceviche Cabaña 28", "Leche de Tigre"}

STRIP_A = ["Pollo a la Brasa", "Lomo Saltado", "Ceviche", "Ají de Gallina", "Chaufa", "Papa a la Huancaína",
           "Anticuchos", "Jalea", "Tallarín Saltado", "Picarones", "Chicha Morada"]
STRIP_B = ["Ven con hambre", "Pollo a la Brasa", "Comida de casa", "Parihuela", "Buen provecho",
           "Suspiro a la Limeña", "La mesa está servida", "Causa", "Inca Kola"]


def strip(words):
    return "<ul>" + "".join(f"<li>{e(w)}</li>" for w in words) + "</ul>"


def money(p):
    return f"${p:,.2f}"


# Photo panels dropped into the menu after these categories
# (img, w, h, title, text, dish name whose price is shown)
BREAKS = {
    "appetizers": ("images/menu/causa-acevichada-lg.jpg", 1200, 1202, "Causa Acevichada",
                   "Cold whipped potato with ají amarillo and avocado, crowned with fresh ceviche. A classic way to start.",
                   "Causa Acevichada"),
    "family": ("images/pollo-a-la-brasa.jpg", 760, 500, "Pollo a la Brasa",
               "Marinated overnight and roasted on the spit until the skin crackles. Get the whole bird with two sides for the table.",
               "Whole Chicken, 2 Sides"),
    "peruvian": ("images/lomo-saltado.jpg", 1600, 1200, "Lomo Saltado",
                 "Tenderloin, red onion and tomato hit a screaming hot wok, then meet the fries and rice. One of our most ordered plates.",
                 "Lomo Saltado"),
    "seafood": ("images/ceviche-mixto.jpg", 1600, 2133, "Ceviche Mixto",
                "Fish, shrimp and calamari cured in fresh lime leche de tigre, with cancha, corn and sweet potato.",
                "Ceviche Mixto"),
    "pastas": ("images/menu/tallarin-saltado-de-carne-lg.jpg", 1200, 673, "Tallarín Saltado",
               "Spaghetti thrown into the wok with beef, onion and tomato. Chifa-style comfort food.",
               "Tallarín Saltado de Carne"),
    "bowls": ("images/menu/brasa-bowl-lg.jpg", 1200, 1200, "Brasa Bowl",
              "Rotisserie chicken over rice and black beans with house salad and pico de gallo. Lunch, sorted.",
              "Brasa Bowl"),
    "soups": ("images/menu/parihuela-lg.jpg", 1200, 673, "Parihuela",
              "A rich, spicy seafood soup with half a fried fish and rice on the side. Big enough to share.",
              "Parihuela"),
    "kids": ("images/menu/picarones-lg.jpg", 1200, 673, "Picarones",
             "Warm Peruvian doughnuts drizzled with spiced syrup. Save room.",
             "Picarones"),
}
PRICES = {n: pr for *_, items in MENU for n, _, pr, _ in items}


def menu_break(img, w, h, title, text, dish):
    star = '<span class="raw">*</span>' if dish in RAW else ""
    return (
        f'<aside class="mbreak">'
        f'<img src="{img}" alt="{e(title)} at Cabaña 28" width="{w}" height="{h}" loading="lazy">'
        f'<div class="mbreak-text"><p class="mbreak-k">De nuestra cocina</p><h3>{e(title)}{star}</h3>'
        f'<p>{e(text)}</p><div class="mbreak-foot"><span>{e(dish)} &middot; <b>{money(PRICES[dish])}</b></span>'
        f'<a class="btn mbreak-btn" href="{PICKUP}">Order</a></div></div></aside>'
    )


def photo(name):
    """Thumbnail from images/menu/ (downloaded by fetch_photos.py), if we have one."""
    from fetch_photos import slug
    f = f"images/menu/{slug(name)}.jpg"
    if not (ROOT / f).exists():
        return ""
    return f'<img class="dish-img" src="{f}" alt="{e(name)}" width="360" height="360" loading="lazy" decoding="async">'


def build_menu():
    tabs, sections = [], []
    for i, (slug, es, en, note, items) in enumerate(MENU):
        tabs.append(f'<a href="#m-{slug}" data-tab="{slug}">{e(en)}</a>')
        rows = []
        for name, desc, price, popular in items:
            raw = '<span class="raw" title="Served raw or undercooked. See food safety notice.">*</span>' if name in RAW else ""
            fav = '<span class="fav">Our fav</span>' if popular else ""
            p = money(price) if price is not None else f'<a href="{PICKUP}" class="opts">Options</a>'
            d = f'<p class="dish-desc">{e(desc)}</p>' if desc else ""
            img = photo(name)
            rows.append(
                f'<li class="dish{" is-fav" if popular else ""}{" has-img" if img else ""}" data-search="{e((name + " " + desc).lower())}">'
                f'{img}<div class="dish-body"><div class="dish-line"><h4 class="dish-name">{e(name)}{raw}</h4>'
                f'<span class="leader" aria-hidden="true"></span><span class="dish-price">{p}</span></div>'
                f'{fav}{d}</div></li>'
            )
        n = f'<p class="cat-note">{e(note)}</p>' if note else ""
        sections.append(
            f'<section class="cat{" alt" if i % 2 else ""}" id="m-{slug}" data-cat="{slug}">'
            f'<header class="cat-head"><h3>{e(es)}</h3><span class="cat-en">{e(en)}</span>{n}</header>'
            f'<ul class="dishes">{"".join(rows)}</ul></section>'
        )
        if slug in BREAKS:
            sections.append(menu_break(*BREAKS[slug]))
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


def finish(out, preview):
    if preview:
        out = out.replace('src="images/', 'src="../images/').replace('href="images/', 'href="../images/')
        out = out.replace('content="index, follow"', 'content="noindex, nofollow"')
    return out


def main():
    import sys
    import legal
    preview = "--preview" in sys.argv
    dest = ROOT / "v2" if preview else ROOT
    dest.mkdir(exist_ok=True)
    tabs, sections = build_menu()
    rjson, fjson = schema()
    count = sum(len(c[4]) for c in MENU)
    tpl = (ROOT / "_src" / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{MENU_TABS}}", tabs)
              .replace("{{MENU_SECTIONS}}", sections)
              .replace("{{STRIP_A}}", strip(STRIP_A))
              .replace("{{STRIP_B}}", strip(STRIP_B))
              .replace("{{SCHEMA_RESTAURANT}}", rjson)
              .replace("{{SCHEMA_FAQ}}", fjson)
              .replace("{{FAQ}}", faq_html())
              .replace("{{HOURS}}", hours_html())
              .replace("{{PICKUP}}", PICKUP).replace("{{DOORDASH}}", DOORDASH)
              .replace("{{UBER}}", UBER).replace("{{GOOGLE}}", GOOGLE)
              .replace("{{TEL}}", TEL).replace("{{PHONE}}", PHONE)
              .replace("{{SITE}}", SITE))
    assert "{{" not in out, "unreplaced placeholder"
    (dest / "index.html").write_text(finish(out, preview), encoding="utf-8")
    lp = legal.pages(TEL, PHONE)
    for slug, (title, body) in lp.items():
        page = legal.render(tpl, SITE, PICKUP, TEL, PHONE, slug, title, body)
        (dest / f"{slug}.html").write_text(finish(page, preview), encoding="utf-8")
    print(f"built {dest}: {len(MENU)} categories, {count} dishes, {len(lp)} legal pages")


if __name__ == "__main__":
    main()
