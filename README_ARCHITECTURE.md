Clean Architecture Notes

Goal
- Keep domain and application free of Flask, PyMySQL, dotenv, or infrastructure concerns.
- Depend on abstractions (ports) toward the core, and wire implementations in infrastructure.

Current Layering (Target)
- domain/: entities, value objects, and pure rules.
- application/: use cases + DTOs + ports (interfaces/protocols).
- interface_adapters/: web controllers, presenters, and mapping between HTTP and application.
- infrastructure/: concrete adapters (DB, config, framework wiring).

Dependency Rules
- infrastructure -> interface_adapters -> application -> domain
- No imports from infrastructure into application or domain.
- Controllers validate and map inputs; use cases own business flow.

Conventions
- Ports live in src/application/ports.
- Adapters implement ports under src/infrastructure.
- Web-specific models or serializers live under src/interface_adapters.
