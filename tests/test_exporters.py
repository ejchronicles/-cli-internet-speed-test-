import unittest
import tempfile
import os
import json
import csv
from src.netspeed.exporters import ResultExporter

class TestResultExporter(unittest.TestCase):
    
    def setUp(self):
        self.sample_results = {
            'timestamp': '2024-01-01 12:00:00',
            'download_mbps': 50.5,
            'upload_mbps': 25.2,
            'latency_ms': 15.0,
            'jitter_ms': 2.1,
            'packet_loss': 0.0,
            'server': 'Test Server',
            'server_country': 'Test Country'
        }
    
    def test_to_json(self):
        """Test JSON export functionality"""
        json_output = ResultExporter.to_json(self.sample_results)
        parsed_json = json.loads(json_output)
        self.assertEqual(parsed_json['download_mbps'], 50.5)
    
    def test_to_csv(self):
        """Test CSV export functionality"""
        csv_output = ResultExporter.to_csv(self.sample_results)
        self.assertIn('50.5', csv_output)
        self.assertIn('download_mbps', csv_output)
    
    def test_to_text(self):
        """Test text export functionality"""
        text_output = ResultExporter.to_text(self.sample_results)
        self.assertIn('Internet Speed Test Results', text_output)
        self.assertIn('50.5 Mbps', text_output)

if __name__ == '__main__':
    unittest.main()
