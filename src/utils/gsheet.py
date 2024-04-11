import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ..config import APP_SETTINGS

from typing import Any

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
client_secret_file_path = APP_SETTINGS.GSHEET_CLIENT_SECRET_FILE_PATH
token_file_path = APP_SETTINGS.GSHEET_TOKEN_FILE_PATH

def auth_google():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file_path, SCOPES
                )
            creds = flow.run_local_server(port=54285)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def get_gsheet_data(gsheet_id: str, range_name: str):
    try:
        creds = auth_google()
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=gsheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
    except HttpError as e:
        print(f"An error occurred while getting data from Google Sheet: {e}")
        raise e
    else:
        return values
    finally:
        service.close()

def write_gsheet_data(gsheet_id: str, sheet_name: str, first_column: str, last_column: str, data: list[list[Any]]):
    try:
        creds = auth_google()
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        range_name = f"{sheet_name}!{first_column}:{last_column}"
        # Check if there are already rows in the sheet to append the new data at the end
        read_lines_result = (
            sheet.values()
            .get(spreadsheetId=gsheet_id, range=range_name)
            .execute()
        )
        read_lines = read_lines_result.get("values", [])
        if read_lines:
            range_name = f"{sheet_name}!{first_column}{len(read_lines)+1}"
        
        body = {"values": data}
        result = (
            sheet.values()
            .update(
                spreadsheetId=gsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=body,
            )
            .execute()
        )
        
    except HttpError as e:
        print(f"An error occurred while writing data to Google Sheet: {e}")
        raise e
    else:
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    finally:
        service.close()

