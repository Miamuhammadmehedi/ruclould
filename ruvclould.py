import os
import http.server
import socketserver
import cgi
import io
import sys
import subprocess
import threading
import time
from colorama import Fore, Style, init

init(autoreset=True)

# ডিরেক্টরি পাথ সেট করা
BASE_PATH = '/storage/emulated/0/RuvCloud'
STORAGE_PATH = os.path.join(BASE_PATH, 'files')
WEB_PATH = os.path.join(BASE_PATH, 'www')

# ফোল্ডারগুলো না থাকলে তৈরি করে নেওয়া
for path in [STORAGE_PATH, WEB_PATH]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

PORT_STORAGE = 8080
PORT_WEB = 9090

# --- ১. ফাইল ম্যানেজারের জন্য কাস্টম হ্যান্ডলার ---
class RuvStorageHandler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            list_dir = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
            
        list_dir.sort(key=lambda a: a.lower())
        f = io.BytesIO()
        displaypath = cgi.escape(self.path)
        
        f.write(b'<!DOCTYPE html>\n<html>\n<head>')
        f.write(b'<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        f.write(b'<title>RuvCloud - File Manager</title>')
        f.write(b'''<style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #121212; color: #e0e0e0; margin: 0; padding: 20px; }
            h2 { color: #00ffcc; border-bottom: 2px solid #333; padding-bottom: 10px; }
            ul { list-style-type: none; padding: 0; }
            li { background: #1e1e1e; margin: 8px 0; padding: 12px; border-radius: 6px; display: flex; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.5); }
            a { color: #33b5e5; text-decoration: none; font-weight: 500; word-break: break-all; }
            a:hover { text-decoration: underline; color: #00ffcc; }
            .upload-box { background: #252525; border: 2px dashed #00ffcc; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 20px; }
            input[type="file"] { display: none; }
            .custom-file-upload { border: 1px solid #00ffcc; display: inline-block; padding: 8px 16px; cursor: pointer; border-radius: 4px; color: #00ffcc; transition: 0.3s; }
            .custom-file-upload:hover { background: #00ffcc; color: #121212; }
            input[type="submit"] { background: #00ffcc; color: #121212; border: none; padding: 8px 20px; border-radius: 4px; font-weight: bold; cursor: pointer; margin-left: 10px; }
        </style>\n</head>\n<body>''')
        
        f.write(f'<div class="upload-box"><h3>Upload File to Current Directory</h3>'.encode('utf-8'))
        f.write(f'<form ENCTYPE="multipart/form-data" method="post" action="/upload?path={displaypath}">'.encode('utf-8'))
        f.write(b'<label class="custom-file-upload"><input type="file" name="file"/>Choose File</label>')
        f.write(b'<input type="submit" value="Upload"/></form></div>')
        
        f.write(f'<h2>File Manager: {displaypath}</h2><ul>'.encode('utf-8'))
        
        if displaypath != '/':
            f.write(b'<li><a href="..">📁 [ Parent Directory ]</a></li>')
            
        for name in list_dir:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            
            f.write(f'<li><a href="{linkname}">{displayname}</a></li>'.encode('utf-8'))
            
        f.write(b'</ul>\n</body>\n</html>\n')
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def do_POST(self):
        if self.path.startswith('/upload'):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )
            file_field = form['file']
            if file_field.filename:
                file_data = file_field.file.read()
                filename = os.path.basename(file_field.filename)
                
                clean_path = self.path.split('?path=')[1]
                target_dir = os.path.normpath(STORAGE_PATH + clean_path)
                target_path = os.path.join(target_dir, filename)
                
                with open(target_path, 'wb') as f:
                    f.write(file_data)
                
                self.send_response(303)
                self.send_header('Location', clean_path)
                self.end_headers()
                return
        self.send_error(400, "Bad Request")

# --- ২. সার্ভার রান করার ফাংশনসমূহ ---
def run_storage_server():
    os.chdir(STORAGE_PATH)
    handler = RuvStorageHandler
    with socketserver.TCPServer(("", PORT_STORAGE), handler) as httpd:
        httpd.serve_forever()

def run_web_server():
    os.chdir(WEB_PATH)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT_WEB), handler) as httpd:
        httpd.serve_forever()

# --- ৩. টানেল চালু করার ফাংশনসমূহ ---
def start_storage_tunnel():
    subprocess.run(["ssh", "-R", "80:localhost:8080", "nokey@localhost.run"])

def start_web_tunnel():
    subprocess.run(["ssh", "-R", "80:localhost:9090", "nokey@localhost.run"])

if __name__ == "__main__":
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    print(Fore.GREEN + Style.BRIGHT + "      RUVCLOUD: DUAL HOSTING ENGINE     ")
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    
    t1 = threading.Thread(target=run_storage_server, daemon=True)
    t1.start()
    
    t2 = threading.Thread(target=run_web_server, daemon=True)
    t2.start()
    
    print(Fore.GREEN + "[✓] File Manager Engine Active on Port 8080")
    print(Fore.GREEN + "[✓] Web Hosting Engine Active on Port 9090")
    print(Fore.YELLOW + "\n[*] Booting up Public Tunnels... Please wait.")
    print(Fore.WHITE + "-------------------------------------------------------------")
    time.sleep(2)
    
    tunnel_web = threading.Thread(target=start_web_tunnel, daemon=True)
    tunnel_web.start()
    
    try:
        start_storage_tunnel()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Dual Servers stopped by user.")