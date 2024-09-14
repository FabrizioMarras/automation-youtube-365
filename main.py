# main.py
import os
from dotenv import load_dotenv
from src.auth import get_authenticated_service
from src.fetch_xlsx import fetch_xlsx_data
from src.fetch_video import fetch_video
from src.util import find_files, convert_date
from src.generate_title import generate_title
from src.upload_video import upload_video
from pytz import timezone
import pandas as pd

# Load environment variables from .env file
load_dotenv()

def main():
    youtube, drive = get_authenticated_service()

    # Fetch the main folder ID and subfolder name from environment variables
    main_folder_id = os.getenv('MAIN_FOLDER_ID')

    # Fetch the Excel data
    schedule_df = fetch_xlsx_data(drive, main_folder_id)

    for index, row in schedule_df.iterrows():
        video_no = row['No']
        test_type = row['Test']
        test_name = row['Name']
        char_name = row['Char']
        cell_date = row['Date']
        content = row['AInsyte Message']
        tags = " ".join([row[col] for col in schedule_df.columns if "hash" in col.lower() and pd.notna(row[col])])

       # Fetch the video file
        try:
            video_file = fetch_video(drive, main_folder_id, video_no)
            print(f"Downloaded video file for {video_no}")
        except FileNotFoundError as e:
            print(e)
            continue

        # set date and time for the post
        time = 17
        date = convert_date(cell_date, hour=time)
        print(f"The post is scheduled for {date}")

        # set the post content
        post = f'{content}\n\n{tags}'

        # create the title of the post
        title = generate_title(char_name, test_type, test_name)
        print(f'Title: {title}')
        # Print the final output for verification
        print('Video : ', video_no)
        print('Scheduled On: ', date)
        print('Title: ', title)
        # print('Post: ', post)

        # Upload the video to YouTube
        try:
            upload_video(youtube, video_file, title, post, date)
            print(f"Uploaded and scheduled video: {video_no} for {date}")
        except Exception as e:
            print(f"Failed to upload video {video_no}: {e}")

if __name__ == '__main__':
    main()
