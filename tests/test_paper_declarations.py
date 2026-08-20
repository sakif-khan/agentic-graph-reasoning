"""The manuscript must carry the declarations Elsevier requires.

These are the items an editor bounces a submission for before it reaches
a reviewer, and none of them is visible in a clean build: the paper
compiled to 47 pages with no corresponding author, no CRediT statement,
no funding declaration and no AI disclosure. LaTeX has no opinion about
any of that, so it is checked here.

Verified against Elsevier sources in August 2026. The Knowledge-Based
Systems guide for authors returns HTTP 403 to an automated fetch by every
route tried -- sciencedirect.com directly, and elsevier.com, which 301s
to it -- so the requirements below come from Elsevier's journal-wide
policy pages, which do serve:

  generative AI  elsevier.com/about/policies-and-standards/
                 generative-ai-policies-for-journals -- required wording,
                 and the placement "immediately before the references"
  CRediT         elsevier.com/researcher/author/policies-and-guidelines/
                 credit-author-statement -- the fourteen role names
  funding        the recommended no-funding sentence, which appears
                 verbatim across Elsevier guides for authors

What is NOT verified: that KBS imposes no additional or differently
worded requirement of its own. If that page ever becomes fetchable, check
it rather than trusting this docstring.
"""
import io
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
MAIN = ROOT / "thesis_paper" / "agr-paper.tex"

pytestmark = pytest.mark.skipif(not MAIN.exists(), reason="manuscript absent")

COMMENT = re.compile(r"(?<!\\)%.*")


def body():
    return re.sub(r"\s+", " ", COMMENT.sub("", io.open(MAIN, encoding="utf-8").read()))


# The fourteen roles of the CRediT taxonomy, spelled as Elsevier spells
# them. A role outside this vocabulary is not a role.
CREDIT = {
    "Conceptualization", "Methodology", "Software", "Validation",
    "Formal analysis", "Investigation", "Resources", "Data curation",
    "Writing -- original draft", "Writing -- review & editing",
    "Visualization", "Supervision", "Project administration",
    "Funding acquisition",
}


def test_a_corresponding_author_is_designated():
    """\\ead is an address, not a designation; \\corref/\\cortext is.

    Both halves and a matching label: \\corref{cor1} with no \\cortext[cor1]
    prints a marker pointing at a footnote that does not exist.
    """
    t = body()
    refs = set(re.findall(r"\\corref\{([^}]*)\}", t))
    texts = set(re.findall(r"\\cortext\[([^\]]*)\]", t))
    assert refs, "no author carries \\corref: nobody is the corresponding author"
    assert texts, "no \\cortext: the corresponding-author footnote has no text"
    assert refs <= texts, f"\\corref labels with no \\cortext: {sorted(refs - texts)}"


def test_every_required_declaration_is_present():
    t = body().lower()
    required = {
        "CRediT authorship contribution statement": "credit authorship contribution statement",
        "Funding": "funding",
        "Declaration of competing interest": "declaration of competing interest",
        "Declaration of generative AI": "declaration of generative ai",
        "Data availability": "data availability",
    }
    missing = [k for k, v in required.items()
               if not re.search(r"\\section\*\{[^}]*" + re.escape(v), t)]
    assert not missing, f"declarations Elsevier requires are absent: {missing}"


def test_credit_names_every_author_and_only_real_roles():
    t = body()
    authors = re.findall(r"\\author\[[^\]]*\]\{([^}\\]*)", t)
    m = re.search(r"\\section\*\{CRediT[^}]*\}(.*?)\\section\*", t)
    assert m, "no CRediT section body"
    credit = m.group(1)
    for a in authors:
        assert a.strip() in credit, f"CRediT does not mention {a.strip()!r}"
    # Roles are comma-separated after each bolded name; strip the names out
    # first so "Md. Sakif Khan" is not read as a role.
    roles = re.sub(r"\\textbf\{[^}]*\}", "", credit)
    # "Writing -- review \& editing" in the source is "... & ..." as a role
    # name; compare the text, not the escaping.
    roles = roles.replace(r"\&", "&")
    named = {r.strip(" .") for r in re.split(r"[,.]", roles) if r.strip(" .")}
    bogus = named - CREDIT
    assert not bogus, (
        f"not CRediT roles: {sorted(bogus)}. The taxonomy is fixed; a "
        f"plausible invention is rejected on submission.")


def test_the_ai_declaration_carries_the_responsibility_sentence():
    """The disclosure is the tool and the reason; the obligation is the
    sentence where the authors take responsibility. Elsevier's suggested
    form has both, and a declaration missing the second half discloses
    without accepting anything."""
    t = body()
    m = re.search(r"\\section\*\{Declaration of generative AI[^}]*\}(.*?)"
                  r"\\bibliographystyle", t, re.I)
    assert m, "the AI declaration is not the last section before the references"
    d = m.group(1)
    assert "reviewed and edited the content" in d, \
        "missing Elsevier's review clause"
    assert "take full responsibility for the content" in d, \
        "missing the responsibility clause, which is the point of the declaration"
    assert re.search(r"used\s+\S+", d), "the declaration names no tool"


def test_the_ai_declaration_is_immediately_before_the_references():
    """Elsevier's policy is specific about placement."""
    t = body()
    ai = t.find("Declaration of generative AI")
    bib = t.find("\\bibliographystyle")
    assert ai != -1 and bib != -1
    between = t[t.find("}", ai):bib]
    assert "\\section*" not in between, (
        "another section sits between the AI declaration and the "
        "references; Elsevier asks for it immediately before them")
