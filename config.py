# ============================================================
# AI Answer Bubble - Configuration
# ============================================================

import os

# NVIDIA NIM API Key (Get your free key at: https://build.nvidia.com)
# You can set it in system environment variables or paste it below:
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "YOUR_NVIDIA_API_KEY_HERE")

# Model Configuration
NVIDIA_MODEL = "nvidia/nemotron-3.5-super-vl-120b-a12b"
NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"

# Hotkeys (Configurable)
HOTKEY_CAPTURE = "ctrl+q"        # Instant screen scan & answer
HOTKEY_LOOP_TOGGLE = "ctrl+l"   # Toggle hands-free auto-loop mode
HOTKEY_TOGGLE_HIDE = "ctrl+h"   # Hide / Show bubble
HOTKEY_QUIT = "ctrl+shift+x"    # Close app completely

# Auto-Loop Settings
AUTO_LOOP_INTERVAL = 4.0        # Seconds between checks in loop mode
IMAGE_MAX_WIDTH = 1280          # Crisp resolution for small fonts & MCQs
IMAGE_JPEG_QUALITY = 72         # JPEG compression quality

# UI Styling
BUBBLE_OPACITY = 0.94            # Window transparency (0.0 to 1.0)
BUBBLE_POSITION = "bottom-right" # bottom-right, bottom-left, top-right, top-left
BUBBLE_MAX_WIDTH = 440           # Base card width
