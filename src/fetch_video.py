from src.util import find_files, download_file
import tempfile

def fetch_video(drive, folder_id, video_no):
    # Generate a list of possible names with varying leading zeros
    possible_names = [str(video_no).zfill(i) for i in range(1, 4)]

    # Search for folders that contain any of these possible names
    query = " or ".join([f"name contains '{name}'" for name in possible_names])
    video_folders = find_files(drive, f"({query}) and '{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'")

    if not video_folders:
        raise FileNotFoundError(f"Folder for video No '{video_no}' not found in any format")
    
    print(f"Found video folders: {video_folders}")
    video_folder_id = video_folders[0]['id']

    # Find the video file inside the video folder
    video_files = []
    for name in possible_names:
        videos = find_files(drive, f"name='Post {name}.mp4' and '{video_folder_id}' in parents")
        if videos:
            video_files = videos
            break
    
    if not video_files:
        raise FileNotFoundError(f"Video file for No '{video_no}' not found in any format")

    video_file_id = video_files[0]['id']
    video_file_name = video_files[0]['name']
    print(f"Video file ID: {video_file_id}, Video file name: {video_file_name}")

    # Download the video file to a temporary location
    video_file = download_file(drive, video_file_id)
    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_video_file.write(video_file.read())
    temp_video_file.close()

    return temp_video_file.name
