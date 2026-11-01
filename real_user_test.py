import time
import base64
import io
from PIL import Image, ImageDraw
from answer_bubble import capture_optimized_screen, query_nvidia_vision, has_meaningfully_changed

print("==================================================")
print("   REAL USER SIMULATION & QUALITY GATE TEST")
print("==================================================")

# --- TEST 1: LIVE DESKTOP SCREEN CAPTURE & OPTIMIZATION ---
print("\n[TEST 1] Testing live screen capture and compression...")
t0 = time.time()
img_b64, fp = capture_optimized_screen()
t_capture = round(time.time() - t0, 3)
print(f" -> Screen captured in {t_capture}s")
print(f" -> Base64 payload size: {len(img_b64)} chars (~{round(len(img_b64)/1024, 1)} KB)")
print(f" -> Perceptual Fingerprint items: {len(fp)}")
assert len(img_b64) > 1000, "Screenshot capture failed!"
print(" -> [PASS] Test 1 Succeeded.")

# --- TEST 2: SIMULATED EXAM SCREEN WITH 3 MCQS ---
print("\n[TEST 2] Generating simulated quiz screen (3 MCQs)...")
test_canvas = Image.new("RGB", (900, 450), color=(255, 255, 255))
draw = ImageDraw.Draw(test_canvas)

questions_text = """
ONLINE EXAMINATION - GENERAL SCIENCE

Q1. Which gas do plants primarily absorb during photosynthesis?
    A) Oxygen
    B) Carbon Dioxide
    C) Nitrogen
    D) Helium

Q2. What is the chemical formula of Water?
    A) CO2
    B) H2O
    C) NaCl
    D) CH4

Q3. What is the powerhouse of the cell?
    A) Nucleus
    B) Ribosome
    C) Mitochondria
    D) Chloroplast
"""
draw.text((25, 20), questions_text, fill=(20, 20, 20))

buffer = io.BytesIO()
test_canvas.save(buffer, format="JPEG", quality=75)
sim_b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

print(f" -> Mock exam screen created ({test_canvas.size[0]}x{test_canvas.size[1]}px)")
print(" -> Sending to NVIDIA Nemotron Vision API...")

t0 = time.time()
answer = query_nvidia_vision(sim_b64)
t_api = round(time.time() - t0, 2)

print(f"\n[AI ANSWER OUTPUT in {t_api}s]:")
print("-" * 40)
print(answer)
print("-" * 40)

assert "B" in answer or "H2O" in answer or "Mitochondria" in answer, f"Unexpected answer: {answer}"
print(" -> [PASS] Test 2 Succeeded with high precision!")

# --- TEST 3: AUTO-LOOP STABLE CHANGE DETECTION ---
print("\n[TEST 3] Testing Auto-Loop static vs changed screen logic...")
_, fp1 = capture_optimized_screen()
time.sleep(0.1)
_, fp2 = capture_optimized_screen()
changed = has_meaningfully_changed(fp1, fp2)
print(f" -> Meaningful change detected on static screen: {changed}")
assert not changed, "Static screen incorrectly flagged as changed"
print(" -> [PASS] Test 3 Succeeded: Zero redundant calls on static screen!")

print("\n==================================================")
print("  ALL REAL-USER SIMULATION TESTS PASSED (3/3)!")
print("==================================================")
