import asyncio
import os
from telethon import TelegramClient, events


# Необходимо получить эти данные от Telegram API
api_id = '25823892'
api_hash = 'f6de7188d8e10e8fb559db06e6ff8a6c'
phone_number = '+79961969868'  # Номер телефона, к которому привязан ваш аккаунт

# Создаем клиента для взаимодействия с Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Функция для обработки новых сообщений
@client.on(events.NewMessage(chats='https://t.me/gifts_buy'))
async def handler(event):
    try:
        # Получаем отправителя сообщения
        sender = await event.get_sender()
        if sender is not None:
            # Если у пользователя есть юзернейм, используем его, иначе первое имя
            username = sender.username or sender.first_name
            print(f"Получено имя пользователя: {username}")
            
            # Проверка существования файла usernames.txt и запись имени пользователя
            with open('usernames.txt', 'a+') as file:
                content = file.read().splitlines()
                if username not in content:
                    file.write(f"{username}\n")
    except Exception as e:
        print(f"Произошла ошибка при обработке сообщения: {e}")

# Функция для авторизации
async def main():
    try:
        # Пытаемся закрыть существующий клиент, если он был запущен ранее
        if client.is_connected():
            await client.disconnect()

        # Удаление старого файла сессии, если он существует
        if os.path.exists('session_name.'):
            os.remove('session_name.')

        # Авторизация через телефонный номер
        await client.start(phone=phone_number)
        print("Вы вошли в систему!")

        # Запуск клиента до его отключения
        await client.run_until_disconnected()

    except Exception as e:
        print(f"Произошла ошибка авторизации или работы клиента: {e}")
# Запуск программы
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
