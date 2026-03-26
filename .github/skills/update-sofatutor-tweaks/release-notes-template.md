## What's Changed

### Upstream Changes (${PREVIOUS_STABLE_TAG} -> ${LATEST_STABLE_TAG})

- See full changelog: https://github.com/BerriAI/litellm/compare/${PREVIOUS_STABLE_TAG}...${LATEST_STABLE_TAG}
- Add a concise summary of upstream fixes or features that matter to Sofatutor.

### Sofatutor Customizations

- CloudWatch logging support: custom callback, configuration, docs, and tests.

### Additional Bug Fixes Carried Forward Only If Still Missing Upstream

- OpenAI audio speech: deferred streaming support plus TTS logging and cost-accounting fixes.
- Responses API: support `instructions` as a list when using prompt objects.
- Slack alerting: failed-tracking alerts are non-blocking when webhook configuration is missing.
- CI or deployment-specific workflow adjustments, if still required.

Trim this section aggressively after checking the live diff against `origin/main` and the chosen upstream stable tag. If upstream already includes an equivalent fix, do not list it as a Sofatutor-specific change.

### Based On

- LiteLLM ${LATEST_STABLE_TAG}
- Previous Sofatutor release: ${PREVIOUS_SOFATUTOR_TAG}

**Full Changelog**: https://github.com/sofatutor/litellm/compare/${PREVIOUS_SOFATUTOR_TAG}...${NEW_SOFATUTOR_TAG}