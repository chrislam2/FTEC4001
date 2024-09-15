from Block import * 

class Coin:

    def __init__(self):
        self.blk_list = []
        self.blk_num = 0
        self.owner_list = []

    def create_genesis_block(self): 
        """create first block of blockchain, make sure this function is called only once initially"""
        version = int.from_bytes(b'\x02\x00\x00\x20', 'little')
        temp = 0
        pre_block = temp.to_bytes(32, 'little')
        merkle_root = random_hexstring(32)
        timestamp = current_sec_time()
        bits = b'\xe9\x3c\x01\x1e'
        nonce = b'\x09\x08\x01\x09'

        blk = Block_header(version, pre_block, merkle_root, timestamp, bits, nonce)
        self.blk_list.append(blk.serialize())
        self.blk_num = self.blk_num + 1
        self.owner_list.append('Kirito')
        self.last_time = timestamp
        self.last_blk = 0
        self.create_new_block_task()

    def create_block(self, blk, owner):
        """accept a new blk and save up signature"""
        self.blk_list.append(blk.serialize())
        self.blk_num = self.blk_num + 1
        self.owner_list.append(owner)
        self.create_new_block_task()

    def set_difficulty(self, diff):
        self.temp_blk.bits = calc_difficulty(diff)

    def create_new_block_task(self):
        """Create a new mining task base on previous block, the result will be save in self.temp_blk"""
        temp = Block_header.parse(self.blk_list[-1])
        pre_blk = temp.hash()
        temp.pre_block = pre_blk
        temp.merkle_root = random_hexstring(32)
        temp.timestamp = current_sec_time()
        
        if(temp.timestamp - self.last_time > TIME_INTERVAL):
            blk_num = self.blk_num - self.last_blk - 1
            blk = Block_header.parse(self.blk_list[-1])
            if(blk_num == 0):
                time_diff = TIME_INTERVAL * 4
            else:
                # time_diff = blk.timestamp - self.blk_list[self.last_blk].timestamp
                time_diff = blk.timestamp - Block_header.parse(self.blk_list[self.last_blk]).timestamp
                time_diff = time_diff * (BLK_INTERVAL / blk_num)
            temp.bits = calculate_new_bits(blk.bits, time_diff)
            self.last_blk = self.blk_num - 1
            self.last_time = blk.timestamp
        else:
            blk = Block_header.parse(self.blk_list[-1])
            temp.bits = blk.bits
        self.temp_blk = temp
    
    def check_new_block(self, blk):
        """Check a new block is valid or not"""
        if(blk.check_pow() == False):
            return False
        temp = self.temp_blk
        if(temp.version != blk.version or
            temp.pre_block != blk.pre_block or
            temp.merkle_root != blk.merkle_root or
            temp.timestamp != blk.timestamp or
            temp.bits != blk.bits):
            return False
        return True
    
    def get_task(self):
        """return current task"""
        return self.temp_blk.serialize()

    def save(self, file_name):
        fo = open(file_name, "wb")
        for i in range(self.blk_num):
            fo.write(self.blk_list[i])
            temp = self.owner_list[i].encode()
            fo.write(len(temp).to_bytes(1, 'little'))
            fo.write(temp)
        fo.close()

    def load(self, file_name):
        fi = open(file_name, "rb")
        while(True):
            s = fi.read(80)
            if(not s):
                break
            len = int.from_bytes(fi.read(1), 'little')
            owner = fi.read(len).decode()
            self.blk_list.append(s)
            self.owner_list.append(owner)
            self.blk_num = self.blk_num + 1
        fi.close()
        print('Load successful!')
        n = self.blk_num
        self.last_time = Block_header.parse(self.blk_list[n - 1]).timestamp
        self.last_blk = n - 1
        self.create_new_block_task()

    def Query(self, sig):
        """return number of block via signature"""
        cnt = 0
        for i in range(len(self.owner_list)):
            if(self.owner_list[i] == sig):
                cnt = cnt + 1
        return cnt
            

