from src.util import find_files, download_file
import tempfile

def fetch_video(drive, folder_id, video_no):

    # Generate a list of possible folder names with varying leading zeros (for folder search)
    possible_folder_names = [video_no.zfill(i) for i in range(1, 4)]
    print(f"Searching for video folder with possible names: {possible_folder_names}")

    # Search for folders that contain any of these possible names
    query = " or ".join([f"name contains '{name}'" for name in possible_folder_names])
    video_folders = find_files(drive, f"({query}) and '{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")

    if not video_folders:
        print(f"Folder for video No '{video_no}' not found with query: {query}")
        raise FileNotFoundError(f"Folder for video No '{video_no}' not found in any format")
    
    print(f"Found video folders: {video_folders}")

    # Generate the exact video file name (e.g., Post 017.mp4)
    possible_video_name = f"Post {video_no.zfill(3)}.mp4"
    print(f"Looking for exact video file: {possible_video_name}")

    # Iterate through each folder to find the video file
    video_file_id = None
    video_file_name = None

    for folder in video_folders:
        video_folder_id = folder['id']
        print(f"Searching in folder: {folder['name']} (ID: {video_folder_id})")

        # List all files inside the folder for debugging
        subfolder_files = find_files(drive, f"'{video_folder_id}' in parents")
        print(f"Files found in folder {video_folder_id}:")
        for file in subfolder_files:
            file_name = file.get('name', 'Unknown Name')
            mime_type = file.get('mimeType', 'Unknown MIME Type')
            print(f"File Name: {file_name}, MIME Type: {mime_type}")

        # Search for the exact video file inside the folder
        videos = find_files(drive, f"name = '{possible_video_name}' and '{video_folder_id}' in parents and mimeType contains 'video/'")
        
        if videos:
            print(f"Found exact matching video in folder {folder['name']}: {videos}")
            video_file_id = videos[0]['id']
            video_file_name = videos[0]['name']
            break
        else:
            print(f"No video file '{possible_video_name}' found in folder {folder['name']}")

    if not video_file_id:
        raise FileNotFoundError(f"Exact video file '{possible_video_name}' not found in any of the folders")

    print(f"Video file ID: {video_file_id}, Video file name: {video_file_name}")

    # Download the video file to a temporary location
    video_file = download_file(drive, video_file_id)
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file.write(video_file.read())
    temp_video_file.close()

    return temp_video_file.name
