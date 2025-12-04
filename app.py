import streamlit as st
import pandas as pd
import re

st.title("Rightmove Listing Scoring Tool — Enhanced Version")
st.write("Paste listing text OR upload a .txt file. The tool will score beauty, virality, hooks, and film-worthiness.")

# -------------------------------
# LOAD TEXT
# -------------------------------
uploaded_file = st.file_uploader("Upload a text file (optional)", type=["txt"])
input_text = st.text_area("Or paste listings here (separate each with a blank line):", height=300)

if uploaded_file is not None:
    try:
        input_text = uploaded_file.read().decode("utf-8")
    except:
        st.error("Could not read uploaded file.")

# -------------------------------
# BASE BEAUTY SCORING
# -------------------------------
def beauty_score(text):
    keywords = {
        "georgian": 3,
        "victorian": 3,
        "art deco": 4,
        "period": 2,
        "architect": 4,
        "grade ii": 4,
        "view": 2,
        "sea": 3,
        "restored": 3,
        "unique": 2,
        "loft": 2,
        "warehouse": 3,
        "conversion": 2,
    }
    score = 5
    for k, v in keywords.items():
        if k in text.lower():
            score += v
    return min(score, 10)

# -------------------------------
# ENHANCED GEORGIAN/VICTORIAN BEAUTY SCORING
# -------------------------------
georgian_victorian_keywords = {
    "georgian": 5,
    "victorian": 4,
    "regency": 4,
    "sash windows": 4,
    "bay window": 3,
    "period features": 4,
    "original features": 3,
    "cornicing": 3,
    "coving": 3,
    "fireplace": 2,
    "townhouse": 3,
    "stucco": 3,
    "mouldings": 3,
    "high ceilings": 4,
    "cellar": 2,
    "basement": 2,
}

extra_bonus_keywords = {
    "crittall": 3,
    "brutalist": 4,
    "mid-century": 4,
    "artisan": 2,
    "handcrafted": 2,
    "designer": 2,
    "restoration": 2,
    "vaulted": 3,
    "double-height": 3,
    "panoramic": 3,
    "penthouse": 4,
}

def llm_beauty_score(text):
    score = beauty_score(text)

    # Add Georgian/Victorian weighted features
    for k, v in georgian_victorian_keywords.items():
        if k in text.lower():
            score += v

    # Add extra premium architecture features
    for k, v in extra_bonus_keywords.items():
        if k in text.lower():
            score += v

    return min(score, 10)

# -------------------------------
# PRICE + BAND
# -------------------------------
def extract_price(text):
    match = re.search(r"£([0-9,]+)", text)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

def price_band(price):
    if price is None:
        return "Unknown"
    if price < 500000:
        return "Low"
    if price < 1500000:
        return "Mid"
    if price < 4000000:
        return "Mid-High"
    return "High"

# -------------------------------
# VIRALITY / CLUSTERS
# -------------------------------
def virality(beauty, band):
    if beauty >= 9 and band == "Mid-High":
        return "High"
    if beauty >= 7:
        return "Medium"
    return "Low"

def cluster_bias(vir):
    if vir == "High":
        return "Cluster 0"
    if vir == "Medium":
        return "Cluster 2"
    return "Cluster 1"

# -------------------------------
# LOCATION GROWTH SCORE
# -------------------------------
def location_growth_score(location):
    high = ["London", "Edinburgh", "Brighton", "Cornwall", "Liverpool", "Manchester", "Bath"]
    medium = ["Bristol", "York", "Leeds", "Glasgow", "Cardiff", "Cambridge", "Oxford"]

    location_lower = location.lower()

    if any(c.lower() in location_lower for c in high):
        return "High"
    if any(c.lower() in location_lower for c in medium):
        return "Medium"
    return "Low"

# -------------------------------
# ADVANCED HOOK GENERATOR
# -------------------------------
def advanced_hook(text, beauty, band, location):

    standout_patterns = [
        ("crittall", "these Crittall windows are doing the heavy lifting"),
        ("vaulted", "the vaulted ceilings are outrageous"),
        ("sea view", "the sea view is absolutely ridiculous"),
        ("grade ii", "it's literally a protected Grade II listed building"),
        ("loft", "this loft conversion goes way harder than it needs to"),
        ("architect", "the architect clearly had something to prove"),
        ("panoramic", "the panoramic view is borderline disrespectful"),
    ]

    text_lower = text.lower()
    standout = None

    for key, phrase in standout_patterns:
        if key in text_lower:
            standout = phrase
            break

    if standout:
        return f"Right, this house in {location} has {standout}."
    if beauty >= 9:
        return f"Right, this might be one of the nicest houses for sale in {location}."
    if band == "Mid-High":
        return f"Right, this house is stupidly good value for {location}."
    return f"Right, this house is way more interesting than it looks in {location}."

# -------------------------------
# PROCESS BUTTON
# -------------------------------
if st.button("Analyse Listings") and input_text.strip():

    listings = input_text.split("\n\n")
    data = []

    for lst in listings:
        txt = lst.strip()
        if not txt:
            continue

        price = extract_price(txt)
        band = price_band(price)
        beauty = llm_beauty_score(txt)
        vir = virality(beauty, band)
        cluster = cluster_bias(vir)

        loc_match = re.search(r"in ([A-Za-z ,]+)", txt)
        location = loc_match.group(1) if loc_match else "Unknown"

        growth = location_growth_score(location)

        vir_score = {"High": 10, "Medium": 6, "Low": 2}[vir]
        loc_score = {"High": 10, "Medium": 5, "Low": 1}[growth]

        film_score = int(0.4*beauty + 0.4*vir_score + 0.2*loc_score)

        hook = advanced_hook(txt, beauty, band, location)

        data.append([
            price, band, beauty, vir, cluster, location, growth, film_score, hook
        ])

    df = pd.DataFrame(
        data,
        columns=[
            "Price", "Price Band", "Beauty Score", "Virality",
            "Cluster", "Location", "Location Growth", "Film Score", "Hook"
        ]
    )

    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="rightmove_scores.csv",
        mime="text/csv"
    )
