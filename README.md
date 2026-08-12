# Agentic Graph Reasoning

Autonomous knowledge-graph navigation for fact verification and hallucination
mitigation in large language models.

An LLM agent answers multi-hop questions by *navigating* a Freebase-derived
knowledge graph rather than by retrieving text about it. It plans the question
into ordered sub-objectives, walks the graph through a five-operation tool API,
backtracks when a branch stops paying off, and — before it answers — decomposes
its own draft into claims and checks each one against the triples it actually
traversed. Claims it cannot ground are dropped, so the system hedges instead of
asserting something the graph does not support.

The accompanying M.Sc. Engg. thesis is in this repository at
[thesis_book/buetcsepgthesis.pdf](thesis_book/buetcsepgthesis.pdf).

---

## Read this before you start

This is a research repository, not a package you install and run. The agent
needs a **2.6-million-node Neo4j graph** that you have to build yourself, and
every question costs real OpenAI API calls. Budget accordingly:

| | |
| --- | --- |
| **Clone size** | ~290 MB (233 MB working tree + ~56 MB history) |
| **Extra disk** | ~3 GB for Neo4j, plus **~10.4 GB** if you want the VectorRAG baseline |
| **Setup time** | Hours, dominated by embedding 2.6 M entities on CPU |
| **Running cost** | Real API spend. Responses are cached, so a *repeat* run is free |

If you only want to read the results, everything is already committed under
[results/](results/) and summarised in the thesis — you do not need to build
anything.

### Prerequisites

| Requirement | Version | Notes |
| --- | --- | --- |
| Python | 3.10 or newer | Developed on 3.14 |
| Neo4j Community | 5.26.x | The results were produced on 5.26.28 |
| Java | Bundled with Neo4j | Only if you install Neo4j without its bundled JRE |
| RAM | 16 GB recommended | The bulk import peaked at 1.09 GiB; embedding is the heavy step |
| OpenAI API key | — | The backbone is a hosted model |
| git | any | |

---

## 1. Clone

```bash
git clone https://github.com/sakif-khan/agentic-graph-reasoning.git
cd agentic-graph-reasoning
```

Every command in this guide is run **from the repository root**. Scripts resolve
paths like `data/` and `results/` relative to the working directory, so running
them from elsewhere will fail.

---

## 2. Python environment

### Create and activate a virtual environment

**Windows (PowerShell)** — from the repository root:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, allow it for the current session:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

**macOS / Linux** — from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install

There are two install paths. They are not alternatives to pick at random:

| Command | What you get | Use when |
| --- | --- | --- |
| `pip install -e .` | Direct dependencies from `pyproject.toml`, unpinned | You are developing, or want current library versions |
| `pip install -r requirements.txt` | The exact resolved environment the reported results came from, including transitive pins | You are reproducing the thesis numbers |

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt      # or:  pip install -e .
```

`requirements.txt` already contains `-e .`, so it installs the `agr` package in
editable mode as well. Both paths make `import agr` work from anywhere.

> **PyTorch note.** `sentence-transformers` pulls in `torch`. The default wheel
> is CPU-only, which is what the pipeline was built and timed on. If you want
> GPU acceleration for the embedding steps, install the CUDA build of `torch`
> first, from <https://pytorch.org/get-started/locally/>, then install the rest.

---

## 3. Environment variables

Copy the template and fill it in.

**Windows (PowerShell)** — from the repository root:

```powershell
Copy-Item .env.example .env
```

**macOS / Linux** — from the repository root:

```bash
cp .env.example .env
```

| Variable | Example | Purpose |
| --- | --- | --- |
| `NEO4J_URI` | `bolt://localhost:7687` | Bolt endpoint of your Neo4j instance |
| `NEO4J_USERNAME` | `neo4j` | Set when the database was initialised |
| `NEO4J_PASSWORD` | — | Set when the database was initialised |
| `OPENAI_API_KEY` | `sk-...` | Backbone model access |

`.env` is gitignored and will not be committed.

> **All four are mandatory, even for the offline tests.** `agr/env.py` validates
> them at *import* time, and `tests/conftest.py` imports the runtime module, so
> without a complete `.env` pytest fails during collection — including the fifteen
> tests that need neither Neo4j nor the API.

---

## 4. Install and start Neo4j

Download Neo4j Community 5.26.x from
<https://neo4j.com/deployment-center/> (Graph Database Self-Managed), or use a
package manager.

**Windows** — unpack the archive next to this repository, then:

```powershell
..\neo4j-community-5.26.28\bin\neo4j.bat console
```

`neo4j-console.bat` in the repository root is a shortcut for exactly this and
assumes that layout.

**macOS** — with Homebrew:

```bash
brew install neo4j
neo4j console
```

