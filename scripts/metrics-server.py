#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from datetime import datetime
import threading
import subprocess

# Хранилище метрик
metrics_history = {
    'connections': [],
    'active_connections': [],
    'timestamps': []
}

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            # Получаем текущий статус Nginx
            try:
                result = subprocess.run(
                    ['curl', '-s', 'http://localhost/status'],
                    capture_output=True, text=True, timeout=5
                )
                lines = result.stdout.strip().split('\n')
                
                if len(lines) >= 3:
                    connections = int(lines[1].split()[1])
                    active = int(lines[2].split()[1])
                    
                    # Сохраняем в историю
                    timestamp = datetime.now().isoformat()
                    metrics_history['connections'].append(connections)
                    metrics_history['active_connections'].append(active)
                    metrics_history['timestamps'].append(timestamp)
                    
                    # Ограничиваем историю последними 100 точками
                    if len(metrics_history['connections']) > 100:
                        metrics_history['connections'] = metrics_history['connections'][-100:]
                        metrics_history['active_connections'] = metrics_history['active_connections'][-100:]
                        metrics_history['timestamps'] = metrics_history['timestamps'][-100:]
                    
                    response = {
                        'current': {
                            'connections': connections,
                            'active_connections': active,
                            'timestamp': timestamp
                        },
                        'history': metrics_history
                    }
                else:
                    response = {'error': 'Invalid nginx status format'}
                    
            except Exception as e:
                response = {'error': str(e)}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_metrics_server():
    server = HTTPServer(('0.0.0.0', 8080), MetricsHandler)
    print("Metrics server running on port 8080...")
    server.serve_forever()

if __name__ == '__main__':
    run_metrics_server()