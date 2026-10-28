#!/bin/sh
# Builds a zip of the skill for one listing channel, for marketplaces that take
# an upload rather than a GitHub install.
#
#   tools/package.sh agensi   ->   dist/orviqa-lite-agensi.zip
#
# The zip holds one top-level folder, orviqa-lite/, with SKILL.md at its root.
# The skill's links back to Orviqa carry utm_medium=<channel> instead of
# utm_medium=skill. Medium, not utm_content, because /lite and /go/analyse keep
# only source, medium and campaign; that is what lets Orviqa's funnel tell
# which listing an install came from. The repository copy is never changed.
set -eu

channel="${1:?usage: tools/package.sh <channel>}"
case "$channel" in *[!a-z0-9-]*) echo "channel must be lowercase letters, digits or -" >&2; exit 64 ;; esac

root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

cp -R "$root/skills/orviqa-lite" "$work/orviqa-lite"
find "$work" \( -name '.DS_Store' -o -name '__pycache__' \) -prune -exec rm -rf {} +
sed -i.bak "s#utm_medium=skill#utm_medium=$channel#g" "$work/orviqa-lite/SKILL.md"
rm "$work/orviqa-lite/SKILL.md.bak"

mkdir -p "$root/dist"
out="$root/dist/orviqa-lite-$channel.zip"
rm -f "$out"
(cd "$work" && zip -qr "$out" orviqa-lite)
echo "$out"