**Linux** — follow the Debian/RPM instructions at
<https://neo4j.com/docs/operations-manual/current/installation/linux/>, then:

```bash
sudo systemctl start neo4j
```

Open <http://localhost:7474>, log in as `neo4j` with the initial password
`neo4j`, and set a new one. Put that password in `.env`.

---

## 5. Build the knowledge environment

This is the long part. Steps 5.1–5.5 are required; 5.6 is already done for you
and 5.7 is optional.

> **Do not run these casually.** Several of these scripts write into
> [results/](results/), which holds the committed experimental record backing
> the thesis. `union_graph_construction.py` overwrites
> `results/phase1/coverage_report.json`, and `build_testsets.py` overwrites the
> frozen 400-question test samples. Work on a branch and check `git status`
> before committing anything.

### 5.1 Get the source datasets

The graph is built from the RoG releases of WebQSP and CWQ, which ship the
per-question subgraphs. The scripts expect them as **siblings of this
repository**, not inside it:

```text
parent-directory/
├── agentic-graph-reasoning/     <- this repo
├── RoG-webqsp/data/             <- train-*.parquet, validation-*.parquet, test-*.parquet
└── RoG-cwq/data/
```

```bash
cd ..
git clone https://huggingface.co/datasets/rmanluo/RoG-webqsp
git clone https://huggingface.co/datasets/rmanluo/RoG-cwq
cd agentic-graph-reasoning
```

The `../RoG-{name}/data` path is hard-coded in the scripts that read it
(`union_graph_construction.py`, `build_testsets.py`, `entity_resolver.py`,
`mine_smoke_candidates.py`). Change it there if you put the data elsewhere.

### 5.2 Build the union graph

```bash
python scripts/union_graph_construction.py
```

Unions the WebQSP and CWQ subgraphs, applies the answer-reachability gate, and
writes `data/nodes.csv.gz` and `data/rels.csv.gz` in `neo4j-admin` import
format. Expect **2,592,892 nodes and 8,309,194 relationships** over 7,058
distinct relation types — if your counts differ, the datasets differ. These are
reference values for checking your own build, not thesis claims; the thesis
quotes them from `results/phase1/` via `tab:graphstats`.

### 5.3 Bulk-import into Neo4j

The offline importer needs the database **stopped**. Stop Neo4j, then run the
importer from wherever your `nodes.csv.gz` and `rels.csv.gz` are:

```bash
neo4j-admin database import full \
  --nodes=data/nodes.csv.gz \
  --relationships=data/rels.csv.gz \
  --skip-duplicate-nodes \
  --skip-bad-relationships \
  neo4j
```

On Windows use `neo4j-admin.bat` and drop the line continuations. The CSV
headers already carry `:ID`, `:LABEL`, `:START_ID`, `:END_ID` and `:TYPE`, so no
label or type arguments are needed.

The reference import took **36.4 s at 1.09 GiB peak** and skipped zero rows;
`results/phase1/import.report` is the log it produced, and both figures are read
off it (`IMPORT DONE in 36s 401ms`, `Peak memory usage: 1.093GiB`). Start Neo4j
again afterwards.

### 5.4 Create the constraint and the full-text index

Run in Neo4j Browser or `cypher-shell`:

```cypher
CREATE CONSTRAINT entity_id IF NOT EXISTS
FOR (e:Entity) REQUIRE e.id IS UNIQUE;

CREATE FULLTEXT INDEX entity_name IF NOT EXISTS
FOR (e:Entity) ON EACH [e.name];

CREATE INDEX entity_name_exact IF NOT EXISTS
FOR (e:Entity) ON (e.name);
```

The fulltext index's **name matters**: `agr/resolver.py` calls
`db.index.fulltext.queryNodes('entity_name', ...)` by that literal name.

The third is a plain range index and is about running time, not results. A
fulltext index does not serve exact `MATCH (e:Entity {name: $n})` lookups, so
without it every such lookup is a label scan over 2.6 M nodes. The resolver's
exact stage, `scripts/groundedness.py` and `scripts/check_coverage.py` all do
that lookup in a loop; the analysis scripts go from hours to minutes with it.

### 5.5 Embed entities and create the vector index

```bash
python scripts/embed_entities_and_write_back.py
```

Encodes entity names with `all-MiniLM-L6-v2` (384 dimensions) and writes the
vectors back into Neo4j. Mediator nodes are skipped — they are 63.7% of the
graph and their names are opaque MIDs like `m.0y5k79m`. The script's own note:
*"Expect a few hours on CPU for a few million entities; storage adds roughly
1.5 KB per node."*

Then create the vector index:

```cypher
CREATE VECTOR INDEX entity_embedding IF NOT EXISTS
FOR (e:Entity) ON (e.embedding)
OPTIONS { indexConfig: {
  `vector.dimensions`: 384,
  `vector.similarity_function`: 'cosine'
} };
```

