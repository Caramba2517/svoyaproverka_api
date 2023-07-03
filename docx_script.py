import os
import subprocess
import time

while True:
    folder_path = '/complaints/prs/ALL_DATA'
    doc_files = []
    count_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith('.doc'):
                count_files += 1
                print(f'Convert file #{count_files}. Folder name: {file_path.split("/")[4]}')
                output_path = os.path.splitext(file_path)[0] + ".docx"
                process = subprocess.Popen(['soffice', '--headless', '--convert-to', 'docx', '--outdir',
                                            os.path.dirname(file_path), file_path],
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"Timeout expired for file: {file_path}")
                    process.terminate()
                    print(f"Process terminated for file: {file_path}")
                    os.remove(file_path)
                    print(f'File {file_path} successfully deleted!')
                try: 
                    os.remove(file_path)
                except FileNotFoundError:
                    pass
                    