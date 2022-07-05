"""
Test management commands for django.
"""

from psycopg2.errors import OperationalError as Psycopg2Error

from unittest.mock import patch

from django.core.management import call_command
from django.db import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Tests for management commands."""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db is succesful."""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep', return_value=None)
    def test_wait_for_db_not_ready(self, patched_time_sleep, patched_check):
        """Test waiting for database when getting an OperationalError."""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 2 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 5)
        patched_check.assert_called_with(databases=['default'])
