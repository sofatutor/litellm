#!/bin/bash
set -euo pipefail

UPSTREAM_REMOTE="upstream"
ORIGIN_REMOTE="origin"

git remote get-url "$UPSTREAM_REMOTE" >/dev/null 2>&1 || git remote add "$UPSTREAM_REMOTE" https://github.com/BerriAI/litellm.git
git fetch "$UPSTREAM_REMOTE" --tags

LATEST_STABLE_TAG=$(git tag -l "*-stable*" | grep -v sofatutor | sort -V | tail -1)
echo "Latest stable tag: $LATEST_STABLE_TAG"

BRANCH_NAME="stable-update-${LATEST_STABLE_TAG}"
git checkout -b "$BRANCH_NAME" "$LATEST_STABLE_TAG"
git push -u "$ORIGIN_REMOTE" "$BRANCH_NAME"

if ! git merge sofatutor-tweaks -m "Merge sofatutor-tweaks into ${LATEST_STABLE_TAG}"; then
  echo "Conflicts detected. Resolve them, then continue with verification and release steps from the skill instructions."
  exit 1
fi

pytest tests/local_testing/ -v --tb=short -x

git checkout sofatutor-tweaks
git merge "$BRANCH_NAME"
git push "$ORIGIN_REMOTE" sofatutor-tweaks

NEW_SOFATUTOR_TAG="${LATEST_STABLE_TAG}-sofatutor"
git tag -a "$NEW_SOFATUTOR_TAG" -m "Sofatutor release based on ${LATEST_STABLE_TAG}"
git push "$ORIGIN_REMOTE" "$NEW_SOFATUTOR_TAG"

echo "Prepared branch: $BRANCH_NAME"
echo "Prepared tag: $NEW_SOFATUTOR_TAG"
echo "Review .github/skills/update-sofatutor-tweaks/release-notes-template.md before creating the release."