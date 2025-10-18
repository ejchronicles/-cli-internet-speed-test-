import unittest
from unittest.mock import patch
from click.testing import CliRunner
from src.netspeed.cli import main

class TestCLI(unittest.TestCase):
    
    def setUp(self):
        self.runner = CliRunner()
    
    @patch('src.netspeed.cli.InternetSpeedTest')
    def test_cli_help(self, mock_speedtest):
        """Test that help command works"""
        result = self.runner.invoke(main, ['--help'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('--help', result.output)
    
    @patch('src.netspeed.cli.InternetSpeedTest')
    def test_json_output_flag(self, mock_speedtest):
        """Test JSON output flag"""
        result = self.runner.invoke(main, ['--json'])
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()
