import http.server
import socketserver
import json
import urllib.parse
import os
import logging
import time
from datetime import datetime

PORT = 8000

# Professional Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("DLLMS-Server")

# Global Data Store
db = []
cases = []
judgments = []
geo = {}

def load_data():
    global db, cases, judgments, geo
    try:
        if os.path.exists('data/db.json'):
            logger.info("Loading data/db.json")
            with open('data/db.json', 'r', encoding='utf-8') as f:
                db = json.load(f)
        if os.path.exists('data/cases.json'):
            logger.info("Loading data/cases.json")
            with open('data/cases.json', 'r', encoding='utf-8') as f:
                cases = json.load(f)
        if os.path.exists('data/judgments.json'):
            logger.info("Loading data/judgments.json")
            with open('data/judgments.json', 'r', encoding='utf-8') as f:
                judgments = json.load(f)
        if os.path.exists('data/geo.json'):
            logger.info("Loading data/geo.json")
            with open('data/geo.json', 'r', encoding='utf-8') as f:
                geo = json.load(f)
        logger.info(f"Loaded {len(db)} records, {len(cases)} cases, {len(judgments)} judgments, and geography data.")
    except Exception as e:
        logger.error(f"Initialization error: {e}")

load_data()

class APIRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='public', **kwargs)

    def translate_path(self, path):
        # Allow serving from the archive directory for judgments
        if path.startswith('/archive'):
            # Use the root-relative path for archive files
            return os.path.join(os.getcwd(), path.lstrip('/'))
        return super().translate_path(path)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        params = urllib.parse.parse_qs(parsed.query)

        # Router
        if path == '/api/records': return self.handle_get_records(params)
        if path == '/api/cases': return self.handle_get_cases(params)
        if path == '/api/stats': return self.handle_get_stats()
        if path == '/api/judgments': return self.handle_get_judgments(params)
        if path == '/api/geo': return self.send_json(geo)
        if path == '/api/chat': return self.handle_chat(params)
        
        return super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/api/auth/login': return self.handle_login()
        if path == '/api/records': return self.handle_post_record()
        self.send_error(404)

    def do_PUT(self):
        path = urllib.parse.urlparse(self.path).path
        # Path format: /api/records/CASE_ID
        parts = path.split('/')
        if len(parts) == 4 and parts[1] == 'api' and parts[2] == 'records':
            return self.handle_put_record(parts[3])
        self.send_error(404)

    # --- Handlers ---

    def handle_get_records(self, params):
        filtered = db
        # Extract filters
        f_state = params.get('state', [''])[0]
        f_dist = params.get('district', [''])[0]
        f_vill = params.get('villageName', [''])[0]
        f_sect = params.get('sectorNumber', [''])[0]
        f_case = params.get('caseId', [''])[0]

        if f_state: filtered = [r for r in filtered if r.get('state') == f_state]
        if f_dist:  filtered = [r for r in filtered if r.get('district') == f_dist]
        if f_vill:  filtered = [r for r in filtered if r.get('villageName', '').lower() == f_vill.lower()]
        if f_sect:  filtered = [r for r in filtered if r.get('sectorNumber') == f_sect]
        if f_case:  filtered = [r for r in filtered if r.get('caseNumber', '').lower() == f_case.lower()]

        self.send_json({"success": True, "count": len(filtered), "data": filtered})

    def handle_get_cases(self, params):
        filtered = cases
        # Extract filters
        f_state = params.get('state', [''])[0]
        f_dist = params.get('district', [''])[0]
        f_vill = params.get('village', [''])[0]
        f_sect = params.get('survey', [''])[0] # Mapping survey to sector for consistency if needed
        f_id = params.get('id', [''])[0]

        if f_state: filtered = [c for c in filtered if c.get('state') == f_state]
        if f_dist:  filtered = [c for c in filtered if c.get('district') == f_dist]
        if f_vill:  filtered = [c for c in filtered if c.get('village', '').lower() == f_vill.lower()]
        if f_sect:  filtered = [c for c in filtered if c.get('survey', '').lower() == f_sect.lower()]
        if f_id:    filtered = [c for c in filtered if c.get('id', '').lower() == f_id.lower()]

        self.send_json({"success": True, "count": len(filtered), "data": filtered})

    def handle_get_judgments(self, params):
        # ... (keep existing code)
        filtered = judgments
        f_year = params.get('year', [''])[0]
        f_search = params.get('search', [''])[0]
        if f_year: filtered = [j for j in filtered if j.get('year') == f_year]
        if f_search:
            s = f_search.lower()
            filtered = [j for j in filtered if s in j.get('title', '').lower() or s in j.get('petitioner', '').lower() or s in j.get('respondent', '').lower()]
        if not f_year and not f_search: filtered = filtered[:100]
        elif len(filtered) > 500: filtered = filtered[:500]
        self.send_json({"success": True, "count": len(filtered), "data": filtered})

    def handle_chat(self, params):
        query = params.get('query', [''])[0].lower()
        
        # Smart Response Simulation (Simulating Gemini Pro)
        responses = {
            "help": "I am your DLLMS AI Assistant. You can ask me about case status, land records, or legal procedures.",
            "status": "To check your case status, please use the 'Case Status' tab and enter your 10-digit Case ID or select your location.",
            "document": "Commonly required documents include PATTA, Sale Deed, Encumbrance Certificate (EC), and ID proof.",
            "boundary": "For boundary disputes, our portal allows you to request a physical survey via the 'File Case' section.",
            "encroachment": "Encroachment cases are handled with priority. Please file a formal complaint under the Land Encroachment Act.",
            "hello": "Namaste! I am the DLLMS AI Assistant powered by Google Gemini. How can I help you today?",
            "hi": "Hello! Welcome to the National Land Litigation Portal. How may I assist you with your land records?"
        }
        
        reply = "That's an interesting question about land litigation. Based on current Revenue Department guidelines, you should consult the 'Help' section for detailed procedures or file a formal inquiry."
        for k, v in responses.items():
            if k in query:
                reply = v
                break
        
        # Simulate thinking time
        time.sleep(1)
        self.send_json({"reply": reply, "model": "Gemini 1.5 Pro (Simulated)"})

    def handle_get_stats(self):
        # Calculate real-time analytics
        stats = {
            "total_cases": len(cases),
            "by_type": {},
            "by_district": {},
            "by_status": {},
            "monthly": {
                "Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0,
                "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0
            }
        }
        
        for c in cases:
            # Status count
            st = c.get('status', 'Pending')
            stats['by_status'][st] = stats['by_status'].get(st, 0) + 1
            
            # Type count
            tp = c.get('type', 'Other')
            stats['by_type'][tp] = stats['by_type'].get(tp, 0) + 1
            
            # District count
            ds = c.get('district', 'Other')
            stats['by_district'][ds] = stats['by_district'].get(ds, 0) + 1
            
            # Monthly distribution
            filed_date = c.get('filed', '')
            # Expected formats: "DD MMM YYYY" or "YYYY-MM-DD"
            try:
                if '-' in filed_date:
                    dt = datetime.strptime(filed_date, '%Y-%m-%d')
                else:
                    dt = datetime.strptime(filed_date, '%d %b %Y')
                mon = dt.strftime('%b')
                if mon in stats['monthly']:
                    stats['monthly'][mon] += 1
            except:
                pass

        self.send_json({"success": True, "data": stats})

    def handle_login(self):
        try:
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            if body.get('adminId') == 'GOV-EMP-2026' and body.get('password') == 'admin123':
                self.send_json({"success": True, "token": "senior-dev-token-998811", "message": "Auth Success"})
            else:
                self.send_json({"success": False, "message": "Invalid Credentials"}, 401)
        except Exception as e:
            self.send_json({"success": False, "message": str(e)}, 400)

    def handle_post_record(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            
            # Basic schema validation
            required = ['id', 'applicant', 'district', 'type']
            if not all(k in data for k in required):
                return self.send_json({"success": False, "message": "Missing required fields"}, 400)

            new_case = {
                "id": data.get("id"),
                "applicant": data.get("applicant"),
                "respondent": data.get("respondent", "Unknown"),
                "district": data.get("district"),
                "taluka": data.get("taluka", "Common"),
                "village": data.get("village", "Common"),
                "survey": data.get("survey", "N/A"),
                "patta": data.get("patta", "N/A"),
                "area": data.get("area", "0.0"),
                "type": data.get("type"),
                "status": "Pending",
                "filed": data.get("filed", datetime.now().strftime('%d %b %Y')),
                "officer": "Pending Assignment",
                "nextHearing": "TBD",
                "timeline": [
                    { "d": data.get("filed"), "e": "Case filed online via DLLMS Portal v2.0" }
                ]
            }
            
            cases.insert(0, new_case) # Add to start (Recent)
            with open('data/cases.json', 'w', encoding='utf-8') as f:
                json.dump(cases, f, indent=2)
            
            logger.info(f"New case filed: {data.get('id')}")
            self.send_json({"success": True, "data": new_case}, 201)
        except Exception as e:
            logger.error(f"POST Record Error: {e}")
            self.send_json({"success": False, "message": "Server internal error"}, 500)

    def handle_put_record(self, case_id):
        try:
            length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(length).decode('utf-8'))
            
            found = False
            for record in db:
                if record.get('caseNumber', '').lower() == case_id.lower():
                    if 'status' in body: record['litigationStatus'] = body['status']
                    if 'nextHearing' in body: record['nextHearing'] = body['nextHearing']
                    found = True
                    break
            
            if found:
                with open('data/db.json', 'w', encoding='utf-8') as f:
                    json.dump(db, f, indent=4)
                self.send_json({"success": True, "message": "Record updated"})
            else:
                self.send_json({"success": False, "message": "Record not found"}, 404)
        except Exception as e:
            self.send_json({"success": False, "message": str(e)}, 500)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    try:
        with ThreadedTCPServer(("", PORT), APIRequestHandler) as httpd:
            logger.info(f"DLLMS Government Portal replica running at http://localhost:{PORT}")
            httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopping...")
    except Exception as e:
        logger.critical(f"Server crash: {e}")
