"""
Servidor MCP con prompts reutilizables.
Demuestra cómo exponer plantillas de prompts parametrizadas.
"""

from fastmcp import FastMCP

app = FastMCP("Prompts Server")

@app.prompt()
def revisar_codigo(lenguaje: str, codigo: str, enfoque: str = "general"):
    """
    Genera un prompt para revisar código.
    
    Args:
        lenguaje: Lenguaje de programación (python, javascript, etc.)
        codigo: Código a revisar
        enfoque: Aspecto en el que enfocarse (general, seguridad, rendimiento)
    """
    enfoques_texto = {
        "general": "calidad general del código, buenas prácticas y posibles mejoras",
        "seguridad": "vulnerabilidades de seguridad y mejores prácticas de seguridad",
        "rendimiento": "optimizaciones de rendimiento y eficiencia del código",
        "mantenibilidad": "legibilidad, mantenibilidad y documentación del código"
    }
    
    enfoque_descripcion = enfoques_texto.get(enfoque, enfoques_texto["general"])
    
    return f"""Eres un experto en {lenguaje} con años de experiencia en desarrollo de software.

Por favor revisa el siguiente código enfocándote en: {enfoque_descripcion}

```{lenguaje}
{codigo}
```

Proporciona un análisis que incluya:

1. **Evaluación General**: Calificación del código (1-10) y resumen
2. **Aspectos Positivos**: Qué está bien implementado
3. **Áreas de Mejora**: Problemas identificados y sugerencias específicas
4. **Código Mejorado**: Versión mejorada del código (si aplica)
5. **Explicación**: Justificación de los cambios sugeridos

Sé específico, práctico y constructivo en tu feedback.
"""

@app.prompt()
def generar_tests(funcion_nombre: str, funcion_codigo: str, lenguaje: str = "python"):
    """
    Genera un prompt para crear tests unitarios.
    
    Args:
        funcion_nombre: Nombre de la función a testear
        funcion_codigo: Código de la función
        lenguaje: Lenguaje de programación
    """
    return f"""Eres un experto en testing y TDD para {lenguaje}.

Necesito crear tests unitarios completos para la siguiente función:

```{lenguaje}
{funcion_codigo}
```

Por favor genera:

1. **Suite de Tests Completa**: Todos los tests necesarios
2. **Casos Normales**: Tests para uso esperado
3. **Casos Extremos**: Tests para edge cases
4. **Casos de Error**: Tests para manejo de errores
5. **Mocks/Fixtures**: Si son necesarios, inclúyelos
6. **Documentación**: Breve explicación de qué testea cada caso

Usa las mejores prácticas de testing para {lenguaje} y asegura buena cobertura.
"""

@app.prompt()
def documentar_api(endpoint: str, metodo: str, descripcion: str):
    """
    Genera documentación para un endpoint de API.
    
    Args:
        endpoint: Ruta del endpoint (ej: /api/users)
        metodo: Método HTTP (GET, POST, etc.)
        descripcion: Descripción breve del endpoint
    """
    return f"""Genera documentación completa y profesional para este endpoint de API:

**Endpoint**: `{metodo} {endpoint}`
**Descripción**: {descripcion}

La documentación debe incluir:

1. **Descripción Detallada**: Qué hace el endpoint y cuándo usarlo
2. **Parámetros**: 
   - Path parameters (si aplica)
   - Query parameters (si aplica)
   - Request body (si aplica)
   Con tipos de datos y si son requeridos u opcionales

3. **Respuestas**:
   - Código 200: Respuesta exitosa con ejemplo
   - Códigos de error: 400, 401, 404, 500 con ejemplos
   
4. **Ejemplos de Uso**:
   - Ejemplo con curl
   - Ejemplo con JavaScript/fetch
   - Ejemplo con Python/requests

5. **Notas Importantes**: Consideraciones especiales, rate limits, etc.

Usa formato Markdown y sé claro y conciso.
"""

@app.prompt()
def explicar_codigo(codigo: str, nivel: str = "intermedio"):
    """
    Genera un prompt para explicar código.
    
    Args:
        codigo: Código a explicar
        nivel: Nivel del destinatario (principiante, intermedio, avanzado)
    """
    niveles = {
        "principiante": "alguien que está aprendiendo programación",
        "intermedio": "un desarrollador con experiencia básica",
        "avanzado": "un desarrollador experimentado"
    }
    
    audiencia = niveles.get(nivel, niveles["intermedio"])
    
    return f"""Explica el siguiente código como si estuvieras enseñando a {audiencia}:

```
{codigo}
```

Tu explicación debe incluir:

1. **Resumen**: Qué hace el código en términos simples
2. **Desglose Línea por Línea**: Explicación detallada de cada parte
3. **Conceptos Clave**: Conceptos importantes usados en el código
4. **Analogías**: Comparaciones con situaciones de la vida real (si ayuda)
5. **Casos de Uso**: Cuándo y por qué usarías este código

Ajusta el nivel de detalle y vocabulario técnico según la audiencia.
"""

@app.prompt()
def refactorizar_codigo(codigo: str, objetivo: str = "legibilidad"):
    """
    Genera un prompt para refactorizar código.
    
    Args:
        codigo: Código a refactorizar
        objetivo: Objetivo del refactoring (legibilidad, rendimiento, modularidad)
    """
    return f"""Refactoriza el siguiente código optimizando para: {objetivo}

Código original:
```
{codigo}
```

Por favor proporciona:

1. **Análisis Inicial**: Problemas actuales del código
2. **Código Refactorizado**: Versión mejorada completa
3. **Cambios Realizados**: Lista de modificaciones con justificación
4. **Mejoras Logradas**: Cómo el código mejoró
5. **Trade-offs**: Si hay compromisos, explícalos

Mantén la funcionalidad original mientras mejoras el código según el objetivo.
"""

if __name__ == "__main__":
    # Usa stdio para comunicación directa entre procesos
    app.run()
