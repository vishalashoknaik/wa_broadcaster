import requests
import pandas as pd
import tempfile
import os
import logging
import re
import time
import platform
from requests.exceptions import SSLError

class GoogleSheetsClient:
    """Client to fetch data from Google Sheets as Excel (preserves formatting)"""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    @staticmethod
    def _safe_remove_temp_file(tmp_path, max_retries=3):
        """
        Safely remove temp file with retry logic for Windows file locking

        Args:
            tmp_path: Path to temporary file
            max_retries: Number of retry attempts
        """
        for attempt in range(max_retries):
            try:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                return  # Success
            except (PermissionError, OSError) as e:
                if attempt < max_retries - 1:
                    # Wait a bit and retry (Windows file locking issue)
                    time.sleep(0.1 * (attempt + 1))
                else:
                    # Last attempt failed, log warning but don't crash
                    # The temp file will be cleaned up by OS eventually
                    if platform.system() == "Windows":
                        # This is expected on Windows sometimes
                        pass
                    else:
                        raise

    @staticmethod
    def extract_spreadsheet_id(sheet_url):
        """
        Extract spreadsheet ID from Google Sheets URL

        Supports formats:
        - https://docs.google.com/spreadsheets/d/SHEET_ID/edit
        - https://docs.google.com/spreadsheets/d/SHEET_ID/edit#gid=0
        - SHEET_ID (if already just ID)
        """
        if not sheet_url:
            raise ValueError("Sheet URL is empty")

        # If it's already just an ID (no slashes), return it
        if '/' not in sheet_url:
            return sheet_url

        # Extract from URL
        match = re.search(r'/spreadsheets/d/([a-zA-Z0-9-_]+)', sheet_url)
        if match:
            return match.group(1)

        raise ValueError(f"Could not extract spreadsheet ID from URL: {sheet_url}")

    def get_sheet_metadata(self, spreadsheet_id):
        """
        Get sheet metadata including title and all tab names with GIDs

        Returns:
            dict with 'title' and 'sheets' list
        """
        try:
            # Download as Excel to get all sheets
            url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

            try:
                response = requests.get(url, timeout=30)
                response.raise_for_status()
            except SSLError:
                response = requests.get(url, verify=False, timeout=30)
                response.raise_for_status()

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name

            try:
                # Read Excel file to get sheet names
                excel_file = pd.ExcelFile(tmp_path)
                sheet_names = excel_file.sheet_names

                # Clean up
                self._safe_remove_temp_file(tmp_path)

                # Note: We can't get the actual Google Sheet title or GIDs from Excel export
                # The Excel file only has sheet names, not GIDs
                # We'll need to use sheet names directly with pandas

                return {
                    'spreadsheet_id': spreadsheet_id,
                    'sheet_names': sheet_names
                }

            except Exception as e:
                if os.path.exists(tmp_path):
                    self._safe_remove_temp_file(tmp_path)
                raise e

        except Exception as e:
            raise Exception(f"Failed to get sheet metadata: {str(e)}")

    def fetch_messages_by_tab_name(self, sheet_url, tab_name):
        """
        Download messages from a specific tab by name

        Args:
            sheet_url: Full Google Sheets URL
            tab_name: Name of the tab/sheet

        Returns:
            List of rows from that tab
        """
        spreadsheet_id = self.extract_spreadsheet_id(sheet_url)

        self.logger.info(f"Downloading tab '{tab_name}' from Google Sheets: {spreadsheet_id}")

        try:
            # Download entire workbook as Excel
            url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

            try:
                self.logger.info("Downloading with SSL verification...")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
            except SSLError:
                self.logger.warning("SSL verification failed. Retrying without verification...")
                response = requests.get(url, verify=False, timeout=30)
                response.raise_for_status()

            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name

            try:
                # Read specific sheet by name
                df = pd.read_excel(tmp_path, sheet_name=tab_name)

                # Convert to list of rows
                rows = []
                for _, row in df.iterrows():
                    row_data = []
                    for i in range(len(df.columns)):
                        cell_value = row.iloc[i]
                        if pd.notna(cell_value):
                            row_data.append(str(cell_value))
                        else:
                            row_data.append("")
                    rows.append(row_data)

                # Get available sheet names for error messaging
                excel_file = pd.ExcelFile(tmp_path)
                available_sheets = excel_file.sheet_names

                # Clean up
                self._safe_remove_temp_file(tmp_path)

                if not rows:
                    raise Exception(f"Tab '{tab_name}' is empty")

                self.logger.info(f"Successfully downloaded {len(rows)} rows from tab '{tab_name}'")

                return rows, available_sheets

            except ValueError as e:
                # Sheet name not found
                excel_file = pd.ExcelFile(tmp_path)
                available_sheets = excel_file.sheet_names
                self._safe_remove_temp_file(tmp_path)

                raise Exception(
                    f"Tab '{tab_name}' not found.\n"
                    f"Available tabs: {', '.join(available_sheets)}"
                )
            except Exception as e:
                if os.path.exists(tmp_path):
                    self._safe_remove_temp_file(tmp_path)
                raise e

        except Exception as e:
            raise Exception(f"Failed to download tab '{tab_name}': {str(e)}")

    def fetch_messages(self, spreadsheet_id, sheet_gid=0):
        """
        Download messages from a Google Sheet as Excel

        Args:
            spreadsheet_id: The Google Sheet ID from the URL
            sheet_gid: The sheet GID (default 0 for first sheet)

        Returns:
            List of rows, where each row is [first_message, followup_message]

        Raises:
            Exception: If download fails or sheet is not accessible
        """
        try:
            # Construct Excel export URL (preserves formatting, newlines, emojis)
            url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=xlsx"

            self.logger.info(f"Downloading messages from Google Sheets: {spreadsheet_id}")

            # Download with timeout
            try:
                self.logger.info("Downloading with SSL verification...")
                response = requests.get(url, timeout=30)
                response.raise_for_status()
            except SSLError:
                self.logger.warning("SSL verification failed. Retrying without verification...")
                response = requests.get(url, verify=False, timeout=30)
                response.raise_for_status()

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                tmp_file.write(response.content)
                tmp_path = tmp_file.name

            try:
                # Read Excel file with pandas (preserves all formatting)
                df = pd.read_excel(tmp_path, sheet_name=sheet_gid if sheet_gid > 0 else 0)

                # Convert to list of rows
                rows = []
                for _, row in df.iterrows():
                    row_data = []
                    for i in range(len(df.columns)):
                        cell_value = row.iloc[i]
                        # Convert to string, handle NaN
                        if pd.notna(cell_value):
                            row_data.append(str(cell_value))
                        else:
                            row_data.append("")
                    rows.append(row_data)

                # Clean up temp file
                self._safe_remove_temp_file(tmp_path)

                if not rows:
                    raise Exception("Google Sheet is empty")

                self.logger.info(f"Successfully downloaded {len(rows)} message variants from Google Sheets")

                return rows

            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(tmp_path):
                    self._safe_remove_temp_file(tmp_path)
                raise e

        except requests.exceptions.Timeout:
            raise Exception("Timeout while downloading from Google Sheets. Check your internet connection.")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise Exception("Google Sheet not found. Check the spreadsheet ID.")
            elif e.response.status_code == 403:
                raise Exception("Access denied. Make sure the sheet is shared with 'Anyone with the link can view'.")
            else:
                raise Exception(f"HTTP error while downloading Google Sheet: {e}")
        except Exception as e:
            raise Exception(f"Failed to download from Google Sheets: {str(e)}")

    def validate_connection(self, spreadsheet_id, sheet_gid=0):
        """
        Test if the Google Sheet can be accessed

        Returns:
            Tuple of (success: bool, message: str, row_count: int)
        """
        try:
            rows = self.fetch_messages(spreadsheet_id, sheet_gid)
            return True, f"Successfully connected! Found {len(rows)} message variants", len(rows)
        except Exception as e:
            return False, str(e), 0
