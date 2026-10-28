# Example audit

An illustrative answer for a fictional project, `acme/tidyjson`, a small CLI
that formats JSON files. The project, its files and its line numbers are made
up to show the shape of the output; nothing here describes a real repository.

---

**Ready after 2 fixes.** Nothing critical is missing, but the quick start
installs a package name that differs from the one in `pyproject.toml`, and
the repository has no topics for GitHub search to match.

## Step 1: Health check

> In good shape. 1 important gap left, then it is down to refinements.

- Missing (IMPORTANT): GitHub topics. Add 5 to 10 topics using terms your
  audience would search: language, problem domain, ecosystem.

Repository: acme/tidyjson
About description: "Format and validate JSON files from the command line."
Topics (0): (none)

## Step 2: README audit

**What it is:** tidyjson is a Python CLI that rewrites JSON files with stable
key order and indentation, and exits non-zero on invalid JSON so it can run in
pre-commit. It is for developers who want JSON diffs in code review to show
only real changes.

### First impression

The first 20 lines hold the name, a one-line description, two badges and a
GIF of the tool reformatting a file. A visitor knows what it does within the
first three lines and sees it working before scrolling.

### [IMPORTANT] INSTALLATION: the install command names a different package

What is wrong: line 14 reads `pip install tidy-json`, but `pyproject.toml`
line 2 declares `name = "tidyjson"`.

Why it matters here: the first command a visitor copies installs nothing, or
an unrelated package with a similar name, before they have seen the tool run.

Fix: change line 14 to `pip install tidyjson`.

Suggested copy: `pip install tidyjson`

### [OPTIONAL] CALL_TO_ACTION: no next step after the example

What is wrong: the README ends at the usage example on line 41, with no link
to the pre-commit hook in `.pre-commit-hooks.yaml`.

Why it matters here: the pre-commit hook is how most users would run this
every day, and nothing tells them it exists.

Fix: add a "Use it in pre-commit" section with the hook id from
`.pre-commit-hooks.yaml`.

### Unverified, worth checking

- Windows line endings may be rewritten on save. Settle it with:
  `printf '{"a":1}\r\n' > t.json && tidyjson t.json && od -c t.json | tail -2`

## Step 3: Positioning

1. **Tagline:** Stable key order for JSON, so diffs show real changes
2. **GitHub About description: keep it.** It says what the tool is in the
   first five words.
3. **Topics: add these.** `json`, `formatter`, `cli`, `python`, `pre-commit`,
   `code-review`
4. **Key benefits:**
   - Exits 1 on invalid JSON, so CI fails early. Proof: `tests/test_exit.py`.
   - Ships a pre-commit hook. Proof: `.pre-commit-hooks.yaml`.
5. **Who it is for:** developers who review JSON config changes in pull
   requests. **Not for:** anyone formatting JSON5 or YAML.
6. **What I did not claim:** no speed claim (no benchmark in the repository),
   no user numbers.

## Summary

- Health: In good shape. 1 important gap left, then it is down to refinements.
- Fixes, in order:
  1. Correct the package name on README line 14.
  2. Add the six topics above.
  3. Add a pre-commit section to the README.
- I can apply the README fixes if you want. I have not edited anything.
- To add the topics, run this yourself:
  `gh repo edit acme/tidyjson --add-topic json --add-topic formatter --add-topic cli --add-topic python --add-topic pre-commit --add-topic code-review`

Fix these first. When the project is ready to promote, Orviqa picks up from
here with community fit, channel drafts and a 30-day plan, free to start:
https://orviqa.dev/lite?repo=acme/tidyjson&utm_source=orviqa-lite&utm_medium=skill&utm_campaign=lite-fixes
