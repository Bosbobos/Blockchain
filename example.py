from MerkleTree import MerkleTree
from SchnorrSignature import SchnorrSiganture
import hash, psevdo


def str_to_bin(msg: str) -> str:
    return ''.join(bin(ord(char))[2:].zfill(8) for char in msg)


def hex_to_bin(hex_msg: str) -> str:
    return bin(int(hex_msg, 16))[2:]

def create_block_header(size:str, prev_block_hash: str, merkle_root: str, timestamp: str, nonce: str) \
    -> str:
    if len(size) != 32:
        raise ValueError('size must be 32 bits')
    if len(prev_block_hash) != 256:
        raise ValueError('prev_block_hash must be 256 bits')
    if len(merkle_root) != 256:
        raise ValueError('merkle_root must be 256 bits')
    if len(timestamp) != 32:
        raise ValueError('timestamp must be 32 bits')
    if len(nonce) != 32:
        raise ValueError('nonce must be 32 bits')

    return f'{size}{prev_block_hash}{merkle_root}{timestamp}{nonce}'

if __name__ == '__main__':
    p = int('EE8172AE8996608FB69359B89EB82A6985451000977A4D63BC97322CE5DC3386EA0A12B343E9190F32177539845839786BB0C345D165976EF2195EC9B1C379E3', 16)
    q = int('98915E7EC8265EDFCDA31E88F24809DDB064BDC7285DD50D7289F0AC6F49DD2D', 16)
    a = int('9E96031500C8774A86958D4AFDE2127AFAD2538B4B6270A6F7C8837B50D50F206755984A49E509304D648BE2AB5AAB18EBE2CD46AC3D8495B142AA6CE23E21C', 16)

    seed = 'Konovalov and Matiev'
    schnorr = SchnorrSiganture(p, q, a, seed)
    transactions_count = 5

    random_numbers = psevdo.prng(seed, transactions_count + 1, True)

    dec_transactions = random_numbers[0:transactions_count-1]
    transactions = [bin(transaction)[2:202] for transaction in dec_transactions]
    transactions.append(str_to_bin(seed).zfill(200))
    signatures = [schnorr.generate_sig(transaction) for transaction in transactions]
    merkle = MerkleTree(transactions)
    merkle_root = hex_to_bin(merkle.get_root_hash()).zfill(256)

    random1 = bin(random_numbers[transactions_count]-1)[2:]
    random2 = bin(random_numbers[transactions_count])[2:]
    for dec_nonce in range(2**32):
        size = random1[:32]
        prev_block_hash = random2
        timestamp = bin(19)[2:].zfill(8) + bin(29)[2:].zfill(8) + bin(5)[2:].zfill(8) + bin(25)[2:].zfill(8)
        nonce = bin(dec_nonce)[2:].zfill(32)
        header = create_block_header(size, prev_block_hash, merkle_root, timestamp, nonce)

        hash_header = hex_to_bin(hash.stribog_both(hex(int(header, 2))[2:])).zfill(256)
        if hash_header[:5] == '0'*5:
            print(f'Нужный nonce: {dec_nonce}')
            print(f'Заголовок: {header}')
            print(f'Студенты, выполнявшие работу: Коновалов Матвей и Матиев Магомед')
            break
