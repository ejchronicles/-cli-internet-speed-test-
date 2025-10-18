import json
import csv
import os
from datetime import datetime
from typing import Dict

class ResultExporter:
    @staticmethod
    def to_json(results: Dict, filepath: str = None) -> str:
        """Export results to JSON format"""
        json_output = json.dumps(results, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_output)
            print(f"Results saved to {filepath}")
        
        return json_output
    
    @staticmethod
    def to_csv(results: Dict, filepath: str = None) -> str:
        """Export results to CSV format"""
        if filepath:
            # Append to CSV file or create new
            file_exists = os.path.isfile(filepath)
            
            with open(filepath, 'a', newline='') as f:
                writer = csv.writer(f)
                
                if not file_exists:
                    # Write header
                    writer.writerow(results.keys())
                
                writer.writerow(results.values())
            
            print(f"Results appended to {filepath}")
        
        # Return CSV string
        csv_output = ",".join(str(x) for x in results.values())
        header = ",".join(results.keys())
        return f"{header}\n{csv_output}"
    
    @staticmethod
    def to_text(results: Dict) -> str:
        """Format results as human-readable text"""
        text_output = f"""
Internet Speed Test Results
===========================
Timestamp: {results['timestamp']}
Download: {results['download_mbps']} Mbps
Upload: {results['upload_mbps']} Mbps
Latency: {results['latency_ms']} ms
Jitter: {results['jitter_ms']} ms
Packet Loss: {results['packet_loss']}%
Server: {results['server']} ({results['server_country']})
        """
        return text_output.strip()
