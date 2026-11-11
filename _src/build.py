"""Build index.html for Cabaña 28. Run: python _src/build.py"""
import html
import json
from pathlib import Path

from menu import MENU

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://samirawad24.github.io/cabana28-site/"
PICKUP = "https://food.orders.co/cabaa28"
DELIVERY = "https://food.orders.co/cabaa28/menu?deliveryOption=delivery"
EZCATER = "https://www.ezcater.com/"  # swap for the Cabaña 28 ezCater page link when we have it
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


def dish_li(name, desc, price, popular):
    raw = '<span class="raw" title="Served raw or undercooked. See food safety notice.">*</span>' if name in RAW else ""
    fav = '<span class="fav">Our fav</span>' if popular else ""
    p = money(price) if price is not None else f'<a href="{PICKUP}" class="opts">Options</a>'
    d = f'<p class="dish-desc">{e(desc)}</p>' if desc else ""
    img = photo(name)
    return (
        f'<li class="dish{" is-fav" if popular else ""}{" has-img" if img else ""}" data-search="{e((name + " " + desc).lower())}">'
        f'{img}<div class="dish-body"><div class="dish-line"><h4 class="dish-name">{e(name)}{raw}</h4>'
        f'<span class="leader" aria-hidden="true"></span><span class="dish-price">{p}</span></div>'
        f'{fav}{d}</div></li>'
    )


def build_menu():
    tabs, sections = [], []
    for i, (slug, es, en, note, items) in enumerate(MENU):
        tabs.append(f'<a href="#m-{slug}" data-tab="{slug}">{e(en)}</a>')
        rows = []
        for name, desc, price, popular in items:
            rows.append(dish_li(name, desc, price, popular))
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
        "hasMenu": SITE + "menu.html",
        "acceptsReservations": "False",
        "potentialAction": {"@type": "OrderAction", "target": [DELIVERY, PICKUP, DOORDASH, UBER]},
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    return json.dumps(restaurant, ensure_ascii=False, indent=2), json.dumps(faq, ensure_ascii=False, indent=2)


