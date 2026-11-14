#!/usr/bin/env python3
"""Prepare a source-bound R8.1 human review packet from original editorial PDFs.

The packet intentionally starts with 972 PENDING page decisions. A green
machine workflow never creates or asserts human, UFC/ABNT or release approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "artifacts/r81-v310-human-review"
PROOF_SOURCE = "de99db499cbc5bb78097f415fb91e3bb3ca3128a"
CLASS_BLOB = "299293e273dcefb80256eed2e17d2557db6aae52"
R5_RUN = 43467471975
REPO = "tiagosombrra/abntexto-ufc"
PROFILES = ("undergraduate-capstone", "specialization-capstone",
            "masters-thesis", "doctoral-thesis", "research-project",
            "anonymized-research-project", "scientific-article")
LOCALES = ("pt", "en", "es", "fr")
LOCALE_PAGES = {"pt": 246, "en": 240, "es": 240, "fr": 246}
REVIEW_PAGE_COUNT = sum(LOCALE_PAGES.values())
ARTIFACTS = {
    "pt": (14059297908, "d44df18aafdd38a721b2861c97ebf695906e0399201071eb28d1081bc6297790"),
    "en": (14057939644, "812c17969708e847fc1f6225002df3632a162b259baf66470bd0d42d0635ec59"),
    "es": (14059198079, "8a3b26219f72cdde5da050482a64914269ae1934d71a8cd5db0c93d9ccea8d2a"),
    "fr": (14058644629, "356028075dd9a5cb638dd05264d2e1959d7ba625cfa7228ebd1f4bf6cb99c5e8"),
}
REVIEW_DIMENSIONS = (
    "normative_UFC_ABNT", "physical_visual_layout",
    "academic_profile_applicability", "linguistic_terminology",
    "frontmatter_lists_references", "figures_tables_code_sources",
    "page_breaks_duplex_folios", "privacy_anonymization",
)


def require(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError(reason)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_blob(commit: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", commit + ":abntexto-ufc.cls"],
        cwd=ROOT, text=True).strip()


def verify_own_source() -> None:
    current = subprocess.check_output(
        ["git", "hash-object", "abntexto-ufc.cls"],
        cwd=ROOT, text=True).strip()
    require(current == CLASS_BLOB and source_blob(PROOF_SOURCE) == CLASS_BLOB,
            "source class changed since editorial PDF proof; regenerate review PDFs")
    # Archived PDFs bind to the original source and immutable Git blobs.
    # Current HEAD generators may evolve; they cannot retroactively change
    # these original PDF/source SHA receipts or approve newly generated PDFs.
    frozen_producers = {
        "tools/review/generate_readable_28.py":
            "35fbdc94505d138c0dcf8e6179d895c2dcd64ecf",
        "tools/review/build_readable_28.py":
            "993b36e475b12bf34d10b7b695194bc0ff24f948",
        "tests/integration/frontmatter/generate-comprehensive-corpus.py":
            "cb4091294743dc49a0e6ecfa1f8b2aeac7cac59d",
    }
    for producer, expected_blob in frozen_producers.items():
        actual = subprocess.check_output(
            ["git", "rev-parse", f"{PROOF_SOURCE}:{producer}"],
            cwd=ROOT, text=True).strip()
        require(actual == expected_blob,
                f"Archived original PDF source drifted: {producer}")

def github_zip(locale: str, dest: Path, token: str) -> None:
    require(token, "GH_TOKEN must authorize original GitHub artifact inspection")
    artifact_id, digest = ARTIFACTS[locale]
    url = f"https://api.github.com/repos/{REPO}/actions/artifacts/{artifact_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as stream:
        item = json.load(stream)
    require(item["id"] == artifact_id
            and item["workflow_run"]["id"] == R5_RUN
            and item["workflow_run"]["head_sha"] == PROOF_SOURCE
            and item["digest"] == "sha256:" + digest
            and item["expired"] is False,
            f"GitHub original artifact metadata/commit mismatch for {locale}")
    subprocess.run([
        "curl", "--fail", "--location", "--silent", "--show-error", "--retry", "3",
        "-H", "Authorization: Bearer " + token,
        "-H", "Accept: application/vnd.github+json",
        url + "/zip", "--output", str(dest),
    ], check=True)
    require(sha(dest.read_bytes()) == digest,
            f"original {locale} ZIP bytes differ from authenticated GitHub digest")


def find_member(z: zipfile.ZipFile, rel: str) -> bytes:
    path = rel.removeprefix("artifacts/")
    require(path in z.namelist(), "original ZIP lacks " + path)
    return z.read(path)


def pdf_pages(data: bytes) -> int:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
        tmp.write(data)
        tmp.flush()
        q = subprocess.run(
            ["qpdf", "--check", tmp.name], capture_output=True, text=True)
        require(q.returncode == 0, "qpdf rejected an original editorial PDF")
        info = subprocess.check_output(["pdfinfo", tmp.name], text=True)
        found = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
        require(found is not None, "pdfinfo did not return a physical page count")
        return int(found.group(1))


def document_receipts(locale: str, zip_path: Path) -> list[dict]:
    artifact_id, digest = ARTIFACTS[locale]
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        require(len(names) == len(set(names))
                and all(not n.startswith("/") and ".." not in Path(n).parts
                        for n in names)
                and z.testzip() is None, "ZIP members are duplicate, unsafe or corrupt")
        pref = f"human-readable-28/{locale}/"
        manifest = json.loads(find_member(z, pref + "review-pdfs.json"))
        sources = json.loads(find_member(z, pref + "review-sources.json"))
        require(manifest["locale"] == locale
                and manifest["source_commit_sha"] == PROOF_SOURCE
                and manifest["pdf_count"] == 7
                and manifest["failures"] == 0
                and manifest["human_approval"] == "PENDING"
                and manifest["release_authorized"] is False,
                "original editorial PDF receipt is not source-bound and PENDING")
        require(sources["locale"] == locale and sources["human_approval"] == "PENDING"
                and len(sources["entries"]) == 7,
                "original editable source evidence incomplete")
        original_sources = {r["profile"]: r for r in sources["entries"]}
        entries = {r["profile"]: r for r in manifest["documents"]}
        require(set(entries) == set(original_sources) == set(PROFILES),
                "original seven-profile editorial set is incomplete")
        result = []
        for profile in PROFILES:
            pdf = entries[profile]
            source = original_sources[profile]
            require(pdf["profile"] == profile and pdf["locale"] == locale
                    and source["locale"] == locale and not pdf["failures"]
                    and pdf["human_visual_approval"] == "PENDING",
                    "source/profile mismatches or premature human acceptance")
            raw_pdf = find_member(z, pdf["pdf"])
            raw_tex = find_member(z, source["source"])
            require(sha(raw_pdf) == pdf["pdf_sha256"]
                    and sha(raw_tex) == source["source_sha256"]
                    and source["source_sha256"] == pdf["source_sha256"],
                    "original PDF and TeX bytes differ from their signed receipts")
            count = pdf_pages(raw_pdf)
            require(count == pdf["pages"] and count > 0,
                    "physical PDF count differs from original editorial receipt")
            name = Path(pdf["pdf"]).name
            receipt = json.loads(find_member(
                z, pref + name.removesuffix(".pdf") + "-receipt.json"))
            require(receipt == pdf, "original per-document receipt is not identical")
            cover = pref + name.removesuffix(".pdf") + "-cover.png"
            raw_cover = find_member(z, cover)
            require(raw_cover.startswith(b"\x89PNG\r\n\x1a\n"),
                    "review cover raster is absent or invalid")
            result.append({
                "profile": profile, "locale": locale,
                "pdf_name": name, "pdf_sha256": pdf["pdf_sha256"],
                "tex_sha256": pdf["source_sha256"],
                "cover_png_sha256": sha(raw_cover),
                "physical_pages": count,
                "original_artifact_id": artifact_id,
                "original_artifact_zip_sha256": digest,
                "original_pdf_path": pdf["pdf"],
                "review": {
                    "reviewer": None, "date_utc": None,
                    "overall": "PENDING",
                    "dimensions": {key: "PENDING" for key in REVIEW_DIMENSIONS},
                    "page_decisions": [
                        {"page": n, "status": "PENDING",
                         "normative_justification": None, "observations": None}
                        for n in range(1, count + 1)
                    ],
                },
            })
        require(sum(x["physical_pages"] for x in result) == LOCALE_PAGES[locale],
                f"unexpected {locale} physical page total")
        return result


def validate_pending(packet: dict) -> None:
    require(packet["schema_version"] == 1
            and packet["review_source_commit_sha"] == PROOF_SOURCE
            and packet["runtime_class_git_blob"] == CLASS_BLOB
            and packet["source_workflow_run_id"] == R5_RUN
            and packet["status"] == "READY_FOR_HUMAN_REVIEW_NOT_ACCEPTED"
            and packet["human_normative_linguistic_review"] == "PENDING"
            and packet["human_visual_acceptance"] == "PENDING"
            and packet["publication_authorized"] is False,
            "review packet falsifies source identity or human approval")
    documents = packet["documents"]
    require(len(documents) == 28
            and {(x["locale"], x["profile"]) for x in documents}
                == {(l, p) for l in LOCALES for p in PROFILES},
            "duplicate or missing profile/locale in R8.1 review packet")
    require(sum(x["physical_pages"] for x in documents) == REVIEW_PAGE_COUNT,
            "R8.1 review packet does not match corrected page counts")
    for locale in LOCALES:
        require(sum(x["physical_pages"] for x in documents if x["locale"] == locale)
                == LOCALE_PAGES[locale],
                f"{locale} review packet has incorrect physical pages")
    for d in documents:
        require(re.fullmatch(r"[0-9a-f]{64}", d["pdf_sha256"]) is not None
                and re.fullmatch(r"[0-9a-f]{64}", d["tex_sha256"]) is not None
                and d["review"]["overall"] == "PENDING"
                and d["review"]["reviewer"] is None
                and d["review"]["date_utc"] is None,
                "missing PDF/TeX digest or false approval in R8.1 document")
        require(d["review"]["dimensions"] == {
            k: "PENDING" for k in REVIEW_DIMENSIONS},
            "a human review dimension was automatically approved")
        pages = d["review"]["page_decisions"]
        require(len(pages) == d["physical_pages"]
                and [x["page"] for x in pages] == list(range(1, len(pages) + 1))
                and all(x["status"] == "PENDING"
                        and x["normative_justification"] is None
                        and x["observations"] is None for x in pages),
                "a page was missed or approved without human examination")


def selftest() -> None:
    # Build a synthetic 28-document packet to test fail-closed review semantics.
    rows = []
    for locale in LOCALES:
        for profile in PROFILES:
            count = 16 if profile == "scientific-article" else (
                29 if profile in ("research-project", "anonymized-research-project")
                else 43)
            if locale in ("en", "es") and profile != "scientific-article":
                count -= 1
            rows.append({
                "locale": locale, "profile": profile, "physical_pages": count,
                "pdf_sha256": "a"*64, "tex_sha256": "b"*64,
                "review": {
                    "reviewer": None, "date_utc": None, "overall": "PENDING",
                    "dimensions": {x: "PENDING" for x in REVIEW_DIMENSIONS},
                    "page_decisions": [{"page": i, "status": "PENDING",
                                        "normative_justification": None,
                                        "observations": None}
                                       for i in range(1, count+1)],
                },
            })
    packet = {
        "schema_version": 1,
        "review_source_commit_sha": PROOF_SOURCE,
        "runtime_class_git_blob": CLASS_BLOB,
        "source_workflow_run_id": R5_RUN,
        "status": "READY_FOR_HUMAN_REVIEW_NOT_ACCEPTED",
        "review_packet_scope": "ARCHIVED_SOURCE_ONLY_NOT_CURRENT_HEAD",
        "human_normative_linguistic_review": "PENDING",
        "human_visual_acceptance": "PENDING",
        "publication_authorized": False,
        "documents": rows,
    }
    validate_pending(packet)
    import copy
    mutants = []
    for key, val in (
        ("publication_authorized", True),
        ("human_visual_acceptance", "ACCEPT"),
        ("runtime_class_git_blob", "0"*40),
    ):
        m = copy.deepcopy(packet)
        m[key] = val
        mutants.append(m)
    m = copy.deepcopy(packet)
    m["documents"][0]["review"]["page_decisions"][0]["status"] = "ACCEPT"
    mutants.append(m)
    m = copy.deepcopy(packet)
    m["documents"][0]["review"]["dimensions"]["normative_UFC_ABNT"] = "ACCEPT"
    mutants.append(m)
    m = copy.deepcopy(packet)
    m["documents"][0]["physical_pages"] -= 1
    mutants.append(m)
    for m in mutants:
        try:
            validate_pending(m)
        except ValueError:
            continue
        raise ValueError("R8.1 human-review mutation bypassed the pending contract")
    print("R81-HUMAN-REVIEW-SELFTEST status=PASS mutants=6 pending_pages=972"
          " publication_authorized=false")


def markdown(packet: dict) -> str:
    lines = [
        "# R8.1 — 28 PDFs, preparação para revisão humana da classe corrigida",
        "",
        "**Estado: PRONTO PARA REVISÃO, NÃO HOMOLOGADO.** Não há aceite humano.",
        "",
        f"Fonte auditada: `{PROOF_SOURCE}`. Classe Git blob: `{CLASS_BLOB}`.",
        f"Execução original: https://github.com/{REPO}/actions/runs/{R5_RUN}.",
        "",
        "A matriz contém 28 PDFs, 972 páginas e 972 decisões por página **PENDING**.",
        "O pacote é imutável como solicitação: decisões assinadas devem ser registradas",
        "em um documento separado, sem reescrever os comprovantes originais.",
        "",
        "| Idioma | Perfil | Páginas | PDF SHA-256 | Artefato GitHub | Aceite |",
        "|---|---|---:|---|---|---|",
    ]
    for doc in packet["documents"]:
        loc = doc["locale"]
        lines.append(
            f"| {loc} | {doc['profile']} | {doc['physical_pages']} | "
            f"`{doc['pdf_sha256']}` | "
            f"[ZIP #{doc['original_artifact_id']}](https://github.com/{REPO}/actions/runs/{R5_RUN}/artifacts/{doc['original_artifact_id']}) "
            "| PENDING |"
        )
    lines += [
        "",
        "## Critérios para o mantenedor e revisão institucional",
        "",
        "Revisar **cada página** para confirmar: margens, recuos, fontes e entrelinhas;",
        "paginação/versos duplex; capa/folha de rosto/banca conforme perfil;",
        "sumário, listas, glossário, índice e referências; elementos gráficos,",
        "legendas, fontes, notas e importação de código; coerência dos idiomas;",
        "privacidade do projeto anonimizado; e fundamentação UFC/ABNT por",
        "edição e dispositivo aplicável.",
        "",
        "Registrar para cada documento: examinador, data, páginas inspecionadas,",
        "observações, norma e seção aplicável, e uma das decisões",
        "`ACCEPT`, `NEEDS_CHANGES` ou `REJECT`. Versos vazios exigem",
        "justificativa específica. Não presumir aprovação por qpdf, veraPDF ou",
        "sucesso do CI. Qualquer alteração de classe exige novo conjunto de",
        "PDFs e nova avaliação vinculada à fonte.",
        "",
        "## Portas ainda bloqueadas",
        "",
        "- R8.1 visual/normativa e linguística: PENDING.",
        "- Aprovação institucional: PENDING.",
        "- Release/tag/CTAN v3.1.0: NÃO AUTORIZADOS.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--archives", type=Path)
    args = parser.parse_args()
    selftest()
    if args.self_test:
        return
    require(args.archives is not None, "missing --archives")
    verify_own_source()
    args.archives.mkdir(parents=True, exist_ok=True)
    all_docs: list[dict] = []
    for loc in LOCALES:
        archive_path = args.archives / f"readable-complete-{loc}-{R5_RUN}.zip"
        if args.download:
            github_zip(loc, archive_path, os.environ.get("GH_TOKEN", ""))
        require(archive_path.is_file()
                and sha(archive_path.read_bytes()) == ARTIFACTS[loc][1],
                f"missing or changed original R5 PDF artifact: {loc}")
        items = document_receipts(loc, archive_path)
        all_docs.extend(items)
        print(f"R81-HUMAN-REVIEW-INPUT status=PASS locale={loc} pdfs=7 pages={LOCALE_PAGES[loc]}", flush=True)
    packet = {
        "schema_version": 1,
        "status": "READY_FOR_HUMAN_REVIEW_NOT_ACCEPTED",
        "review_source_commit_sha": PROOF_SOURCE,
        "runtime_class_git_blob": CLASS_BLOB,
        "source_workflow_run_id": R5_RUN,
        "human_normative_linguistic_review": "PENDING",
        "human_visual_acceptance": "PENDING",
        "publication_authorized": False,
        "original_artifact_receipts": {
            loc: {"id": ARTIFACTS[loc][0], "zip_sha256": ARTIFACTS[loc][1]}
            for loc in LOCALES
        },
        "summary": {
            "documents": 28, "physical_pages": REVIEW_PAGE_COUNT,
            "pending_page_decisions": REVIEW_PAGE_COUNT,
            "human_approved_documents": 0,
        },
        "review_dimensions": list(REVIEW_DIMENSIONS),
        "documents": all_docs,
    }
    validate_pending(packet)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "request.json").write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT / "REVIEW-REQUEST.md").write_text(markdown(packet), encoding="utf-8")
    print("R81-HUMAN-REVIEW-PACKET status=PASS pdfs=28 pages=972"
          " pending_page_decisions=972 human_acceptance=PENDING"
          " publication_authorized=false", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError,
            zipfile.BadZipFile, json.JSONDecodeError) as e:
        raise SystemExit(f"R81-HUMAN-REVIEW-PACKET status=FAIL reason={e}") from e
