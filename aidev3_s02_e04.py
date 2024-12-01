import os
from openai import OpenAI


def get_files_by_extension(directory_path: str, extension: str) -> list:
    """
    Returns a list of files with the specified extension from the given directory.
    
    Args:
        directory_path (str): Path to the directory to search in
        extension (str): File extension to filter (e.g., '.txt', '.mp3')
    
    Returns:
        list: List of filenames with the specified extension
    """
    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = '.' + extension
    
    # List to store matching files
    matching_files = []
    
    try:
        # Iterate through files in the directory
        for filename in os.listdir(directory_path):
            # Check if the file ends with the specified extension
            if filename.lower().endswith(extension.lower()):
                matching_files.append(filename)
                
        return matching_files
    
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return []
    except PermissionError:
        print(f"Permission denied to access directory: {directory_path}")
        return []


def process_mp3_file(filePath):
    client = OpenAI()
    audio_file= open(filePath, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    print(transcription.text)

if __name__ == "__main__":
    katalog_path = "/home/rafal/Pobrane/pliki_z_fabryki/"
    pliki_mp3 = get_files_by_extension( katalog_path , "mp3")
    testowy_mp3 =  f"{katalog_path}{pliki_mp3[0]}"
    print(testowy_mp3)
    process_mp3_file(testowy_mp3)