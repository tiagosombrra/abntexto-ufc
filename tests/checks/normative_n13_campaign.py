#!/usr/bin/env python3
from __future__ import annotations

import runpy
from pathlib import Path

ENGINE = Path(__file__).with_name("normative_n13_negative_paths.py")

EXPECTED_CASE_IDS = (
    "page-margins-right",
    "body-font-size",
    "short-direct-citation-quotes",
    "ibge-table-open-sides",
    "project-required-resources",
)

EXPECTED_MECHANISMS = {
    "final-pdf-geometry": "REPRESENTED",
    "text-typography-extraction": "REPRESENTED",
    "citation-quotation-presentation": "REPRESENTED",
    "vector-rule-geometry": "REPRESENTED",
    "configuration-strict-rejection": "REPRESENTED",
    "semantic-structural-observers": "REPRESENTED",
    "pdf-pdfa-validation": "INVENTORY_PENDING",
}


def main() -> None:
    namespace = runpy.run_path(str(ENGINE), run_name="n13_negative_engine")
    engine_main = namespace["main"]
    engine_globals = engine_main.__globals__
    engine_globals["EXPECTED_CASE_IDS"] = EXPECTED_CASE_IDS
    engine_globals["EXPECTED_MECHANISMS"] = EXPECTED_MECHANISMS
    engine_main()


if __name__ == "__main__":
    main()
