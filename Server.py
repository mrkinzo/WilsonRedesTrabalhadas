#porta 9003

import threading
from time import sleep

import socket

HOST = "0.0.0.0"
PORT = 9003

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        data = conn.recv(1024)
        
# Fila de mensagens
FILA = []

# Semáforo de acesso à fila
SEMAFORO_ACESSO = threading.Semaphore(1) # Apenas 1 thread pode acessar a fila por vez

# Quantidade de itens. Quem insere na fila, incrementa. Quem consome, decrementa.
SEMAFORO_ITENS = threading.Semaphore(0)  # A fila inicia com 0 elementos

def produzir(mensagem):
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Inclui a mensagem na fila
    FILA.append(mensagem)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Informa que há itens na fila.
    SEMAFORO_ITENS.release() 

def consumir():
    global FILA
    global SEMAFORO_ACESSO
    global SEMAFORO_ITENS

    # Aguarda até que existam itens na fila
    SEMAFORO_ITENS.acquire()

    # Aguarda acesso ao recurso
    SEMAFORO_ACESSO.acquire()
    # Verifica se há mensagens na fila
    if FILA:
        # Retira a primeira mensagem da fila
        mensagem = FILA.pop(0)
    # Libera o acesso ao recurso
    SEMAFORO_ACESSO.release()

    # Retorna a mensagem que estava na fila
    return mensagem

def thread_produtora(id_thread):
    # Inclui mensagens na fila
    id_msg = 0
    
    while True:
        id_msg += 1
        sleep(1)

def thread_consumidora(id_thread):
    # Retira mensagens da fila
    while True:
        msg_consumida = consumir()
        print(f"[Thread {id_thread} consumiu] {msg_consumida}", flush=True)
        sleep(1)

def escutar_porta():
 # Escuta a porta para receber mensagens dos clientes e as inclui na fila
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', 9002))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
         data = conn.recv(1024)
       
    
def envia_tela(porta):
 # Envia a mensagem ao cliente
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', porta))
        for mensagem in FILA:
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                conn.sendall(mensagem.encode("utf-8"))
                sleep(1)
        
def main():
    # Cria a thread receptora
    t0 = threading.Thread(
                target=escutar_porta, args=(9002,), # Será a thread 0, que escuta a porta 9002 para receber mensagens 
            )

    # Cria 2 threads consumidoras
    t1 = threading.Thread(
                target=thread_consumidora, args=(1,), # Será a thread 1,que consome as mensagens da 
                daemon=True
            )
    t2 = threading.Thread(
                target= envia_tela, args=(9003,), # Será a thread 2, que envia as mensagens para o cliente da tela
            )
    
    t0.start()
    
    t1.start()
    
    t2.start()

    t0.join()
    t1.join()
    t2.join()


if __name__ == "__main__":
    main()
    