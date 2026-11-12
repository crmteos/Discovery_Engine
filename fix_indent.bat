@echo off
python3 << 'PYEOF'
with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\00_Project_Interface\\src\\google_ai_gateway.py', 'r') as f:
    content = f.read()
# Fix the _list_models indentation
content = content.replace('        return []\n    try:', '    if client is None:\n        return []\n    try:')
with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\00_Project_Interface\\src\\google_ai_gateway.py', 'w') as f:
    f.write(content)
print("Fixed")
PYEOF