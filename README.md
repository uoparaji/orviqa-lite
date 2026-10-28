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

### Gemini CLI

```bash
gemini extensions install https://github.com/uoparaji/orviqa-lite
```

### Codex, Copilot, Cursor, OpenCode, Amp, Goose

These agents load [Agent Skills](https://agentskills.io) from `.agents/skills`.
Install for every project:

```bash
git clone --depth 1 https://github.com/uoparaji/orviqa-lite /tmp/orviqa-lite
mkdir -p ~/.agents/skills
cp -R /tmp/orviqa-lite/skills/orviqa-lite ~/.agents/skills/
```

Or for one repository only, copy it into `.agents/skills/` at the repository
root instead.

### Windsurf, Cline, Kiro

Same folder, different place. Copy `skills/orviqa-lite/` into:

| Agent | One repository | Every project |
| --- | --- | --- |
| Windsurf | `.windsurf/skills/` | `~/.codeium/windsurf/skills/` |
| Cline | `.cline/skills/` | `~/.cline/skills/` |
| Kiro | `.kiro/skills/` | `~/.kiro/skills/` |

Then, inside your repository, ask: "Is this repo ready to promote?" Some agents
also let you call it directly, for example `/orviqa-lite` in Copilot, Cursor and
Kiro, or `$orviqa-lite` in Codex.

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
