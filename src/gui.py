import streamlit as st
import json
import os
import sys
import subprocess
import platform
from lib import normalize_phone

# Add version
__version__ = "1.10.2"

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

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_config():
    """Load configuration from config.json or config.example.json"""
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            return json.load(f)
    elif os.path.exists("config.example.json"):
        with open("config.example.json", "r") as f:
            return json.load(f)
    else:
        # Default config
        return {
            "user_profile": {
                "name": "",
                "phone_number": ""
            },
            "google_sheets_config": {
                "messages": {"sheet_url": "", "tab_name": "Sheet1"},
                "contacts": {"sheet_url": "", "tab_name": "Sheet1"}
            },
            "followup_config": {"enabled": True, "delay_seconds": 3},
            "default_delay": 60,
            "log_file": "config/whatsapp.log",
            "exclude_file": "config/exclude.txt",
            "sent_numbers_file": "config/sent_numbers.log",
            "error_numbers_file": "config/failed_numbers.log",
            "chrome_user_data": "/tmp/WhatsAppSession/Session1",
            "timeouts": {"100": 30, "300": 30}
        }

def save_config(config):
    """Save configuration to config.json"""
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

def get_nested_config(config, *keys, default=""):
    """Safely extract nested config value with multiple .get() calls

    Args:
        config: Configuration dictionary
        *keys: Variable number of nested keys to traverse
        default: Default value if any key is missing

    Returns:
        Value at nested path or default

    Example:
        get_nested_config(config, "google_sheets_config", "messages", "sheet_url")
        # Instead of: config.get("google_sheets_config", {}).get("messages", {}).get("sheet_url", "")
    """
    result = config
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, {})
        else:
            return default
    return result if result != {} else default

def update_sheets_config(config, messages_url, messages_tab, contacts_url, contacts_tab, delay):
    """Update Google Sheets configuration

    Args:
        config: Configuration dictionary to update
        messages_url: Messages sheet URL
        messages_tab: Messages sheet tab name
        contacts_url: Contacts sheet URL
        contacts_tab: Contacts sheet tab name
        delay: Default delay between messages
    """
    config["google_sheets_config"]["messages"]["sheet_url"] = messages_url
    config["google_sheets_config"]["messages"]["tab_name"] = messages_tab
    config["google_sheets_config"]["contacts"]["sheet_url"] = contacts_url
    config["google_sheets_config"]["contacts"]["tab_name"] = contacts_tab
    config["default_delay"] = delay

def save_and_update_session(config, success_message=None):
    """Save config to file and update session state

    Args:
        config: Configuration dictionary
        success_message: Optional success message to display
    """
    save_config(config)
    st.session_state.config = config
    if success_message:
        st.success(success_message)


def read_exclude_file(path):
    """Read exclude file and return list of stripped lines"""
    if not path:
        return []
    try:
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        st.error(f"Could not read exclude file: {e}")
        return []


def write_exclude_file(path, numbers):
    """Write list of numbers to exclude file (one per line)"""
    if not path:
        st.error("Exclude file path is not configured.")
        return False
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            for n in numbers:
                f.write(f"{n}\n")
        return True
    except Exception as e:
        st.error(f"Failed to write exclude file: {e}")
        return False

def launch_terminal_process(script_path, config_path):
    """Launch wa_broadcaster.py in a new terminal window

    Args:
        script_path: Absolute path to wa_broadcaster.py
        config_path: Absolute path to config.json

    Returns:
        subprocess.Popen object or None if failed
    """
    try:
        if platform.system() == "Windows":
            # Use CREATE_NEW_CONSOLE flag to properly detach the process
            # Close pipes to prevent deadlock when parent doesn't read them
            # process = subprocess.Popen(
            #     ['cmd', '/k', 'python', script_path, '--config', config_path],
            #     creationflags=subprocess.CREATE_NEW_CONSOLE,
            #     stdin=subprocess.DEVNULL,
            #     stdout=subprocess.DEVNULL,
            #     stderr=subprocess.DEVNULL
            # )
            command = ' '.join(['python', script_path, '--config', config_path])
            print("Executing system command", command)
            os.system(command)

        elif platform.system() == "Darwin":  # macOS
            process = subprocess.Popen([
                'osascript', '-e',
                f'tell application "Terminal" to do script "cd {os.getcwd()} && python3 {script_path} --config {config_path}"'
            ])
        else:  # Linux
            process = subprocess.Popen([
                'x-terminal-emulator', '-e',
                'python3', script_path, '--config', config_path
            ])
        return process
    except Exception as e:
        raise Exception(f"Failed to launch terminal: {str(e)}")

