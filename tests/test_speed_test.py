import unittest
from unittest.mock import Mock, patch
from src.netspeed.speed_test import InternetSpeedTest

class TestInternetSpeedTest(unittest.TestCase):
    
    def setUp(self):
        self.tester = InternetSpeedTest()
    
    @patch('speedtest.Speedtest')
    def test_initialization(self, mock_speedtest):
        self.assertIsNotNone(self.tester.speedtester)
        self.assertEqual(self.tester.results, {})
    
    # Add more test methods here

if __name__ == '__main__':
    unittest.main()
