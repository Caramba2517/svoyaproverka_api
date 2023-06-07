import json
import os
import psycopg2
import re

from decouple import config
import datetime
from api.search_text import search_text_in_folder

db = psycopg2.connect(
    host=config("DB_HOST"),
    port=config("DB_PORT"),
    database=config("DB_NAME"),
    user=config("DB_USER"),
    password=config("DB_PASS")
)

cur = db.cursor()
data_folder = '/complaints/prs/ALL_DATA'
folders = os.listdir(data_folder)
current_date = datetime.datetime.now()
three_days_ago = current_date - datetime.timedelta(days=3)
three_days_ago_str = three_days_ago.strftime("%d.%m.%Y")
days = datetime.datetime.strptime(three_days_ago_str, '%d.%m.%Y').date()
cur.execute(f"SELECT complaint_id FROM api_complaint WHERE date >= '{days}'")
list_for_update = [folder[0] for folder in cur.fetchall()]
cur.execute(f"SELECT complaint_id FROM api_complaint WHERE date < '{days}'")
list_for_passing = [folder[0] for folder in cur.fetchall()]
folder_num = 0
docs_complaint = ""
docs_solution = ""
docs_prescriptions = ""
for folder_name in folders:
    if folder_name in ['.DS_Store', 'docs_Решение', 'docs_Жалоба', 'docs_Предписание',' .json']:
        pass
    if "_" in str(folder_name):
        folder_name = folder_name.replace('_', '/')
    if folder_name in list_for_passing:
        folder_num += 1
        print(f"\rPassing {folder_num} of {len(list_for_passing)} existing folders", end='')
    else:
        if "/" in str(folder_name):
            folder_name = folder_name.replace('/', '_')
        try:
            json_path = os.path.join(data_folder, folder_name, folder_name + '.json')
            with open(json_path, 'r') as f:
                json_data = json.load(f)
        except NotADirectoryError:
            pass
        except KeyError:
            pass
        except FileNotFoundError:
            continue

        try:
            for x in ['docs_Жалоба', 'docs_Решение', 'docs_Предписание']:
                list_docs_path = os.path.join(data_folder, folder_name, x)
                file_paths = ""
                if len(os.listdir(list_docs_path)) == 0:
                    file_paths = 'Нет файлов'
                else:
                    for item in os.listdir(list_docs_path):
                        item_path = os.path.join(list_docs_path, item)
                        if os.path.isfile(item_path):
                            file_paths += f'{item_path};'
                            content = search_text_in_folder(list_docs_path)
                            latin_chars = re.compile('[a-zA-Z]')
                            print(content)
                            print(x)
                            if content is not None and not latin_chars.search(content):
                                content = content.replace('\n', '').replace('\f', '')
                                if x == "docs_Жалоба":
                                    docs_complaint += f'{content} '
                                elif x == 'docs_Решение':
                                    docs_solution += f'{content} '
                                elif x == 'docs_Предписание':
                                    docs_prescriptions += f'{content} '

                    if len(file_paths) == 1:
                        file_paths = file_paths[0]
                        content = search_text_in_folder(list_docs_path)
                        latin_chars = re.compile('[a-zA-Z]')
                        x = ""
                        print(content)

                        if content is not None and not latin_chars.search(content):
                            content = content.replace('\n', '').replace('\f', '')
                            if x == "docs_Жалоба":
                                docs_complaint += f'{content} '
                            elif x == 'docs_Решение':
                                docs_solution += f'{content} '
                            elif x == 'docs_Предписание':
                                docs_prescriptions += f'{content} '

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
                date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
            else:
                date = None
        except KeyError:
            try:
                date_str = json_data[f'{folder_name}']['cardHeaderBlock_dict']['dates_dict']['Размещено']
                if date_str:
                    date = datetime.datetime.strptime(date_str, '%d.%m.%Y').date()
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
            if docs_complaint == '':
                docs_complaint = None
            if docs_solution == '':
                docs_solution = None
            if docs_prescriptions == '':
                docs_prescriptions = None
            if folder_name in list_for_update:
                cur.execute("UPDATE api_complaint SET status = %s, date = %s, region = %s, customer_name = %s, "
                            "customer_inn = %s, complainant_name = %s, complainant_inn = %s, justification = %s, "
                            "numb_purchase = %s, prescription = %s, list_docs = %s, json_data = %s, docs_complaint = %s,"
                            " docs_solution = %s, docs_prescriptions = %s WHERE complaint_id = %s",
                            (status, date, region.upper(), customer_name, customer_inn, complainant_name,
                             complainant_inn,
                             justification, numb_purchase, prescription, file_paths, json.dumps(json_data),
                             docs_complaint, docs_solution, docs_prescriptions, folder_name))
                db.commit()
                folder_num = folder_num + 1
            else:
                cur.execute(f"INSERT INTO api_complaint (complaint_id, status, date, region, customer_name, customer_inn, "
                            f"complainant_name, complainant_inn, justification, numb_purchase, prescription, list_docs, "
                            f"json_data, docs_complaint, docs_solution, docs_prescriptions)"
                            f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (complaint_id, status, date, region.upper(), customer_name, customer_inn, complainant_name,
                             complainant_inn, justification, numb_purchase, prescription, file_paths,
                             json.dumps(json_data), docs_complaint, docs_solution, docs_prescriptions))
                db.commit()
                folder_num = folder_num + 1
                folder_amount = len(folders)
                print(f'\rInserted {folder_num} of {folder_amount} existing folders', end='')
        except Exception as e:
            print(f'Have an error: \n{e} \nWith folder:\n {folder_name}')
            continue
