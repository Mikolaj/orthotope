# CLAUDE.md

This directory is worked on from a session rooted in `~/r/horde-ad`, and that repository's `CLAUDE.md` binds here as applicable: its portable-notes section by that section's own terms, and the rest --- the standing checks, the working style, the session facts --- wherever this directory has no rule of its own. Read it in full before touching anything here. What this directory has of its own is `README.md`, the run chapter above all, and the README wins where the two differ.

Two of its rules are restated here because a session read them the other way round:

- **A request to test or check this directory runs `check-all .` whole, before the commit, the audit and the mutants included.** They replay older readers against today's `Main.hs`, so an edit to `Main.hs`, `read-run.py` or `defects.py` owes them; the run chapter's step 8 subset is the preparation's shortcut, not the session's. *Why:* on 2026-09-03 a data change in `Main.hs` passed every hand-picked check and broke 25 audits, found by the next `check-all`.

- **The wrong-repo rule in horde-ad's file reads from here in mirror image.** Its build, test and lint commands are the ones that do not transfer; the commands that do are this README's run chapter and `checks.py`, and the shared tools in `~/.claude/bin` take this directory as their argument. *Why:* the same session took horde-ad's standing-checks section for the wrong repo's and the run chapter's step 8 subset for the tree's whole check, and the subset is what let the 25 audits break unseen.
