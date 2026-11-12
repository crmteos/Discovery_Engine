#!/usr/bin/env python3
"""Update PROJECT_SPEC.md to v5.3.0 / Phase 44."""

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_SPEC.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the version line
content = content.replace(
    '# PROJECT_SPEC — Discovery Engine (v5.2.0 / Phase 43)',
    '# PROJECT_SPEC — Discovery Engine (v5.3.0 / Phase 44)'
)

# Update the DoD section
old_dod = '''## 6. Definition of Done (DoD)
- [ ] All Python files pass `py_compile`.
- [ ] Zero ungrounded or external dependencies.
- [ ] `PROJECT_STATE.md` updated and synchronized to `v5.0.0 / Phase 41`.
- [ ] Run `scripts/jules_code_health.py --check` and verify JSON report.
---'''

new_dod = '''## 6. Definition of Done (DoD)
- [ ] All Python files pass `py_compile`.
- [ ] Zero ungrounded or external dependencies.
- [ ] `PROJECT_STATE.md` updated and synchronized to `v5.3.0 / Phase 44`.
- [ ] Run `scripts/jules_code_health.py --check` and verify JSON report.
- [ ] **Enterprise Gateway support**: `--enterprise` and `--location` (EU/US) CLI arguments functional.
- [ ] **Data Residency**: `europe-west1` (EU) and `us-central1` (US) location support verified.
---'''

content = content.replace(old_dod, new_dod)

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_SPEC.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('PROJECT_SPEC.md updated successfully')