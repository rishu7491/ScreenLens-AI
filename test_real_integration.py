import sys
import time
import answer_bubble

print("=== VERIFYING ADAPTIVE TWO-TIER QA ENGINE ===")

app = answer_bubble.AdaptiveBubbleApp()
print(f" -> Bubble started. Dimensions: {app.root.winfo_geometry()}")

# Test parsing helper
mock_response = """QUESTION:
Q1. Which data structure is used for Breadth First Search of a graph?
A) Stack
B) Queue
C) Tree

ANSWER:
Option B: Queue (BFS uses a FIFO queue to visit adjacent nodes level-by-level)"""

q, a = answer_bubble.parse_qa_response(mock_response)
print("\nParsed Q:")
print(q)
print("\nParsed A:")
print(a)

app.update_content(q, a, "[DONE]", "#10B981")
app.root.update()

q_content = app.q_box.get("1.0", "end-1c")
a_content = app.a_box.get("1.0", "end-1c")

print("\nUI Box Verification:")
print(f" -> Question Box Content: {q_content[:60]}...")
print(f" -> Answer Box Content: {a_content[:60]}...")
print(f" -> Final Window Geometry: {app.root.winfo_geometry()}")

assert "Breadth First Search" in q_content, "Question not shown in Question Box!"
assert "Option B: Queue" in a_content, "Answer not shown in Answer Box!"

# Test Copy function
app.copy_answer_to_clipboard()
copied = app.root.clipboard_get()
print(f" -> Clipboard Copy Verified: {copied[:40]}...")
assert "Option B: Queue" in copied, "Clipboard copy failed!"

app.root.destroy()
print("\n=== ALL ADAPTIVE QA TESTS PASSED (100%) ===")