Again the name is load-bearing: the resolver's third tier queries
`db.index.vector.queryNodes('entity_embedding', ...)`.

### 5.6 Relation vocabulary — already shipped

`data/relation_embeddings.npy` and `data/relation_names.json` (the 7,058
relation names, verbalised and embedded) are committed, as is
`data/id2name.json`. You only need to rebuild them if you changed the graph:

```bash
python scripts/build_id2name.py               # data/id2name.json
python scripts/embed_relation_vocabulary.py   # relation_embeddings.npy + names
python scripts/check_relation_embeddings.py   # spot-check the result
```

The last one is the functional check Sec 4.5 reports: it ranks the vocabulary
against `where was the person born` and prints the top five. Its archived output
is `results/phase1/check_relation_embeddings_log.txt`, and
`tests/test_relation_embeddings.py` holds the thesis prose to that archive, so
rebuilding the vocabulary without re-running the probe will surface as a test
failure rather than as a stale number in the text.

### 5.7 Triple index — optional, for the VectorRAG baseline only

```bash
python scripts/build_triple_index.py
```

Embeds every verbalised triple and builds a FAISS flat index at
`data/triple_index/`. This costs about **10.4 GB** of disk (6.7 GB index,
3.4 GB fp16 vectors, 0.3 GB texts) and is the longest single step. Skip it
unless you intend to run `run_baseline.py`; nothing else touches it.

---

## 6. Verify the install

### Smoke-check the tool layer

```bash
python scripts/check_tools.py
```

Exercises all five graph operations against the live database. It probes
`Justin Bieber` / `people.person.parents` by default — edit the constants at the
top of the file if you built a different graph.

### Run the test suite

```bash
python -m pytest
```

28 tests, all of which should pass on a complete install. `pytest.ini` sets
`addopts = -m "not integration"`, so a bare run is the offline selection and a
green result does not mean the whole suite ran — ask for the rest explicitly:

| Selection | Command | Runs | Needs |
| --- | --- | ---: | --- |
| Offline only (the default) | `python -m pytest` | 15 | `.env` complete |
| Everything | `python -m pytest -m ""` | 28 | Neo4j running, `.env` complete |
| Integration only | `python -m pytest -m integration` | 13 | Neo4j running |

The `integration` marker is declared in `pytest.ini` and covers the 13 tests
that talk to Neo4j. The other 15 need no services and read only committed files:
five pure unit tests over plan validation, budget accounting and Lucene
escaping; two that check the two Cohen's kappa implementations against each
other and against the pre-registered bar; four that check the question-identifier
convention Chapter 9 states to the reader against the `.tex` sources; one that
fails if the annotated and the built bibliography drift apart; and three that
hold Sec 4.5's relation-embedding probe to the run it was written from.

One thing worth knowing about the suite: the integration tests do not skip when
Neo4j is unreachable; they fail with `neo4j.exceptions.ServiceUnavailable`. If
you see that, start Neo4j.

---

## 7. Run it

### One question, end to end

```bash
python scripts/run_one.py
```

Answers a single hard-coded question and prints the answer, the budget snapshot
and the full navigation trace. This is the fastest way to confirm the whole
stack works. Its tool log goes to the untracked `scratch/` directory.

### Twenty questions

```bash
python scripts/smoke20.py
```

Runs the hand-picked 20-question smoke set (`results/phase3/smoke20.json`):
6 one-hop, 8 two-hop composition, 3 conjunction, 2 mediator-heavy, 1
unanswerable.

### The full evaluation

```bash
python scripts/run_agr_matrix.py    # AGR over both 400-question test samples
python scripts/run_baseline.py      # no-retrieval, VectorRAG, GraphRAG, ToG
```

Both are **resumable**: they read back the questions already present in their
output log and skip them, so an interrupted run continues where it stopped.
This is also the expensive part — roughly 6 model calls per WebQSP question and
9 per CWQ question, across 800 questions per system.

### Scoring

```bash
python scripts/score_test.py            # the ten runs of the main matrix
python scripts/build_thesis_numbers.py
```

`score_test.py` takes run files as arguments and falls back to the main matrix
when given none, so the bare call above is the one that produced
`results/phase4/score_test_log.txt`. Passing files scores those instead
(`*_tools.jsonl` is filtered out either way).

`score_test.py` reports Hits@1, F1, precision, recall and hedge rate with
bootstrap intervals. `build_thesis_numbers.py` regenerates
`results/phase4/thesis_numbers.json`, the single file every figure quoted in
the thesis is read from.

### About the cache

