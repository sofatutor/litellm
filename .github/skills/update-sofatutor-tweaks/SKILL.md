---
name: update-sofatutor-tweaks
description: Update the sofatutor-tweaks branch to the latest upstream stable LiteLLM tag, resolve merge conflicts, verify the result, cut the matching -sofatutor tag, and prepare release notes. Use this when asked to refresh the Sofatutor fork against the newest stable upstream release.
argument-hint: Optional inputs: target stable tag, target PR number, notes about expected custom conflict resolutions.
---

# Update sofatutor-tweaks

Use this skill when the task is to refresh the Sofatutor fork against the latest stable upstream LiteLLM release and publish the matching Sofatutor release artifacts.

## Why This Fork Exists

Sofatutor keeps one clearly fork-specific customization on top of upstream LiteLLM:

- CloudWatch logging support, including callback wiring, configuration, docs, and tests.

The branch may also contain bug fixes or operational tweaks that were developed here first, such as OpenAI TTS streaming fixes, Responses API prompt-object compatibility, or Slack alert hardening. Do not treat those as required fork behaviors by default. Keep them only if the target upstream stable tag still does not contain an equivalent fix.

## Inputs To Confirm

- Current repository is the Sofatutor fork or has both `origin` and `upstream` remotes configured correctly.
- GitHub CLI is installed and authenticated.
- The operator has permission to push branches, tags, and release updates.
- The default PR to check is `#4` unless the user specifies a different one.

## Working Rules

- Inspect the current branch, remotes, and worktree state before changing anything.
- Prefer the latest non-`-sofatutor` stable tag unless the user specifies a target tag explicitly.
- Preserve both upstream fixes and Sofatutor customizations; do not blindly take one side for mixed conflicts.
- Verify current branch-specific customizations against `origin/main` before drafting release notes or claiming that a historical tweak is still required.
- If tests fail or conflicts are ambiguous, stop and summarize the blocker with exact files or commands.
- Prefer file-backed release notes over giant inline shell strings. Use [release-notes-template.md](./release-notes-template.md) and pass it to `gh release create --notes-file` after filling in the placeholders.

## Workflow

### 1. Validate Setup

Run the following checks first:

```bash
git status --short --branch
git remote -v
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream https://github.com/BerriAI/litellm.git
gh auth status
```

If the worktree is dirty, confirm that the user wants to proceed before mutating branch state.

### 2. Fetch Upstream Tags And Detect The Target

```bash
git fetch upstream --tags
git tag -l "*-stable*" | grep -v sofatutor | sort -V | tail -10
LATEST_STABLE_TAG=$(git tag -l "*-stable*" | grep -v sofatutor | sort -V | tail -1)
echo "$LATEST_STABLE_TAG"
```

If the user supplied a specific tag, use it instead of `LATEST_STABLE_TAG`.

### 3. Create The Update Branch

```bash
BRANCH_NAME="stable-update-${LATEST_STABLE_TAG}"
git checkout -b "$BRANCH_NAME" "$LATEST_STABLE_TAG"
git push -u origin "$BRANCH_NAME"
```

If the branch already exists locally or remotely, inspect it and reuse it only if it already points at the intended base.

### 4. Merge `sofatutor-tweaks`

```bash
git merge sofatutor-tweaks -m "Merge sofatutor-tweaks into ${LATEST_STABLE_TAG}"
```

If there are conflicts:

1. Inspect `git status`.
2. Use `git checkout --theirs` for Sofatutor-owned files that should stay as customized fork behavior, such as `.github/workflows/sofatutor_image.yml`.
3. Use `git checkout --ours` when the upstream version should win unchanged.
4. Manually resolve mixed files, especially under `litellm/proxy/` and `litellm/llms/openai/`.
5. Stage each resolved file with `git add <file>`.
6. Complete the merge commit if Git did not finish it automatically.

Conflict heuristics:

