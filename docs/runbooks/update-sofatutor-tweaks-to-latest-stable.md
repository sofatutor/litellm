# Runbook: Update sofatutor-tweaks to Latest Stable Tag

This runbook describes how to update the `sofatutor-tweaks` branch to the latest stable tag from the upstream BerriAI/litellm repository.

## Prerequisites

- Git configured with access to both `origin` (sofatutor/litellm) and `upstream` (BerriAI/litellm) remotes
- GitHub CLI (`gh`) installed and authenticated
- Python environment with test dependencies installed

## Overview

1. Fetch latest upstream tags
2. Identify the latest stable tag
3. Create a new branch based on that tag
4. Merge sofatutor-tweaks into the new branch (or vice versa)
5. Resolve any conflicts
6. Run tests to verify
7. Update PR #4 with the new base branch
8. Create a new `-sofatutor` tag
9. Draft a new release with all changes

---

## Step 1: Fetch Latest Upstream Tags

```bash
# Ensure upstream remote is configured
git remote -v | grep upstream || git remote add upstream https://github.com/BerriAI/litellm.git

# Fetch all tags from upstream
git fetch upstream --tags
```

## Step 2: Identify the Latest Stable Tag

```bash
# List all stable tags, sorted by version
git tag -l "*-stable*" | sort -V | tail -10

# The latest stable tag should be something like: v1.XX.Y-stable.Z
# Store it in a variable for later use
LATEST_STABLE_TAG=$(git tag -l "*-stable*" | grep -v sofatutor | sort -V | tail -1)
echo "Latest stable tag: $LATEST_STABLE_TAG"
```

## Step 3: Create a New Branch Based on the Stable Tag

```bash
# Create and checkout a new branch from the stable tag
git checkout -b "stable-update-${LATEST_STABLE_TAG}" "${LATEST_STABLE_TAG}"

# Push this branch to origin
git push -u origin "stable-update-${LATEST_STABLE_TAG}"
```

## Step 4: Merge sofatutor-tweaks into the New Branch

```bash
# Merge sofatutor-tweaks into the new stable branch
git merge sofatutor-tweaks
```

### If there are conflicts:

1. **Identify conflicting files:**
   ```bash
   git status
   ```

2. **Common conflict resolution strategies:**

   - **For our custom files** (e.g., `.github/workflows/sofatutor_image.yml`):
     Keep our version (`--ours` from sofatutor-tweaks perspective, but since we're merging INTO stable, use `--theirs`):
     ```bash
     git checkout --theirs <file>
     ```

   - **For upstream changes we want to keep:**
     ```bash
     git checkout --ours <file>
     ```

   - **For mixed changes** (manual resolution required):
     Open the file, look for conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), and manually resolve.

3. **After resolving each file:**
   ```bash
   git add <resolved-file>
   ```

4. **Complete the merge:**
   ```bash
   git commit -m "Merge sofatutor-tweaks into ${LATEST_STABLE_TAG}"
   ```

## Step 5: Run Tests

```bash
# Install dependencies if needed
pip install -e ".[dev]"

# Run the core test suite
pytest tests/local_testing/ -v --tb=short

# Run specific tests related to our customizations
pytest tests/llm_responses_api_testing/ -v

# If you have specific proxy tests
pytest tests/proxy_unit_tests/ -v -k "not slow"
```

### If tests fail:

1. Investigate the failure
2. Fix the issue in the merge branch
3. Commit the fix:
   ```bash
   git add .
   git commit -m "fix: resolve test failures after merge"
   ```

## Step 6: Update sofatutor-tweaks Branch

```bash
# Switch to sofatutor-tweaks
git checkout sofatutor-tweaks

# Fast-forward merge from the stable-update branch
git merge "stable-update-${LATEST_STABLE_TAG}"

# Push the updated sofatutor-tweaks
git push origin sofatutor-tweaks
```

## Step 7: Update PR #4 Base Branch

PR #4 contains all sofatutor customizations. After updating sofatutor-tweaks, PR #4 should automatically reflect the changes if it's based on sofatutor-tweaks.

If you need to update the PR base branch:

```bash
# Via GitHub CLI
gh pr edit 4 --base main  # or whatever the target base should be
```

Or update via GitHub UI:
1. Go to https://github.com/sofatutor/litellm/pull/4
2. Click "Edit" next to the base branch
3. Select the appropriate base branch

## Step 8: Create the New Sofatutor Tag

```bash
# Create the new tag with -sofatutor suffix
NEW_SOFATUTOR_TAG="${LATEST_STABLE_TAG}-sofatutor"
git tag -a "${NEW_SOFATUTOR_TAG}" -m "Sofatutor release based on ${LATEST_STABLE_TAG}"

# Push the new tag
git push origin "${NEW_SOFATUTOR_TAG}"
```

## Step 9: Draft a New Release

### Get the previous sofatutor tag:

```bash
PREVIOUS_SOFATUTOR_TAG=$(git tag -l "*-sofatutor" | sort -V | tail -2 | head -1)
echo "Previous sofatutor tag: $PREVIOUS_SOFATUTOR_TAG"
```

### Generate changelog between tags:

```bash
# Get commits between the two sofatutor tags
git log "${PREVIOUS_SOFATUTOR_TAG}..${NEW_SOFATUTOR_TAG}" --oneline --no-merges

# Get upstream changes (from previous stable to new stable)
PREVIOUS_STABLE_TAG=$(echo $PREVIOUS_SOFATUTOR_TAG | sed 's/-sofatutor//')
git log "${PREVIOUS_STABLE_TAG}..${LATEST_STABLE_TAG}" --oneline --no-merges | head -50
```

