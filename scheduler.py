import asyncio
import datetime
from database_script import script


async def start_tasks():
    print("Выполнение задач запущено!")
    while True:
        now = datetime.datetime.now()
        if now.hour == 3:
            script()
            print(f"Выгрузка завершена: {datetime.datetime.now()}")
        await asyncio.sleep(60*60)

if __name__ == '__main__':
    asyncio.run(start_tasks())