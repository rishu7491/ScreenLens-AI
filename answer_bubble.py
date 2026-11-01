# ============================================================
# AI Answer Bubble - Enhanced Adaptive UI Engine
# ============================================================
# Features:
#   - Two-Tier View: QUESTION on top, ANSWER on bottom
#   - Dynamic Resizing: Auto-expands for Coding & Subjective answers
#   - Copy to Clipboard: [📋 Copy] button for instant answer copying
#   - High-Res Vision: 1200px capture for razor-sharp MCA MCQ / Code detection
#   - Non-Admin Hotkeys via Pynput (Ctrl+Q, Ctrl+L, Ctrl+H, Ctrl+Shift+X)
# ============================================================

import sys
import os
import io
import time
import base64
import queue
import logging
import threading
import requests
import ctypes
from ctypes import wintypes
from PIL import Image

# UTF-8 Console Safety
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

# DPI Awareness
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
try:
    user32.SetProcessDPIAware()
except Exception:
    pass

import tkinter as tk
from tkinter import font as tkfont

try:
    from pynput import keyboard as pynput_keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

from config import (
    NVIDIA_API_KEY, NVIDIA_MODEL, NVIDIA_BASE_URL,
    AUTO_LOOP_INTERVAL
)

# Enhanced resolution for small exam fonts / MCA MCQs
IMAGE_MAX_WIDTH = 1280
IMAGE_JPEG_QUALITY = 72

SYSTEM_PROMPT = """You are an expert exam, quiz, and coding interview solver.
Analyze the provided screenshot carefully and extract the questions.

OUTPUT FORMAT REQUIREMENTS:
Always structure your output strictly into two sections:

QUESTION:
<Write the detected question(s) and options clearly>

ANSWER:
<For MCQ: Provide Option Letter + Option Text, e.g. "Option B: Queue">
<For Coding: Provide the exact, clean, working code directly>
<For Subjective/Numerical: Provide direct, concise solution without conversational filler>

If no question is visible, state: "No question visible on screen".
Be direct, accurate, and concise."""


# ── Win32 Screen Capture ──────────────────────────────────────

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]


def capture_desktop_image() -> Image.Image:
    hDesk = user32.OpenInputDesktop(0, False, 0x01FF)
    if hDesk:
        user32.SetThreadDesktop(hDesk)

    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)

    hdc_screen = user32.GetDC(0)
    hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
    hbm = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
    gdi32.SelectObject(hdc_mem, hbm)

    SRCCOPY_CAPTUREBLT = 0x40CC0020
    gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc_screen, 0, 0, SRCCOPY_CAPTUREBLT)

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0

    buf = (ctypes.c_char * (w * h * 4))()
    gdi32.GetDIBits(hdc_mem, hbm, 0, h, buf, ctypes.byref(bmi), 0)

    raw_img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1)
    rgb_img = raw_img.convert('RGB')

    gdi32.DeleteObject(hbm)
    gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(0, hdc_screen)
    if hDesk:
        user32.CloseDesktop(hDesk)

    return rgb_img


def compute_screen_fingerprint(pil_img: Image.Image):
    thumb = pil_img.resize((32, 32), Image.Resampling.BILINEAR).convert("L")
    return list(thumb.getdata())


def has_meaningfully_changed(fp1, fp2, threshold=8.0):
    if not fp1 or not fp2:
        return True
    avg_diff = sum(abs(a - b) for a, b in zip(fp1, fp2)) / float(len(fp1))
    return avg_diff > threshold


def capture_optimized_screen():
    try:
        pil_img = capture_desktop_image()
    except Exception as e:
        logging.warning(f"Fallback to ImageGrab: {e}")
        from PIL import ImageGrab
        pil_img = ImageGrab.grab()

    fingerprint = compute_screen_fingerprint(pil_img)

    w, h = pil_img.size
    if w > IMAGE_MAX_WIDTH:
        scale = IMAGE_MAX_WIDTH / float(w)
        pil_img = pil_img.resize((IMAGE_MAX_WIDTH, int(h * scale)), Image.Resampling.LANCZOS)

    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG", quality=IMAGE_JPEG_QUALITY, optimize=True)
    img_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return img_b64, fingerprint


# ── AI Model Inference ────────────────────────────────────────

