import sys
import os  # Добавляем импорт os
from emulator import ShellEmulator
from vr import VirtualFileSystem
from logger import Logger

def main():
    # Обработка аргументов командной строки
    if len(sys.argv) != 4:
        print("Использование: python main.py <имя компьютера> <путь к архиву> <путь к лог-файлу>")
        sys.exit(1)

    computer_name = sys.argv[1]
    zip_path = sys.argv[2]
    log_path = sys.argv[3]

    # Проверка существования файла zip
    if not os.path.isfile(zip_path):
        print(f"Ошибка: Файл виртуальной файловой системы '{zip_path}' не найден.")
        sys.exit(1)

    # Инициализация компонентов
    logger = Logger(log_path)
    vfs = VirtualFileSystem(zip_path)
    handler = CommandHandler(vfs, logger)

    # Эмуляция оболочки
    print(f"Добро пожаловать в эмулятор оболочки [{computer_name}]!")
    while True:
        try:
            command = input(f"{computer_name}> ").strip()
            handler.execute(command)  # Передаём команду на обработку
        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            break

if __name__ == "__main__":
    main()
