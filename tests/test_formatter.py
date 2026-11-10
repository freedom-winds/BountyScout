import pytest
from bountyscout.formatter import format_bounty_alert_title


def test_format_bounty_alert_title_plural():
    title = format_bounty_alert_title(23)
    assert title == "🎯 Bounty Alert: 23 New Opportunities found"


def test_format_bounty_alert_title_singular():
    title = format_bounty_alert_title(1)
    assert title == "🎯 Bounty Alert: 1 New Opportunity found"


def test_format_bounty_alert_title_zero():
    title = format_bounty_alert_title(0)
    assert title == "🎯 Bounty Alert: 0 New Opportunities found"
