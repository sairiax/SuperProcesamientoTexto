# Conceptos Clave: Advanced Python for AI Engineering

Esta lista resume los conceptos fundamentales aprendidos durante el curso, organizada por días para facilitar el seguimiento del progreso en futuros proyectos.

## Día 1: Fundamentos y Configuración
- [x] **Python Idioms**: Uso de list/dict comprehensions vs loops tradicionales.
- [x] **Generadores**: Implementación de generadores para eficiencia de memoria.
- [x] **Virtual Environments**: Creación y gestión de entornos con `venv`.
- [x] **Módulos e Imports**: Estructura de paquetes, `__init__.py`, e imports absolutos/relativos.
- [x] **Type Hinting Básico**: Uso de `List`, `Dict`, `Optional`, y `Union` para robustez.
- [x] **Code Quality Tools**: Configuración y uso de `Ruff` (linting/formateo) y `Pyright` (static type checking).
- [x] **Package Distribution**: Uso de `pyproject.toml` y estructura de carpetas `src/`.

## Día 2: Clean Code y Funciones
- [x] **Build Backends**: Diferencias entre `Hatchling` y `setuptools`.
- [x] **Clean Functions**: Creación de funciones pequeñas con una única responsabilidad.
- [x] **Meaningful Names**: Uso de nombres descriptivos para variables y funciones.
- [x] **Principios Clean Code**: Aplicación de SRP, DRY y KISS.
- [x] **Refactoring**: Técnicas para simplificar código complejo y eliminar duplicados.

## Día 3: Robustez y Legibilidad
- [x] **Type Hints Avanzados**: Uso de `Generic`, `Protocol`, `TypeVar` y `Callable`.
- [x] **Error Handling**: Creación y uso de excepciones personalizadas (`custom exceptions`).
- [x] **Logging Estratégico**: Implementación de niveles de log, formateo y handlers en pipelines.
- [x] **Documentación**: Escritura de docstrings completos siguiendo el formato **Sphinx**.
- [x] **Defensive Programming**: Validación de inputs, uso de `assertions` y patrón *Fail Fast*.
- [x] **Diseño de Objetos**: Aplicación de la *Ley de Demeter* y separación de preocupaciones (*Separation of Concerns*).

## Día 4: Arquitectura y SOLID
- [x] **Modelado de Datos**: Uso de `@property`, `dataclasses` (inmutables) y `Pydantic v2`.
- [x] **Pydantic**: Validación avanzada con `Field`, `validators` y `discriminated unions`.
- [x] **Composición sobre Herencia**: Diseño de sistemas flexibles evitando jerarquías profundas.
- [x] **Protocols**: Definición de contratos mediante *structural typing*.
- [x] **Principios SOLID**:
    - [x] **SRP**: Single Responsibility Principle.
    - [x] **OCP**: Open/Closed Principle (extensión sin modificación).
    - [x] **LSP**: Liskov Substitution Principle (intercambiabilidad).
    - [x] **ISP**: Interface Segregation Principle (interfaces específicas).
    - [x] **DIP**: Dependency Inversion Principle (depender de abstracciones/Protocols).

## Día 5: Testing Profesional
- [x] **Tipos de Tests**: Diferenciación entre tests unitarios, de integración y funcionales.
- [x] **Patrón AAA**: Estructuración de tests en *Arrange, Act, Assert*.
- [x] **pytest Features**:
    - [x] **Fixtures**: Creación de componentes de prueba reutilizables.
    - [x] **Parametrize**: Pruebas masivas con diferentes juegos de datos.
- [x] **Mocking**: Uso de `unittest.mock` (`patch`, `MagicMock`) para aislar dependencias externas (APIs, DBs).
- [x] **Coverage**: Medición y análisis de cobertura de código con `pytest-cov`.
- [x] **Functional Testing**: Pruebas de I/O usando `tmp_path`.

## Día 6: Proyecto y Distribución
- [x] **CLI Development**: Creación de interfaces de línea de comandos con `argparse` o `typer`.
- [x] **Integración Total**: Aplicación conjunta de todos los patrones de arquitectura y calidad.
- [x] **Producción**: Generación de paquetes distribuibles (`wheels`).
- [x] **Documentación de Proyecto**: Creación de READMEs profesionales con instrucciones de instalación y uso.
