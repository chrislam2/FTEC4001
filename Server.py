from Coin import *
import socket
import threading
import argparse

def tcplink(con, addr, cu_coin, file_name):
    print("Accept new connection from %s:%s..." % addr)
    con.send('ok'.encode())
    time.sleep(1)
    data = con.recv(1024).decode()
    time.sleep(1)
    if(not data):
        con.send('timeout'.encode())
    elif(data == 'get'):
        con.send(cu_coin.get_task())
    elif(data == 'submit'):
        con.send('done'.encode())
        time.sleep(1)
        data = con.recv(1024)
        if(len(data) != 80):
            con.send('Wrong submit!'.encode())
        else:
            blk = Block_header.parse(data)
            if(cu_coin.check_new_block(blk)):
                con.send('bingo!'.encode())
                time.sleep(1)
                data = con.recv(1024).decode()
                print(data + ": bingo!")
                cu_coin.create_block(blk, data)
                if(file_name != ""):
                    cu_coin.save(file_name)
                con.send('finished'.encode())
            else:
                con.send('Wrong submit!'.encode())
    elif(data == 'query'):
        con.send('done'.encode())
        time.sleep(1)
        data = con.recv(1024).decode()
        cnt = cu_coin.Query(data)
        con.send(cnt.to_bytes(2, 'little'))
    con.close()
    print('Connection from %s:%s closed.' % addr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="192.168.50.146")
    parser.add_argument("--port", type=int, default=8333)
    parser.add_argument("--save_file", type=str, default="chain.bin")
    parser.add_argument("--load_file", type=str, default="")
    parser.add_argument("--difficulty", type=float, default=0.003)
    args = parser.parse_args()
    cu_coin = Coin()
    if(args.load_file != ""):
        cu_coin.load(args.load_file)
    else:
        cu_coin.create_genesis_block()

    cu_coin.set_difficulty(args.difficulty)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.bind((args.host, args.port))
    s.listen(1)
    while(True):
        con, addr = s.accept()
        t = threading.Thread(target = tcplink, args = (con, addr, cu_coin, args.save_file))
        t.start()
    
