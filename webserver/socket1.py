
import socket
import os

def main():
    # Ler o conteúdo do arquivo index.html
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Define o caminho da pasta de imagens
    image_folder = 'img'

    # Cria o socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Associa o socket à porta 9000
    server_socket.bind(('localhost', 9000))

    # Escuta por conexões entrantes
    server_socket.listen(1)
    print("Esperando por conexões na porta 9000...")

    while True:
        # Aguardando por uma conexão
        connection, client_address = server_socket.accept()

        try:
            print("Conexão estabelecida com", client_address)

            # Recebe e exibe os dados enviados pelo cliente
            request = connection.recv(1024)
            print("Dados recebidos:", request.decode())

            # Verifica se o cliente está requisitando a página HTML
            if request.startswith(b'GET / HTTP/1.1'):
                # Envia a resposta HTTP contendo o conteúdo do arquivo index.html
                http_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html_content
                connection.sendall(http_response.encode())

            # Verifica se o cliente está requisitando uma imagem
            elif request.startswith(b'GET /img/'):
                # Extrai o nome do arquivo da requisição
                filename = request.split(b' ')[1].decode().split('/')[-1]

                # Verifica se o arquivo existe na pasta de imagens
                if filename in os.listdir(image_folder):
                    # Ler o conteúdo da imagem
                    with open(os.path.join(image_folder, filename), 'rb') as image_file:
                        image_data = image_file.read()

                    # Envia a resposta HTTP contendo a imagem
                    http_response = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n"
                    connection.sendall(http_response.encode() + image_data)

            # Caso haja outras requisições
            else:
                # Envia uma resposta de "404 Not Found"
                http_response = "HTTP/1.1 404 Not Found\r\n\r\n"
                connection.sendall(http_response.encode())

        finally:
            # Fecha a conexão
            connection.close()

if __name__ == "__main__":
    main()
