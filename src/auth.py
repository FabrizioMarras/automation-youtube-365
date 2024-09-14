import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_authenticated_service():
    # Path to your service account key JSON file
    SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')
    
    # Scopes required for YouTube Data API and Google Drive API
    SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl', 
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    # Create credentials using the service account file and the scopes
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    # If using domain-wide delegation, specify the user to impersonate
    credentials = credentials.with_subject(os.getenv('DELEGATED_USER_EMAIL'))

    # Build the service objects for YouTube and Google Drive
    youtube = build('youtube', 'v3', credentials=credentials)
    drive = build('drive', 'v3', credentials=credentials)
    
    return youtube, drive
