with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_STATE.md', 'r') as f:
    content = f.read()

# Update version header
content = content.replace('Phase 44 — v5.3.0', 'Phase 45 — v5.4.0', 1)

# Log Phase 45 execution in Gateway Report
phase45_log = '''\ * **Фаза**: Phase 45 — v5.4.0
* **Дата та час**: 2026-11-12
* **Фаза**: Phase 45 — v5.4.0
* **Шина повідомлень (Message ID)**: msg_20261112_phase45 (status: completed)
* **Виконані дії**:
    1. [x] Реалізовано скрипт `scripts/bigquery_agent_search.py`.
    2. [x] Створено інтеграційний тест `tests/integration/test_bigquery_agent_search.py`.
    3. [x] Оновлено файли пам'яті до v5.4.0 / Phase 45 (PROJECT_SPEC.md, PROJECT_CONTEXT.md, PROJECT_STATE.md).
    4. [x] Виконано `scripts/sync_gdrive.py` та синхронізація з Google Drive.
    5. [x] Виконано `git commit` та `git push origin main`.
    6. [x] Логовано Phase 45 виконання у Gateway Report'''

# Insert Phase 45 log after Phase 44 block
# Find the Phase 44 block and insert Phase 45 after it
idx = content.find('* **Дата та час**: 2026-11-12')
if idx >= 0:
    # Find the second occurrence of * **Фаза** after the date
    idx2 = content.find('* **Фаза**:', idx + 1)
    if idx2 >= 0:
        content = content[:idx2] + phase45_log + '\n' + content[idx2:]

with open('c:\\Users\\crmte\\OneDrive\\Desktop\\Projects\\Discovery_Engine\\PROJECT_STATE.md', 'w') as f:
    f.write(content)
print('PROJECT_STATE.md updated')