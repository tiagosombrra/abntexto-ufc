#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

VERTICAL_TOLERANCE_PT = 1.5
COLUMN_TOLERANCE_PT = 1.5


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().upper()


def word_text(word: ET.Element) -> str:
    return "".join(word.itertext()).strip()


def page_words(page: ET.Element) -> list[ET.Element]:
    return [node for node in page.iter() if local(node.tag) == "word"]


def center_y(word: ET.Element) -> float:
    return (float(word.attrib["yMin"]) + float(word.attrib["yMax"])) / 2


def find_page(root: ET.Element, heading: str) -> ET.Element:
    wanted = normalize(heading)
    for page in (node for node in root.iter() if local(node.tag) == "page"):
        text = normalize(" ".join(word_text(word) for word in page_words(page)))
        if wanted in text:
            return page
    raise SystemExit(f"Front matter validation falhou: página não localizada: {heading}.")


def find_word(page: ET.Element, value: str) -> ET.Element:
    wanted = normalize(value)
    for word in page_words(page):
        if normalize(word_text(word)) == wanted:
            return word
    raise SystemExit(f"Front matter validation falhou: palavra não localizada: {value}.")


def aligned_row(page: ET.Element, description_first_word: str) -> tuple[float, float]:
    description = find_word(page, description_first_word)
    desc_x = float(description.attrib["xMin"])
    desc_y = center_y(description)
    candidates = [
        word
        for word in page_words(page)
        if float(word.attrib["xMax"]) < desc_x - 10
        and abs(center_y(word) - desc_y) < 20
    ]
    if not candidates:
        raise SystemExit(
            f"Front matter validation falhou: rótulo não localizado para {description_first_word}."
        )
    label = min(candidates, key=lambda word: abs(center_y(word) - desc_y))
    delta = abs(center_y(label) - desc_y)
    if delta > VERTICAL_TOLERANCE_PT:
        raise SystemExit(
            "Front matter validation falhou: rótulo e descrição estão verticalmente desalinhados "
            f"em {description_first_word}: delta={delta:.2f} pt."
        )
    return float(label.attrib["xMin"]), desc_x


def assert_columns(label: str, rows: list[tuple[float, float]]) -> None:
    label_positions = [row[0] for row in rows]
    description_positions = [row[1] for row in rows]
    if max(label_positions) - min(label_positions) > COLUMN_TOLERANCE_PT:
        raise SystemExit(
            f"Front matter validation falhou: coluna de rótulos desalinhada na lista de {label}: "
            f"{label_positions}."
        )
    if max(description_positions) - min(description_positions) > COLUMN_TOLERANCE_PT:
        raise SystemExit(
            f"Front matter validation falhou: coluna de descrições desalinhada na lista de {label}: "
            f"{description_positions}."
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate UFC abbreviation/symbol definition-list alignment."
    )
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    payload = subprocess.check_output(
        ["pdftotext", "-bbox-layout", str(args.pdf), "-"]
    )
    root = ET.fromstring(payload)

    abbreviations = find_page(root, "LISTA DE ABREVIATURAS E SIGLAS")
    symbols = find_page(root, "LISTA DE SÍMBOLOS")

    assert_columns(
        "abreviaturas e siglas",
        [
            aligned_row(abbreviations, "Associação"),
            aligned_row(abbreviations, "Universidade"),
        ],
    )
    assert_columns(
        "símbolos",
        [
            aligned_row(symbols, "Curva"),
            aligned_row(symbols, "Malha"),
        ],
    )

    print("Alinhamento das listas de abreviaturas/siglas e símbolos validado.")


if __name__ == "__main__":
    main()
