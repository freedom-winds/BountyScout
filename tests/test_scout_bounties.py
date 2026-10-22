import os
import tempfile
import unittest

from scout_bounties import (
    format_github_issue_content,
    format_notification_message,
    is_clean_candidate,
    load_seen_bounties,
    pluralize_opportunity,
    save_seen_bounties,
)


def make_bounty(index=1):
    """Build a bounty dict shaped like the ones produced by main()."""
    return {
        "title": f"Fix bug {index}",
        "url": f"https://github.com/example/repo/issues/{index}",
        "repo": "example/repo",
        "comments": 1,
        "updated_at": "2026-10-21T01:06:04Z",
    }


class PluralizationTests(unittest.TestCase):
    def test_singular_and_plural_forms(self):
        self.assertEqual(pluralize_opportunity(1), "opportunity")
        self.assertEqual(pluralize_opportunity(0), "opportunities")
        self.assertEqual(pluralize_opportunity(2), "opportunities")
        self.assertEqual(pluralize_opportunity(7), "opportunities")

    def test_capitalized_forms(self):
        self.assertEqual(pluralize_opportunity(1, capitalize=True), "Opportunity")
        self.assertEqual(pluralize_opportunity(7, capitalize=True), "Opportunities")

    def test_notification_message_pluralizes_correctly(self):
        message = format_notification_message(
            [make_bounty(i) for i in range(1, 8)], "2026-10-21 01:16 UTC"
        )
        self.assertIn("Found 7 new opportunities:", message)
        self.assertNotIn("opportunityies", message.lower())

    def test_notification_message_singular(self):
        message = format_notification_message(
            [make_bounty()], "2026-10-21 01:16 UTC"
        )
        self.assertIn("Found 1 new opportunity:", message)

    def test_issue_title_and_body_pluralize_correctly(self):
        title, body = format_github_issue_content(
            [make_bounty(i) for i in range(1, 8)], "2026-10-21 01:16 UTC"
        )
        self.assertEqual(title, "🎯 Bounty Alert: 7 New Opportunities found")
        self.assertIn("### Active Bounty Scan Results", body)
        self.assertNotIn("opportunityies", title.lower())
        self.assertNotIn("opportunityies", body.lower())

    def test_issue_title_singular(self):
        title, _ = format_github_issue_content(
            [make_bounty()], "2026-10-21 01:16 UTC"
        )
        self.assertEqual(title, "🎯 Bounty Alert: 1 New Opportunity found")


class CandidateFilteringTests(unittest.TestCase):
    def base_item(self, **overrides):
        item = {
            "title": "Fix the widget parser ($50 bounty)",
            "body": "Details about the paid bounty.",
            "html_url": "https://github.com/example/repo/issues/1",
            "assignees": [],
            "comments": 3,
            "state": "open",
            "locked": False,
        }
        item.update(overrides)
        return item

    def test_accepts_clean_bounty(self):
        self.assertTrue(is_clean_candidate(self.base_item()))

    def test_rejects_pull_requests(self):
        item = self.base_item(pull_request={"url": "https://api.github.com/pulls/1"})
        self.assertFalse(is_clean_candidate(item))

    def test_rejects_assigned_issues(self):
        self.assertFalse(is_clean_candidate(self.base_item(assignees=[{"login": "alice"}])))

    def test_rejects_overcrowded_threads(self):
        self.assertFalse(is_clean_candidate(self.base_item(comments=26)))
        self.assertTrue(is_clean_candidate(self.base_item(comments=25)))

    def test_rejects_closed_and_locked_issues(self):
        self.assertFalse(is_clean_candidate(self.base_item(state="closed")))
        self.assertFalse(is_clean_candidate(self.base_item(locked=True)))

    def test_rejects_spam_keywords(self):
        self.assertFalse(is_clean_candidate(self.base_item(title="Airdrop bounty")))
        self.assertFalse(is_clean_candidate(self.base_item(body="Join our referral program")))

    def test_rejects_own_alert_issues(self):
        item = self.base_item(
            title="🎯 Bounty Alert: 7 New Opportunities found",
            html_url="https://github.com/freedom-winds/BountyScout/issues/1290",
        )
        self.assertFalse(is_clean_candidate(item, host_repo="freedom-winds/BountyScout"))

    def test_rejects_alert_signature_from_any_repo(self):
        item = self.base_item(
            title="🎯 Bounty Alert: 7 New Opportunityies found",
            body="### Active Bounty Scan Results",
            html_url="https://github.com/someone/BountyScout-fork/issues/9",
        )
        self.assertFalse(is_clean_candidate(item, host_repo="freedom-winds/BountyScout"))


class StatePersistenceTests(unittest.TestCase):
    def test_roundtrip_and_deterministic_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_file = os.path.join(tmp, "seen.json")
            urls = {
                "https://github.com/b/repo/issues/2",
                "https://github.com/a/repo/issues/1",
            }
            save_seen_bounties(urls, state_file)
            self.assertEqual(load_seen_bounties(state_file), urls)

            with open(state_file, encoding="utf-8") as f:
                first = f.read()
            save_seen_bounties(urls, state_file)
            with open(state_file, encoding="utf-8") as f:
                second = f.read()
            self.assertEqual(first, second)

    def test_missing_state_file_returns_empty_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                load_seen_bounties(os.path.join(tmp, "missing.json")), set()
            )


if __name__ == "__main__":
    unittest.main()
