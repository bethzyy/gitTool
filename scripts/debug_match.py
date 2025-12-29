import re

content = open('git_gui_app.py', 'r', encoding='utf-8').read()
pattern = r'mongodb://[^@]+@'
matches = list(re.finditer(pattern, content, re.IGNORECASE))

print(f"Found {len(matches)} matches")
for i, match in enumerate(matches, 1):
    text = match.group()
    print(f"\nMatch {i}:")
    print(f"  Text: {repr(text)}")
    print(f"  Contains r': {\"r'\" in text}")
    print(f"  Contains r\": {'r\"' in text}")
    print(f"  Contains [^: {'[^' in text}")
    print(f"  Contains [: {\"'\" in text or '\"' in text}")
