import speedtest
import time
from ping3 import ping
from typing import Dict, List
import statistics

class InternetSpeedTest:
    def __init__(self):
        self.speedtester = speedtest.Speedtest()
        self.results = {}
    
    def measure_latency(self, host="8.8.8.8", count=10) -> Dict:
        """Measure latency and jitter using ICMP ping"""
        latencies = []
        
        for i in range(count):
            try:
                latency = ping(host, unit='ms')
                if latency is not None:
                    latencies.append(latency)
                time.sleep(0.5)  # Wait between pings
            except Exception as e:
                print(f"Ping error: {e}")
                continue
        
        if latencies:
            return {
                'latency_ms': statistics.mean(latencies),
                'jitter_ms': statistics.stdev(latencies) if len(latencies) > 1 else 0,
                'packet_loss': ((count - len(latencies)) / count) * 100
            }
        return {'latency_ms': 0, 'jitter_ms': 0, 'packet_loss': 100}
    
    def run_speed_test(self, server_id=None) -> Dict:
        """Run comprehensive speed test"""
        print("Finding optimal server...")
        if server_id:
            self.speedtester.get_servers(servers=[server_id])
        else:
            self.speedtester.get_best_server()
        
        print("Testing download speed...")
        download_speed = self.speedtester.download() / 1_000_000  # Convert to Mbps
        
        print("Testing upload speed...")
        upload_speed = self.speedtester.upload() / 1_000_000  # Convert to Mbps
        
        print("Measuring latency and jitter...")
        latency_results = self.measure_latency()
        
        self.results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'download_mbps': round(download_speed, 2),
            'upload_mbps': round(upload_speed, 2),
            **latency_results,
            'server': self.speedtester.best['name'],
            'server_country': self.speedtester.best['country']
        }
        
        return self.results
