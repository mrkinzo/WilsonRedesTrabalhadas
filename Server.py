import threading
from time import sleep
import socket

# Fila de mensagens
FILA = []

# Semáforos
SEMAFORO_ACESSO = threading.Semaphore(1)
SEMAFORO_ITENS = threading.Semaphore(0)

def produzir(mensagem):
    global FILA
    SEMAFORO_ACESSO.acquire()
    FILA.append(mensagem)
    print(f"[Produzido] {mensagem}")
    SEMAFORO_ACESSO.release()
    SEMAFORO_ITENS.release()

def consumir():
    global FILA
    SEMAFORO_ITENS.acquire()
    SEMAFORO_ACESSO.acquire()
    mensagem = FILA.pop(0) if FILA else None
    SEMAFORO_ACESSO.release()
    return mensagem

def escutar_teclado():
    """Thread que recebe mensagens do ClienteTeclado na porta 9002"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 9002))
        s.listen()
        print("Servidor aguardando mensagens do teclado na porta 9002...")
        
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if data:
                    mensagem = data.decode("utf-8")
                    produzir(mensagem)

def enviar_tela():
    """Thread que envia mensagens para o ClienteTela na porta 9003"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 9003))
        s.listen()
        print("Servidor aguardando conexão da tela na porta 9003...")
        
        conn, addr = s.accept()
        with conn:
            print(f"Cliente Tela conectado: {addr}")
            
            while True:
                mensagem = consumir()
                if mensagem:
                    conn.sendall(mensagem.encode("utf-8"))
                    print(f"[Enviado para tela] {mensagem}")
                    sleep(1)

def main():
    t1 = threading.Thread(target=escutar_teclado, daemon=True)
    t2 = threading.Thread(target=enviar_tela)
    
    t1.start()
    t2.start()
    
    try:
        t2.join()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    main()