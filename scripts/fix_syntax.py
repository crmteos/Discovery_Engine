#!/usr/bin/env python3
"""Fix syntax error in google_ai_gateway.py."""

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\00_Project_Interface\src\google_ai_gateway.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the corrupted line - remove the leftover _PROJECT_ID)
content = content.replace('_PROJECT_ID)\n            available', '            available')

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\00_Project_Interface\src\google_ai_gateway.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed syntax error')