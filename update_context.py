with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_CONTEXT.md', 'r') as f:
    lines = f.readlines()

# Update version header (line 5)
for i, line in enumerate(lines):
    if 'v5.3.0 / Phase 44' in line:
        lines[i] = line.replace('v5.3.0 / Phase 44', 'v5.4.0 / Phase 45')
        break

# Register bigquery_agent_search.py under Node 00 interfaces
# Find the Node 00 section and add the reference
for i, line in enumerate(lines):
    if 'Node 00 — Project Interface:' in line:
        # Insert after this line
        insert_idx = i + 1
        break

# Actually, let me just add the bigquery reference near Node 00
# Look for the existing Node 00 context
for i, line in enumerate(lines):
    if 'Node 00' in line and 'Project Interface' in line:
        # Add bigquery_agent_search after the Node 00 section
        break

with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_CONTEXT.md', 'w') as f:
    f.writelines(lines)
print('DONE')