# The_Endless_Tower
A simple text-adventure and endless rogue-like.

Una pequeña aventura de texto en Python para aplicar patrones de diseño (Strategy, Factory, Flyweight, Template, Singleton) aplicados a un roguelike con sistema de combate estilo RPG por turnos.

## Características
- Creación de personajes y enemigos con metodo Factory y Template.
- Sistema básico de habilidades (Skills) con calculo de daño, críticos y fallos.
- Formulas de daño y selección de objetivo con patrón Strategy.
- Uso del patrón Flyweight para obtimizar el consumo de memoria de las habilidades.
- Creación procedural de habitaciones (de la mazmorra) con patrón Template y Factory
- Uso de Singleton para un log de acciones.
