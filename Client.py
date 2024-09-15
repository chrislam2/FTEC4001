from Coin import *
import socket
import argparse

def get_task(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    time.sleep(1)
    data = s.recv(1024).decode()
    time.sleep(1)
    if(data != 'ok'):
        return
    s.send('get'.encode())
    time.sleep(1)
    data = s.recv(1024)
    s.close()
    return data

def MINT(task):
    blk = Block_header.parse(task) 
    nonce = b'\x00\x00\x00\x00'
    while True:
        blk.nonce = nonce
        if blk.check_pow():  # Check if the hash result meets the desired criteria
            break
        nonce = int_to_little_endian(little_endian_to_int(nonce) + 1, 4)
    return blk

def MINT_improve(task):
    blk = Block_header.parse(task) 
    nonce = b'\x00\x00\x00\x00'
    while True:
        blk.nonce = nonce
        if blk.check_pow():  # Check if the hash result meets the desired criteria
            break
        nonce = int_to_little_endian((little_endian_to_int(nonce) + random.randint(1, 2 ** 8)) % (2 ** 32), 4)
    return blk

def Submit(blk, sig, host, port):
    while(True):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        time.sleep(1)
        data = s.recv(1024).decode()
        if(data != 'ok'):
            continue
        print("Connection successful!")
        s.send('submit'.encode())
        time.sleep(1)
        data = s.recv(1024).decode()
        if(data != 'done'):
            print("Reconnecting...")
            s.close()
            continue
        s.send(blk.serialize())
        time.sleep(1)
        data = s.recv(1024).decode()
        print(data)
        if(data == 'bingo!'):
            s.send(sig.encode())
            time.sleep(1)
        else:
            print('Wrong submission!')
            return
        data = s.recv(1024).decode()
        if(data == 'finished'):
            print('Successful submission')
            break
        else:
            print('Commit failed. Trying again...')

def Query(sig, host, port):
    """query the number of block 'sig' constructed"""
    while(True):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        time.sleep(1)
        data = s.recv(1024).decode()
        if(data != 'ok'):
            continue
        print("Connection successful!")
        s.send('query'.encode())
        time.sleep(1)
        data = s.recv(1024).decode()
        if(data != 'done'):
            print("Reconnecting...")
            s.close()
            continue
        s.send(sig.encode())
        time.sleep(1)
        data = s.recv(1024)
        print("%s have constructed %d blocks" %(sig, int.from_bytes(data, 'little')))
        return 
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=8333)
    args = parser.parse_args()

    # Experiment
    if False:
        i = 1
        begin_milli_time = current_milli_time()
        begin_sec_time = current_sec_time()
        print(f'current milli time:{begin_milli_time}')
        print(f'current sec time:{begin_sec_time}')
        while(i <= 10):
            while(True): # get task from host
                task = get_task(args.host, args.port)
                if(task == None or len(task) != 80):
                    print("Connection failed!")
                    time.sleep(1)
                    continue
                print("Obtaining a task Succeeded!")
                # task.print_task()
                break
            # break
            #blk = MINT(task) # mining
            blk = MINT_improve(task) # mining
            Submit(blk, 'lamchunman1155158397yr4', args.host, args.port) # Set your signature here!
            i += 1
        print("Finish Experiment")
        end_milli_time = current_milli_time()
        end_sec_time = current_sec_time()
        print(f'current milli time:{end_milli_time}')
        print(f'current sec time:{end_sec_time}')
        print(f'milli time used:{end_milli_time - begin_milli_time}')
        print(f'sec time used:{end_sec_time - begin_sec_time}')

    # Mining
    if True:
        while(True):
            while(True): # get task from host
                task = get_task(args.host, args.port)
                if(task == None or len(task) != 80):
                    print("Connection failed!")
                    time.sleep(1)
                    continue
                print("Obtaining a task Succeeded!")
                # task.print_task()
                break
            # break
            #blk = MINT(task) # mining with (t2)
            blk = MINT_improve(task) # mining with (t3)
            Submit(blk, 'lamchunman1155158397yr4', args.host, args.port) # Set your signature here!