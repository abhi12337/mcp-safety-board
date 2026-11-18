"""Recompute every MCP Safety Board score from the published data and check it matches.

Usage:
    python score.py                 # downloads https://mcp-safety-board.pages.dev/data/board.json
    python score.py board.json      # or use a local copy (one is kept in data/board.json)

Python 3.8+, standard library only. Reads JSON, makes no other network calls.

Rubric (also on https://mcp-safety-board.pages.dev/method.html):
    start at 100
    -2 per risky tool (deletes, writes or runs code) without destructiveHint/readOnlyHint, max -30
    -10 if fewer than half of all tools carry annotations
    -10 if the README launch snippet (npx/uvx/...) does not pin a version
    config findings from mcp-audit: High -8, Medium -4, Low -1, at most 3 counted per rule, max -40 in total
    (MCP106 is already covered by the risky-tool line, MCP105 is informational: neither is counted twice)
    A >= 90, B 80-89, C 70-79, D 60-69, F < 60
"""
import json
import sys
import urllib.request

URL = "https://mcp-safety-board.pages.dev/data/board.json"

# mcp-audit severity of each config rule that can appear in the data, as points
RULE_POINTS = {
    "MCP002": 4,   # Medium: npx/uvx launch without a pinned version
    "MCP003": 4,   # Medium: pinned to a moving tag such as @latest
    "MCP004": 8,   # High: filesystem root too broad
    "MCP005": 8,   # Critical/High: risky docker flags or mounts (Medium cases would count 4; none in the data yet)
    "MCP006": 8,   # High: remote server over plain http
    "MCP105": 0,   # Info: not scored
    "MCP106": 0,   # Low, but already scored by the risky-tool line
}


def score(r):
    s = 100
    unlabelled = r["destructive_like"] - r["destructive_with_hint"]
    s -= min(30, 2 * unlabelled)
    if r["tools_with_annotations"] < 0.5 * r["tools_total"]:
        s -= 10
    if r["install_pinned"] == "no":
        s -= 10
    findings = sum(RULE_POINTS[rule] * min(3, n) for rule, n in r.get("findings", {}).items())
    s -= min(40, findings)
    return max(0, s)


def grade(s):
    return "A" if s >= 90 else "B" if s >= 80 else "C" if s >= 70 else "D" if s >= 60 else "F"


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            board = json.load(f)
    else:
        req = urllib.request.Request(URL, headers={"User-Agent": "mcp-safety-board-score/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            board = json.load(resp)
    bad = 0
    for r in board["graded"]:
        s = score(r)
        if s != r["score"] or grade(s) != r["grade"]:
            bad += 1
            print(f"MISMATCH {r['full_name']}: recomputed {s} {grade(s)}, published {r['score']} {r['grade']}")
    n = len(board["graded"])
    print(f"{n - bad} of {n} published grades reproduced exactly (snapshot {board.get('snapshot')}).")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
