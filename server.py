"""
CreditFit 360 - Dedicated Localhost Server Runner
Starts the web application, prints local and network access URLs,
and automatically opens the default web browser.

Usage:
    python server.py
    python server.py --port 8080
    python server.py --no-browser
"""

import os
import sys
import socket
import threading
import time
import webbrowser
import argparse

# Ensure current working directory is project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

from app import app
import db


def get_local_ip():
    """Finds the machine's local LAN IP address (for mobile device access)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not actually connect, just identifies default outbound interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def is_port_in_use(port, host='0.0.0.0'):
    """Checks if a network port is already occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0


def find_available_port(start_port=5000, max_attempts=20):
    """Finds the first available port starting from start_port."""
    port = start_port
    while port < start_port + max_attempts:
        if not is_port_in_use(port):
            return port
        port += 1
    return start_port


def open_browser_delayed(url, delay=1.2):
    """Opens the user's default browser after the server has initialized."""
    def _open():
        time.sleep(delay)
        print(f"[*] Opening browser at {url} ...")
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"[!] Could not launch browser automatically: {e}")
    
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def print_banner(host, port, local_ip):
    """Displays a clean startup terminal dashboard banner."""
    print("=" * 64)
    print("           CREDITFIT 360 - LOCAL SERVER RUNNER           ")
    print("     Smart Credit Health, Reverse Underwriting & FinAI   ")
    print("=" * 64)
    print(f"  - Local Web URL:     http://localhost:{port}")
    print(f"  - Localhost IP:      http://127.0.0.1:{port}")
    print(f"  - Network / Mobile:  http://{local_ip}:{port}")
    print(f"  - Database:          {os.path.join(PROJECT_ROOT, 'database.db')} (SQLite Active)")
    print(f"  - Privacy Standard:  RBI CEPC 2023-24 & DPDP Act 2023 Shield")
    print("-" * 64)
    print(f"  [i] Quick Demo Login: demo@creditfit360.com / Demo@123")
    print(f"  [i] Press CTRL + C anytime in this terminal to stop.")
    print("=" * 64)
    print()


def main():
    parser = argparse.ArgumentParser(description="CreditFit 360 Localhost Server")
    parser.add_argument("--port", "-p", type=int, default=5000, help="Port to listen on (default: 5000)")
    parser.add_argument("--host", "-H", type=str, default="0.0.0.0", help="Host interface (default: 0.0.0.0)")
    parser.add_argument("--no-browser", action="store_true", help="Do not automatically launch web browser")
    parser.add_argument("--no-debug", action="store_true", help="Disable Flask debug mode")

    args = parser.parse_args()

    # Initialize database
    db.init_db()

    # Determine free port
    port = args.port
    if is_port_in_use(port):
        print(f"[!] Port {port} is currently in use.")
        free_port = find_available_port(start_port=port + 1)
        print(f"[+] Automatically switching to available port: {free_port}")
        port = free_port

    local_ip = get_local_ip()
    target_url = f"http://localhost:{port}"

    print_banner(args.host, port, local_ip)

    if not args.no_browser:
        open_browser_delayed(target_url, delay=1.0)

    debug_mode = not args.no_debug
    try:
        app.run(
            host=args.host,
            port=port,
            debug=debug_mode,
            use_reloader=False  # Disabled in dedicated runner to prevent duplicate browser launches
        )
    except (KeyboardInterrupt, SystemExit):
        print("\n[+] CreditFit360 server stopped gracefully. Goodbye!")


if __name__ == "__main__":
    main()
