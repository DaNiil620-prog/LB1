import socket
import threading


# Echo-сервер (обробка одного клієнта)
def echo_server():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Echo-сервер запущено. Очікування підключень...")

        conn, addr = server_socket.accept()
        with conn:
            print(f"Підключення від: {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


# Мультиклієнтський сервер (обробка багатьох клієнтів)
def multi_client_server():
    HOST = '127.0.0.1'
    PORT = 65432

    def handle_client(conn, addr):
        print(f"Підключення від: {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Мультиклієнтський сервер запущено.")
        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()


# Сервер для отримання текстового файлу
def file_server():
    HOST = '127.0.0.1'
    PORT = 65433

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Сервер для отримання файлів запущено.")
        while True:
            conn, addr = server_socket.accept()
            print(f"Підключення від: {addr}")
            with conn:
                with open("received_file.txt", "wb") as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print("Файл отримано та збережено.")


# Echo-клієнт
def echo_client():
    HOST = '127.0.0.1'
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        message = input("Введіть повідомлення для сервера: ")
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Отримано від сервера: {data.decode()}")


# TCP-клієнт для відправки текстового файлу
def file_client():
    HOST = '127.0.0.1'
    PORT = 65433

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Підключено до сервера для відправки файлу.")

        with open("test_file.txt", "rb") as f:
            while chunk := f.read(1024):
                client_socket.sendall(chunk)

        print("Файл успішно відправлено.")


# Меню для вибору режиму роботи
if __name__ == "__main__":
    print("Виберіть режим роботи:")
    print("1. Echo-сервер")
    print("2. Мультиклієнтський сервер")
    print("3. Сервер для отримання файлів")
    print("4. Echo-клієнт")
    print("5. Клієнт для відправки файлу")

    choice = input("Ваш вибір: ")
    if choice == "1":
        echo_server()
    elif choice == "2":
        multi_client_server()
    elif choice == "3":
        file_server()
    elif choice == "4":
        echo_client()
    elif choice == "5":
        file_client()
    else:
        print("Невірний вибір!")
