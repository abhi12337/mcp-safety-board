# MCP Safety Board

Grades of popular open-source MCP servers, A to F, on safety hygiene: whether tools carry safety labels (`readOnlyHint`, `destructiveHint`, …), whether install instructions pin a version, and whether committed config is risky.

**Board:** https://mcp-safety-board.pages.dev
**Check your own MCP setup** (runs in your browser, nothing uploaded): https://mcp-safety-board.pages.dev/check.html
**How grades are worked out:** https://mcp-safety-board.pages.dev/method.html

Every grade on the board was checked by hand against the server's code at the commit shown on its page. More servers are added as they are checked.

This is not a security audit. Security issues are never published here; anything that looks exploitable is reported privately to the maintainers first.

## Verify every grade yourself

You don't have to trust the grades. [`score.py`](score.py) recomputes every published score from the board's public data and checks that each one matches:

```
python score.py                   # uses the live data
python score.py data/board.json   # or the snapshot kept in this repo
```

Python standard library only. The rubric is written at the top of the file and on the [method page](https://mcp-safety-board.pages.dev/method.html).

## Independence

The board is run by one person. It has no sponsors, takes no money from any server listed, and is not affiliated with Anthropic, the MCP project or any company whose server appears on it. Nobody can pay for a grade; grades change only through re-checks.

## Request a re-check

If your server's grade is out of date or wrong, open an issue using the **Re-check** template with the repository and the commit or release to check. Grades are a snapshot of one commit, so a re-check after you add labels or pin your install command is the fastest way to raise a grade.

## Badge

Each server page has a markdown snippet for a README badge that links back to the server's grade.

By Abheesht Tripathi ([@AbheeshtTr10795](https://x.com/AbheeshtTr10795)).
