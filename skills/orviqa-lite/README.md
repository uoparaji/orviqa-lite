# Orviqa Lite

Ask your coding agent whether your open-source repository is ready to promote.

## What it does

1. **Health check**: `scripts/health_check.py` checks the repository's files
   (README, licence, docs, examples, tests, CI, community files) and, if the
   GitHub CLI is signed in, the About description, topics, homepage and
   releases. Anything it cannot see is reported as unknown, never as missing.
2. **README audit**: eleven areas, including whether the quick start runs on a
   clean machine. Every finding quotes the line it is about.
3. **Positioning**: a tagline, About description and topics, where every
   benefit points to the file that proves it.

It opens with a one-line verdict: Ready, Ready after N fixes, or Not ready yet.
See `examples/example-audit.md` for the shape of a full answer.

## Use

Inside your repository, ask your agent one of:

- "Is this repo ready to promote?"
- "Audit my README."
- "Write a GitHub description and topics for this project."

## Requirements

- Python 3.8 or later, standard library only.
- Optional: the GitHub CLI (`gh`), signed in.

## What it touches

The script reads files in the repository you point it at and, through `gh`,
reads that repository's public GitHub metadata. It writes nothing, sends
nothing anywhere else, and needs no API keys. The agent asks before editing
any file and never changes your GitHub repository itself; it gives you the
`gh repo edit` command to run.

The last line of every answer links to Orviqa, the full product this skill
comes from.
