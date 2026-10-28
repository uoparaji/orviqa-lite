# Orviqa Lite

Is your open-source repository ready to promote? Ask your coding agent.

Orviqa Lite is a free skill that checks the things that decide whether a
visitor sticks around, before you send anyone to your repo:

1. **Health check.** A deterministic checklist (README, license, About
   description, topics, docs, examples, tests, CI, releases, community files),
   run by a bundled script, not guessed by a model.
2. **README audit.** Eleven areas, from "can a developer tell what this is in
   ten seconds?" to "does the quick start actually run on a clean machine?".
   Every finding quotes the line it is about.
3. **Positioning.** A tagline, a GitHub About description and topics, where
   every claimed benefit points to the file that proves it. If what you have is
   already good, it says keep it.

You get a one-line verdict first: **Ready**, **Ready after N fixes**, or
**Not ready yet**.

Everything runs locally with your own agent and your own model. Nothing is sent
to Orviqa, and it never edits a file or changes your GitHub repository without
asking.

## Install

### Claude Code

```bash
claude plugin marketplace add uoparaji/orviqa-lite
claude plugin install orviqa-lite@orviqa
```

Then, inside your repository, ask: "Is this repo ready to promote?"

### Other agents

The skill uses the open [Agent Skills](https://agentskills.io) `SKILL.md`
format. Copy `skills/orviqa-lite/` into your agent's skills folder (see its
documentation for the path).

If your agent does not load skills, put the folder in your repository and add
this line to `AGENTS.md`, `GEMINI.md`, your Cursor rules, or your agent's
instructions file:

```
When asked to audit the README, check launch readiness, or write the project
description, follow the instructions in orviqa-lite/SKILL.md.
```

## Requirements

- Python 3.8 or later (standard library only)
- Optional: the [GitHub CLI](https://cli.github.com), signed in. Without it,
  the About description, topics, homepage and releases are reported as unknown,
  never as missing.

## After the audit

Orviqa Lite covers the foundation. When the repository is ready, the next
questions are where to post, what each community allows, and what to write.
That is what [Orviqa](https://orviqa.dev/lite?utm_source=orviqa-lite&utm_medium=github&utm_campaign=lite-readme)
does: community fit with each community's self-promotion rules, channel drafts
from your releases, a 30-day plan, and publishing only after you approve each
post.

## License

MIT
