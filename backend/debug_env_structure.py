from pathlib import Path

env_path = Path("backend/.env")
print(f"Reading {env_path.absolute()}")

with open(env_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if "=" in line:
            key, val = line.split("=", 1)
            print(f"Line {i+1}: Key='{key.strip()}', ValLength={len(val.strip())}")
        else:
            print(f"Line {i+1}: [No '=' found] Content: {line.strip()[:10]}...")
