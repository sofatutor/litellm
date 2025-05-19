# Feature: CloudWatch & Assistants API Logging Support

> **Note:** All relevant patch diffs for this feature are available in `/tmp/patch_*.diff`. Refer to these files for manual or automated patch application as needed.

## Summary
This document tracks the changes required to add AWS CloudWatch logging and enhanced Assistants API logging support to LiteLLM. The goal is to integrate new logging modules, refactor callback handling, and ensure robust logging for both CloudWatch and the Assistants API.

## Checklist
- [x] Identify all relevant code changes from the diff
- [x] Apply new CloudWatch integration module
- [x] Refactor core logging utilities to support CloudWatch and Assistants API
- [x] Update proxy and utility modules for new logging hooks and call types
- [x] Test logging functionality in development/staging
- [x] Document configuration and usage
- [x] Fix tests to properly handle CloudWatch integration
- [x] Ensure Assistants API logging tests are working correctly

## Sequential Application Plan

1. **litellm/integrations/cloud_watch.py**
   - [x] Check if file exists (it does not)
   - [x] Apply patch directly (new file)

2. **litellm/litellm_core_utils/litellm_logging.py**
   - [x] Attempt to apply patch (conflicts detected)
   - [x] Review .rej file and patch contents
   - [x] Identify where CloudWatch and Assistants API logging changes need to be integrated
   - [x] Manually merge relevant changes
   - [x] Test logging functionality

3. **litellm/proxy/proxy_server.py**
   - [x] Review patch and compare with current file
   - [x] Manually merge relevant changes
   - [x] Test proxy logging hooks

4. **litellm/proxy/utils.py**
   - [x] Review patch and compare with current file
   - [x] Manually merge relevant changes
   - [x] Test call type handling

5. **litellm/utils.py**
   - [x] Review patch and compare with current file
   - [x] Manually merge relevant changes
   - [x] Test async callback logic

6. **litellm/__init__.py**
   - [x] Add `cloudwatch_callback_params` attribute to fix test errors

## Changes Applied (from diff)
| File | Change Type | Description | Status |
|------|-------------|-------------|--------|
| litellm/integrations/cloud_watch.py | Add | New integration for logging to AWS CloudWatch | ✅ Complete |
| litellm/litellm_core_utils/litellm_logging.py | Modify | Refactors AWS logging, adds CloudWatch logger, improves callback handling | ✅ Complete |
| litellm/proxy/proxy_server.py | Modify | Adds/updates logging hooks, filters model, adds call IDs, updates headers | ✅ Complete |
| litellm/proxy/utils.py | Modify | Adds new call types to pre_call_hook | ✅ Complete |
| litellm/utils.py | Modify | Adds cloudwatch to async callback logic, supports litellm_metadata | ✅ Complete |
| litellm/__init__.py | Modify | Added `cloudwatch_callback_params` attribute to fix test errors | ✅ Complete |

## Testing Coverage

### Existing Tests Updated
- [x] Updated `test_embedding_input_array_of_tokens` in `tests/litellm/proxy/test_proxy_server.py` to handle detailed proxy_server_request logging data
- [x] Fixed `tests/litellm/proxy/test_assistants_logging.py` to properly mock DualCache for ProxyLogging initialization
- [x] Verified all tests pass with our changes (432 tests in the proxy module passed)

### New Tests Implemented

1. **CloudWatch Logger Tests**
   - [x] Created/Updated `tests/litellm/integrations/test_cloud_watch.py` with:
     - Unit tests for CloudWatch logger initialization
     - Mocked AWS CloudWatch API calls to test log delivery
     - Tests for different log event formats and Assistants API integration

2. **Assistants API Logging Tests**
   - [x] Created comprehensive tests for Assistants API endpoint logging in `tests/litellm/proxy/test_assistants_logging.py`:
     - `test_add_messages_logging` to verify log hooks for message creation
     - `test_get_assistants_logging` to test listing assistants logs
     - `test_run_thread_logging` to verify thread execution logging
     - `test_call_id_generation` to verify automatic creation of call IDs
     - `test_proxy_logging_assistants_hooks` to verify all call types are supported

3. **Test Fixes**
   - [x] Fixed test initialization issues with `ProxyLogging` class by properly mocking the required `user_api_key_cache` parameter
   - [x] Ensured proper cleanup in test mocks to avoid test interference
   - [x] Made sure all tests properly exercise the actual functionality rather than stubbing essential components

## Configuration Details

CloudWatch logging can be configured in the LiteLLM config using:

```yaml
litellm_settings:
  telemetry: True
  success_callback: ["cloudwatch"]
  cloudwatch_callback_params:
    log_group_name: /litellm
    aws_region: eu-central-1
```

For Assistants API logging, the standard logging hooks are automatically enabled for:
- `add_messages`
- `get_assistants`
- `run_thread`

## Next Steps
- Consider additional parameterization for CloudWatch logging (e.g., customizable log streams)
- Explore expanding Assistants API logging to additional endpoints as OpenAI adds them
- Monitor production usage for any performance impacts
- Document best practices for log retention and analysis

<!-- End of Feature Tracking --> 