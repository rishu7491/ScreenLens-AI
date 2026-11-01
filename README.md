# AI Answer Bubble 🫧

An intelligent, non-intrusive floating desktop assistant that reads questions, MCQs, or code directly from your screen and provides instant answers in a sleek, adaptive floating bubble.

---

## ✨ Features

- **Two-Tier Visual Layout:**
  - 📌 **Question Box (Top):** Shows the exact question detected on screen.
  - 💡 **Answer Box (Bottom):** Shows the solution, correct option, or complete working code snippet.
- **Dynamic Auto-Resizing:** Compact for short MCQs, automatically expands downwards for complex coding problems and subjective answers.
- **High-Definition Vision:** 1280px screen capture engine powered by **NVIDIA Nemotron 3.5 Super VL**, capable of reading small fonts and dense exam layouts.
- **One-Click Copy:** Built-in `[📋 Copy]` button to instantly copy code or answers to your clipboard.
- **Hands-Free Auto-Loop Mode:** Monitors your screen automatically and updates only when a new question appears (perceptual change detection prevents redundant calls).
- **Stealth & Draggable:** Floating card with subtle transparency that stays on top and can be dragged anywhere.

---

## 🖥️ UI Preview

```text
┌────────────────────────────────────────────────────────┐
│  AI ASSISTANT                                   [DONE] │
│                                                        │
│  QUESTION DETECTED:                                    │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Q1. Which data structure is used for BFS of graph? │ │
│ │ A) Stack   B) Queue   C) Priority Queue            │ │
│ └────────────────────────────────────────────────────┘ │
│                                                        │
│  ANSWER / CODE:                                        │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Option B: Queue                                    │ │
│ │ (BFS traverses level-by-level using a FIFO queue)  │ │
│ └────────────────────────────────────────────────────┘ │
│                                                        │
│  [📸 Scan Now]  [🔄 Loop: OFF]  [📋 Copy]         [✕] │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Setup in 2 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/rishu7491/ai-answer-bubble.git
cd ai-answer-bubble
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API Key
Open `config.py` and paste your free **NVIDIA NIM API Key**:
```python
NVIDIA_API_KEY = "YOUR_NVIDIA_API_KEY_HERE"
```
*(Get a free key at [build.nvidia.com](https://build.nvidia.com/))*

### 4. Run
Double-click **`START.bat`** or run:
```bash
python answer_bubble.py
```

---

## ⌨️ Controls & Shortcuts

| Action | Mouse Click | Global Shortcut |
|---|---|---|
| **Scan & Solve** | Click `[📸 Scan Now]` | `Ctrl + Q` |
| **Auto-Loop Toggle** | Click `[🔄 Loop: OFF/ON]` | `Ctrl + L` |
| **Copy Answer** | Click `[📋 Copy]` | — |
| **Hide / Show** | Click `[✕]` | `Ctrl + H` |
| **Move Bubble** | Drag header with mouse | — |
| **Exit App** | — | `Ctrl + Shift + X` |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **GUI:** Tkinter (Thread-safe queue architecture, custom modern dark theme)
- **Vision AI:** NVIDIA Nemotron-3.5-Super-VL-120B via NIM API
- **Screen Engine:** Win32 GDI with `CAPTUREBLT` for hardware-accelerated windows + perceptual difference hashing
- **Hotkeys:** Pynput (Universal global hook, no admin rights required)

---

## 📄 License

MIT License. Free to use and modify for learning and productivity.
