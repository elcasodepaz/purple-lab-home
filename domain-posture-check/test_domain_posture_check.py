"""Offline tests for Domain Posture Check."""

import socket
import unittest
from unittest.mock import patch

import domain_posture_check as checker


class NormalizeHostTests(unittest.TestCase):
    def test_normalizes_hostname_and_url(self):
        self.assertEqual(checker.normalize_host("HTTPS://Example.COM/"), "example.com")
        self.assertEqual(checker.normalize_host("example.com"), "example.com")

    def test_rejects_paths(self):
        with self.assertRaises(ValueError):
            checker.normalize_host("example.com/private")


class ReportTests(unittest.TestCase):
    @patch.object(checker, "check_https_headers", return_value={"status": 200, "present": {"HSTS": True}})
    @patch.object(checker, "check_tls", return_value={"validated": True})
    @patch.object(checker, "resolve_host", return_value=["203.0.113.10"])
    def test_combines_successful_checks(self, resolve, tls, https):
        report = checker.build_report("example.com", 5)
        self.assertEqual(report["dns"]["addresses"], ["203.0.113.10"])
        self.assertTrue(report["tls"]["validated"])
        self.assertEqual(report["https"]["status"], 200)
        resolve.assert_called_once_with("example.com")
        tls.assert_called_once_with("example.com", 5)
        https.assert_called_once_with("example.com", 5)

    @patch.object(checker, "check_tls")
    @patch.object(checker, "resolve_host", side_effect=socket.gaierror("name not found"))
    def test_stops_after_dns_failure(self, resolve, tls):
        report = checker.build_report("missing.invalid", 5)
        self.assertFalse(report["dns"]["resolved"])
        self.assertNotIn("tls", report)
        tls.assert_not_called()


if __name__ == "__main__":
    unittest.main()
