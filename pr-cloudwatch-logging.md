# Add CloudWatch Logging Support

## Relevant issues
Implements enhanced logging capability for AWS CloudWatch

## Pre-Submission checklist
- [x] I have Added testing in the `tests/litellm/` directory
- [x] My PR passes all unit tests on `make test-unit`
- [x] My PR's scope is as isolated as possible, it only solves 1 specific problem

## Type
🆕 New Feature
✅ Test

## Changes
This PR adds support for AWS CloudWatch logging integration to LiteLLM.

### Summary
Implements complete CloudWatch logging integration. This allows:
1. Logging LiteLLM activity to AWS CloudWatch
2. Standardized log format across all logging destinations

### Implementation Details
| File | Change Type | Description |
|------|-------------|-------------|
| litellm/integrations/cloud_watch.py | New | CloudWatch integration module |
| litellm/litellm_core_utils/litellm_logging.py | Modified | Refactored AWS logging support |
| litellm/utils.py | Modified | Added CloudWatch to async callback logic |
| litellm/__init__.py | Modified | Added cloudwatch_callback_params attribute |

### Testing
- Added comprehensive tests for CloudWatch integration in `tests/litellm/integrations/test_cloud_watch.py`
- Fixed test initialization issues with proper DualCache mocking

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
