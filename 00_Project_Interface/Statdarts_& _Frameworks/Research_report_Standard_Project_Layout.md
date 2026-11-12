# Researcher: Стандарти розробки проєктів та структура каталогів (Standard Project Layout)

Ми знайшли **6 джерел** щодо стандартів розробки, моделей архітектури та уніфікованих структур каталогів/файлів у проєктах.

---

## 🔧 Technical & Specs (6)

| # | Title | Source | Date |
|---|-------|--------|------|
| 1 | [How to organize your project's folders - A quick guide to repository and folder structures](https://dev.to/gvegacl/how-to-organize-your-projects-folders-a-quick-guide-to-repository-and-folder-structures-5fje) | DEV Community | 2024 |
| 2 | [Python Project Layout Best Practices](https://realpython.com/ref/best-practices/project-layout/) | Real Python | 2024 |
| 3 | [Mastering Frontend Project Structures: Choosing the Right Folder Architecture](https://satviksharma.in/blog/frontend-project-structures-guide) | Satvik Sharma Blog | 2024 |
| 4 | [Software-Development-Project-Structure Template Repository](https://github.com/AlexDCode/Software-Development-Project-Structure) | GitHub | 2024 |
| 5 | [Project Structure Guide: Standardize Layouts](https://mcpmarket.com/tools/skills/project-structure-guide-6) | MCP Market | 2025 |
| 6 | [Best Practices for File Structures & Organization](https://mitcommlab.mit.edu/broad/commkit/file-structure/) | MIT Broad Institute | 2024 |

**(1)** Практичний посібник з вибору архітектури папок: за типом файлів, Atomic Design, за фічами (Feature-based) чи за доменами.
**(2)** Огляд сучасного `src/` layout та стандартного розташування конфігурацій (`pyproject.toml`, `README.md`, `tests/`, `docs/`).
**(3)** Порівняння архітектурних підходів для веб-розробки: Flat Layout (для малих проєктів), Feature-Based (для середніх/великих), та Domain-Driven (для корпоративних застосунків).
**(4)** Уніфікований шаблон структури папок для малих та середніх проєктів із чітким розділенням коду, тестів та конфігурацій.
**(5)** Стандарт організації структури для багатьох мов програмування (Python, Node.js, Go, Rust), автоматизація `.gitignore` та поділу вихідних файлів.
**(6)** Принципи розділення відповідальності (Separation of Concerns), хронологічного та логічного найменування файлів для забезпечення відтворюваності розробки.

---

## Ключові теми та рекомендації

- **Стандартний базовий каркас (Standard Root Layout)**:
  - `src/` — весь сирцевий код проєкту (ізоляція від кореня).
  - `tests/` — модульні, інтеграційні та E2E тести.
  - `docs/` — документація, архітектурні рішення (ADR), специфікації.
  - `scripts/` або `bin/` — службові скрипти для збірки, CI/CD, міграцій.
  - Корінь проєкту (`/`): `.gitignore`, `README.md`, `LICENSE`, файли конфігурації залежностей (`pyproject.toml`, `package.json` тощо).

- **Вибір внутрішньої структури коду (`src/`) залежно від масштабу**:
  1. **Layer-Based / Type-Based (За типом/шарами)**: `src/controllers`, `src/models`, `src/views` (чудово для малих проєктів / MVP).
  2. **Feature-Based (За функціоналом / фічами)**: `src/features/auth`, `src/features/billing`, `src/features/dashboard` (найпопулярніший варіант для 80% продакшн-проєктів).
  3. **Domain-Driven (За доменами)**: `src/modules/users`, `src/core/http` (для великих enterprise-проєктів чи мікрофронтендів).

- **Стандартизація найменувань та конвенцій (Conventions)**:
  - Використання змістовних, коротких макро-назв папок нижнім регістром (`snake_case` або `kebab-case`).
  - Чітке відділення розробницьких артефактів від продуктивних збірок (використання `.gitignore`).

---

*Дослідження проведено 2026-11-09.*