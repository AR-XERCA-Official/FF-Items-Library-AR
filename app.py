import http.server
import os
import sys
import shutil
import webbrowser
import re
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080
DIRECTORY = "."

COLOR_RESET  = "\033[0m"
COLOR_BOLD   = "\033[1m"
COLOR_CYAN   = "\033[96m"
COLOR_GREEN  = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED    = "\033[91m"
COLOR_BLUE   = "\033[94m"
COLOR_GREY   = "\033[90m"

def ansi_visible(text):
    return len(re.sub(r'\x1b\[[0-9;]*m', '', text))

def truncate_path(path, max_len):
    if len(path) <= max_len:
        return path
    return path[:max_len - 3] + '...'

def status_color(code):
    if 200 <= code < 300:
        return COLOR_GREEN
    if 300 <= code < 400:
        return COLOR_BLUE
    if 400 <= code < 500:
        return COLOR_YELLOW
    return COLOR_RED

class BeautifulHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def log_message(self, format, *args):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(args) >= 2:
            code = int(args[0])
            size = args[1]
        else:
            code = 0
            size = "-"
        sc = status_color(code)
        code_str = f"{COLOR_BOLD}{sc}{code}{COLOR_RESET}"
        print(f"{COLOR_GREY}{timestamp}{COLOR_RESET}  {COLOR_CYAN}{self.command:<6}{COLOR_RESET} {self.path:<40} → {code_str}  {COLOR_GREY}({size} bytes){COLOR_RESET}")

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    term_width = shutil.get_terminal_size().columns

    cwd = os.getcwd()
    max_path = term_width - 4 - len("Directory : ")
    dir_display = truncate_path(cwd, max_path) if max_path > 10 else cwd

    BANNER_LINES = [
        f"{COLOR_CYAN}{COLOR_BOLD}╔══════════════════════════════════════════════════╗",
        f"║             Free Fire Items Library              ║",
        f"╠══════════════════════════════════════════════════╣",
        f"║  Directory : {COLOR_GREEN}{dir_display}{COLOR_CYAN}         ║",
        f"║    Address   : {COLOR_GREEN}http://{HOST}:{PORT}{COLOR_CYAN}               ║",
        f"╚══════════════════════════════════════════════════╝{COLOR_RESET}"
    ]

    for line in BANNER_LINES:
        visible_len = ansi_visible(line)
        padding = max(0, (term_width - visible_len) // 2)
        print(" " * padding + line)

    print()
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, BeautifulHandler)
    webbrowser.open(f'http://localhost:{PORT}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{COLOR_YELLOW}Server stopped.{COLOR_RESET}")
        httpd.server_close()
        sys.exit(0)

if __name__ == "__main__":
    main()