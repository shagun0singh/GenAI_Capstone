import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import run_agent

st.set_page_config(page_title="🏠 Property Advisor AI", page_icon="🏠", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .hero {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero h1 { font-size: 2.5rem; font-weight: 800; margin-bottom: 0.3rem; }
    .hero p { font-size: 1.05rem; opacity: 0.75; max-width: 600px; margin: 0 auto; }
    
    .step-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: transform 0.2s, border-color 0.2s;
    }
    .step-card:hover { transform: translateY(-3px); border-color: rgba(102,126,234,0.5); }
    .step-icon { font-size: 2rem; margin-bottom: 0.4rem; }
    .step-title { font-weight: 700; font-size: 0.95rem; color: #e0e0e0; }
    .step-sub { font-size: 0.75rem; color: #888; margin-top: 0.2rem; }
    
    .price-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin: 1.5rem 0;
    }
    .price-display .label { font-size: 0.85rem; opacity: 0.8; text-transform: uppercase; letter-spacing: 2px; }
    .price-display .amount { font-size: 2.8rem; font-weight: 800; margin: 0.3rem 0; }
    
    .trust-badge {
        padding: 0.8rem 1.5rem;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 1rem 0;
    }
    .trust-high { background: linear-gradient(135deg, #11998e, #38ef7d); color: white; }
    .trust-medium { background: linear-gradient(135deg, #f7971e, #ffd200); color: #333; }
    .trust-low { background: linear-gradient(135deg, #eb3349, #f45c43); color: white; }
    
    .score-row { display: flex; align-items: center; margin: 0.4rem 0; gap: 0.6rem; }
    .score-label { min-width: 140px; font-weight: 600; font-size: 0.85rem; color: #bbb; }
    .score-bar-bg { flex: 1; height: 18px; background: #1e1e30; border-radius: 9px; overflow: hidden; }
    .score-bar-fill { height: 100%; border-radius: 9px; }
    .score-val { min-width: 40px; text-align: right; font-weight: 700; font-size: 0.85rem; color: #ddd; }
    
    .divider {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102,126,234,0.4), transparent);
        margin: 2rem 0;
    }
    
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HERO SECTION
# ============================================================
st.markdown("""
<div class="hero">
    <h1>🏠 Agentic Property Advisor</h1>
    <p>AI-powered property analysis with ML price prediction, RAG market insights, LLM advisory, and trust scoring</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HOW IT WORKS — 4 Step Cards
# ============================================================
st.markdown("#### 🔄 How It Works")
c1, c2, c3 = st.columns(3)
steps = [
    ("🔮", "Predict Price", "ML Model"),
    ("📚", "Retrieve Data", "RAG / FAISS"),
    ("🤖", "Generate Advice", "Groq LLM"),
]
for col, (icon, title, sub) in zip([c1, c2, c3], steps):
    col.markdown(f"""
    <div class="step-card">
        <div class="step-icon">{icon}</div>
        <div class="step-title">{title}</div>
        <div class="step-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# INPUT SECTION
# ============================================================
st.markdown("#### 🏡 Enter Property Details")

col_a, col_b, col_c = st.columns(3)

with col_a:
    latitude = st.number_input("Latitude", value=51.50, format="%.4f")
    longitude = st.number_input("Longitude", value=-0.12, format="%.4f")
    bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, value=2, step=1)

with col_b:
    bathrooms = st.number_input("Bathrooms", min_value=0, max_value=10, value=1, step=1)
    floorAreaSqM = st.number_input("Floor Area (sqm)", min_value=10.0, max_value=1000.0, value=75.0, step=5.0)
    livingRooms = st.number_input("Living Rooms", min_value=0, max_value=5, value=1, step=1)

with col_c:
    tenure = st.selectbox("Tenure", ["FREEHOLD", "LEASEHOLD"])
    property_type = st.selectbox("Property Type", ["FLAT", "DETACHED", "SEMI_DETACHED", "TERRACED"])
    energy_rating = st.selectbox("Energy Rating", ["A", "B", "C", "D", "E", "F", "G"], index=3)

st.markdown("")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    analyze = st.button("🔍 Analyze Property", use_container_width=True, type="primary")

# ============================================================
# RESULTS SECTION
# ============================================================
if analyze:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    input_data = {
        "latitude": latitude, "longitude": longitude,
        "bedrooms": bedrooms, "bathrooms": bathrooms,
        "floorAreaSqM": floorAreaSqM, "livingRooms": livingRooms,
        "tenure": tenure, "propertyType": property_type,
        "currentEnergyRating": energy_rating
    }

    # Agent pipeline with live progress
    with st.status("🤖 Agent is analyzing your property...", expanded=True) as status:
        st.write("🔮 **Step 1:** Predicting price with ML model...")
        result = run_agent(input_data)
        st.write(f"✅ Price: £{result['price']:,.2f}")

        st.write("📚 **Step 2:** Retrieved market insights via RAG")
        st.write("🤖 **Step 3:** Generated advisory report via LLM")

        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)

    # --- Predicted Price ---
    st.markdown(f"""
    <div class="price-display">
            <div class="label">Predicted Property Price</div>
            <div class="amount">£{result['price']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🤖 AI Advisory Report")
    st.markdown(result["advice"])