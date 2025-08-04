import random

class TripleDES:
    def __init__(self):
        self.key_64bit_1 = ""
        self.key_64bit_2 = ""
        self.key_64bit_3 = ""
        self.sub_keys_1 = []
        self.sub_keys_2 = []
        self.sub_keys_3 = []
        self.encrypted_binary_string = ""

    def get_encrypted_text(self, binary_string):
        """ encryption"""
        print(f"do encryption")

        print("\n\n\n\nbinary input is: \n" + binary_string)

        # add method for encryption  and the method return text
        key1 = self.generate_key()
        self.key_64bit_1 = key1[1]
        self.sub_keys_1 = key1[0]

        key2 = self.generate_key()
        self.key_64bit_2 = key2[1]
        self.sub_keys_2 = key2[0]

        key3 = self.generate_key()
        self.key_64bit_3 = key3[1]
        self.sub_keys_3 = key3[0]

        bits = binary_string
        
        encryption_1_binary_string = self.encrypt_des(bits , 1)
        encryption_2_binary_string = self.decrypt_des(encryption_1_binary_string, 2)
        encryption_3_binary_string = self.encrypt_des(encryption_2_binary_string, 3)

        self.encrypted_binary_string = encryption_3_binary_string

        return self.encrypted_binary_string


    def get_decrypted_text(self, encrypted_binary_string):
        """ decryption"""
        print(f"\n\n\n\ndo decryption")
        # add method for decryption and the method return text
        

        bits = encrypted_binary_string

        decryption_1_binary_string = self.decrypt_des(bits , 3)
        decryption_2_binary_string = self.encrypt_des(decryption_1_binary_string, 2)
        decryption_3_binary_string = self.decrypt_des(decryption_2_binary_string, 1)

        #decryptedtext = f"decryption method: {encrypted_text}"

        #decryption_3_binary_string = decryption_3_binary_string.lstrip("0")

        print("\n\n\n\ndecrypted binary: \n" + decryption_3_binary_string)

        return decryption_3_binary_string
    

    def generate_key(self):
        key_with_parity = ""
        key_8bit = ""
        for i in range(0,8):
            even_counter = 0
            for j in range(0,7):
                random_bit = random.randint(0,1)
                key_8bit += str(random_bit)

                if random_bit == 1:
                    even_counter += 1
                
                if j == 6:
                    if even_counter % 2 == 1: # parity check
                        key_8bit += str(1)
                    else:
                        key_8bit += str(0)
                    key_with_parity += key_8bit

                    even_counter = 0
                    key_8bit = ""

        permutated_56bit_key = self.key_permutation1(key_with_parity)
        return (self.key_rotation(permutated_56bit_key), key_with_parity)
        
    def key_permutation1(self, key_64bit):
        permutated_key = (key_64bit[56] + key_64bit[48] + key_64bit[40] + key_64bit[32] + key_64bit[24] + key_64bit[16] + key_64bit[8] + key_64bit[0] 
        + key_64bit[57] + key_64bit[49] + key_64bit[41] + key_64bit[33] + key_64bit[25] + key_64bit[17] + key_64bit[9] + key_64bit[1]
        + key_64bit[58] + key_64bit[50] + key_64bit[42] + key_64bit[34] + key_64bit[26] + key_64bit[18] + key_64bit[10] + key_64bit[2]
        + key_64bit[59] + key_64bit[51] + key_64bit[43] + key_64bit[35] + key_64bit[62] + key_64bit[54] + key_64bit[46] + key_64bit[38]
        + key_64bit[30] + key_64bit[22] + key_64bit[14] + key_64bit[6] + key_64bit[61] + key_64bit[53] + key_64bit[45] + key_64bit[37]
        + key_64bit[29] + key_64bit[21] + key_64bit[13] + key_64bit[5] + key_64bit[60] + key_64bit[52] + key_64bit[44] + key_64bit[36]
        + key_64bit[28] + key_64bit[20] + key_64bit[12] + key_64bit[4] + key_64bit[27] + key_64bit[19] + key_64bit[11] + key_64bit[3])

        return permutated_key

    def key_rotation(self, key_56bit):
        key_56_bit = key_56bit
        sub_keys =[]
        for i in range(0,16):
            left_key_28bit = key_56_bit[:28]
            right_key_28bit = key_56_bit[28:]

            if i in [1, 2, 9, 16]:
                left_key_28bit = left_key_28bit[1:] + left_key_28bit[:1]
                right_key_28bit = right_key_28bit[1:] + right_key_28bit[:1]

            else:
                left_key_28bit = left_key_28bit[2:] + left_key_28bit[:2]
                right_key_28bit = right_key_28bit[2:] + right_key_28bit[:2]

            transformed_key_56bit = left_key_28bit + right_key_28bit
            key_56_bit = transformed_key_56bit
            sub_keys.append(self.key_permutation2(transformed_key_56bit))
            
        return sub_keys
    
    def key_permutation2(self, transformed_56bit_key):

        permutated_key = (transformed_56bit_key[13] + transformed_56bit_key[16] + transformed_56bit_key[10] + transformed_56bit_key[23] + transformed_56bit_key[0] + transformed_56bit_key[4] + transformed_56bit_key[2] + transformed_56bit_key[27] 
        + transformed_56bit_key[14] + transformed_56bit_key[5] + transformed_56bit_key[20] + transformed_56bit_key[9] + transformed_56bit_key[22] + transformed_56bit_key[18] + transformed_56bit_key[11] + transformed_56bit_key[3]
        + transformed_56bit_key[25] + transformed_56bit_key[7] + transformed_56bit_key[15] + transformed_56bit_key[6] + transformed_56bit_key[26] + transformed_56bit_key[19] + transformed_56bit_key[12] + transformed_56bit_key[1]
        + transformed_56bit_key[40] + transformed_56bit_key[51] + transformed_56bit_key[30] + transformed_56bit_key[36] + transformed_56bit_key[46] + transformed_56bit_key[54] + transformed_56bit_key[29] + transformed_56bit_key[39]
        + transformed_56bit_key[50] + transformed_56bit_key[44] + transformed_56bit_key[32] + transformed_56bit_key[47] + transformed_56bit_key[43] + transformed_56bit_key[48] + transformed_56bit_key[38] + transformed_56bit_key[55]
        + transformed_56bit_key[33] + transformed_56bit_key[52] + transformed_56bit_key[45] + transformed_56bit_key[41] + transformed_56bit_key[49] + transformed_56bit_key[35] + transformed_56bit_key[28] + transformed_56bit_key[31])

        return permutated_key

    def encrypt_des(self, text, key_index):
        bits = text

        encrypted_bits = ""

        while len(bits) > 0:
            if len(bits) < 64:
                block_64_bits = bits.zfill(64) #padding in case of last block of bits less then 64 bits
                bits = ""
            else:
                block_64_bits = bits[:64]
                bits = bits[64:]


            permutated_block = self.initial_permutation(block_64_bits)
            feistel_network_output = self.feistel_network(permutated_block, key_index)
            final_permutation_output = self.final_permutation(feistel_network_output)

            encrypted_bits += final_permutation_output

        return encrypted_bits

        

    def initial_permutation(self, block):
        permutated_block = (block[57] + block[49] + block[41] + block[33] + block[25] + block[17] + block[9] + block[1] 
        + block[59] + block[51] + block[43] + block[35] + block[27] + block[19] + block[11] + block[3]
        + block[61] + block[53] + block[45] + block[37] + block[29] + block[21] + block[13] + block[5]
        + block[63] + block[55] + block[47] + block[39] + block[31] + block[23] + block[15] + block[7]
        + block[56] + block[48] + block[40] + block[32] + block[24] + block[16] + block[8] + block[0]
        + block[58] + block[50] + block[42] + block[34] + block[26] + block[18] + block[10] + block[2]
        + block[60] + block[52] + block[44] + block[36] + block[28] + block[20] + block[12] + block[4]
        + block[62] + block[54] + block[46] + block[38] + block[30] + block[22] + block[14] + block[6])

        return permutated_block

    def feistel_network(self, permutated_block, key_index, is_decrypting = False):

        sub_keys = []
        if key_index == 1:
            sub_keys = self.sub_keys_1
        elif key_index == 2:
            sub_keys = self.sub_keys_2
        elif key_index == 3:
            sub_keys = self.sub_keys_3

        feistel_block = permutated_block

        for i in range(0,16):

            left_block = feistel_block[:32]
            right_block = feistel_block[32:]
        

            if(is_decrypting):
                f_function_output = self.f_function(right_block, sub_keys[15 - i])

            else:
                f_function_output = self.f_function(right_block, sub_keys[i]) 
                     
            feistel_xor_operation = bin(int(left_block, 2) ^ int(f_function_output, 2))[2:]
            feistel_xor_operation = feistel_xor_operation.zfill(32)

            feistel_round_output_64bit = right_block + feistel_xor_operation
            feistel_block = feistel_round_output_64bit
        
        
        feistel_block = feistel_block[32:] + feistel_block[:32]
        return feistel_block


    def f_function(self, right_block, sub_key):

        right_block_expanded = self.right_block_expansion(right_block)
        xor_operation = bin(int(right_block_expanded, 2) ^ int(sub_key, 2))[2:]
        xor_operation = xor_operation.zfill(48)

        s_box_result = self.s_box_substitution(xor_operation)
        f_function_permutation_output = self.f_function_permutation(s_box_result)

        return f_function_permutation_output

        

    def right_block_expansion(self, right_block):

        expanded_32bit_right_block = (right_block[31] + right_block[0] + right_block[1] + right_block[2] + right_block[3] + right_block[4] 
        + right_block[3] + right_block[4] + right_block[5] + right_block[6] + right_block[7] + right_block[8]
        + right_block[7] + right_block[8] + right_block[9] + right_block[10] + right_block[11] + right_block[12]
        + right_block[11] + right_block[12] + right_block[13] + right_block[14] + right_block[15] + right_block[16]
        + right_block[15] + right_block[16] + right_block[17] + right_block[18] + right_block[19] + right_block[20]
        + right_block[19] + right_block[20] + right_block[21] + right_block[22] + right_block[23] + right_block[24]
        + right_block[23] + right_block[24] + right_block[25] + right_block[26] + right_block[27] + right_block[28]
        + right_block[27] + right_block[28] + right_block[29] + right_block[30] + right_block[31] + right_block[0])

        return expanded_32bit_right_block
    
    def s_box_substitution(self, xor_result):
        xor_result_divided_6bits = []
        s_box_output_32bits = ""

        for i in range(0,8):
            xor_result_divided_6bits.append(xor_result[:6])
            xor_result = xor_result[6:]

        for i in range(0, len(xor_result_divided_6bits)):
            s_box_result = self.get_s_box_result(i, xor_result_divided_6bits[i])
            s_box_output_32bits += s_box_result
        
        return s_box_output_32bits
            

    def get_s_box_result(self, s_box_index, divided_6bits):
        row_index = int(divided_6bits[0] + divided_6bits[5], 2)
        column_index = int(divided_6bits[1] + divided_6bits[2] + divided_6bits[3] + divided_6bits[4] , 2)

        if s_box_index == 0:
            s_box_1 = [
                ["14", "04", "13", "01", "02", "15", "11", "08", "03", "10", "06", "12", "05", "09", "00", "07"],
                ["00", "15", "07", "04", "14", "02", "13", "10", "03", "06", "12", "11", "09", "05", "00", "15"],
                ["04", "01", "14", "08", "13", "06", "02", "11", "15", "12", "09", "07", "03", "10", "05", "00"],
                ["15", "12", "08", "02", "04", "09", "01", "07", "05", "11", "03", "14", "10", "00", "06", "13"]]
            
            return bin(int(s_box_1[row_index][column_index]))[2:].zfill(4)
    
        elif s_box_index == 1:
            s_box_2 = [
                ["15", "01", "08", "14", "06", "11", "03", "04", "09", "07", "02", "13", "12", "00", "05", "10"],
                ["03", "13", "04", "07", "15", "02", "08", "14", "12", "00", "01", "10", "06", "09", "11", "05"],
                ["00", "14", "07", "11", "10", "04", "13", "01", "05", "08", "12", "06", "09", "03", "02", "15"],
                ["13", "08", "10", "01", "03", "15", "04", "02", "11", "06", "07", "12", "00", "05", "14", "09"]]
            return bin(int(s_box_2[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 2:
            s_box_3 = [
                ["10", "00", "09", "14", "06", "03", "15", "05", "01", "13", "12", "07", "11", "04", "02", "08"],
                ["13", "07", "00", "09", "03", "04", "06", "10", "02", "08", "05", "14", "12", "11", "15", "01"],
                ["13", "06", "04", "09", "08", "15", "03", "00", "11", "01", "02", "12", "05", "10", "14", "07"],
                ["01", "10", "13", "00", "06", "09", "08", "07", "04", "15", "14", "03", "11", "05", "12", "02"]]
            return bin(int(s_box_3[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 3:
            s_box_4 = [
                ["07", "13", "14", "03", "00", "06", "09", "10", "01", "02", "08", "05", "11", "12", "04", "15"],
                ["13", "08", "11", "05", "06", "15", "00", "03", "04", "07", "02", "12", "01", "10", "14", "09"],
                ["10", "06", "09", "00", "12", "11", "07", "13", "15", "01", "03", "14", "05", "02", "08", "04"],
                ["03", "15", "00", "06", "10", "01", "13", "08", "09", "04", "05", "11", "12", "07", "02", "14"]]
            return bin(int(s_box_4[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 4:
            s_box_5 = [
                ["02", "12", "04", "01", "07", "10", "11", "06", "08", "05", "03", "15", "13", "00", "14", "09"],
                ["14", "11", "02", "12", "04", "07", "13", "01", "05", "00", "15", "10", "03", "09", "08", "06"],
                ["04", "02", "01", "11", "10", "13", "07", "08", "15", "09", "12", "05", "06", "03", "00", "14"],
                ["11", "08", "12", "07", "01", "14", "02", "13", "06", "15", "00", "09", "10", "04", "05", "03"]]
            return bin(int(s_box_5[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 5:
            s_box_6 = [
                ["12", "01", "10", "15", "09", "02", "06", "08", "00", "13", "03", "04", "14", "07", "05", "11"],
                ["10", "15", "04", "02", "07", "12", "09", "05", "06", "01", "13", "14", "00", "11", "03", "08"],
                ["09", "14", "15", "05", "02", "08", "12", "03", "07", "00", "04", "10", "01", "13", "11", "06"],
                ["04", "03", "02", "12", "09", "05", "15", "10", "11", "14", "01", "07", "06", "00", "08", "13"]]
            return bin(int(s_box_6[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 6:
            s_box_7 = [
                ["04", "11", "02", "14", "15", "00", "08", "13", "03", "12", "09", "07", "05", "10", "06", "01"],
                ["13", "00", "11", "07", "04", "09", "01", "10", "14", "03", "05", "12", "02", "15", "08", "06"],
                ["01", "04", "11", "13", "12", "03", "07", "14", "10", "15", "06", "08", "00", "05", "09", "02"],
                ["06", "11", "13", "08", "01", "04", "10", "07", "09", "05", "00", "15", "14", "02", "03", "12"]]
            return bin(int(s_box_7[row_index][column_index]))[2:].zfill(4)
        
        elif s_box_index == 7:
            s_box_8 = [
                ["13", "02", "08", "04", "06", "15", "11", "01", "10", "09", "03", "14", "05", "00", "12", "07"],
                ["01", "15", "13", "08", "10", "03", "07", "04", "12", "05", "06", "11", "00", "14", "09", "02"],
                ["07", "11", "04", "01", "09", "12", "14", "02", "00", "06", "10", "13", "15", "03", "05", "08"],
                ["02", "01", "14", "07", "04", "10", "08", "13", "15", "12", "09", "00", "03", "05", "06", "11"]]
            return bin(int(s_box_8[row_index][column_index]))[2:].zfill(4)
        
    def f_function_permutation(self, sbox_result):
        permutated_sbox_result = (sbox_result[15] + sbox_result[6] + sbox_result[19] + sbox_result[20] + sbox_result[28] + sbox_result[11] + sbox_result[27] + sbox_result[16] 
        + sbox_result[0] + sbox_result[14] + sbox_result[22] + sbox_result[25] + sbox_result[4] + sbox_result[17] + sbox_result[30] + sbox_result[9]
        + sbox_result[1] + sbox_result[7] + sbox_result[23] + sbox_result[13] + sbox_result[31] + sbox_result[26] + sbox_result[2] + sbox_result[8]
        + sbox_result[18] + sbox_result[12] + sbox_result[29] + sbox_result[5] + sbox_result[21] + sbox_result[10] + sbox_result[3] + sbox_result[24])

        return permutated_sbox_result
        

    def final_permutation(self, block):
        permutated_block = (block[39] + block[7] + block[47] + block[15] + block[55] + block[23] + block[63] + block[31] 
        + block[38] + block[6] + block[46] + block[14] + block[54] + block[22] + block[62] + block[30]
        + block[37] + block[5] + block[45] + block[13] + block[53] + block[21] + block[61] + block[29]
        + block[36] + block[4] + block[44] + block[12] + block[52] + block[20] + block[60] + block[28]
        + block[35] + block[3] + block[43] + block[11] + block[51] + block[19] + block[59] + block[27]
        + block[34] + block[2] + block[42] + block[10] + block[50] + block[18] + block[58] + block[26]
        + block[33] + block[1] + block[41] + block[9] + block[49] + block[17] + block[57] + block[25]
        + block[32] + block[0] + block[40] + block[8] + block[48] + block[16] + block[56] + block[24])

        return permutated_block

    def decrypt_des(self, encrypted_text, key_index):
        bits = encrypted_text

        decrypted_bits = ""

        while len(bits) > 0:
            if len(bits) < 64:
                block_64_bits = bits.zfill(64) #padding in case of last block of bits less then 64 bits
                bits = ""
            else:
                block_64_bits = bits[:64]
                bits = bits[64:]

            permutated_block = self.initial_permutation(block_64_bits)
            feistel_network_output = self.feistel_network(permutated_block, key_index, True)
            final_permutation_output = self.final_permutation(feistel_network_output)

            decrypted_bits += final_permutation_output

        return decrypted_bits


    def get_key1_text(self):
        text = self.key_64bit_1
        return text

    def get_key2_text(self):
        text = self.key_64bit_2
        return text

    def get_key3_text(self):
        text = self.key_64bit_3
        return text

    def set_key1(self, key):
        print("permutation key: \n" + key)
        permutated_56bit_key = self.key_permutation1(key)
        self.key_64bit_1 = key
        self.sub_keys_1 = self.key_rotation(permutated_56bit_key)
    
    def set_key2(self, key):
        print("permutation key: \n" + key)
        permutated_56bit_key = self.key_permutation1(key)
        self.key_64bit_2 = key
        self.sub_keys_2 = self.key_rotation(permutated_56bit_key)

    def set_key3(self, key):
        print("permutation key: \n" + key)
        permutated_56bit_key = self.key_permutation1(key)
        self.key_64bit_3 = key
        self.sub_keys_3 = self.key_rotation(permutated_56bit_key)

apply_triple_des = TripleDES()