# SYSTEM DIRECTIVE: PHASE 47 — TDA OPTIMIZATION & BASIS TRANSFORMER (v5.6.0)

**Header Metadata:**
* **Directive ID**: `directive-phase47-v5.6.0`
* **Sender**: `system.master_architect`
* **Receiver**: `cline.executor`
* **Target Node**: `01_Formal_Core` (Symbolic & TDA Mathematical Core)
* **System Version**: `v5.6.0` (Phase 47)
* **Budget Limit**: `$0.00` (Pure Open-Source Stack / Local CPU / Free Limits)
* **Timestamp**: `2026-11-12T09:00:00Z`

---

## 1. МЕТА ТА КОНТЕКСТ
Фаза 47 розпочинає інтелектуальну модернізацію **Вузла 01 (`01_Formal_Core`)** на основі Системної документації покращень Вузлів 01 та 06.
Мета: Впровадити детермінований математичний модуль для топологічного аналізу даних (TDA) та формальної зміни обчислювальних базисів (**Basis Transformation**) без використання зовнішніх платно-підписочних моделей ($0.00 CPU budget).

---

## 2. СПЕЦИФІКАЦІЯ РОБІТ ТА АРТЕФАКТИ

### Task 1: Оптимізація Topologically-Grounded Engine
* **Шлях артефакту**: `01_Formal_Core/src/pure_tda_engine.py` (або оновлення існуючого модуля)
* **Вимоги до функціоналу**:
  * Реалізація побудови симпліціальних комплексів (Vietoris-Rips / Alpha Complexes) та обчислення інваріантів Бетті ($H_0, H_1$) у Pure Python / SciPy / NumPy.
  * Впровадження методу **Time-Delay Embedding** для реконструкції фазового простору скалярних часових рядів.
  * Фільтрація шуму на основі DTM (Distance-to-Measure).

### Task 2: Модуль трансформера базисів (Basis Transformer)
* **Шлях артефакту**: `01_Formal_Core/src/basis_transformer.py`
* **Вимоги до функціоналу**:
  * **Логарифмічний зсув базису**: Детермінований перерахунок масивів даних із десяткової антропоморфної шкали $\log_{10}(x)$ у двоковий природний двійково-інформаційний базис $\log_2(x)$.
  * **Хвильова трансформація параметра "часу"**: Перетворення параметрів часового рядка $T$ у суперпозицію частотних процесів за допомогою Discrete Fourier Transform (ДФТ/FFT через `scipy.fft` чи Pure Python fallback).

### Task 3: Інтеграційне тестування
* **Шлях артефакту**: `tests/integration/test_tda_basis_transformer.py`
* **Вимоги**:
  * Тест 1: Перевірка коректності обчислення $H_0/H_1$ для тестової хмари точок.
  * Тест 2: Перевірка конверсії $\log_{10} \to \log_2$ та ДФТ-спектрального розкладу параметра $T$.
  * Статус виконання: `assert exit_code == 0`.

### Task 4: Синхронізація Пам'яті та Репозиторію
* **Оновлення потрійного контуру**:
  * `PROJECT_SPEC.md` — оновлення шапки та версії до `v5.6.0 / Phase 47`.
  * `PROJECT_CONTEXT.md` — зафіксувати стан Вузла 01 (TDA & Basis Transformer).
  * `PROJECT_STATE.md` — оновити заголовок, внести запис про виконання Phase 47 (v5.6.0).
* **Синхронізація та Пуш**:
  * Виконати `python scripts/sync_gdrive.py`.
  * Виконати `git commit` та `git push origin main`.

---

## 3. DEFINITION OF DONE (DoD)
1. Модулі `pure_tda_engine.py` та `basis_transformer.py` розширено і перевірено через `python -m py_compile`.
2. Інтеграційний тест `python tests/integration/test_tda_basis_transformer.py` виконується з `exit_code: 0`.
3. Файли `PROJECT_SPEC.md`, `PROJECT_CONTEXT.md`, `PROJECT_STATE.md` оновлено до версії `v5.6.0 / Phase 47`.
4. Скрипт `scripts/sync_gdrive.py` виконано успішно.
5. Комміт згенеровано та відправлено у репозиторій через `git push origin main`.