Every model call is keyed by a hash over the model id, temperature,
reasoning-effort setting and the full prompt, and cached under `cache/`
(gitignored, so your clone starts empty). A cache hit is deliberately
indistinguishable from a live call inside the agent — the budget check still
runs, the counter still increments, and the original token counts are replayed
— so a fully cached rerun reproduces the original budget snapshots exactly
rather than reporting zeros. In practice: the first run costs money, reruns
cost nothing.

---

## Repository layout

| Path | Contents |
| --- | --- |
| [agr/](agr/) | The agent: planner, explorer, scorer, verifier, graph tools, budget meter |
| [agr/baselines/](agr/baselines/) | No-retrieval, VectorRAG, GraphRAG and ToG comparison systems |
| [scripts/](scripts/) | 48 pipeline, experiment, scoring and analysis entry points |
| [tests/](tests/) | Unit and integration tests |
| [data/](data/) | Graph exports and embeddings; large artifacts are gitignored and rebuilt |
| [results/](results/) | The committed experimental record, by phase — see below |
| [thesis_book/](thesis_book/) | LaTeX sources and the compiled thesis PDF |
| [thesis_templates/](thesis_templates/) | Departmental material, none of it built: the BUET template (`Thesis Template PG/`, unmodified), the approved proposal and CASR presentation, reference PDFs, and review notes |

`results/` is organised by experimental phase: `phase1` the knowledge
environment, `phase2` backbone qualification, `phase3` the development sweep,
`phase4` the test matrix with its `ablations/`, `tier1_groundedness/` and
`tier2_judge/` sub-studies.

Two things in there are not what they look like. `smoke20_tog.jsonl` holds 10
records where its three sibling baselines hold 20 — an interrupted run, kept
because deleting a committed record is worse than explaining one. No reported
number reads it; the smoke baselines are a sanity check, and the ToG comparison
in the thesis is computed from the 400-question `test_*_tog.jsonl` files.
`results/phase3/smoke20.json` is a subset of `dev80.json` by construction, not a
contamination of it (§7.9.1).

---

## Configuration reference

Defaults live in `agr/config.py` and `agr/budget.py`.

| Setting | Default | Meaning |
| --- | --- | --- |
| `alpha` | 0.7 | Blend weight between embedding and LLM relation scores |
| `tau` | 0.20 | Low-signal threshold that triggers backtracking |
| `use_planner` | `True` | Decompose the question into sub-objectives |
| `verify_claims` | `True` | Check the draft's claims before answering |
| `use_gold_entities` | `True` | Seed anchors from the dataset's topic entities |
| `max_depth` | 4 | Traversal depth budget |
| `beam_width` | 3 | Frontier width |
| `max_backtracks` | 3 | Backtracks allowed per question |
| `max_llm_calls` | 25 | Model calls per question |
| `max_seconds` | 300 | Wall-clock budget per question |

The backbone is pinned in `agr/config.py` as `gpt-5.4-mini-2026-03-17` at
temperature 0.0 with `reasoning_effort` set to `"none"`. `alpha` and `tau` were
frozen from the development sweep and not revisited.

---

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `RuntimeError: NEO4J_URI is not set` | No `.env`, or you are not in the repository root. All four variables are required. |
| `neo4j.exceptions.ServiceUnavailable` | Neo4j is not running, or `NEO4J_URI` points somewhere else. |
| `ConnectionRefusedError [WinError 10061]` | Same as above, on Windows. |
| `Failed to invoke procedure db.index.fulltext.queryNodes: index 'entity_name' not found` | Step 5.4 was skipped, or the index has a different name. |
| `... 'entity_embedding' not found` | Step 5.5 was skipped, or entity embeddings were never written back. |
| `FileNotFoundError: data/relation_embeddings.npy` | Running from a directory other than the repository root. |
| `FileNotFoundError: data/triple_index/flat.faiss` | Only VectorRAG needs it — build it with step 5.7 or skip that baseline. |
| Tests fail at collection with an import error | `.env` is incomplete. `conftest.py` imports the runtime module, which validates the variables eagerly. |
| Entity search returns nothing sensible | The graph did not import, or the constraint and indexes are missing. Re-run `scripts/check_tools.py`. |

---

## Thesis

[thesis_book/buetcsepgthesis.pdf](thesis_book/buetcsepgthesis.pdf) — *Agentic
Graph Reasoning: Autonomous Knowledge Graph Navigation for Fact Verification and
Hallucination Mitigation in Large Language Models*, M.Sc. Engg. (CSE),
Bangladesh University of Engineering and Technology. §1.7 reads the title's terms
against what the measurements establish.

To rebuild it you need a TeX distribution with `latexmk`:

```bash
cd thesis_book
latexmk -pdf buetcsepgthesis.tex
```

---

## License

No license file is present, so default copyright applies and no permissions are
granted. If you intend others to use, modify or build on this work, add a
`LICENSE` file — MIT or Apache-2.0 are the usual choices for research code.