# ============================================================================
# MAIN APP
# ============================================================================

# Initialize session state
if 'config' not in st.session_state:
    st.session_state.config = load_config()

if 'process' not in st.session_state:
    st.session_state.process = None

config = st.session_state.config

# Header
st.title("🥷⚡ SPAMURAI")
st.caption("Each strike opens a window. Each message a potential possibility")

# Initialize default values for advanced settings (used in Tab 2 but defined in Tab 3)
# This prevents NameError if user clicks "Launch Strike" without visiting Tab 3
override_enabled = get_nested_config(config, "message_override", "enabled", default=False)
override_source = get_nested_config(config, "message_override", "source", default="sadhguru_quote")
quick_message_text = get_nested_config(config, "message_override", "quick_message_text", default="")
followup_enabled = get_nested_config(config, "followup_config", "enabled", default=True)
followup_delay = get_nested_config(config, "followup_config", "delay_seconds", default=3)
chrome_user_data = config.get("chrome_user_data", "/tmp/WhatsAppSession/Session1")
log_file = config.get("log_file", "config/whatsapp.log")
sent_file = config.get("sent_numbers_file", "config/sent_numbers.log")
error_file = config.get("error_numbers_file", "config/failed_numbers.log")
exclude_file = config.get("exclude_file", "config/exclude.txt")
timeouts = config.get("timeouts", {"100": 30, "300": 30})
timeout_1_msg = 100
timeout_2_msg = 300
timeout_1_min = timeouts.get("100", 30)
timeout_2_min = timeouts.get("300", 30)

# Tabs
tab1, tab2, tab3 = st.tabs(["📜 Ninja Codex", "⚔️ Prepare Your Weapons", "🎯 Advanced Tactics"])

# ============================================================================
# TAB 1: Ninja Codex (About)
# ============================================================================
with tab1:
    st.markdown(f"""
    ### The Craft of the Spiritual Nurturer

    **Version:** {__version__}

    > *"Each strike opens a window. Each message a potential possibility"*

    > *Experience SPAMURAI as a ninja-nurturer, carrying one carefully crafted drop of consciousness through every message.*
    > *Each message becomes an act of awareness, a quiet moment of stillness carried through action.*

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

    *Align within. Strike with awareness. Slip back into stillness.* 🥷
    """)

