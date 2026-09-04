from pathlib import Path

OLD_AGENTS = "- Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix; final Linux run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b."
NEW_AGENTS = "- In source workflow run `33649620219`, Windows full-candidate-matrix job `100313006509` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix. The workflow-level conclusion was failure because its Linux inspection job failed; separate final Linux inspection run `33655108349` / job `100331601354` subsequently passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b."

OLD_README = "R1-BLOCK-8 is DONE. Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. Final Linux inspection run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b."
NEW_README = "R1-BLOCK-8 is DONE. In source workflow run `33649620219`, Windows full-candidate-matrix job `100313006509` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. The workflow-level conclusion was failure because its Linux inspection job failed; separate final Linux inspection run `33655108349` / job `100331601354` subsequently passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b."

for path, old, new in [
    (Path("AGENTS.md"), OLD_AGENTS, NEW_AGENTS),
    (Path("README.md"), OLD_README, NEW_README),
]:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one historical B8 wording match in {path}, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")
