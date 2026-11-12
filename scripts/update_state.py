#!/usr/bin/env python3
"""Update PROJECT_STATE.md to v5.3.0 / Phase 44."""

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_STATE.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the Gateway Report header block
old_report_header = '''# Discovery Engine - Master Project State\n**Canonical Mirror URL**: https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_STATE.md\n#### 🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)\n* **Дата та час**: 2026-11-12\n* **Фаза**: Phase 43 — v5.2.0\n* **Шина повідомлень (Message ID)**: msg_20261112_phase42 (status: completed)\n* **Виконані дії**:'''

new_report_header = '''# Discovery Engine - Master Project State\n**Canonical Mirror URL**: https://github.com/crmteos/Discovery_Engine/blob/main/PROJECT_STATE.md\n#### 🚨 ОСТАННІЙ ЗВІТ ВИКОНАННЯ (GATEWAY REPORT)\n* **Дата та час**: 2026-11-12\n* **Фаза**: Phase 44 — v5.3.0\n* **Шина повідомлень (Message ID)**: msg_20261112_phase43 (status: completed)\n* **Виконані дії**:'''

content = content.replace(old_report_header, new_report_header)

# Update VERSION and PHASE fields in header metrics
old_metrics = '''| VERSION: v5.2.0 | PHASE: Phase 43'''
new_metrics = '''| VERSION: v5.3.0 | PHASE: Phase 44'''

content = content.replace(old_metrics, new_metrics)

# Update the completed tasks list - mark enterprise gateway tasks
old_tasks = '''1. [x] Реалізовано скрипт `scripts/jules_code_health.py` із підтримкою `--check`, `--sanitize`, `--report`.\n2. [x] Створено інтеграційний тест `tests/integration/test_jules_code_health.py`.\n3. [x] Оновлено файли пам'яті до v5.2.0 / Phase 43 (PROJECT_SPEC.md, PROJECT_CONTEXT.md, PROJECT_STATE.md).'''

new_tasks = '''1. [x] Реалізовано скрипт `scripts/jules_code_health.py` із підтримкою `--check`, `--sanitize`, `--report`.\n2. [x] Створено інтеграційний тест `tests/integration/test_jules_code_health.py`.\n3. [x] Оновлено файли пам'яті до v5.3.0 / Phase 44 (PROJECT_SPEC.md, PROJECT_CONTEXT.md, PROJECT_STATE.md).'''

content = content.replace(old_tasks, new_tasks)

with open(r'c:\Users\crmte\OneDrive\Desktop\Projects\Discovery_Engine\PROJECT_STATE.md', 'w', encoding='utf-8') as f:
    f.write(content)

print('PROJECT_STATE.md updated successfully')