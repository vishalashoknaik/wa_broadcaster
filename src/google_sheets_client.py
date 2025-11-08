import requests
import pandas as pd
import tempfile
import os
import logging
from requests.exceptions import SSLError

class GoogleSheetsClient:
    """Client to fetch data from Google Sheets as Excel (preserves formatting)"""

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

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
                os.remove(tmp_path)

                if not rows:
                    raise Exception("Google Sheet is empty")

                self.logger.info(f"Successfully downloaded {len(rows)} message variants from Google Sheets")

                return rows

            except Exception as e:
                # Clean up temp file on error
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
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
