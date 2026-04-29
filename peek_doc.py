
import os

def read_doc_raw(path):
    try:
        with open(path, 'rb') as f:
            content = f.read()
            # Extract printable characters
            readable = "".join([chr(c) if 32 <= c <= 126 else " " for c in content])
            print(readable[:2000])
    except Exception as e:
        print(f"Error reading: {e}")

read_doc_raw(r"c:\master project\LLS\LLS\ppt instruction\CIP univ review - ppt preparation 25-26.doc")
