with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_SPEC.md', 'r') as f:
    lines = f.readlines()

# Update line 43 (index 42) - change version
lines[42] = lines[42].replace('v5.0.0 / Phase 41', 'v5.4.0 / Phase 45')

# Add new DoD items after line 43 (insert at index 43)
new_lines = [
    '- [ ] `00_Project_Interface/src/bigquery_agent_search.py` implemented with offline fallback.\n',
    '- [ ] `tests/integration/test_bigquery_agent_search.py` passes with `exit_code: 0`.\n',
    '- [ ] Memory triad updated to `v5.4.0` / Phase 45.\n'
]
lines[43:43] = new_lines

with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_SPEC.md', 'w') as f:
    f.writelines(lines)
print('DONE')