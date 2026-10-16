// Generated from document-applicability.json; do not edit manually.
export const documentApplicability = Object.freeze({
  "schema_version": 1,
  "scope": "Profile-specific applicability for text-only structure.* checks in Web/Lite and CLI/Deep; does not certify element order, placement or semantic adequacy.",
  "check_ids": [
    "cover",
    "approval",
    "resumo",
    "abstract",
    "toc",
    "refs",
    "keywords",
    "keywords-en"
  ],
  "modalities": [
    "required",
    "optional",
    "not-applicable"
  ],
  "evidence_boundary": "required: missing token FAIL, present token PASS (automatic-partial). optional: absent NOT APPLICABLE, present MANUAL REVIEW. not-applicable: NOT APPLICABLE regardless of token presence; not a prohibition.",
  "document_types": {
    "undergraduate-capstone": {
      "authority": "Existing final academic-work profile; ABNT/UFC structural baseline",
      "checks": {
        "cover": "required",
        "approval": "required",
        "resumo": "required",
        "abstract": "required",
        "toc": "required",
        "refs": "required",
        "keywords": "required",
        "keywords-en": "required"
      }
    },
    "specialization-capstone": {
      "authority": "Existing final academic-work profile; ABNT/UFC structural baseline",
      "checks": {
        "cover": "required",
        "approval": "required",
        "resumo": "required",
        "abstract": "required",
        "toc": "required",
        "refs": "required",
        "keywords": "required",
        "keywords-en": "required"
      }
    },
    "masters-thesis": {
      "authority": "Existing final academic-work profile; ABNT/UFC structural baseline",
      "checks": {
        "cover": "required",
        "approval": "required",
        "resumo": "required",
        "abstract": "required",
        "toc": "required",
        "refs": "required",
        "keywords": "required",
        "keywords-en": "required"
      }
    },
    "doctoral-thesis": {
      "authority": "Existing final academic-work profile; ABNT/UFC structural baseline",
      "checks": {
        "cover": "required",
        "approval": "required",
        "resumo": "required",
        "abstract": "required",
        "toc": "required",
        "refs": "required",
        "keywords": "required",
        "keywords-en": "required"
      }
    },
    "research-project": {
      "authority": "ABNT NBR 15287:2025 and standards/rules/coverage-rules-project.json",
      "checks": {
        "cover": "optional",
        "approval": "not-applicable",
        "resumo": "not-applicable",
        "abstract": "not-applicable",
        "toc": "required",
        "refs": "required",
        "keywords": "not-applicable",
        "keywords-en": "not-applicable"
      }
    },
    "anonymized-research-project": {
      "authority": "ABNT NBR 15287:2025 and standards/rules/coverage-rules-project.json; author anonymity",
      "checks": {
        "cover": "optional",
        "approval": "not-applicable",
        "resumo": "not-applicable",
        "abstract": "not-applicable",
        "toc": "required",
        "refs": "required",
        "keywords": "not-applicable",
        "keywords-en": "not-applicable"
      }
    },
    "scientific-article": {
      "authority": "ABNT NBR 6022:2018 and docs/ARTICLE-NORMATIVE-CONTRACT.md; journal-specific requirements remain conditional",
      "checks": {
        "cover": "not-applicable",
        "approval": "not-applicable",
        "resumo": "required",
        "abstract": "optional",
        "toc": "not-applicable",
        "refs": "required",
        "keywords": "required",
        "keywords-en": "optional"
      }
    }
  }
});