# ============================================================================
# TAB 2: Campaign Setup
# ============================================================================
with tab2:
    # User Profile Section (Mandatory)
    st.markdown("### 👤 User Profile")
    st.caption("Your identity - required for all campaigns")

    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input(
            "Your Name *",
            value=get_nested_config(config, "user_profile", "name", default=""),
            placeholder="Enter your full name...",
            help="This will be used as your default nickname"
        )

    with col2:
        user_phone = st.text_input(
            "Your Phone Number *",
            value=get_nested_config(config, "user_profile", "phone_number", default=""),
            placeholder="Enter your 10-digit phone number...",
            help="This will be used as the test number for campaigns"
        )

    # Validation messages
    validation_errors = []
    if user_name and len(user_name.strip()) < 2:
        validation_errors.append("❌ Name must be at least 2 characters")

    if user_phone:
        try:
            normalized_phone = normalize_phone(user_phone)
            if len(normalized_phone) != 10:
                validation_errors.append("❌ Phone number must be exactly 10 digits")
        except Exception:
            validation_errors.append("❌ Invalid phone number format")

    if validation_errors:
        for error in validation_errors:
            st.error(error)

    st.markdown("---")

    # Google Sheets Configuration
    st.markdown("### 📊 Google Sheets")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Messages Sheet**")
        messages_url = st.text_input(
            "Messages Sheet URL",
            value=get_nested_config(config, "google_sheets_config", "messages", "sheet_url"),
            placeholder="Paste your Google Sheets URL here...",
            key="messages_url",
            label_visibility="collapsed"
        )
        messages_tab = st.text_input(
            "Tab Name",
            value=get_nested_config(config, "google_sheets_config", "messages", "tab_name", default="Sheet1"),
            key="messages_tab"
        )

    with col2:
        st.markdown("**Contacts Sheet**")
        contacts_url = st.text_input(
            "Contacts Sheet URL",
            value=get_nested_config(config, "google_sheets_config", "contacts", "sheet_url"),
            placeholder="Paste your Google Sheets URL here...",
            key="contacts_url",
            label_visibility="collapsed"
        )
        contacts_tab = st.text_input(
            "Tab Name",
            value=get_nested_config(config, "google_sheets_config", "contacts", "tab_name", default="Sheet1"),
            key="contacts_tab"
        )

    # Campaign Settings
    st.markdown("### ⏱️ Campaign Settings")

    default_delay = st.number_input(
        "Default Delay (seconds between messages)",
        min_value=1,
        max_value=300,
        value=config.get("default_delay", 60),
        help="Time to wait between sending messages to different contacts"
    )

    # Action Buttons
    st.markdown("")  # Small spacing
    col1, col2 = st.columns(2)

    with col1:
        if st.button("💾 Save Configuration", use_container_width=True, type="secondary"):
            # Validate user profile
            if not user_name or not user_name.strip():
                st.error("🚫 Name is required!")
            elif not user_phone or not user_phone.strip():
                st.error("🚫 Phone number is required!")
            elif validation_errors:
                st.error("🚫 Fix validation errors before saving!")
            else:
                # Save user profile
                if "user_profile" not in config:
                    config["user_profile"] = {}

                config["user_profile"]["name"] = user_name.strip()
                config["user_profile"]["phone_number"] = normalize_phone(user_phone)

                # Update sheets config
                update_sheets_config(config, messages_url, messages_tab, contacts_url, contacts_tab, default_delay)

                # Save to file and update session
                save_and_update_session(config, "✅ Configuration saved successfully!")

    with col2:
        if st.button("⚡ Launch Strike", use_container_width=True, type="primary"):
            # Validate user profile first
            if not user_name or not user_name.strip():
                st.error("🚫 Strike aborted! Enter your name first.")
            elif not user_phone or not user_phone.strip():
                st.error("🚫 Strike aborted! Enter your phone number first.")
            elif validation_errors:
                st.error("🚫 Strike aborted! Fix validation errors first.")
            elif not messages_url or not contacts_url:
                st.error("🚫 Strike aborted! Enter Google Sheets URLs first.")
            else:
                # Save user profile
                if "user_profile" not in config:
                    config["user_profile"] = {}

                config["user_profile"]["name"] = user_name.strip()
                config["user_profile"]["phone_number"] = normalize_phone(user_phone)

                # Auto-save config before launching (including advanced tactics)
                update_sheets_config(config, messages_url, messages_tab, contacts_url, contacts_tab, default_delay)

                # Save advanced tactics configuration
                if "message_override" not in config:
                    config["message_override"] = {}
                config["message_override"]["enabled"] = override_enabled
                if override_enabled:
                    config["message_override"]["source"] = override_source
                    if override_source == "quick_message":
                        config["message_override"]["quick_message_text"] = quick_message_text

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

                save_and_update_session(config)

                # Show saving confirmation
                with st.spinner("⚙️ Preparing strike..."):
                    import time
                    time.sleep(0.5)

                # Launch terminal with the broadcaster
                try:
                    script_path = os.path.abspath('src/wa_broadcaster.py')
                    config_path = os.path.abspath('config.json')

                    process = launch_terminal_process(script_path, config_path)
                    st.session_state.process = process

                    st.success("⚡ Strike launched! Terminal opened. Unleash with honor, SPAMURAI!")
                except Exception as e:
                    st.error(f"🚫 Strike failed: {str(e)}")

