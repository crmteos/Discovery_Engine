# Директива Фази 26 (v3.4.1 / v3.5.0)

**Тема:** Pure Python Engine Core & Zero-Dependency Fallbacks (Напрямок 3)  
**Цільова версія:** `v3.5.0`  
**Статус:** `PENDING_EXECUTION`  
**Дата:** 2026-11-10  
**Автор:** `system.master_architect`  
**Виконавець:** `cline.executor`

---

## 1. Контекст та обґрунтування

У системній телеметрії та звітах виконання зафіксовано відсутність рядка зовнішніх Python-пакетів (`rdflib`, `dspy-ai`, `pysr`, `giotto-tda`, `gudhi`, `ollama`) та системного C/C++ компілятора (`gcc`/`cl.exe`) через роботу в ізольованому локальному середовищі zero-dollar бюджету.

Для забезпечення 100% автономності, надійності та відтворюваності системного контуру Discovery Engine на будь-якому ПК без встановлення сторонніх C-бібліотек, Фаза 26 впроваджує **нативні Pure Python реалізації (Zero-Dependency Engines)** для трьох критичних математичних і семантичних модулів.

---

## 2. Специфікація завдань

### Завдання 1. Pure Python RDF Engine (`05_Knowledge_Aggregator/src/pure_rdf_engine.py`)
- Розробити нативний Pure Python парсер, валідатор та серіалізатор для W3C N-Triples та Turtle без використання `rdflib`.
- Забезпечити підтримку нормалізації триплетів `(Subject, Predicate, Object)`, розпізнавання URI, префіксів SKOS/PROV-O та генерацію чистих JSON-LD / N-Triples структур.

### Завдання 2. Pure Python TDA Engine (`01_Formal_Core/src/pure_tda_engine.py`)
- Розробити алгоритм побудови симпліціальних комплексів Вієторіса-Ріпса (Vietoris-Rips Filtration) та обчислення чисел Бетті ($H_0, H_1$) на чистому Python (з використанням `math`, `collections`, `itertools`, `heapq` / `sympy`).
- Замінити залежність від `giotto-tda` / `gudhi`, забезпечити точний пошук компонентів зв'язаності ($H_0$) та 1-вимірних концептуальних циклів/гапів ($H_1$).

### Завдання 3. Pure Python Symbolic Regression Engine (`04_Discovery_Engine/src/pure_symbolic_engine.py`)
- Замінити тимчасову заглушку `symbolic_regression_stub.py` на нативний Pure Python двигун символьної регресії та виведення математичних формул на основі AST-дерев виразів та `sympy`.
- Реалізувати пошук оптимальних алгебраїчних співвідношень між числовими інваріантами знань без використання `pysr` або C++ бібліотек.

### Завдання 4. ADR-0007 та системна інтеграція
- Створити запис архітектурного рішення `docs/adr/0007-pure-python-zero-dependency-engines.md`.
- Оновити паспорти та контексти Вузлів 01, 04, 05 (`NOTEBOOK_PASSPORT_*.md`, `CONTEXT_DOMAIN_*.md`).
- Синхронізувати `system_manifest.json` та `PROJECT_STATE.md` до версії **`v3.5.0`**.

---

## 3. Критерії приймання та верифікації

1. **Синтаксис та компіляція**: `python -m py_compile` для всіх створених скриптів завершується без помилок.
2. **Модульні тести**:
   - `python 05_Knowledge_Aggregator/src/pure_rdf_engine.py --test` ➔ успішна парсинг-серіалізація N-Triples (exit code 0).
   - `python 01_Formal_Core/src/pure_tda_engine.py --test` ➔ точний розрахунок $H_0, H_1$ для тестового графа (exit code 0).
   - `python 04_Discovery_Engine/src/pure_symbolic_engine.py --test` ➔ успішний вивід формули з масиву інваріантів (exit code 0).
3. **E2E Pipeline Test**: `python tests/e2e/test_e2e_pipeline.py` успішно проходить усі етапи (4/4) без жодних зовнішніх C-залежностей.

---

## 4. Реєстрація на шині повідомлень
- **Topic**: `directive-phase26-v3.5.0`
- **Sender**: `system.master_architect`
- **Receiver**: `cline.executor`
- **Vector**: `vertical`
