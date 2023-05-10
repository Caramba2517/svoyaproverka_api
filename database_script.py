import json
import os
import psycopg2

from decouple import config
from datetime import datetime
from api.search_text import search_text_in_folder

db = psycopg2.connect(
    host=config("DB_HOST"),
    port=config("DB_PORT"),
    database=config("DB_NAME"),
    user=config("DB_USER"),
    password=config("DB_PASS")
)

cur = db.cursor()
data_folder = '/Parser/parser_jalob_/ALL_DATA'
folders = os.listdir(data_folder)
folder_num = 0
for folder_name in folders:
    if folder_name in ['.DS_Store', 'docs', '.json']:
        pass
    else:
        try:
            json_path = os.path.join(data_folder, folder_name, folder_name + '.json')
            with open(json_path, 'r') as f:
                json_data = json.load(f)
        except NotADirectoryError as e:
            print(e)
        except KeyError as e:
            print(e)
        try:
            list_docs_path = os.path.join(data_folder, folder_name, 'docs')
            file_paths = ""
            file_content = ""
            if len(os.listdir(list_docs_path)) == 0:
                file_paths = 'Нет файлов'
            else:
                for item in os.listdir(list_docs_path):
                    item_path = os.path.join(list_docs_path, item)
                    if os.path.isfile(item_path):
                        file_paths += f'{item_path};'
                        content = search_text_in_folder(list_docs_path)
                        file_content += f'{content};'
                if len(file_paths) == 1:
                    file_paths = file_paths[0]
                    file_content = search_text_in_folder(list_docs_path)
        except KeyError:
            file_paths = 'Нет файлов'
            file_content = ""
        if "_" in str(folder_name):
            folder_name = folder_name.replace('_', '/')
        try:
            complaint_id = json_data[f'{folder_name}']['cardHeaderBlock_dict']['number']
        except KeyError:
            complaint_id = 'Нет данных'
        try:
            status = json_data[f'{folder_name}']['cardHeaderBlock_dict']['status']
        except KeyError:
            status = 'Статус не определён'
        try:
            date_str = json_data[f'{folder_name}']['cardHeaderBlock_dict']['dates_dict']['Поступление жалобы']
            if date_str:
                date = datetime.strptime(date_str, '%d.%m.%Y').date()
            else:
                date = None
        except KeyError:
            try:
                date_str = json_data[f'{folder_name}']['cardHeaderBlock_dict']['dates_dict']['Размещено']
                if date_str:
                    date = datetime.strptime(date_str, '%d.%m.%Y').date()
                else:
                    date = None
            except KeyError:
                date_str = "Нет данных"
                date = None
        try:
            region = json_data[f'{folder_name}']['cardHeaderBlock_dict']['dop_data']['Орган контроля']
        except KeyError:
            region = 'Нет данных'
        try:
            customer_name = json_data[f'{folder_name}']['section_card_common_dict']['Информация о субъекте контроля'][
                'Наименование организации']
        except KeyError:
            customer_name = 'Нет данных'
        try:
            customer_inn = json_data[f'{folder_name}']['section_card_common_dict']['Информация о субъекте контроля'][
                'ИНН']
            print(customer_inn)
        except KeyError:
            customer_inn = 'Нет данных'
        try:
            complainant_name = json_data[f'{folder_name}']['cardHeaderBlock_dict']['dop_data']['Лицо, подавшее жалобу']
        except KeyError:
            complainant_name = 'Нет данных'
        try:
            complainant_inn = json_data[f'{folder_name}']['section_card_common_dict'][
                'Данные участника контрактной системы в сфере закупок, подавшего жалобу']['ИНН']
        except KeyError:
            complainant_inn = 'Нет данных'
        try:
            justification = json_data[f'{folder_name}']['cardHeaderBlock_dict']['obosnovanie']
            if justification == '':
                justification = 'Статус еще не определён'
        except KeyError:
            justification = 'Статус еще не определён'
        try:
            numb_purchase = json_data[f'{folder_name}']['section_card_common_dict']['Сведения о закупке'][
                'Номер извещения']
        except KeyError:
            numb_purchase = 'Нет данных'
        try:
            prescription = json_data[f'{folder_name}']['cardHeaderBlock_dict']['predpisnaie']
            if prescription == '':
                prescription = "Нет данных"
        except KeyError:
            prescription = 'Нет данных'
        try:
            cur.execute(f"INSERT INTO api_complaint (complaint_id, status, date, region, customer_name, customer_inn, "
                        f"complainant_name, complainant_inn, justification, numb_purchase, prescription, list_docs, "
                        f"json_data, docs)"
                        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (complaint_id, status, date, region.upper(), customer_name, customer_inn, complainant_name,
                         complainant_inn, justification, numb_purchase, prescription, file_paths,
                         json.dumps(json_data), file_content))
            db.commit()
            folder_num = folder_num + 1
            folder_amount = len(folders)
            print(f'\rInserted {folder_num} of {folder_amount} folders', end='')
        except:
            folder_num = folder_num + 1
            print(f'\rFolder {folder_name} already exist!', end='')
