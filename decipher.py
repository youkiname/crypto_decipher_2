from typing import Dict, List, Tuple
import sys


#       012345678901234567890123456789012
ALPH = " абвгдежзийклмнопрстуфхцчшщъыьэюя"

S = "чшщдаърещмсувзеьгъеуялиуйссдфлыуэъктмхеуучоы ожтяжпдюьжс ьфссэррчыеф эсксюфи " \
"лреьлнейчждэяуесщлфбъунзмлсмхесбмрдяфеттшлптлуесужръюаосэлхчнцгяжтдвфдтъстдюфцдщмеуьщфссърттлхр юуусужпбжш сфеп шуегмеф афлтлуесшфиъчщдьякесщлдцъскгмлчсщодчротмхемфярдуъсайъйуспфх ржд руеьъеп шуегметчлз эмефдэше"


def get_matrix(S: str, key_length: int = 1) -> List[str]:
    matrix = []
    for key_index in range(key_length):
        matrix.append("")
        for char_index in range(key_index, len(S), key_length):
            matrix[key_index] += S[char_index]
    return matrix


def get_index_of_coincidence(S: str) -> float:
    result = 0
    n = len(S)
    for char in ALPH:
        result += (S.count(char) * (S.count(char) - 1)) / (n * (n - 1))
    return result


def calculate_key_length(S, max_length: int = 8) -> Tuple[int, List[int]]:
    avgs = []
    indices_of_coincidence = []
    for key_length in range(1, max_length):
        indices_of_coincidence.append([])
        # print("Key", key_length)
        matrix = get_matrix(S, key_length)
        sum_coincidence = 0
        for i, row in enumerate(matrix):
            index_of_coincidence = get_index_of_coincidence(row)
            sum_coincidence += index_of_coincidence
            indices_of_coincidence[-1].append(index_of_coincidence)
            # print("\t", index_of_coincidence)
        avgs.append(sum_coincidence / len(matrix))
    key_length = sorted(enumerate(avgs), key=lambda x: x[1], reverse=True)[0][0] + 1
    return key_length, indices_of_coincidence[key_length - 1]


def get_top_by_frequency(S: str) -> List[int]:
    frequency = {}
    for c in set(S):
        frequency[c] = S.count(c)
    return sorted(frequency.items(), key=lambda x: x[1], reverse=True)[0][0]


def calculate_offsets(S:str, key_length: int) -> Dict[str, int]:
    result = {}
    matrix = get_matrix(S, key_length)
    for row in matrix:
        top_char = get_top_by_frequency(row)
        result[top_char] = ALPH.index(top_char)
    return result


def decipher(S: str, key: str) -> str:
    offsets = [ALPH.index(c) for c in key]
    result = list(S)
    for i, char in enumerate(result):
        offset_index = i % len(offsets)
        offset = offsets[offset_index]
        new_char_index = (ALPH.index(char) - offset) % len(ALPH)
        result[i] = ALPH[new_char_index]
    return "".join(result)


def main():
    KEY_LENGTH, _ = calculate_key_length(S)
    print("Предположительная длина ключа", KEY_LENGTH)
    offsets = calculate_offsets(S, KEY_LENGTH).values()
    print(f"Предположительные сдвиги {offsets}")
    presumptive_key = "".join([ALPH[i] for i in offsets])
    print(f"Предположительный ключ '{presumptive_key}'")
    try:
        key = sys.argv[1]
    except IndexError:
        key = presumptive_key
    print(f"Используемый ключ '{key}'")

    print()
    print("Полученный результат расшифровки:")
    decipher_text = decipher(S, key)
    print(decipher_text)


if __name__ == "__main__":
    main()