- `litellm/integrations/cloud_watch.py`, `litellm/litellm_core_utils/litellm_logging.py`, `litellm/utils.py`, `litellm/__init__.py`, `docs/my-website/docs/proxy/logging.md`: preserve the CloudWatch customization unless the user explicitly decides to remove it.
- `litellm/llms/openai/*.py`, `litellm/types/llms/openai.py`, `litellm/integrations/SlackAlerting/*.py`: treat as conditional bug fixes. Keep them only if upstream stable still lacks the equivalent behavior.
- `.github/workflows/sofatutor_image.yml`: keep only if the Sofatutor deployment still depends on this workflow.
- `tests/*`: keep both sides when possible.

### 5. Verify The Merge

Install test dependencies if needed, then run the relevant suites:

```bash
pip install -e ".[dev]"
pytest tests/local_testing/ -v --tb=short
pytest tests/llm_responses_api_testing/ -v
pytest tests/proxy_unit_tests/ -v -k "not slow"
```

If one of these suites is too expensive or unavailable in the current environment, say exactly what was skipped and why.

### 6. Update `sofatutor-tweaks`

```bash
git checkout sofatutor-tweaks
git merge "$BRANCH_NAME"
git push origin sofatutor-tweaks
```

If fast-forward is not possible, explain why before creating any additional merge commit on `sofatutor-tweaks`.

### 7. Check Or Update The PR

PR `#4` is expected to carry the Sofatutor customizations. Verify whether it already reflects the updated branch. Only edit the base branch if the user asks for that specific change.

Example:

```bash
gh pr view 4
gh pr edit 4 --base main
```

### 8. Create The New Sofatutor Tag

```bash
NEW_SOFATUTOR_TAG="${LATEST_STABLE_TAG}-sofatutor"
git tag -a "$NEW_SOFATUTOR_TAG" -m "Sofatutor release based on ${LATEST_STABLE_TAG}"
git push origin "$NEW_SOFATUTOR_TAG"
```

If the tag already exists, inspect whether it points to the intended commit before deleting or recreating it.

### 9. Prepare And Publish Release Notes

Gather the comparison range:

```bash
PREVIOUS_SOFATUTOR_TAG=$(git tag -l "*-sofatutor" | sort -V | tail -2 | head -1)
PREVIOUS_STABLE_TAG=$(echo "$PREVIOUS_SOFATUTOR_TAG" | sed 's/-sofatutor//')
git log "${PREVIOUS_SOFATUTOR_TAG}..${NEW_SOFATUTOR_TAG}" --oneline --no-merges
git log "${PREVIOUS_STABLE_TAG}..${LATEST_STABLE_TAG}" --oneline --no-merges | head -50
```

Fill in [release-notes-template.md](./release-notes-template.md) with the resolved tag values and any noteworthy upstream or Sofatutor-specific changes. Then create the release with a notes file instead of embedding a large multiline string directly in the shell.

When writing the Sofatutor customization section, separate true fork-specific behavior from bug fixes:

- CloudWatch logging support should be treated as the primary Sofatutor customization unless the user says otherwise.
- OpenAI TTS streaming, Responses API prompt-object compatibility, Slack alert hardening, and similar fixes should only be listed if the chosen upstream stable tag still lacks them.
- Operational items like `.github/workflows/sofatutor_image.yml` should only be listed if they are still part of the deployment model.

Example:

```bash
gh release create "$NEW_SOFATUTOR_TAG" \
  --title "$NEW_SOFATUTOR_TAG" \
  --notes-file .github/skills/update-sofatutor-tweaks/release-notes-template.md
```

## Completion Checklist

- Upstream tags fetched.
- Latest stable tag identified and confirmed.
- Stable update branch created from that tag.
- `sofatutor-tweaks` merged and conflicts resolved.
- Relevant tests run or explicitly skipped.
- `sofatutor-tweaks` updated and pushed.
- PR status checked, and base edited only if requested.
- New `-sofatutor` tag created and pushed.
- Release notes prepared and release created or draft-ready.

## Resources

- [release-notes-template.md](./release-notes-template.md)
- [quick-reference.sh](./quick-reference.sh)