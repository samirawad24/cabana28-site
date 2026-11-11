"""Download dish photos from the Cabaña 28 ordering page (food.orders.co) into images/menu/.
Run: python _src/fetch_photos.py   (needs network access to food.orders.co and ik.imagekit.io)"""
import json
import re
import unicodedata
import urllib.request
from pathlib import Path

from menu import MENU

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "menu"
API = "https://food.orders.co/api/api01/menu/food2/v3/cabaa28"

# site dish name -> product name on the ordering page, where the names differ
ALIAS = {
    "Tamal": "TAMAL- TAMALE",
    "Chicken Sandwich": "sandwich pollo",
    "Causa Acevichada": "causa acebichada",
    "Pollipapas": "Polli papas",
    "Parrilla Cabaña": "Parilla cabaña",
    "2 Chickens + Saltado": "2 Rotisserie Chickens with 3 Sides and 10 oz of Lomo or Pollo Saltado",
    "1 Chicken, 2 Sides + Juice": "1. rotisserie chicken, 2 sides 1/2 gallon chicha , lemonade or passion fruit",
    "1 Chicken, 2 Sides + Tequeños": "1Rotisserie, 2 Sides and Tequeños",
    "1 Chicken, 2 Sides + Beef or Chicken": "1 Rotiserrie, 2 Sides, Beef or Boneless Chicken",
    "1 Chicken, 2 Sides + Inca Kola": "1 Rotiserrie, 2 sides, 2 litters inka cola",
    "1 Chicken with 2 Sides": "1Rotisserie Chicken with 2 Sides",
    "Whole Chicken, 2 Sides": "1 rotisserie chicken 2 sides",
    "Whole Chicken, Rice and Beans": "1 rotisserie chicken rice and beans.",
    "1/2 Chicken, 2 Sides": "1⁄2 rotisserie chicken 2 sides",
    "1/4 Chicken, 2 Sides": "1⁄4 rotisserie chicken 2 sides",
    "Fettuccine a la Huancaína con Pollo a la Brasa": "Fettuccini a la huancaina con pollo a la brasa",
    "Fettuccine al Pesto con Pollo a la Brasa": "Fetuccini al pesto con pollo a la brasa",
    "Chaufa Cabaña 28": "Chaufa Cabaña28",
    "Chaufa Mar y Tierra": "Chaufa Mar & Tierra",
    "Steak with 2 Sides": "Beef with 2 sides",
    "Ceviche Cabaña 28": "Ceviche Cabaña28",
    "Pasta Verde con Filete de Pollo": "Pasta en Salsa Verde con Filete de Pollo",
    "A lo Pobre Burger": "A LO POBRE HAMBURGER",
    "Saltado Burger": "SALTADA HAMBURGER",
    "Rotisserie Chicken Wrap": "Rotiserie chicken wrap",
    "Cabaña 28 Salad": "cabana 28 salad",
    "Ensalada César con Pollo": "Ensalada Caesar con pollo",
    "Fried Egg": "frie egg",
    "Passion Fruit Juice": "Pasion  fruit juice.",
    "Pineapple Juice": "pineaple juice",
    "Strawberry Juice": "strawberry. juice",
    "Inca Kola, 2 Liter": "2 liters inka cola",
    "Coke, 2 Liter": "2 Liters COKE",
    "Cappuccino": "Capuccino",
    "Espresso": "Expresso",
    "Chaufa Rice": "Chaufa",
}
# large versions for the photo panels in the menu
LARGE = ["Causa Acevichada", "Tallarín Saltado de Carne", "Parihuela", "Brasa Bowl", "Jalea", "Suspiro a la Limeña",
         "Chaufa de Mariscos", "Aguadito de Pollo", "Picarones", "Parrilla Cabaña"]


def key(s):
    s = unicodedata.normalize("NFKD", s.replace("⁄", "/")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug(s):
    return key(s).replace(" ", "-")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    data = json.loads(get(API))["data"]
    photos = {}
    for c in data["categories"]:
        for p in c.get("products", []):
            url = (p.get("image") or {}).get("url")
            if url:
                photos.setdefault(key(p["name"]), url)
    OUT.mkdir(parents=True, exist_ok=True)
    done, missing = 0, []
    for _, _, _, _, items in MENU:
        for name, *_ in items:
            url = photos.get(key(ALIAS.get(name, name)))
            if not url:
                missing.append(name)
                continue
            dest = OUT / f"{slug(name)}.jpg"
            if not dest.exists():
                dest.write_bytes(get(url + "?tr=w-360,h-360,fo-auto,f-jpg,q-72"))
            if name in LARGE and not (OUT / f"{slug(name)}-lg.jpg").exists():
                (OUT / f"{slug(name)}-lg.jpg").write_bytes(get(url + "?tr=w-1200,f-jpg,q-78"))
            done += 1
    print(f"{done} dishes with photos; no photo for: {', '.join(sorted(set(missing)))}")


if __name__ == "__main__":
    main()