def query_nvidia_vision(image_b64: str) -> str:
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": NVIDIA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT + "\n\nIMPORTANT: Be concise. Give QUESTION and ANSWER directly."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.1
    }

    try:
        t0 = time.time()
        resp = requests.post(
            f"{NVIDIA_BASE_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=40
        )
        dt = round(time.time() - t0, 2)
        logging.info(f"NVIDIA API responded in {dt}s, status {resp.status_code}")

        if resp.status_code == 200:
            choice = resp.json()["choices"][0]["message"]
            content = choice.get("content")
            if content and content.strip():
                return content.strip()
            reasoning = choice.get("reasoning_content") or ""
            return reasoning.strip()
        elif resp.status_code == 401:
            return "QUESTION:\nAuth Error\n\nANSWER:\nInvalid NVIDIA API Key in config.py"
        elif resp.status_code == 429:
            return "QUESTION:\nRate Limited\n\nANSWER:\nPlease wait a few seconds before scanning again."
        else:
            return f"QUESTION:\nAPI Error\n\nANSWER:\nHTTP Status {resp.status_code}"
    except requests.exceptions.Timeout:
        return "QUESTION:\nTimeout\n\nANSWER:\nNetwork response timed out. Try again."
    except Exception as e:
        logging.error(f"Inference error: {e}")
        return f"QUESTION:\nError\n\nANSWER:\n{str(e)[:50]}"


# ── Parsing Helpers ───────────────────────────────────────────

def parse_qa_response(raw_text: str):
    """Splits raw text into (question_part, answer_part)."""
    q_marker = "QUESTION:"
    a_marker = "ANSWER:"

    if q_marker in raw_text and a_marker in raw_text:
        parts = raw_text.split(a_marker, 1)
        q_part = parts[0].replace(q_marker, "").strip()
        a_part = parts[1].strip()
        return q_part, a_part
    elif a_marker in raw_text:
        parts = raw_text.split(a_marker, 1)
        return parts[0].strip(), parts[1].strip()
    else:
        # Fallback: display everything in answer
        return "Screen Question", raw_text.strip()


# ── Dynamic Adaptive Floating Bubble UI ───────────────────────

class AdaptiveBubbleApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.94)
        self.root.configure(bg="#0B0F19")

        self.is_hidden = False
        self.auto_loop_active = False
        self.last_img_fingerprint = None
        self.is_busy = False

        self.ui_queue = queue.Queue()

        # Dynamic Dimensions
        self.base_width = 440
        self.max_height = 550

        # Main Border Frame
        self.container = tk.Frame(
            self.root,
            bg="#0B0F19",
            highlightbackground="#3B82F6",
            highlightthickness=1,
            padx=10,
            pady=8
        )
        self.container.pack(fill=tk.BOTH, expand=True)

        # Header Bar
        self.header_frame = tk.Frame(self.container, bg="#0B0F19")
        self.header_frame.pack(fill=tk.X, pady=(0, 6))

        self.title_label = tk.Label(
            self.header_frame,
            text="SCREENLENS AI",
            font=("Segoe UI", 9, "bold"),
            fg="#60A5FA",
            bg="#0B0F19"
        )
        self.title_label.pack(side=tk.LEFT)

        self.status_label = tk.Label(
            self.header_frame,
            text="[READY]",
            font=("Consolas", 8, "bold"),
            fg="#10B981",
            bg="#0B0F19"
        )
        self.status_label.pack(side=tk.RIGHT)

        # ── 1. Question Section (Top) ─────────────────────────
        self.q_header = tk.Label(
            self.container,
            text="QUESTION DETECTED:",
            font=("Segoe UI", 8, "bold"),
            fg="#38BDF8",
            bg="#0B0F19",
            anchor="w"
        )
        self.q_header.pack(fill=tk.X, pady=(2, 2))

        self.q_box = tk.Text(
            self.container,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            fg="#CBD5E1",
            bg="#111827",
            relief=tk.FLAT,
            height=3,
            padx=8,
            pady=6,
            highlightbackground="#1F2937",
            highlightthickness=1
        )
        self.q_box.insert(tk.END, "Press [Scan Now] or Ctrl+Q to read questions from screen.")
        self.q_box.configure(state=tk.DISABLED)
        self.q_box.pack(fill=tk.BOTH, expand=False, pady=(0, 6))

        # ── 2. Answer Section (Bottom, Auto-Expanding) ────────
        self.a_header = tk.Label(
            self.container,
            text="ANSWER / CODE:",
            font=("Segoe UI", 8, "bold"),
            fg="#34D399",
            bg="#0B0F19",
            anchor="w"
        )
        self.a_header.pack(fill=tk.X, pady=(2, 2))

        self.a_box = tk.Text(
            self.container,
            wrap=tk.WORD,
            font=("Consolas", 10),
            fg="#F8FAFC",
            bg="#1E293B",
            relief=tk.FLAT,
            height=4,
            padx=8,
            pady=6,
            highlightbackground="#334155",
            highlightthickness=1
        )
        self.a_box.insert(tk.END, "Answer will appear here...")
        self.a_box.configure(state=tk.DISABLED)
        self.a_box.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

        # ── 3. Buttons Action Bar ─────────────────────────────
        self.btn_frame = tk.Frame(self.container, bg="#0B0F19")
        self.btn_frame.pack(fill=tk.X, pady=(2, 0))

        self.btn_scan = tk.Button(
            self.btn_frame,
            text="📸 Scan Now",
            font=("Segoe UI", 8, "bold"),
            fg="#FFFFFF",
            bg="#2563EB",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=10,
            pady=3,
            cursor="hand2",
            command=lambda: self.trigger_scan(is_auto=False)
        )
        self.btn_scan.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_loop = tk.Button(
            self.btn_frame,
            text="🔄 Loop: OFF",
            font=("Segoe UI", 8),
            fg="#E2E8F0",
            bg="#334155",
            activebackground="#475569",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.toggle_auto_loop
        )
        self.btn_loop.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_copy = tk.Button(
            self.btn_frame,
            text="📋 Copy",
            font=("Segoe UI", 8),
            fg="#CBD5E1",
            bg="#1E293B",
            activebackground="#3B82F6",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.copy_answer_to_clipboard
        )
        self.btn_copy.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_hide = tk.Button(
            self.btn_frame,
            text="✕",
            font=("Segoe UI", 8, "bold"),
            fg="#94A3B8",
            bg="#1E293B",
            activebackground="#EF4444",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self.toggle_visibility
        )
        self.btn_hide.pack(side=tk.RIGHT)

        # Dragging
        self._drag_data = {"x": 0, "y": 0}
        for w in [self.root, self.container, self.header_frame, self.title_label, self.q_header, self.a_header]:
            w.bind("<Button-1>", self._start_drag)
            w.bind("<B1-Motion>", self._on_drag)

        self.last_answer_text = ""
        self._reposition_bubble()
        self.poll_queue()

    def _start_drag(self, event):
        self._drag_data["x"] = event.x_root - self.root.winfo_x()
        self._drag_data["y"] = event.y_root - self.root.winfo_y()

    def _on_drag(self, event):
        x = event.x_root - self._drag_data["x"]
        y = event.y_root - self._drag_data["y"]
        self.root.geometry(f"+{x}+{y}")

    def _reposition_bubble(self):
        self.root.update_idletasks()
        sw = user32.GetSystemMetrics(0)
        sh = user32.GetSystemMetrics(1)
        w = self.base_width
        h = max(240, self.root.winfo_reqheight())
        h = min(self.max_height, h)

        x = sw - w - 24
        y = sh - h - 60
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def toggle_visibility(self):
        if self.is_hidden:
            self.root.deiconify()
            self.is_hidden = False
        else:
            self.root.withdraw()
            self.is_hidden = True

    def copy_answer_to_clipboard(self):
        if self.last_answer_text:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.last_answer_text)
            self.btn_copy.config(text="✓ Copied!", bg="#059669")
            self.root.after(1500, lambda: self.btn_copy.config(text="📋 Copy", bg="#1E293B"))

    def update_content(self, question: str, answer: str, status_text: str, status_color: str):
        """Thread-safe UI updater called from poll_queue."""
        self.last_answer_text = answer

        # Update Question Box
        self.q_box.configure(state=tk.NORMAL)
        self.q_box.delete("1.0", tk.END)
        self.q_box.insert(tk.END, question)
        # Adapt height based on line count
        q_lines = max(2, min(6, question.count("\n") + len(question) // 55 + 1))
        self.q_box.configure(height=q_lines, state=tk.DISABLED)

        # Update Answer Box
        self.a_box.configure(state=tk.NORMAL)
        self.a_box.delete("1.0", tk.END)
        self.a_box.insert(tk.END, answer)
        # Adapt height for code / subjective
        a_lines = max(3, min(14, answer.count("\n") + len(answer) // 45 + 1))
        self.a_box.configure(height=a_lines, state=tk.DISABLED)

        # Status
        self.status_label.config(text=status_text, fg=status_color)

        if self.is_hidden:
            self.root.deiconify()
            self.is_hidden = False

        self.root.update_idletasks()
        # Keep window anchored on right side without overflowing
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        req_h = min(self.max_height, self.root.winfo_reqheight())
        sh = user32.GetSystemMetrics(1)
        if current_y + req_h > sh - 40:
            current_y = max(40, sh - req_h - 60)
        self.root.geometry(f"{self.base_width}x{req_h}+{current_x}+{current_y}")

    def poll_queue(self):
        try:
            while True:
                msg_type, payload = self.ui_queue.get_nowait()
                if msg_type == "content":
                    q, a, st_text, st_col = payload
                    self.update_content(q, a, st_text, st_col)
                elif msg_type == "status":
                    st_text, st_col = payload
                    self.status_label.config(text=st_text, fg=st_col)
                elif msg_type == "loop_btn":
                    txt, bg_col = payload
                    self.btn_loop.config(text=txt, bg=bg_col)
        except queue.Empty:
            pass
        self.root.after(40, self.poll_queue)

    def trigger_scan(self, is_auto=False):
        if self.is_busy:
            return
        self.is_busy = True

        def worker():
            try:
                self.ui_queue.put(("status", ("[SCANNING...]", "#F59E0B")))
                img_b64, fingerprint = capture_optimized_screen()

                if is_auto and not has_meaningfully_changed(self.last_img_fingerprint, fingerprint):
                    self.ui_queue.put(("status", ("[WATCHING]", "#10B981")))
                    self.is_busy = False
                    return

                self.last_img_fingerprint = fingerprint
                raw_response = query_nvidia_vision(img_b64)
                q_text, a_text = parse_qa_response(raw_response)

                self.ui_queue.put(("content", (q_text, a_text, "[DONE]", "#10B981")))
                logging.info(f"Scan parsed successfully. Q: {q_text[:40]} | A: {a_text[:40]}")
            except Exception as e:
                logging.error(f"Worker failure: {e}")
                self.ui_queue.put(("content", ("Error", f"{e}", "[ERROR]", "#EF4444")))
            finally:
                self.is_busy = False

        threading.Thread(target=worker, daemon=True).start()

    def toggle_auto_loop(self):
        self.auto_loop_active = not self.auto_loop_active
        if self.auto_loop_active:
            self.ui_queue.put(("loop_btn", ("Loop: ON", "#059669")))
            self.ui_queue.put(("status", ("[AUTO-LOOP]", "#10B981")))
            self._start_loop_thread()
            logging.info("Auto loop turned ON")
        else:
            self.ui_queue.put(("loop_btn", ("Loop: OFF", "#334155")))
            self.ui_queue.put(("status", ("[READY]", "#94A3B8")))
            logging.info("Auto loop turned OFF")

    def _start_loop_thread(self):
        def loop_worker():
            while self.auto_loop_active:
                if not self.is_busy:
                    self.trigger_scan(is_auto=True)
                time.sleep(AUTO_LOOP_INTERVAL)

        threading.Thread(target=loop_worker, daemon=True).start()

    def quit_app(self):
        self.auto_loop_active = False
        logging.info("Quit requested")
        self.root.destroy()
        os._exit(0)


def setup_global_hotkeys(app: AdaptiveBubbleApp):
    if HAS_PYNPUT:
        try:
            hotkeys = pynput_keyboard.GlobalHotKeys({
                '<ctrl>+q': lambda: app.trigger_scan(is_auto=False),
                '<ctrl>+l': lambda: app.toggle_auto_loop(),
                '<ctrl>+h': lambda: app.toggle_visibility(),
                '<ctrl>+<shift>+x': lambda: app.quit_app()
            })
            hotkeys.start()
            logging.info("Pynput GlobalHotKeys registered")
            print("  Hotkeys Active: [Ctrl+Q], [Ctrl+L], [Ctrl+H], [Ctrl+Shift+X]")
            return
        except Exception as e:
            logging.warning(f"Pynput failed: {e}")

    try:
        import keyboard
        keyboard.add_hotkey("ctrl+q", lambda: app.trigger_scan(is_auto=False))
        keyboard.add_hotkey("ctrl+l", lambda: app.toggle_auto_loop())
        keyboard.add_hotkey("ctrl+h", lambda: app.toggle_visibility())
        keyboard.add_hotkey("ctrl+shift+x", lambda: app.quit_app())
    except Exception as e:
        logging.warning(f"Keyboard module failed: {e}")


def start_app():
    print("=" * 60)
    print("  SCREENLENS AI - STEALTH MULTIMODAL COPILOT")
    print("=" * 60)
    print("  * [Scan Now] ya [Ctrl + Q] : Screen Scan & Solve")
    print("  * [Loop]     ya [Ctrl + L] : Auto-Loop Mode")
    print("  * [Copy]                   : Copy Answer to Clipboard")
    print("  * [X]        ya [Ctrl + H] : Hide / Show")
    print("  * [Ctrl + Shift + X]       : Exit App")
    print("=" * 60)

    app = AdaptiveBubbleApp()
    setup_global_hotkeys(app)
    app.root.mainloop()


if __name__ == "__main__":
    start_app()