# ============================================================================
# TAB 3: Advanced Settings
# ============================================================================
with tab3:
    # Message Override Configuration
    st.markdown("### 🎯 Message Override")
    st.caption("Override Google Sheets messages with alternative sources")

    override_enabled = st.checkbox(
        "Override Google Sheet Messages",
        value=override_enabled,
        help="When enabled, use alternative message source instead of Messages Google Sheet"
    )

    # Only show override options when checkbox is enabled
    if override_enabled:
        override_source = st.radio(
            "Select Message Source",
            options=["sadhguru_quote", "quick_message"],
            format_func=lambda x: "🕉️ Sadhguru Quote" if x == "sadhguru_quote" else "✉️ Quick Message",
            index=0 if override_source == "sadhguru_quote" else 1,
            help="Choose your message source"
        )

        # Show text box only for quick_message option
        if override_source == "quick_message":
            quick_message_text = st.text_area(
                "Quick Message",
                value=quick_message_text,
                placeholder="Enter your message here...",
                height=150,
                help="This message will be sent to all contacts"
            )

    st.markdown("---")

    # Followup Configuration
    st.markdown("### 📨 Followup Messages")

    followup_enabled = st.checkbox(
        "Enable followup messages",
        value=followup_enabled,
        help="Send a second message immediately after the first"
    )

    followup_delay = st.number_input(
        "Followup delay (seconds)",
        min_value=1,
        max_value=60,
        value=followup_delay,
        help="Time to wait before sending the followup message"
    )

    # Chrome Settings
    st.markdown("### 🌐 Chrome Settings")

    chrome_user_data = st.text_input(
        "Chrome User Data Path",
        value=chrome_user_data,
        help="Path to Chrome profile directory for persistent WhatsApp Web session"
    )

    # File Paths
    st.markdown("### 📁 File Paths")

    col1, col2 = st.columns(2)

    with col1:
        log_file = st.text_input("Log File", value=log_file)
        sent_file = st.text_input("Sent Numbers File", value=sent_file)

    with col2:
        error_file = st.text_input("Error Numbers File", value=error_file)
        exclude_file = st.text_input("Exclude File", value=exclude_file)

    # Timeouts
    st.markdown("### ⏸️ Timeouts")
    st.caption("Pause the campaign after sending X messages to avoid rate limiting")

    col1, col2 = st.columns(2)

    with col1:
        timeout_1_msg = st.number_input("After messages", value=timeout_1_msg, min_value=1, key="timeout_1_msg")
        timeout_2_msg = st.number_input("After messages", value=timeout_2_msg, min_value=1, key="timeout_2_msg")

    with col2:
        timeout_1_min = st.number_input("Wait (minutes)", value=timeout_1_min, min_value=1, key="timeout_1_min")
        timeout_2_min = st.number_input("Wait (minutes)", value=timeout_2_min, min_value=1, key="timeout_2_min")

    # Save Advanced Settings
    st.markdown("")  # Small spacing
    if st.button("💾 Save Advanced Settings", use_container_width=True):
        # Message Override Configuration
        if "message_override" not in config:
            config["message_override"] = {}

        config["message_override"]["enabled"] = override_enabled
        if override_enabled:
            config["message_override"]["source"] = override_source
            if override_source == "quick_message":
                config["message_override"]["quick_message_text"] = quick_message_text

        # Followup Configuration
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

        save_and_update_session(config, "✅ Advanced settings saved successfully!")

    # ===================== Exclude List UI (End of page) =====================
    st.markdown("---")
    st.markdown("### 🔒 Exclude List")
    st.caption("View and manage numbers that will be skipped by campaigns")

    # Use the local exclude_file input value (not yet saved) so user can manage the intended file
    current_exclude_path = exclude_file or config.get("exclude_file", "config/exclude.txt")

    # Add numbers section
    st.markdown("#### Add Numbers to Exclude")
    new_excludes = st.text_input("Enter number(s) to exclude (comma-separated)")
    if st.button("➕ Add to Exclude", use_container_width=True):
        if not new_excludes.strip():
            st.warning("Enter at least one phone number to add.")
        else:
            excludes = read_exclude_file(current_exclude_path)
            raw_list = [s.strip() for s in new_excludes.split(',') if s.strip()]
            normalized = []
            for raw in raw_list:
                try:
                    norm = normalize_phone(raw)
                except Exception:
                    # Fallback simple normalization
                    norm = raw.replace('.0', '').strip()
                if norm not in excludes and norm not in normalized:
                    normalized.append(norm)

            if normalized:
                combined = excludes + normalized
                if write_exclude_file(current_exclude_path, combined):
                    st.success(f"Added {len(normalized)} number(s) to {current_exclude_path}")
            else:
                st.info("No new numbers to add (duplicates ignored).")

    # Remove numbers section
    st.markdown("#### Remove Numbers from Exclude")
    excludes = read_exclude_file(current_exclude_path)
    if excludes:
        to_remove = st.multiselect("Select numbers to remove from exclude list", options=excludes)
        if st.button("🗑️ Remove selected", use_container_width=True):
            if not to_remove:
                st.warning("Select at least one number to remove.")
            else:
                remaining = [n for n in excludes if n not in to_remove]
                if write_exclude_file(current_exclude_path, remaining):
                    st.success(f"Removed {len(to_remove)} number(s) from {current_exclude_path}")

    # Display currently excluded numbers at the very end
    st.markdown("---")
    st.markdown("#### Currently Excluded Numbers")
    excludes = read_exclude_file(current_exclude_path)
    if excludes:
        st.markdown("**Numbers in exclude list:**")
        for n in excludes:
            st.write(f"• {n}")
    else:
        st.info("No numbers currently in the exclude list.")
