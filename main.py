import sys
from sys import argv
from constant import *
from wsi_types import *


def _get_𝚷(filepath: str) -> PiMatrix:
    # TODO tutaj pobrac pi matrix od ani
    raise NotImplementedError("Czekamy na moduł Pi")


def _pr_server(trigram: NGram) -> float:
    # TODO tutaj z serwera powinnismy otrzymywac juz liczby w domenie log
    raise NotImplementedError("Czekamy na moduł Books")


def _sentence_probability(sentence: list[str], part: NGram) -> float:
    pr: float = 0
    for i in range(1, len(part) + 1):
        trigram: NGram = sentence[len(sentence) - 3 + i :] + part[max(i - 3, 0) : i]
        pr += _pr_server(
            trigram
        )  # TODO: domena log powinna juz byc (Serwer dostarcza log)!
    return pr / len(
        part
    )  # TODO: nie wiem czy dzielenie tego jest wlasciwe (byc moze powinnismy brac srednia geometryczna przez domene logarytmow?)


def _best_ngram_for_word(
    target: list[str], word: str, translations: list[tuple[NGram, float]]
) -> NGram:
    depth: int = int(argv[3] if len(argv) == 4 else 10)
    return max(
        list(map(lambda t: t[0], translations[:depth])),
        key=lambda ngram: _sentence_probability(target, ngram),
    )


def _err_exit(msg: str):
    print("{}: Program zakończył pracę: {}".format(argv[0], msg))
    exit(-1)


def _translate(source: str, 𝚷: PiMatrix) -> str:
    target: list[str] = [SENTENCE_BEGINNING]
    for word in source.split():
        if word not in 𝚷:
            _err_exit('Słowa "{}" nie ma w 𝚷-macierzy'.format(word))
        best_ngram: NGram = _best_ngram_for_word(target, word, 𝚷[word])
    return str(target)


def _show_usage(prog_name: str):
    print("usage: python {} zdanie sciezka [n]".format(prog_name))
    print(
        "zdanie - zdanie w jezyku polskim do przetlumaczenia na angielski. Należy otoczyć je cudzysłowiem."
    )
    print("sciezka - sciezka do pliku z pi-macierza")
    print(
        "n - opcjonalny parametr, liczba naturalna oznaczajaca glebokosc przeszukiwania pi macierzy, domyslnie 10"
    )


def _main():
    if 3 == len(argv) or argv == 4 and argv[3].isnumeric():
        print(_translate(str(argv[1]), _get_𝚷(argv[2])))
    else:
        print("{}: niepoprawne argumenty".format(argv[0]))
        _show_usage(argv[0])
        exit(-1)


# TODO: https://www.tutorialspoint.com/python/python_command_line_arguments.htm
# TODO: dopisac do helpa ze -1 gdy nie znalezlismy tlumaczenia dla jednego ze slow

if __name__ == "__main__":
    _main()
