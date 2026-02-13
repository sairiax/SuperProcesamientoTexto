# Conceptos Clave: Advanced Python for AI Engineering

Esta lista resume los conceptos fundamentales aprendidos durante el curso, organizada por días para facilitar el seguimiento del progreso en futuros proyectos.

## Día 1: Fundamentos y Configuración
- [ ] **Python Idioms**: Uso de list/dict comprehensions vs loops tradicionales.
- [ ] **Generadores**: Implementación de generadores para eficiencia de memoria.
- [ ] **Virtual Environments**: Creación y gestión de entornos con `venv`.
- [ ] **Módulos e Imports**: Estructura de paquetes, `__init__.py`, e imports absolutos/relativos.
- [ ] **Type Hinting Básico**: Uso de `List`, `Dict`, `Optional`, y `Union` para robustez.
- [ ] **Code Quality Tools**: Configuración y uso de `Ruff` (linting/formateo) y `Pyright` (static type checking).
- [ ] **Package Distribution**: Uso de `pyproject.toml` y estructura de carpetas `src/`.

## Día 2: Clean Code y Funciones
- [ ] **Build Backends**: Diferencias entre `Hatchling` y `setuptools`.
- [ ] **Clean Functions**: Creación de funciones pequeñas con una única responsabilidad.
- [ ] **Meaningful Names**: Uso de nombres descriptivos para variables y funciones.
- [ ] **Principios Clean Code**: Aplicación de SRP, DRY y KISS.
- [ ] **Refactoring**: Técnicas para simplificar código complejo y eliminar duplicados.

## Día 3: Robustez y Legibilidad
- [ ] **Type Hints Avanzados**: Uso de `Generic`, `Protocol`, `TypeVar` y `Callable`.
- [ ] **Error Handling**: Creación y uso de excepciones personalizadas (`custom exceptions`).
- [ ] **Logging Estratégico**: Implementación de niveles de log, formateo y handlers en pipelines.
- [ ] **Documentación**: Escritura de docstrings completos siguiendo el formato **Sphinx**.
- [ ] **Defensive Programming**: Validación de inputs, uso de `assertions` y patrón *Fail Fast*.
- [ ] **Diseño de Objetos**: Aplicación de la *Ley de Demeter* y separación de preocupaciones (*Separation of Concerns*).

## Día 4: Arquitectura y SOLID
- [ ] **Modelado de Datos**: Uso de `@property`, `dataclasses` (inmutables) y `Pydantic v2`.
- [ ] **Pydantic**: Validación avanzada con `Field`, `validators` y `discriminated unions`.
- [ ] **Composición sobre Herencia**: Diseño de sistemas flexibles evitando jerarquías profundas.
- [ ] **Protocols**: Definición de contratos mediante *structural typing*.
- [ ] **Principios SOLID**:
    - [ ] **SRP**: Single Responsibility Principle.
    - [ ] **OCP**: Open/Closed Principle (extensión sin modificación).
    - [ ] **LSP**: Liskov Substitution Principle (intercambiabilidad).
    - [ ] **ISP**: Interface Segregation Principle (interfaces específicas).
    - [ ] **DIP**: Dependency Inversion Principle (depender de abstracciones/Protocols).

## Día 5: Testing Profesional
- [ ] **Tipos de Tests**: Diferenciación entre tests unitarios, de integración y funcionales.
- [ ] **Patrón AAA**: Estructuración de tests en *Arrange, Act, Assert*.
- [ ] **pytest Features**:
    - [ ] **Fixtures**: Creación de componentes de prueba reutilizables.
    - [ ] **Parametrize**: Pruebas masivas con diferentes juegos de datos.
- [ ] **Mocking**: Uso de `unittest.mock` (`patch`, `MagicMock`) para aislar dependencias externas (APIs, DBs).
- [ ] **Coverage**: Medición y análisis de cobertura de código con `pytest-cov`.
- [ ] **Functional Testing**: Pruebas de I/O usando `tmp_path`.

## Día 6: Proyecto y Distribución
- [ ] **CLI Development**: Creación de interfaces de línea de comandos con `argparse` o `typer`.
- [ ] **Integración Total**: Aplicación conjunta de todos los patrones de arquitectura y calidad.
- [ ] **Producción**: Generación de paquetes distribuibles (`wheels`).
- [ ] **Documentación de Proyecto**: Creación de READMEs profesionales con instrucciones de instalación y uso.
