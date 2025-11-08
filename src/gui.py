import streamlit as st
import json
import os
import sys
import subprocess
import platform

# Add version
__version__ = "1.9.0"

# Page config
st.set_page_config(
    page_title="SPAMURAI 🥷⚡",
    page_icon="🥷",  # Ninja icon
    layout="centered",  # Changed from "wide" to "centered" for compact view
    initial_sidebar_state="collapsed"
)

# Custom CSS for compact layout with Launch Strike theme
st.markdown("""
    <style>
    /* Compact layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
    }
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }
    h1 {
        padding-top: 0.5rem;
        margin-top: 0;
        line-height: 1.4;
    }
    h2 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        font-size: 1.3rem;
    }
    h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .stTextInput > label, .stNumberInput > label {
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
    }
    .stButton > button {
        width: 100%;
    }

    /* Launch Strike Theme for Run Campaign button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #D72638 0%, #F25C05 100%) !important;
        color: #F5F5F0 !important;
        border: 2px solid #F25C05 !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(215, 38, 56, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #F25C05 0%, #D72638 100%) !important;
        box-shadow: 0 6px 20px rgba(242, 92, 5, 0.6) !important;
        transform: translateY(-2px) !important;
        border-color: #D72638 !important;
    }

    .stButton > button[kind="primary"]:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 8px rgba(215, 38, 56, 0.5) !important;
    }

    /* Save button styling (secondary) */
    .stButton > button[kind="secondary"] {
        background-color: #2C2C2C !important;
        color: #F5F5F0 !important;
        border: 1px solid #4A4A4A !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #3D3D3D !important;
        border-color: #6A6A6A !important;
    }

    /* Ninja animation for expander */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(215, 38, 56, 0.1) 0%, rgba(242, 92, 5, 0.1) 100%) !important;
        border-left: 3px solid #D72638 !important;
        border-radius: 4px !important;
        transition: all 0.3s ease !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(90deg, rgba(215, 38, 56, 0.2) 0%, rgba(242, 92, 5, 0.2) 100%) !important;
        border-left: 4px solid #F25C05 !important;
        transform: translateX(4px) !important;
    }

    .streamlit-expanderContent {
        border-left: 3px solid rgba(242, 92, 5, 0.3) !important;
        padding-left: 1rem !important;
        animation: slideDown 0.3s ease-out !important;
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load existing config or use example
def load_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    elif os.path.exists("config.example.json"):
        with open("config.example.json", "r") as f:
            return json.load(f)
    else:
        # Default config
        return {
            "google_sheets_config": {
                "messages": {"sheet_url": "", "tab_name": "Sheet1"},
                "contacts": {"sheet_url": "", "tab_name": "Sheet1"}
            },
            "followup_config": {"enabled": True, "delay_seconds": 3},
            "default_delay": 15,
            "log_file": "config/whatsapp.log",
            "exclude_file": "config/exclude.txt",
            "sent_numbers_file": "config/sent_numbers.log",
            "error_numbers_file": "config/failed_numbers.log",
            "chrome_user_data": "/tmp/WhatsAppSession/Session1",
            "timeouts": {"100": 30, "300": 30}
        }

def save_config(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = load_config()

config = st.session_state.config

# Header
st.title("🥷⚡ SPAMURAI")
st.caption("Strike fast. Strike precise. Leave no trace.")

# Tabs
tab1, tab2, tab3 = st.tabs(["⚔️ Prepare Your Weapons", "🎯 Advanced Tactics", "📜 Ninja Codex"])

# ============================================================================
# TAB 1: Campaign Setup
# ============================================================================
with tab1:
    # Google Sheets Configuration
    st.markdown("### 📊 Google Sheets")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Messages Sheet**")
        messages_url = st.text_input(
            "Messages Sheet URL",
            value=config.get("google_sheets_config", {}).get("messages", {}).get("sheet_url", ""),
            placeholder="Paste your Google Sheets URL here...",
            key="messages_url",
            label_visibility="collapsed"
        )
        messages_tab = st.text_input(
            "Tab Name",
            value=config.get("google_sheets_config", {}).get("messages", {}).get("tab_name", "Sheet1"),
            key="messages_tab"
        )

    with col2:
        st.markdown("**Contacts Sheet**")
        contacts_url = st.text_input(
            "Contacts Sheet URL",
            value=config.get("google_sheets_config", {}).get("contacts", {}).get("sheet_url", ""),
            placeholder="Paste your Google Sheets URL here...",
            key="contacts_url",
            label_visibility="collapsed"
        )
        contacts_tab = st.text_input(
            "Tab Name",
            value=config.get("google_sheets_config", {}).get("contacts", {}).get("tab_name", "Sheet1"),
            key="contacts_tab"
        )

    # Campaign Settings
    st.markdown("### ⏱️ Campaign Settings")

    default_delay = st.number_input(
        "Default Delay (seconds between messages)",
        min_value=1,
        max_value=300,
        value=config.get("default_delay", 15),
        help="Time to wait between sending messages to different contacts"
    )

    # Action Buttons
    st.markdown("")  # Small spacing
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Configuration", use_container_width=True, type="secondary"):
            # Update config
            config["google_sheets_config"]["messages"]["sheet_url"] = messages_url
            config["google_sheets_config"]["messages"]["tab_name"] = messages_tab
            config["google_sheets_config"]["contacts"]["sheet_url"] = contacts_url
            config["google_sheets_config"]["contacts"]["tab_name"] = contacts_tab
            config["default_delay"] = default_delay

            # Save to file
            save_config(config)
            st.session_state.config = config
            st.success("✅ Configuration saved successfully!")

    with col2:
        if st.button("⚡ Launch Strike", use_container_width=True, type="primary"):
            # Validate required fields
            if not messages_url or not contacts_url:
                st.error("🚫 Strike aborted! Enter Google Sheets URLs first.")
            else:
                # Auto-save config before launching
                config["google_sheets_config"]["messages"]["sheet_url"] = messages_url
                config["google_sheets_config"]["messages"]["tab_name"] = messages_tab
                config["google_sheets_config"]["contacts"]["sheet_url"] = contacts_url
                config["google_sheets_config"]["contacts"]["tab_name"] = contacts_tab
                config["default_delay"] = default_delay
                save_config(config)
                st.session_state.config = config

                # Show saving confirmation
                with st.spinner("⚙️ Preparing strike..."):
                    import time
                    time.sleep(0.5)

                # Launch terminal with the broadcaster
                try:
                    if platform.system() == "Windows":
                        subprocess.Popen(['start', 'cmd', '/k', 'python', 'src/wa_broadcaster.py', '--config', 'config.json'], shell=True)
                    elif platform.system() == "Darwin":  # macOS
                        script_path = os.path.abspath('src/wa_broadcaster.py')
                        config_path = os.path.abspath('config.json')
                        subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "cd {os.getcwd()} && python3 {script_path} --config {config_path}"'])
                    else:  # Linux
                        subprocess.Popen(['x-terminal-emulator', '-e', 'python3', 'src/wa_broadcaster.py', '--config', 'config.json'])

                    st.success("⚡ Strike launched! Terminal opened. Unleash with honor, SPAMURAI!")
                except Exception as e:
                    st.error(f"🚫 Strike failed: {str(e)}")

# ============================================================================
# TAB 2: Advanced Settings
# ============================================================================
with tab2:
    # Followup Configuration
    st.markdown("### 📨 Followup Messages")

    followup_enabled = st.checkbox(
        "Enable followup messages",
        value=config.get("followup_config", {}).get("enabled", True),
        help="Send a second message immediately after the first"
    )

    followup_delay = st.number_input(
        "Followup delay (seconds)",
        min_value=1,
        max_value=60,
        value=config.get("followup_config", {}).get("delay_seconds", 3),
        help="Time to wait before sending the followup message"
    )

    # Chrome Settings
    st.markdown("### 🌐 Chrome Settings")

    chrome_user_data = st.text_input(
        "Chrome User Data Path",
        value=config.get("chrome_user_data", "/tmp/WhatsAppSession/Session1"),
        help="Path to Chrome profile directory for persistent WhatsApp Web session"
    )

    # File Paths
    st.markdown("### 📁 File Paths")

    col1, col2 = st.columns(2)

    with col1:
        log_file = st.text_input("Log File", value=config.get("log_file", "config/whatsapp.log"))
        sent_file = st.text_input("Sent Numbers File", value=config.get("sent_numbers_file", "config/sent_numbers.log"))

    with col2:
        error_file = st.text_input("Error Numbers File", value=config.get("error_numbers_file", "config/failed_numbers.log"))
        exclude_file = st.text_input("Exclude File", value=config.get("exclude_file", "config/exclude.txt"))

    # Timeouts
    st.markdown("### ⏸️ Timeouts")
    st.caption("Pause the campaign after sending X messages to avoid rate limiting")

    col1, col2 = st.columns(2)

    timeouts = config.get("timeouts", {"100": 30, "300": 30})

    with col1:
        timeout_1_msg = st.number_input("After messages", value=100, min_value=1, key="timeout_1_msg")
        timeout_2_msg = st.number_input("After messages", value=300, min_value=1, key="timeout_2_msg")

    with col2:
        timeout_1_min = st.number_input("Wait (minutes)", value=timeouts.get("100", 30), min_value=1, key="timeout_1_min")
        timeout_2_min = st.number_input("Wait (minutes)", value=timeouts.get("300", 30), min_value=1, key="timeout_2_min")

    # Save Advanced Settings
    st.markdown("")  # Small spacing
    if st.button("💾 Save Advanced Settings", use_container_width=True):
        config["followup_config"]["enabled"] = followup_enabled
        config["followup_config"]["delay_seconds"] = followup_delay
        config["chrome_user_data"] = chrome_user_data
        config["log_file"] = log_file
        config["sent_numbers_file"] = sent_file
        config["error_numbers_file"] = error_file
        config["exclude_file"] = exclude_file
        config["timeouts"] = {
            str(timeout_1_msg): timeout_1_min,
            str(timeout_2_msg): timeout_2_min
        }

        save_config(config)
        st.session_state.config = config
        st.success("✅ Advanced settings saved successfully!")

# ============================================================================
# TAB 3: About
# ============================================================================
with tab3:
    st.markdown(f"""
    ### The Way of the Digital Ninja

    **Version:** {__version__}

    > *"Strike fast. Strike precise. Leave no trace."*

    SPAMURAI is the ultimate WhatsApp broadcast weapon, combining ancient ninja precision
    with modern automation power. Master your campaigns with honor and stealth.

    ---

    ### ⚔️ Arsenal
    - 📊 **Google Sheets Mastery** - Command center for messages and contacts
    - 🎲 **Random Strike Patterns** - Unique message combinations for stealth
    - ⚡ **Lightning Execution** - Launch strikes with a single click
    - ⏱️ **Tactical Delays** - Evade detection with smart timing
    - 📈 **Battle Analytics** - Track your campaign victories
    - 🛡️ **Rate Limit Shield** - Automatic protection from detection

    ---
    """)

    with st.expander("⚡ Strike Sequence", expanded=False):
        st.markdown("""
        1. **Prepare Your Weapons** (Campaign Setup tab)
           - Paste your Google Sheets URLs for messages and contacts
           - Set your default delay between strikes

        2. **Configure Advanced Tactics** (Advanced tab - optional)
           - Enable followup messages for double strikes
           - Adjust timeout intervals for stealth mode
           - Customize file paths and Chrome settings

        3. **Launch Your Strike** ⚡
           - Click "Launch Strike" to auto-save and begin
           - Terminal opens with live battle logs
           - Watch your campaign execute with precision
        """)

    st.markdown("""
    ---

    ### 🥋 The Code
    Forged with Python, Selenium, and Streamlit

    *Train hard. Strike harder. Disappear without a trace.* 🥷
    """)
