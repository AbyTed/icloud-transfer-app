import os
import zipfile

def move_folder(file_path):
    
    downloads_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')

    items = [os.path.join(downloads_path, f) for f in os.listdir(downloads_path)]

    items.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    most_recent_file = items[0]

    if most_recent_file.endswith('.zip'):
        print(f"Most recent zip file: {most_recent_file}")

        

        with zipfile.ZipFile(most_recent_file, 'r') as zip_ref:
            zip_ref.extractall(file_path)

        print(f"Contents of the zip file extracted to: {file_path}")

        os.remove(most_recent_file)
    else:
        print("The most recent item is not a zip file.")





