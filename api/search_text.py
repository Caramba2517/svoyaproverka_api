import os
import textract


def search_text_in_folder(list_docs_path):
    folder_path = list_docs_path
    supported_extensions = ['.pdf', '.docx', '.rtf', '.odt', '.txt']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension in supported_extensions:
                if file_extension == '.txt':
                    with open(file_path, 'rb') as f:
                        text = f.read().decode('utf-8', 'ignore')
                        return(text)
                else:
                    try:
                        text = textract.process(file_path).decode('utf-8', 'ignore')
                        return text
                    except Exception:
                        continue
