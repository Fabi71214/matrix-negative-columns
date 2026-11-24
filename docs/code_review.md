# Инспекция кода и ревью тестов

## 1. Инспекция кода (flake8)
Команда проверки: `flake8 src/ tests/ --max-line-length=100`

### Замечания до исправления (в коде из ЛР №3):
- `E302 expected 2 blank lines, found 1` (`src/output_module.py`, `src/input_module.py`, `src/calc_module.py`, `src/stubs_drivers.py`)
- `E401 multiple imports on one line` (`src/main.py`, `tests/test_integration.py`)
- `E501 line too long (> 100 characters)` (`src/input_module.py`, `src/calc_module.py`, `tests/test_integration.py`)

### После исправления:
Все нарушения PEP 8 устранены, код отформатирован, добавлены docstrings. Повторная проверка `flake8 src/ tests/ --max-line-length=100` завершилась без ошибок.

## 2. Ревью тестов
- Проверена полнота граничных значений около 0 (`-0.0001`, `0.0`, `0.0001`) и границ размерностей (`-1`, `0`, `1`).
- Обеспечено комбинаторное покрытие условий `(n <= 0 or m <= 0)` для всех 4 комбинаций истинности.
- Все регрессионные тесты вынесены в отдельный модуль `tests/test_regression.py` и включены в CI/CD пайплайн.
