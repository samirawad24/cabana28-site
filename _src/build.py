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
INSTAGRAM = "https://www.instagram.com/"  # swap for the Cabaña 28 Instagram profile link
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


def svg(d, label=""):
    return f'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{d}"/></svg>'


ICON_DOORDASH = svg("M23.071 8.409a6.09 6.09 0 00-5.396-3.228H.584A.589.589 0 00.17 6.184L3.894 9.93a1.752 1.752 0 001.242.516h12.049a1.554 1.554 0 11.031 3.108H8.91a.589.589 0 00-.415 1.003l3.725 3.747a1.75 1.75 0 001.242.516h3.757c4.887 0 8.584-5.225 5.852-10.413")
ICON_UBEREATS = svg("M0 2.8645v4.9972c0 1.8834 1.3315 3.1297 3.0835 3.1297a2.9652 2.9652 0 0 0 2.1502-.876v.7425H6.445V2.8645H5.223v4.9339c0 1.2642-.8696 2.1198-1.9954 2.122-1.1386-.0023-1.997-.834-1.997-2.122V2.8645zm7.3625 0v7.9934h1.163v-.7318a2.9915 2.9915 0 0 0 2.1177.876c1.714.048 3.1295-1.3283 3.1295-3.0429s-1.4155-3.091-3.1295-3.0429a2.9674 2.9674 0 0 0-2.107.876V2.8645zm9.8857 2.0561c-1.6752-.0074-3.0369 1.3492-3.0356 3.0245 0 1.7366 1.3732 3.0373 3.1537 3.0373a3.123 3.123 0 0 0 2.5578-1.2438l-.8495-.6177a2.0498 2.0498 0 0 1-1.7083.8585c-.9763.0126-1.8147-.6915-1.971-1.6553h4.818v-.379c0-1.734-1.254-3.0238-2.9638-3.0245zm6.1632.0667a1.5943 1.5943 0 0 0-1.376.7657v-.7186h-1.163v5.8235h1.1741V7.5465c0-.9023.5581-1.4847 1.3268-1.4847h.4949V4.9886c-.1576.0013-.3186-.0009-.4568-.0013zm-6.2034.944a1.844 1.844 0 0 1 1.8337 1.486H15.424a1.844 1.844 0 0 1 1.784-1.486zm-6.6589.0056c1.1223-.0084 2.0365.8992 2.0364 2.0215-.0026 1.1203-.914 2.0258-2.0343 2.021a2.0151 2.0151 0 0 1-1.4159-.5987A2.0152 2.0152 0 0 1 8.55 7.9592a2.0152 2.0152 0 0 1 .5838-1.422 2.0152 2.0152 0 0 1 1.4153-.6003zM0 12.9864v7.9716h5.7222v-1.3666H1.5458v-1.971h4.0647v-1.314H1.5458v-1.9556h4.1764v-1.3644zm14.5608.4097v1.6861h-1.1519v1.338h1.1545v3.143c0 .7927.5712 1.4209 1.6005 1.4209h1.6425L17.8 19.646h-1.1412c-.3482 0-.5714-.1509-.5714-.464v-2.7683H17.8v-1.3316h-1.7062v-1.686zm-5.2974 1.5275c-1.7348-.0103-3.141 1.4035-3.1214 3.1382.0196 1.7346 1.4575 3.1163 3.1915 3.0668a2.9915 2.9915 0 0 0 1.912-.6655v.532h1.5175v-5.9129h-1.509v.5257a3.0047 3.0047 0 0 0-1.9205-.6835c-.0244-.0007-.0492-.0006-.0701-.0008zm11.771.0077c-1.5855 0-2.7002.6437-2.7002 1.8854 0 .8607.6132 1.4213 1.936 1.695l1.4478.3286c.5694.1095.7224.2585.7224.4906 0 .3701-.438.6022-1.1279.6022-.876 0-1.3774-.1907-1.5723-.8477h-1.533c.219 1.2307 1.1563 2.05 3.0484 2.05h.0022c1.752 0 2.7422-.819 2.7422-1.9534 0-.8059-.5847-1.4084-1.8089-1.6668l-1.2943-.2605c-.7511-.1358-.988-.2738-.988-.5454 0-.357.3616-.5757 1.0295-.5757.7227 0 1.2527.1925 1.406.8473h1.5175c-.0854-1.2286-.9899-2.0497-2.8273-2.0497zM9.467 16.1815c1.0092.0096 1.8188.8369 1.8067 1.8461.0014 1.0046-.8198 1.816-1.8243 1.8025-1.0075-.0048-1.8203-.8256-1.8155-1.833.0048-1.0076.8255-1.8204 1.833-1.8156z")
ICON_INSTAGRAM = svg("M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077")


def order_logos():
    return (f'<div class="logo-btns">'
            f'<a class="lbtn lbtn-pu" href="{PICKUP}"><img src="images/cabana28-icon.png" alt="" width="28" height="28"><span>Order Pickup</span></a>'
            f'<a class="lbtn lbtn-dd" href="{DOORDASH}">{ICON_DOORDASH}<span>DoorDash</span></a>'
            f'<a class="lbtn lbtn-ue" href="{UBER}" aria-label="Uber Eats">{ICON_UBEREATS}</a>'
            f'</div>')


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
              .replace("{{ORDER_LOGOS}}", order_logos()).replace("{{ICON_INSTAGRAM}}", ICON_INSTAGRAM)
              .replace("{{INSTAGRAM}}", INSTAGRAM).replace("{{ICON_BAG}}", ICON_BAG).replace("{{ICON_PHONE}}", ICON_PHONE)
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
