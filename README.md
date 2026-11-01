<div align="center">

# 🔍 ScreenLens AI ⚡

### *The Ultra-Fast Floating Vision Copilot for Students, Coders & Researchers*

[![GitHub Stars](https://img.shields.io/github/stars/rishu7491/ScreenLens-AI?style=for-the-badge&color=yellow)](https://github.com/rishu7491/ScreenLens-AI/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Model: NVIDIA Nemotron](https://img.shields.io/badge/Vision_AI-NVIDIA_Nemotron_3.5-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows_10%20%2F%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://microsoft.com/windows)

<p align="center">
  <b>A stealth, lightweight floating AI widget that reads any question, MCQ, or coding problem directly from your screen and delivers accurate answers in under 3.5 seconds.</b>
</p>

[Quick Start](#-quick-start) • [Features](#-key-features) • [Controls](#-controls--shortcuts) • [Architecture](#-how-it-works) • [License](#-license)

</div>

---

## 💡 Why ScreenLens AI?

Most AI tools require you to take a manual screenshot, open a browser, paste the image into ChatGPT, and wait 15 seconds. 

**ScreenLens AI cuts that down to 1 click or 1 keystroke (`Ctrl+Q`):**
1. Sees the question directly on your screen (even in hardware-accelerated browsers & PDFs).
2. Uses NVIDIA's ultra-fast multimodal vision model.
3. Automatically breaks the output into a **Question Box (Top)** and **Answer/Code Box (Bottom)**.
4. Auto-expands for complex multi-line code or stays compact for quick MCQs.

---

## 🖥️ Live Interface Preview

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

## ✨ Key Features

- **🎯 Two-Tier View (Verification First):**
  - **Question Box (Top):** Confirms exactly what the AI read from your screen.
  - **Answer Box (Bottom):** Shows the solution with high contrast and monospace font for code.
- **⚡ 3-Second Response Time:** Powered by NVIDIA's `nemotron-3.5-super-vl-120b-a12b` optimized with lightweight 1280px compression.
- **📐 Adaptive Dynamic Sizing:** Compact for short MCQs, auto-expands downward for multi-line Python, C++, or Java code solutions.
- **📋 One-Click Copy:** Click `[📋 Copy]` to instantly transfer answers or code to your clipboard.
- **🔄 Hands-Free Auto-Loop:** Press `Ctrl+L` or click `[Loop]` to monitor your screen. Perceptual diff hashing prevents redundant API calls until a new question appears.
- **👻 Non-Intrusive Floating Window:** Topmost translucent design that stays visible over browsers, PDFs, and coding IDEs. Drag anywhere on screen.
- **🔒 Zero Admin Rights Needed:** Runs smoothly using non-elevated user-level global hooks (`pynput`).

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/rishu7491/ScreenLens-AI.git
cd ScreenLens-AI
```

### 2. Install Requirements
```bash
pip install -r requirements.txt
```

### 3. Add Free API Key
Open `config.py` and paste your free **NVIDIA NIM API Key**:
```python
NVIDIA_API_KEY = "YOUR_NVIDIA_API_KEY_HERE"
```
> 🎁 **Tip:** Get a 100% free API key with free credits at [build.nvidia.com](https://build.nvidia.com/).

### 4. Run the Copilot
Double-click **`START.bat`** or execute:
```bash
python answer_bubble.py
```

---

## ⌨️ Controls & Shortcuts

| Action | Mouse Click | Global Shortcut |
|---|---|---|
| **Scan & Solve** | Click `[📸 Scan Now]` | `Ctrl + Q` |
| **Auto-Loop Toggle** | Click `[🔄 Loop: OFF/ON]` | `Ctrl + L` |
| **Copy to Clipboard** | Click `[📋 Copy]` | — |
| **Hide / Show Window** | Click `[✕]` | `Ctrl + H` |
| **Reposition** | Click & drag window header | — |
| **Exit App** | — | `Ctrl + Shift + X` |

---

## 🔬 How It Works (Technical Architecture)

```
[ Active Display Screen ]
          │
          ▼
[ Win32 CAPTUREBLT Engine ] ──► Captures hardware-accelerated DWM surface
          │
          ▼
[ 32x32 Perceptual Hashing ] ──► Skips static screens (Saves API tokens)
          │
          ▼
[ NVIDIA Nemotron Vision API ] ──► 1280px high-contrast inference
          │
          ▼
[ Thread-Safe UI Queue ] ──► Renders Question & Answer without GUI freeze
```

---

## 🤝 Contributing & Community

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/rishu7491/ScreenLens-AI/issues).

### ⭐ Support the Project
If you find ScreenLens AI helpful, please consider giving it a **Star ⭐** on GitHub! It helps more developers and students discover this open-source tool.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
