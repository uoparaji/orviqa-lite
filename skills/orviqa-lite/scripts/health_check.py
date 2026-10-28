#!/usr/bin/env python3
"""Orviqa Lite repository health check.

A checklist, not a judgement call, so it is computed here rather than by the
model. Reads the local working tree, and the GitHub "About" fields and releases
through the `gh` CLI when it is installed and signed in. Anything it cannot see
is reported as unknown, never as missing.

Usage:
    python3 health_check.py [repo_path] [--json]

Standard library only. Exits 0 whatever it finds.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "target", ".venv",
    "venv", "__pycache__", ".next", ".turbo", "coverage",
}

TESTS_RE = re.compile(
    r"(^|/)(tests?|spec|__tests__|e2e)(/|$)"
    r"|\.(test|spec)\.(ts|tsx|js|jsx|py|go|rb|rs|java|kt)$"
    r"|_test\.(go|py|rb)$",
    re.I,
)


def run(cmd: list[str], cwd: str) -> str | None:
    try:
        out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return out.stdout if out.returncode == 0 else None


def list_paths(root: str) -> list[str]:
    tracked = run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], root)
    if tracked is not None:
        return [p for p in tracked.splitlines() if p]
    paths = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        rel = os.path.relpath(dirpath, root)
        for f in filenames:
            paths.append(f if rel == "." else f"{rel}/{f}".replace(os.sep, "/"))
    return paths


def github_meta(root: str) -> dict | None:
    """Description, topics, homepage and release count, or None if gh is unavailable."""
    if not shutil.which("gh"):
        return None
    raw = run(["gh", "repo", "view", "--json", "nameWithOwner,description,repositoryTopics,homepageUrl"], root)
    if raw is None:
        return None
    data = json.loads(raw)
    releases = run(["gh", "release", "list", "--limit", "1"], root)
    return {
        "nameWithOwner": data.get("nameWithOwner") or "",
        "description": (data.get("description") or "").strip(),
        "topics": [t["name"] for t in (data.get("repositoryTopics") or [])],
        "homepage": (data.get("homepageUrl") or "").strip(),
        "has_releases": None if releases is None else bool(releases.strip()),
    }


def signals(paths: list[str], meta: dict | None) -> dict[str, bool | None]:
    def has(pattern: str) -> bool:
        rx = re.compile(pattern, re.I)
        return any(rx.search(p) for p in paths)

    gh = meta is not None
    return {
        "readme": has(r"^readme(\.md|\.rst|\.txt|\.adoc)?$"),
        "license": has(r"^(licen[cs]e|copying)(\.md|\.txt)?$"),
        "description": bool(meta["description"]) if gh else None,
        "topics": bool(meta["topics"]) if gh else None,
        "examples": has(r"^(examples?|samples?|demos?)/"),
        "docs": has(r"^docs?/") or has(r"^(mkdocs\.ya?ml|docusaurus\.config\.(js|ts)|book\.toml|\.vitepress/)"),
        "contributing": has(r"^(\.github/)?contributing(\.md|\.rst)?$"),
        "tests": any(TESTS_RE.search(p) for p in paths),
        "ci": has(r"^\.github/workflows/.+\.ya?ml$")
        or has(r"^(\.travis\.yml|\.circleci/config\.yml|azure-pipelines\.yml|\.gitlab-ci\.yml|Jenkinsfile)$"),
        "releases": meta["has_releases"] if gh else None,
        "homepage": bool(meta["homepage"]) if gh else None,
        "issue-templates": has(r"^\.github/issue_template"),
        "pr-template": has(r"^(\.github/)?pull_request_template(\.md)?$"),
        "code-of-conduct": has(r"^(\.github/)?code_of_conduct(\.md)?$"),
        "changelog": has(r"^(changelog|history)(\.md|\.rst)?$"),
        "social-preview": None,  # Not exposed by any API.
    }


# id, label, severity, recommendation when missing
CHECKS = [
    ("readme", "README", "CRITICAL",
     "Add a README with a one-line description, an install command, and a minimal runnable example."),
    ("license", "LICENSE", "CRITICAL",
     "Add a LICENSE file. Without one the default is all rights reserved, and most companies block unlicensed dependencies."),
    ("description", "Repository description", "CRITICAL",
     "Set the GitHub About field to one concrete sentence naming what the project does and for whom."),
    ("topics", "GitHub topics", "IMPORTANT",
     "Add 5 to 10 topics using terms your audience would search: language, problem domain, ecosystem."),
    ("examples", "Examples directory", "IMPORTANT",
     "Add examples/ with at least one self-contained, runnable example."),
    ("docs", "Documentation", "IMPORTANT",
     "Start a docs/ directory so the README can stay short and the quick start stays near the top."),
    ("contributing", "CONTRIBUTING.md", "IMPORTANT",
     "Add CONTRIBUTING.md covering local setup, the test command, and what changes you accept."),
    ("tests", "Tests", "IMPORTANT",
     "Add tests for the main public entry points. Evaluators read no tests as risk."),
    ("ci", "Continuous integration", "IMPORTANT",
     "Add a CI workflow that installs, builds and tests on push and pull request."),
    ("releases", "Releases", "IMPORTANT",
     "Cut a tagged release with human-written notes, even at 0.1.0."),
    ("homepage", "Homepage / demo URL", "OPTIONAL",
     "Point the homepage field at your docs site or a live demo."),
    ("issue-templates", "Issue templates", "OPTIONAL",
     "Add bug-report and feature-request templates under .github/ISSUE_TEMPLATE/."),
    ("pr-template", "Pull request template", "OPTIONAL",
     "Add .github/PULL_REQUEST_TEMPLATE.md with a description prompt and a tests/docs checklist."),
    ("code-of-conduct", "CODE_OF_CONDUCT.md", "OPTIONAL",
     "Adopt the Contributor Covenant from the Insights > Community tab on GitHub."),
    ("changelog", "Changelog", "OPTIONAL",
     "Keep a CHANGELOG.md, or generate one from your release notes."),
    ("social-preview", "Social preview image", "OPTIONAL",
     "Check Settings > General > Social preview and upload a 1280x640 image."),
]


def headline(critical: int, important: int, total: int) -> str:
    if critical:
        return f"{critical} critical gap{'s' if critical > 1 else ''} blocking adoption. Fix these before any promotion."
    if important > 2:
        return f"The basics are covered, but {important} important gaps are costing you evaluators."
    if important:
        return f"In good shape. {important} important gap{'s' if important > 1 else ''} left, then it is down to refinements."
    if total:
        return "Everything critical and important is in place. Only optional refinements remain."
    return "Every health check passes."


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    root = os.path.abspath(args[0] if args else ".")

    meta = github_meta(root)
    sig = signals(list_paths(root), meta)

    results = []
    for cid, label, severity, rec in CHECKS:
        value = sig[cid]
        status = "unknown" if value is None else ("present" if value else "missing")
        results.append({"id": cid, "label": label, "severity": severity,
                        "status": status, "recommendation": rec})

    missing = [r for r in results if r["status"] == "missing"]
    crit = sum(r["severity"] == "CRITICAL" for r in missing)
    imp = sum(r["severity"] == "IMPORTANT" for r in missing)
    report = {
        "repository": root,
        "githubMetadata": "read with gh" if meta else "unavailable (gh missing or not signed in)",
        "headline": headline(crit, imp, len(missing)),
        "about": {k: meta[k] for k in ("nameWithOwner", "description", "topics", "homepage")} if meta else None,
        "checks": results,
    }

    if as_json:
        print(json.dumps(report, indent=2))
        return

    print(f"# Health check: {os.path.basename(root)}\n")
    print(f"{report['headline']}\n")
    print(f"GitHub metadata: {report['githubMetadata']}\n")
    if meta:
        print(f"Repository: {meta['nameWithOwner']}")
        print(f"About description: {meta['description'] or '(empty)'}")
        print(f"Topics ({len(meta['topics'])}): {', '.join(meta['topics']) or '(none)'}")
        print(f"Homepage: {meta['homepage'] or '(none)'}\n")
    for sev in ("CRITICAL", "IMPORTANT", "OPTIONAL"):
        print(f"## {sev}")
        for r in (r for r in results if r["severity"] == sev):
            mark = {"present": "[x]", "missing": "[ ]", "unknown": "[?]"}[r["status"]]
            line = f"- {mark} {r['label']}"
            if r["status"] != "present":
                line += f": {r['recommendation']}"
            print(line)
        print()


if __name__ == "__main__":
    main()
