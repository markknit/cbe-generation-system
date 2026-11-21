"""Offline boundary/continuity checks; never contact Codex services."""
import unittest
from check_codex_usage import weekly_meter, decision

CONFIG = {'limit_id': 'codex', 'weekly_window_minutes': 10080}


class UsageGuardTests(unittest.TestCase):
    def test_weekly_can_be_primary(self):
        result = {'rateLimits': {'primary': {'windowDurationMins': 10080, 'usedPercent': 51}, 'secondary': None}}
        self.assertEqual(weekly_meter(result, CONFIG)['remaining_percent'], 49)

    def test_short_window_does_not_replace_weekly(self):
        result = {'rateLimits': {'primary': {'windowDurationMins': 300, 'usedPercent': 99},
                                'secondary': {'windowDurationMins': 10080, 'usedPercent': 30}}}
        self.assertEqual(weekly_meter(result, CONFIG)['remaining_percent'], 70)

    def test_select_requested_bucket(self):
        result = {'rateLimitsByLimitId': {
            'other': {'primary': {'windowDurationMins': 10080, 'usedPercent': 100}},
            'codex': {'primary': {'windowDurationMins': 10080, 'usedPercent': 40}}}}
        self.assertEqual(weekly_meter(result, CONFIG)['remaining_percent'], 60)

    def test_exact_threshold_stops(self):
        self.assertTrue(decision({'remaining_percent': 10}, {}, 10)['pause_requested'])
        self.assertTrue(decision({'remaining_percent': 9.9}, {}, 10)['pause_requested'])
        self.assertFalse(decision({'remaining_percent': 10.1}, {}, 10)['pause_requested'])

    def test_pending_pause_requires_explicit_resume(self):
        prior = {'pause_requested': True}
        self.assertTrue(decision({'remaining_percent': 80}, prior, 10)['pause_requested'])
        self.assertFalse(decision({'remaining_percent': 80}, prior, 10, resume=True)['pause_requested'])
        self.assertTrue(decision({'remaining_percent': 10}, prior, 10, resume=True)['pause_requested'])

    def test_missing_or_invalid_weekly_is_not_unlimited(self):
        for result in ({}, {'rateLimits': {'primary': {'windowDurationMins': 300, 'usedPercent': 10}}},
                       {'rateLimits': {'primary': {'windowDurationMins': 10080, 'usedPercent': None}}},
                       {'rateLimits': {'primary': {'windowDurationMins': 10080, 'usedPercent': float('nan')}}}):
            with self.subTest(result=result), self.assertRaises(ValueError):
                weekly_meter(result, CONFIG)


if __name__ == '__main__':
    unittest.main()
