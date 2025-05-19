# Add CloudWatch & Assistants API Logging Support

## Relevant issues
Implements enhanced logging capability for AWS CloudWatch and Assistants API

## Pre-Submission checklist
- [x] I have Added testing in the `tests/litellm/` directory
- [x] My PR passes all unit tests on `make test-unit`
- [x] My PR's scope is as isolated as possible, it only solves 1 specific problem

## Type
🆕 New Feature
✅ Test

## Changes
This PR adds support for AWS CloudWatch logging integration and comprehensive Assistants API logging to LiteLLM.

### Summary
Implements complete CloudWatch logging integration and enhanced logging for OpenAI Assistants API endpoints. This allows:
1. Logging LiteLLM activity to AWS CloudWatch
2. Capturing Assistants API calls in the logging pipeline
3. Standardized log format across all logging destinations

### Implementation Details
| File | Change Type | Description |
|------|-------------|-------------|
| litellm/integrations/cloud_watch.py | New | CloudWatch integration module |
| litellm/litellm_core_utils/litellm_logging.py | Modified | Refactored AWS logging support |
| litellm/proxy/proxy_server.py | Modified | Added logging hooks for Assistants API |
| litellm/proxy/utils.py | Modified | Added new call types to pre_call_hook |
| litellm/utils.py | Modified | Added CloudWatch to async callback logic |
| litellm/__init__.py | Modified | Added cloudwatch_callback_params attribute |

### Testing
- Added comprehensive tests for CloudWatch integration in `tests/litellm/integrations/test_cloud_watch.py`
- Added dedicated Assistants API logging tests in `tests/litellm/proxy/test_assistants_logging.py`
- Fixed test initialization issues with proper DualCache mocking
- All tests pass with the changes (940 passed, 10 skipped)

### Configuration
CloudWatch logging can be configured in LiteLLM config using:
```yaml
litellm_settings:
  telemetry: True
  success_callback: ["cloudwatch"]
  cloudwatch_callback_params:
    log_group_name: /litellm
    aws_region: eu-central-1
```

Assistants API logging is automatically enabled for:
- add_messages
- get_assistants
- run_thread 