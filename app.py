import streamlit as st
import time
import json
from pathlib import Path

# Configuration
HISTORY_FILE = Path("conversion_history.json")

# Load history from file if available
def load_history():
    if HISTORY_FILE.exists():
        try:
            with HISTORY_FILE.open("r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")
    return []

# Save history to file
def save_history(history):
    try:
        with HISTORY_FILE.open("w") as f:
            json.dump(history, f)
    except Exception as e:
        st.error(f"Error saving history: {str(e)}")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = load_history()
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "Currency"
if 'precision' not in st.session_state:
    st.session_state.precision = 4
if "swap" not in st.session_state:
    st.session_state.swap = False

# Page configuration
st.set_page_config(
    page_title="Universal Converter Pro",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Conversion Data with PKR added for Currency
conversion_data = {
    "Currency": {
        "units": ["USD", "EUR", "GBP", "JPY", "CNY", "INR", "AUD", "CAD", "PKR"],
        "rates": {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "JPY": 148.36,
            "CNY": 7.18,
            "INR": 83.12,
            "AUD": 1.54,
            "CAD": 1.35,
            "PKR": 285.0
        }
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"]
    },
    "Digital Storage": {
        "units": ["Bit", "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte"],
        "factors": {
            "Bit": 1,
            "Byte": 8,
            "Kilobyte": 8192,       # 8 * 1024
            "Megabyte": 8388608,     # 8 * 1024^2
            "Gigabyte": 8589934592,  # 8 * 1024^3
            "Terabyte": 8796093022208  # 8 * 1024^4
        }
    },
    "Scientific": {
        "units": ["Meter", "Kilometer", "Centimeter", "Millimeter",
                  "Kilogram", "Gram", "Milligram",
                  "Second", "Minute", "Hour"],
        "factors": {
            "Meter": 1,
            "Kilometer": 0.001,
            "Centimeter": 100,
            "Millimeter": 1000,
            "Kilogram": 1,
            "Gram": 1000,
            "Milligram": 1e6,
            "Second": 1,
            "Minute": 1/60,
            "Hour": 1/3600
        }
    }
}

# Helper to safely rerun the app
def safe_rerun():
    try:
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        elif hasattr(st, "rerun"):
            st.rerun()
        else:
            raise AttributeError("No rerun function available in Streamlit.")
    except Exception as e:
        st.error(f"Rerun failed: {str(e)}")

# Set swap flag and trigger rerun
def swap_units(category):
    st.session_state.swap = True
    safe_rerun()

# Apply custom theme via CSS
def apply_theme():
    theme = st.session_state.theme
    st.markdown(f"""
    <style>
    :root {{
        --primary: #6C63FF;
        --secondary: #FF6584;
        --accent: #4CAF50;
        --background: {'#f8f9fa' if theme == "light" else '#0a0a0a'};
        --text: {'#2d3436' if theme == "light" else '#f5f6fa'};
        --card-bg: {'#ffffff' if theme == "light" else '#1a1a1a'};
        --shadow: {'0 8px 32px rgba(0, 0, 0, 0.1)' if theme == "light" else '0 8px 32px rgba(0, 0, 0, 0.3)'};
    }}
    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
        100% {{ transform: translateY(0px); }}
    }}
    @keyframes fadeIn {{
        0% {{ opacity: 0; transform: translateY(10px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .stApp {{
        background: var(--background);
        color: var(--text);
        transition: all 0.3s ease;
    }}
    .main-card {{
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: var(--shadow);
        animation: fadeIn 0.6s ease-out;
        border: 1px solid rgba(108, 99, 255, 0.1);
        position: relative;
        overflow: hidden;
    }}
    .main-card::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(108, 99, 255, 0.1), transparent 30%);
        animation: rotate 4s linear infinite;
    }}
    @keyframes rotate {{
        100% {{ transform: rotate(360deg); }}
    }}
    .stButton > button {{
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white !important;
        border-radius: 12px;
        padding: 12px 28px;
        border: none;
        transition: all 0.3s ease;
        font-weight: 600;
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
    }}
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: 0.5s;
    }}
    .stButton > button:hover::before {{
        left: 100%;
    }}
    .header-animation {{
        animation: float 3s ease-in-out infinite;
        text-align: center;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .conversion-result {{
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: fadeIn 0.4s ease-out;
    }}
    .history-item {{
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        background: rgba(108, 99, 255, 0.05);
        transition: all 0.3s ease;
        cursor: pointer;
        border-left: 3px solid var(--primary);
    }}
    .history-item:hover {{
        transform: translateX(8px);
        box-shadow: var(--shadow);
    }}
    @media (max-width: 768px) {{
        .main-card {{
            padding: 1.5rem;
            margin: 0.5rem 0;
        }}
        .stButton > button {{
            width: 100%;
            margin: 8px 0;
        }}
        .conversion-result {{
            font-size: 1.5rem;
        }}
        [data-testid="column"] {{
            width: 100% !important;
            padding: 0.5rem !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    apply_theme()

# Conversion Functions
def convert_units(value, category, from_unit, to_unit):
    try:
        if category == "Currency":
            if from_unit == to_unit:
                return value, ""
            rate = conversion_data["Currency"]["rates"][to_unit] / conversion_data["Currency"]["rates"][from_unit]
            return value * rate, f"{value} {from_unit} × {rate:.4f}"
        
        elif category == "Temperature":
            if from_unit == "Celsius":
                if to_unit == "Fahrenheit":
                    return (value * 9/5) + 32, f"({value} × 9/5) + 32"
                elif to_unit == "Kelvin":
                    return value + 273.15, f"{value} + 273.15"
            elif from_unit == "Fahrenheit":
                if to_unit == "Celsius":
                    return (value - 32) * 5/9, f"({value} - 32) × 5/9"
                elif to_unit == "Kelvin":
                    return (value - 32) * 5/9 + 273.15, f"({value} - 32) × 5/9 + 273.15"
            elif from_unit == "Kelvin":
                if to_unit == "Celsius":
                    return value - 273.15, f"{value} - 273.15"
                elif to_unit == "Fahrenheit":
                    return (value - 273.15) * 9/5 + 32, f"({value} - 273.15) × 9/5 + 32"
            return None, "Unsupported temperature conversion"
        
        elif category == "Digital Storage":
            try:
                factor = conversion_data["Digital Storage"]["factors"][from_unit] / conversion_data["Digital Storage"]["factors"][to_unit]
                return value * factor, f"{value} × {factor}"
            except KeyError as e:
                return None, f"Digital Storage conversion error: {str(e)}"
        
        elif category == "Scientific":
            # Ensure both units belong to the same measurement type.
            categories = {
                "Meter": "length", "Kilometer": "length", "Centimeter": "length", "Millimeter": "length",
                "Kilogram": "mass", "Gram": "mass", "Milligram": "mass",
                "Second": "time", "Minute": "time", "Hour": "time"
            }
            if categories.get(from_unit) != categories.get(to_unit):
                return None, "⚠️ Incompatible units"
            try:
                factor = conversion_data["Scientific"]["factors"][to_unit] / conversion_data["Scientific"]["factors"][from_unit]
                return value * factor, f"{value} × {factor}"
            except KeyError as e:
                return None, f"Scientific conversion error: {str(e)}"
        
        return None, "Invalid category"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"

# Session State Management
def init_session_state(category):
    key_from = f"{category}_from"
    key_to = f"{category}_to"
    if key_from not in st.session_state:
        st.session_state[key_from] = conversion_data[category]["units"][0]
    if key_to not in st.session_state:
        st.session_state[key_to] = conversion_data[category]["units"][1]

# Premium Sidebar with Clear History functionality
def premium_sidebar():
    with st.sidebar:
        st.markdown(
            "<div class='header-animation' style='margin-bottom: 2rem;'>"
            "<h1 style='font-size: 2.5rem; margin: 0;'>🌐 Universal Converter</h1>"
            "<p style='margin: 0; font-size: 1.1rem;'>Your All-in-One Conversion Solution</p>"
            "</div>", unsafe_allow_html=True)
        st.button(f"🌓 {'Dark' if st.session_state.theme == 'light' else 'Light'} Mode",
                  on_click=toggle_theme, use_container_width=True)
        st.markdown("---")
        st.session_state.precision = st.slider("🔢 Decimal Precision", 0, 8, st.session_state.precision)
        st.markdown("---")
        st.markdown("### 📦 Conversion Categories")
        categories = {
            "💱 Currency": "Currency",
            "🌡️ Temperature": "Temperature",
            "💻 Digital Storage": "Digital Storage",
            "🔬 Scientific": "Scientific"
        }
        for btn_text, cat in categories.items():
            if st.button(btn_text, use_container_width=True, key=f"cat_{cat}"):
                st.session_state.selected_category = cat
        st.markdown("---")
        st.markdown("### 📜 Conversion History")
        if st.session_state.history:
            for entry in reversed(st.session_state.history[-5:]):
                st.markdown(f'<div class="history-item">{entry}</div>', unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; color: #666; padding: 1rem;'>No conversions yet</div>",
                        unsafe_allow_html=True)
        if st.button("Clear History", key="clear_history", use_container_width=True):
            st.session_state.history = []
            save_history(st.session_state.history)
            st.experimental_rerun()

# Main Interface
def animated_interface():
    apply_theme()
    category = st.session_state.selected_category
    init_session_state(category)
    
    # Swap values if flag is set
    if st.session_state.get("swap", False):
        key_from = f"{category}_from"
        key_to = f"{category}_to"
        st.session_state[key_from], st.session_state[key_to] = st.session_state[key_to], st.session_state[key_from]
        st.session_state.swap = False

    st.markdown(
        "<div class='header-animation' style='margin-bottom: 2rem;'>"
        "<h1 style='font-size: 2.5rem; margin: 0;'>Universal Converter Pro</h1>"
        "<p style='margin: 0; font-size: 1.2rem;'>World's Most Advanced Conversion Tool</p>"
        "</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([3, 1, 3])
        with col1:
            from_unit = st.selectbox("From Unit", conversion_data[category]["units"],
                                      key=f"{category}_from")
        with col2:
            st.markdown(
                "<div style='display: flex; height: 100%; align-items: center; justify-content: center;'>"
                "<div style='transform: rotate(90deg); margin: 2rem 0;'>🔄</div></div>",
                unsafe_allow_html=True)
            if st.button("Swap Units", key=f"{category}_swap", use_container_width=True):
                swap_units(category)
        with col3:
            to_unit = st.selectbox("To Unit", conversion_data[category]["units"],
                                    key=f"{category}_to")
        
        try:
            value = st.number_input("Enter Value", value=1.0, key=f"{category}_value")
        except Exception as e:
            st.error(f"Invalid input: {str(e)}")
            return
        
        if st.button("Convert Now", type="primary", use_container_width=True, key=f"{category}_convert"):
            with st.spinner('Converting...'):
                time.sleep(0.1)  # Reduced sleep time for better responsiveness
                result, formula = convert_units(value, category, from_unit, to_unit)
                if result is not None:
                    try:
                        precision = st.session_state.precision
                        entry = f"{value:.{precision}f} {from_unit} → {result:.{precision}f} {to_unit}"
                        st.session_state.history.append(entry)
                        save_history(st.session_state.history)
                        st.markdown(f"""
                        <div style='margin-top: 2rem;'>
                            <div class='conversion-result'>
                                {result:.{precision}f} {to_unit}
                            </div>
                            <div style='color: #666; margin-top: 1rem;'>
                                🧮 Formula: {formula}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying result: {str(e)}")
                else:
                    st.error(formula)
        st.markdown("</div>", unsafe_allow_html=True)

# Main App
def main():
    try:
        premium_sidebar()
        animated_interface()
    except Exception as e:
        st.error(f"An unexpected error occurred in the app: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()
