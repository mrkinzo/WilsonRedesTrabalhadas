# ClienteTeclado.py
import socket

HOST = "127.0.0.1"
PORT = 9002


def main():
    # Cria e conecta o socket ao servidor — conexão mantida durante toda a sessão
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Conectado ao servidor! Digite suas mensagens (ou 'sair' para encerrar):")

        while True:
            mensagem = input("> ")

            # Encerra o programa se o usuário digitar 'sair'
            if mensagem.lower() == 'sair':
                print("Encerrando...")
                break

            # Ignora linhas em branco
            if not mensagem.strip():
                continue

            # Envia a mensagem ao servidor pela conexão já aberta
            s.sendall(mensagem.encode("utf-8"))
            print(f"Enviado: {mensagem}")


if __name__ == "__main__":
    main()