### Create the release:

```bash
gh release create "${NEW_SOFATUTOR_TAG}" \
  --title "${NEW_SOFATUTOR_TAG}" \
  --notes "## What's Changed

### Upstream Changes (${PREVIOUS_STABLE_TAG} → ${LATEST_STABLE_TAG})
<!-- List key upstream changes here -->
- See full changelog: https://github.com/BerriAI/litellm/compare/${PREVIOUS_STABLE_TAG}...${LATEST_STABLE_TAG}

### Sofatutor Customizations
- **Proxy**: Centralized error handling with enhanced OpenAI exception mapping and parsing for clearer logs and standardized responses
- **Proxy**: Rename function from \`image_generation\` to \`moderation\` in the moderations endpoint; change call type from \`audio_speech\` to \`pass_through_endpoint\` for accurate logging/metrics
- **OpenAI (audio speech)**: Add streaming support via context managers and implement deferred streaming to avoid prematurely closing upstream streams
- **CloudWatch Logging**: Remove Assistants API references from CloudWatch logging (to reduce log noise)
- **CI**: Add \`.github/workflows/sofatutor_image.yml\` for Sofatutor Docker image builds
- **fix(responses-api)**: Support instructions as list when using prompt objects

### Based on
- LiteLLM ${LATEST_STABLE_TAG}
- Previous Sofatutor release: ${PREVIOUS_SOFATUTOR_TAG}

**Full Changelog**: https://github.com/sofatutor/litellm/compare/${PREVIOUS_SOFATUTOR_TAG}...${NEW_SOFATUTOR_TAG}"
```

### Verify the release:

1. Go to https://github.com/sofatutor/litellm/releases
2. Verify the release was created correctly
3. Edit if needed with `gh release edit "${NEW_SOFATUTOR_TAG}" --notes "..."`

---

## Quick Reference Script

Here's a complete script you can run (after setting the variables):

```bash
#!/bin/bash
set -e

# Configuration
UPSTREAM_REMOTE="upstream"
ORIGIN_REMOTE="origin"

# Step 1: Fetch upstream
git fetch $UPSTREAM_REMOTE --tags

# Step 2: Find latest stable tag
LATEST_STABLE_TAG=$(git tag -l "*-stable*" | grep -v sofatutor | sort -V | tail -1)
echo "Latest stable tag: $LATEST_STABLE_TAG"

# Step 3: Create update branch
BRANCH_NAME="stable-update-${LATEST_STABLE_TAG}"
git checkout -b "$BRANCH_NAME" "$LATEST_STABLE_TAG"

# Step 4: Merge sofatutor-tweaks
echo "Merging sofatutor-tweaks..."
if ! git merge sofatutor-tweaks -m "Merge sofatutor-tweaks into ${LATEST_STABLE_TAG}"; then
    echo "⚠️  Conflicts detected! Please resolve manually, then run:"
    echo "    git add . && git commit"
    echo "    Then re-run this script from step 5"
    exit 1
fi

# Step 5: Run tests
echo "Running tests..."
pytest tests/local_testing/ -v --tb=short -x

# Step 6: Update sofatutor-tweaks
git checkout sofatutor-tweaks
git merge "$BRANCH_NAME"
git push $ORIGIN_REMOTE sofatutor-tweaks

# Step 7: Create new tag
NEW_SOFATUTOR_TAG="${LATEST_STABLE_TAG}-sofatutor"
PREVIOUS_SOFATUTOR_TAG=$(git tag -l "*-sofatutor" | sort -V | tail -1)

git tag -a "$NEW_SOFATUTOR_TAG" -m "Sofatutor release based on ${LATEST_STABLE_TAG}"
git push $ORIGIN_REMOTE "$NEW_SOFATUTOR_TAG"

echo "✅ Done! New tag: $NEW_SOFATUTOR_TAG"
echo "📝 Don't forget to create a release at:"
echo "   https://github.com/sofatutor/litellm/releases/new?tag=${NEW_SOFATUTOR_TAG}"
```

---

## Troubleshooting

### Merge conflicts in specific files

| File Type | Resolution Strategy |
|-----------|---------------------|
| `.github/workflows/sofatutor_image.yml` | Keep sofatutor version |
| `litellm/proxy/*.py` | Carefully merge, keeping both upstream fixes and our customizations |
| `litellm/llms/openai/*.py` | Review changes, upstream usually takes priority unless we have specific fixes |
| `tests/*` | Usually keep both sets of tests |

### Tests failing after merge

1. Check if it's a dependency issue: `pip install -e ".[dev]" --upgrade`
2. Check if upstream changed APIs we depend on
3. Review the failing test to understand what changed

### Tag already exists

If the sofatutor tag already exists:
```bash
# Delete local tag
git tag -d "${NEW_SOFATUTOR_TAG}"

# Delete remote tag (careful!)
git push origin --delete "${NEW_SOFATUTOR_TAG}"

# Recreate
git tag -a "${NEW_SOFATUTOR_TAG}" -m "..."
git push origin "${NEW_SOFATUTOR_TAG}"
```

---

## Checklist

- [ ] Fetched latest upstream tags
- [ ] Identified latest stable tag: `_________________`
- [ ] Created update branch
- [ ] Merged sofatutor-tweaks
- [ ] Resolved all conflicts
- [ ] All tests passing
- [ ] Updated sofatutor-tweaks branch
- [ ] Updated PR #4 if needed
- [ ] Created new `-sofatutor` tag
- [ ] Drafted release with changelog
- [ ] Published release

---

*Last updated: November 2024*
