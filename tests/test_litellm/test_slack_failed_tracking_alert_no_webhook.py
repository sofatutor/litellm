import asyncio
import os
import pytest

from litellm.integrations.SlackAlerting.slack_alerting import SlackAlerting
from litellm.integrations.SlackAlerting.utils import process_slack_alerting_variables
from litellm.proxy._types import AlertType

@pytest.mark.asyncio
async def test_failed_tracking_alert_does_not_raise_without_webhook(monkeypatch):
    # Ensure no webhook in env
    monkeypatch.delenv("SLACK_WEBHOOK_URL", raising=False)

    sa = SlackAlerting(alerting=["slack"], alert_types=[AlertType.failed_tracking_spend])

    # Should not raise even if webhook is missing
    await sa.failed_tracking_alert(error_message="test error", failing_model="gpt-x")
