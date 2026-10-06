"""RoG's answer scorer, copied unchanged, to score AGR's answers RoG's way.

Reasoning on Graphs (Luo et al., ICLR 2024) reports the Hits@1 and F1 that
tab:rog quotes, computed by src/qa_prediction/evaluate_results.py in
https://github.com/RManLuo/reasoning-on-graphs. Its paper defines Hits@1 as
"the proportion of questions whose top-1 predicted answer is correct", but
the scorer counts a hit when any gold answer occurs anywhere inside the
predicted text, as a substring, once both are lower-cased and stripped of
punctuation and articles. scripts/score_test.py, which scores every figure
in this thesis, needs an exact entity match. So the two rows of tab:rog are
scored by different rules, and scoring AGR's own answers by RoG's rule
measures what the difference is worth. build_thesis_numbers.py does that,
into the rog_scorer block of thesis_numbers.json.

The functions from normalize() to extract_topk_prediction() are RoG's,
copied verbatim from that file at commit
ccf8ec847bf61005a1b27cc9e5aff5c8ead7a24b (master on 2025-03-05). The file
last changed in 8553f30, on 2023-10-03, which is the release the paper's
figures come from. They are copied rather than imported because that
repository is not a package. eval_acc and eval_result are left out:
nothing here reports RoG's accuracy column, and eval_result reads and
writes files. score() below follows eval_result's own steps for a list
prediction.

RoG scores against each record's `answer` field, and this thesis's gold is
the same records' `a_entity` (build_testsets.py). The two are identical on
all 800 sampled test questions, checked on 2026-10-07, so AGR's gold here is
the ground truth RoG's scorer would have read.

The same commit is the source for the other difference sec:rog-comparison
names, the graph RoG searches. PromptBuilder in
src/qa_prediction/build_qa_input.py builds it from the question's own record,
utils.build_graph(question_dict['graph']), and follows each predicted
relation path from that question's topic entities. So RoG searches one
question's subgraph at a time, where AGR searches the union of all of them.
"""
import re
import string

# The functions from normalize() to extract_topk_prediction() carry this
# notice, from the LICENSE file at the same commit:
#
# MIT License
#
# Copyright (c) 2023 Linhao Luo (Raymond)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def normalize(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    s = s.lower()
    exclude = set(string.punctuation)
    s = "".join(char for char in s if char not in exclude)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    # remove <pad> token:
    s = re.sub(r"\b(<pad>)\b", " ", s)
    s = " ".join(s.split())
    return s


def match(s1: str, s2: str) -> bool:
    s1 = normalize(s1)
    s2 = normalize(s2)
    return s2 in s1

def eval_hit(prediction, answer):
    for a in answer:
        if match(prediction, a):
            return 1
    return 0

def eval_f1(prediction, answer):
    if len(prediction) == 0:
        return 0, 0, 0
    matched = 0
    prediction_str = ' '.join(prediction)
    for a in answer:
        if match(prediction_str, a):
            matched += 1
    precision = matched / len(prediction)
    recall = matched / len(answer)
    if precision + recall == 0:
        return 0, precision, recall
    else:
        return 2 * precision * recall / (precision + recall), precision, recall

def extract_topk_prediction(prediction, k=-1):
    results = {}
    for p in prediction:
        if p in results:
            results[p] += 1
        else:
            results[p] = 1
    if k > len(results) or k < 0:
        k = len(results)
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return [r[0] for r in results[:k]]

# ---- end of the code copied from RoG ----------------------------------------


def score(gold, entities):
    """One question, scored as RoG's eval_result scores a list prediction.

    Returns (hit, f1). eval_result passes a list through
    extract_topk_prediction with its default topk=-1, which deduplicates and
    keeps every entity, scores F1 on that list, and joins it with spaces for
    the hit test. An empty list is a hedge, and scores 0 on both.
    """
    prediction = extract_topk_prediction(list(entities), -1)
    f1, _, _ = eval_f1(prediction, list(gold))
    return eval_hit(" ".join(prediction), list(gold)), f1