FAQS = [
    ("Where is Cabaña 28?", "6351 N Andrews Ave, Fort Lauderdale, FL 33309. There is parking in front of the restaurant."),
    ("What are your hours?", "Monday to Friday 10:30am to 9pm, Saturday 10:15am to 9pm, Sunday 10:15am to 8pm."),
    ("Do you deliver?", "Yes. Order delivery or pickup on our online ordering page, or call us at (954) 530-5123. We are also on DoorDash and Uber Eats."),
    ("What should I order the first time?", "Start with pollo a la brasa and our green ají, then add lomo saltado or a ceviche for the table. Chaufa de pollo a la brasa is a good pick if you are eating alone."),
    ("Do you have meals for families and groups?", "Yes. Our family meals start at $26.99 for a whole rotisserie chicken with two sides. For catering, call us at (954) 530-5123 and our own team will deliver it, or find us on ezCater."),
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


ICON_BAG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>')
ICON_PHONE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>')

# Restaurant photos that join the food in the gallery: (file, caption)
CASA = [("images/cabana28-dining-room.jpg", "Our dining room"),
        ("images/cabana28-peruvian-dishes-spread.jpg", "La mesa está servida"),
        ("images/cabana28-storefront-fort-lauderdale.jpg", "6351 N Andrews Ave")]

PAGES = {  # slug: (output file, title, description)
    "home": ("index.html", "Cabaña 28 | Peruvian Restaurant in Fort Lauderdale, FL",
             "Family-run Peruvian restaurant in Fort Lauderdale. Pollo a la brasa, lomo saltado, ceviche and chaufa. Order delivery, see the menu, or book catering."),
    "menu": ("menu.html", "Menu | Cabaña 28 Peruvian Restaurant, Fort Lauderdale",
             "The full Cabaña 28 menu with prices and photos: pollo a la brasa, lomo saltado, ceviche, chaufa, soups, bowls and desserts. Order delivery or pickup."),
    "catering": ("catering.html", "Peruvian Catering in Fort Lauderdale | Cabaña 28",
                 "Peruvian catering delivered by Cabaña 28's own team: family trays of pollo a la brasa, lomo saltado, chaufa and more. Call (954) 530-5123."),
    "gallery": ("gallery.html", "Gallery | Cabaña 28 Peruvian Restaurant, Fort Lauderdale",
                "Photos of Cabaña 28's Peruvian food and dining room in Fort Lauderdale: pollo a la brasa, ceviche, lomo saltado, jalea and more."),
    "visit": ("visit.html", "Hours & Location | Cabaña 28, Fort Lauderdale",
              "Cabaña 28 hours, address, map and parking at 6351 N Andrews Ave, Fort Lauderdale, FL 33309. Call (954) 530-5123."),
}


def size(rel):
    from PIL import Image
    with Image.open(ROOT / rel) as im:
        return im.size


def gallery_items():
    from fetch_photos import GALLERY, slug
    items = []
    for name, tag in GALLERY.items():
        f = f"images/gallery/{slug(name)}.jpg"
        if (ROOT / f).exists():
            items.append((f, name, tag))
    for pos, (f, cap) in zip((2, 11, 21), CASA):
        items.insert(pos, (f, cap, "casa"))
    return items


def gallery_grid():
    out = []
    for f, cap, tag in gallery_items():
        w, h = size(f)
        out.append(f'<figure class="gal-item" data-tag="{tag}"><a href="{f}" data-cap="{e(cap)}">'
                   f'<img src="{f}" alt="{e(cap)} at Cabaña 28" width="{w}" height="{h}" loading="lazy" decoding="async"></a>'
                   f'<figcaption>{e(cap)}</figcaption></figure>')
    return "\n".join(out)


def gallery_peek():
    pick = ["images/gallery/lomo-saltado.jpg", "images/gallery/ceviche-mixto.jpg", "images/cabana28-dining-room.jpg",
            "images/gallery/parrilla-cabana.jpg", "images/gallery/picarones.jpg"]
    caps = dict((f, c) for f, c, _ in gallery_items())
    return '<div class="peek">' + "".join(
        f'<a href="gallery.html"><img src="{f}" alt="{e(caps.get(f, "Cabaña 28"))}" loading="lazy" decoding="async"></a>' for f in pick) + "</div>"


def cater_items():
    fam = next(items for slug_, _, _, _, items in MENU if slug_ == "family")
    return "\n".join(dish_li(*it) for it in fam)


def ezcater_block():
    return (f'<div class="ez"><p><strong>Prefer ezCater?</strong> We\'re on ezCater too, for invoicing and company accounts.</p>'
            f'<a class="btn btn-line" href="{EZCATER}">Order on ezCater</a></div>')


def nav_cats():
    return "\n".join(f'<a href="menu.html#m-{slug_}">{e(en)}</a>' for slug_, _, en, _, _ in MENU)


def render(tpl, page, main_html, head_extra=""):
    fname, title, desc = PAGES[page] if page in PAGES else page
    url = SITE + ("" if fname == "index.html" else fname)
    out = (tpl.replace("{{MAIN}}", main_html)
              .replace("{{HEAD_EXTRA}}", head_extra)
              .replace("{{PAGE}}", page if isinstance(page, str) else "legal")
              .replace("{{TITLE}}", e(title)).replace("{{DESC}}", e(desc)).replace("{{URL}}", url)
              .replace("{{NAV_CATS}}", nav_cats()).replace("{{DRAWER_CATS}}", nav_cats())
              .replace("{{STRIP_A}}", strip(STRIP_A)).replace("{{STRIP_B}}", strip(STRIP_B))
              .replace("{{FAQ}}", faq_html()).replace("{{HOURS}}", hours_html())
              .replace("{{ICON_BAG}}", ICON_BAG).replace("{{ICON_PHONE}}", ICON_PHONE)
              .replace("{{DELIVERY}}", DELIVERY).replace("{{PICKUP}}", PICKUP).replace("{{DOORDASH}}", DOORDASH)
              .replace("{{UBER}}", UBER).replace("{{GOOGLE}}", GOOGLE)
              .replace("{{TEL}}", TEL).replace("{{PHONE}}", PHONE)
              .replace("{{SITE}}", SITE))
    if isinstance(page, str):
        out = out.replace(f'data-nav="{page}"', f'data-nav="{page}" aria-current="page"')
    assert "{{" not in out, "unreplaced placeholder: " + out[out.index("{{"):out.index("{{") + 40]
    return out, fname


def ld(obj):
    return f'  <script type="application/ld+json">\n{obj}\n  </script>'


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
    pages_dir = ROOT / "_src" / "pages"
    fill = {
        "{{MENU_TABS}}": tabs, "{{MENU_SECTIONS}}": sections,
        "{{DISH_COUNT}}": str(count), "{{CAT_COUNT}}": str(len(MENU)),
        "{{GALLERY_GRID}}": gallery_grid(), "{{GALLERY_PEEK}}": gallery_peek(),
        "{{CATER_ITEMS}}": cater_items(), "{{EZCATER_BLOCK}}": ezcater_block(),
    }
    extra = {"home": ld(rjson), "visit": ld(fjson)}
    for page in PAGES:
        body = (pages_dir / f"{page}.html").read_text(encoding="utf-8")
        for k, v in fill.items():
            body = body.replace(k, v)
        out, fname = render(tpl, page, body, extra.get(page, ""))
        (dest / fname).write_text(finish(out, preview), encoding="utf-8")
    lp = legal.pages(TEL, PHONE)
    for slug_, (title, body) in lp.items():
        meta = (f"{slug_}.html", f"{title} | Cabaña 28",
                f"{title} for the Cabaña 28 website, a Peruvian restaurant in Fort Lauderdale, FL.")
        out, _ = render(tpl, meta, legal.main_html(title, body), legal.CSS)
        (dest / f"{slug_}.html").write_text(finish(out, preview), encoding="utf-8")
    print(f"built {dest}: {len(PAGES)} pages, {len(MENU)} categories, {count} dishes, {len(lp)} legal pages")


if __name__ == "__main__":
    main()
