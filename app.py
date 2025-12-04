# Streamlit web app with LLM Beauty Scoring, Location Growth Score & Advanced Hooks for analyzing Rightmove listings — upgraded version

import streamlit as st
import re
import pandas as pd

st.title("Rightmove Listing Scoring Tool — Enhanced Version")("Rightmove Listing Scoring Tool")

st.write("Paste listing text, upload text files, and export results as CSV.")("Paste Rightmove listing text (price, location, key features, description). Add multiple listings.")

uploaded_file = st.file_uploader("Upload a text file with listings (optional)", type=["txt"])

input_text = st.text_area("Or paste listings text here (one after another):", height=300)

# Load from uploaded file if present
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    try:
        input_text = file_bytes.decode("utf-8")
    except:
        st.error("Could not decode file.")("Paste listings text here (one after another):", height=300)

# Scoring functions including LLM-based beauty, location growth scoring, and advanced hooks

# --- LLM Beauty Scoring (enhanced for Georgian & Victorian features) ---
# Extra weighting for Georgian/Victorian architecture
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

def llm_beauty_score(text):
    # Start with base beauty score
    score = beauty_score(text)

    # Apply Georgian/Victorian boosts
    for k,v in georgian_victorian_keywords.items():
        if k in text.lower():
            score += v

    # Existing bonus keywords
    bonus_keywords = {
        "crittall": 3,
        "loft": 2,
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
    for k,v in bonus_keywords.items():
        if k in text.lower():
            score += v

    return min(score, 10) (placeholder for API integration) ---
def llm_beauty_score(text):
    # Simulated upgraded beauty score using richer architectural vocab
    bonus_keywords = {
        "crittall": 3,
        "loft": 2,
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
    score = beauty_score(text)
    for k,v in bonus_keywords.items():
        if k in text.lower():
            score += v
    return min(score, 10)

# --- Location Growth Score ---
def location_growth_score(location):
    high_engagement = ["London", "Edinburgh", "Brighton", "Cornwall", "Liverpool", "Manchester", "Bath"]
    medium_engagement = ["Bristol", "York", "Leeds", "Glasgow", "Cardiff", "Cambridge", "Oxford"]
    if any(city.lower() in location.lower() for city in high_engagement):
        return "High"
    if any(city.lower() in location.lower() for city in medium_engagement):
        return "Medium"
    return "Low"

# --- Advanced Hook Generator ---
def advanced_hook(text, beauty, band, location):
    # Detect standout feature
    standout = None
    standout_patterns = [
        ("crittall", "these Crittall windows are doing the heavy lifting"),
        ("vaulted", "the vaulted ceilings are outrageous"),
        ("sea view", "the sea view is absolutely ridiculous"),
        ("grade ii", "it's literally a protected Grade II listed building"),
        ("loft", "this loft conversion goes way harder than it needs to"),
        ("architect", "the architect clearly had something to prove"),
        ("panoramic", "the panoramic view is borderline disrespectful"),
    ]
    for key,phrase in standout_patterns:
        if key in text.lower():
            standout = phrase
            break

    # Build hook
    if standout:
        return f"Right, this house in {location} has {standout}."
    if beauty >= 9:
        return f"Right, this might be one of the nicest houses for sale right now in {location}."
    if band == "Mid-High":
        return f"Right, this house is stupidly good value for {location}."
    return f"Right, this house is way more interesting than it first looks in {location}."

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
        "warehouse": 3,
        "conversion": 2,
    }
    score = 5
    for k,v in keywords.items():
        if k in text.lower():
            score += v
    return min(score, 10)

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

def hook_generator(beauty, band, location):
    base = "Right, this house "
    if beauty >= 9:
        return base + "might be one of the nicest on the market right now in " + location
    if band == "Mid-High":
        return base + "is ridiculously good for the money in " + location
    return base + "is far more interesting than it looks at first glance in " + location

if st.button("Analyse Listings") and input_text.strip():("Analyse Listings"):
    listings = input_text.split("\n\n")
    data = []

    for lst in listings:
        # Detect URL and extract price if pasted
        url_match = re.search(r"https?://[A-Za-z0-9\./_-]+", lst)
        if url_match:
            pass
        txt = lst.strip()
        if not txt:
            continue
        price = extract_price(txt)
        band = price_band(price)
        beauty = llm_beauty_score(txt)
        vir = virality(beauty, band)
        cluster = cluster_bias(vir)
        loc_match = re.search(r"in ([A-Za-z ,]+)", txt) = re.search(r"in ([A-Za-z ]+)", txt)
        loc = loc_match.group(1) if loc_match else "Unknown"
        growth = location_growth_score(loc)
        # Film Score: weighted mix (beauty 40%, virality 40%, location 20%)
        vir_score = {"High": 10, "Medium": 6, "Low": 2}[vir]
        loc_score = {"High": 10, "Medium": 5, "Low": 1}[growth]
        film_score = int(0.4*beauty + 0.4*vir_score + 0.2*loc_score)

        hook = advanced_hook(txt, beauty, band, loc)(loc)
        hook = advanced_hook(txt, beauty, band, loc)(beauty, band, loc)
        data.append([price, band, beauty, vir, cluster, loc, hook])

    df = pd.DataFrame(data, columns=["Price", "Price Band", "Beauty Score", "Virality", "Cluster", "Location", "Location Growth", "Film Score", "Hook"])(data, columns=["Price", "Price Band", "Beauty Score", "Virality", "Cluster", "Location", "Location Growth", "Hook"])
    st.dataframe(df)

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="rightmove_scores.csv",
        mime="text/csv"
    )(df)
