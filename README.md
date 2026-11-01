<div align="center">

# 👁️ ScreenLens AI
### *The Stealth Floating Copilot That Sees Your Screen & Solves Anything in 3 Seconds.*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Model](https://img.shields.io/badge/Vision%20Model-NVIDIA%20Nemotron%20120B-76B900?logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/rishu7491/ScreenLens-AI?style=social)](https://github.com/rishu7491/ScreenLens-AI)

**ScreenLens AI** is an ultra-fast, non-intrusive desktop overlay that captures active questions, MCQs, or complex coding problems from your screen and instantly displays the structured answer in a floating, adaptive card.

[Quick Start](#-quick-start) • [Features](#-key-features) • [Controls](#-controls--shortcuts) • [Architecture](#-how-it-works)

</div>

---

## 📸 Real-World Interface

```text
┌────────────────────────────────────────────────────────┐
│  SCREENLENS AI                                  [DONE] │
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

## 🚀 Key Features

* **Two-Tier Visual QA:**
  * 📌 **Question Box (Top):** Shows the exact question extracted by AI to confirm detection accuracy.
  * 💡 **Answer Box (Bottom):** Shows the verified option letter + full option text, or production-ready code.
* **Auto-Adaptive Sizing:** Compact for short MCQs, smoothly auto-expands downwards for multi-line coding questions and subjective answers.
* **High-Definition Vision (1280px):** Win32 `CAPTUREBLT` engine captures hardware-accelerated browsers and dense exam fonts with zero blurring.
* **One-Click Clipboard Copy:** Instant `[📋 Copy]` button to copy code solutions or text answers.
* **Smart Auto-Loop Mode:** Monitors your screen continuously and only triggers when a new question appears (perceptual change detection prevents redundant API calls).
* **Universal Non-Admin Hotkeys:** Powered by `pynput` global hooks — works on any Windows PC without requiring "Run as Administrator".

---

## ⚡ Quick Start (Ready in 2 Minutes)

### 1. Clone the Repository
```bash
git clone https://github.com/rishu7491/ScreenLens-AI.git
cd ScreenLens-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Add Free API Key
Open `config.py` and set your **NVIDIA NIM API Key**:
```python
NVIDIA_API_KEY = "YOUR_NVIDIA_API_KEY_HERE"
```
> 💡 *Don't have a key? Get one for free with 1,000 free credits at [build.nvidia.com](https://build.nvidia.com/).*

### 4. Launch
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
| **Move Card** | Click & drag header with mouse | — |
| **Exit App** | — | `Ctrl + Shift + X` |

---

## 🧠 How It Works

```
[ Active Screen ]
       │
       ▼
[ Win32 CAPTUREBLT Engine ] ──► [ Perceptual Fingerprint (32x32) ]
       │                                     │
       ▼ (If Changed)                        ▼ (If Static)
[ NVIDIA Nemotron 120B VLM ]            [ Skip API Call ]
       │
       ▼
[ Thread-Safe UI Queue ] ──► [ Adaptive Two-Tier Floating Card ]
```

---

## 🤝 Contributing & Community

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/rishu7491/ScreenLens-AI/issues).

⭐ **If you find ScreenLens AI useful, please give it a Star on GitHub!** It helps the project reach more learners and developers.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
