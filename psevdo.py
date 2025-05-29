from hash import *


def prng(seed: str, count: int, base10 = False) -> list:
    """Генерирует count псевдослучайных чисел на основе seed."""
    b_seed = seed.encode('utf-8')[:64]
    b_seed += b'\x00' * (64 - len(b_seed))  # Дополнение нулями
    hex_seed = b_seed.hex()

    # Нулевой цикл: h0 = H(seed)
    h0 = stribog_both(hex_seed)

    # Генерация count чисел
    results = []
    for i in range(1, count + 1):
        i_hex = format(i, '064x')
        input_block = h0 + i_hex
        h_i = stribog_both(input_block)
        if base10:
            h_i = int(h_i, base=16)
        results.append(h_i)

    return results


if __name__ == '__main__':
    seed = "Konovalov and Matiev"
    random_numbers = prng(seed, count=5)
    for i, num in enumerate(random_numbers, 1):
        print(f"PRNG {i}: {num}")