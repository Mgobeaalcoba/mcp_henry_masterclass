# 🚀 Henry Masterclass: AI Automation con Model Context Protocol (MCP)

> **Proyecto de demostración profesional** para enseñar cómo conectar sistemas empresariales a IAs mediante MCP y Cursor.

## 📚 ¿Qué es MCP y por qué lo necesita Cursor?

### El Problema
Los LLMs (como Claude o GPT) son increíblemente poderosos, pero tienen una limitación fundamental: **solo conocen lo que estaba en sus datos de entrenamiento**. No pueden acceder a:
- Tu base de datos de clientes
- Tu sistema de tickets de soporte
- Tu CRM interno
- APIs de tu empresa
- Archivos y documentos privados

### La Solución: Model Context Protocol (MCP)

**MCP** es un estándar abierto creado por Anthropic que permite a las IAs conectarse de forma segura con fuentes de datos externas. Piensa en ello como "USB para IAs":

```
┌─────────────┐         ┌──────────┐         ┌──────────────┐
│   Cursor    │ ◄─MCP──►│ Servidor │ ◄──────►│ Base de Datos│
│  (Cliente)  │         │   MCP    │         │   SQLite     │
└─────────────┘         └──────────┘         └──────────────┘
```

**Beneficios clave:**
- ✅ **Acceso contextual**: La IA puede consultar datos en tiempo real
- ✅ **Seguridad**: Control granular sobre qué puede hacer la IA
- ✅ **Estandarizado**: Un protocolo, múltiples aplicaciones
- ✅ **Bidireccional**: No solo lee, también puede ejecutar acciones

### ¿Por qué Cursor necesita MCP?

Cursor es un IDE potenciado por IA, pero sin MCP está "ciego" a tus sistemas empresariales. Con MCP:
- Puede consultar tu base de datos directamente desde el chat
- Puede generar reportes analizando datos reales
- Puede sugerir código basado en tu arquitectura actual
- Puede automatizar tareas conectadas a tus sistemas

---

## 🛠️ Setup del Proyecto

### Requisitos previos
- Python 3.12+
- Poetry instalado ([Guía de instalación](https://python-poetry.org/docs/#installation))
- Cursor IDE ([Descargar aquí](https://cursor.sh/))

### 1. Instalar dependencias

```bash
poetry install
```

Esto instalará:
- `mcp`: Biblioteca base del protocolo MCP
- `fastmcp`: Framework para crear servidores MCP fácilmente

### 2. Generar base de datos de prueba

```bash
poetry run python scripts/setup_db.py
```

Este script crea `soporte.db` con 60 tickets realistas que simulan un sistema de soporte técnico real.

**Salida esperada:**
```
✅ Base de datos creada exitosamente!
   Total de tickets: 60

   Distribución por prioridad:
     - alta: 15
     - baja: 21
     - media: 17
     - urgente: 7
```

### 3. Verificar que todo funcione

```bash
poetry run python src/mcp_server.py
```

Si ves logs del servidor MCP sin errores, ¡estás listo! (Presiona Ctrl+C para detenerlo)

---

## ⚙️ Configuración en Cursor IDE

### Paso 1: Abrir configuración de MCP

1. Abre **Cursor**
2. Ve a **Cursor Settings** (Cmd/Ctrl + ,)
3. Busca la pestaña **"MCP"** o **"Model Context Protocol"**
4. Haz clic en **"Edit Config"** o abre directamente el archivo de configuración

**Ubicación del archivo de configuración:**
- **macOS**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- **Windows**: `%APPDATA%\Cursor\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- **Linux**: `~/.config/Cursor/User/globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`

### Paso 2: Añadir configuración del servidor

Pega esta configuración en el archivo JSON:

```json
{
  "mcpServers": {
    "soporte-tecnico": {
      "command": "poetry",
      "args": [
        "run",
        "python",
        "src/mcp_server.py"
      ],
      "cwd": "/RUTA/ABSOLUTA/A/mcp_henry_masterclass",
      "env": {}
    }
  }
}
```

**⚠️ IMPORTANTE**: Reemplaza `/RUTA/ABSOLUTA/A/mcp_henry_masterclass` con la ruta real de este proyecto en tu máquina.

Para obtener la ruta absoluta:
```bash
# En la carpeta del proyecto, ejecuta:
pwd
```

### Paso 3: Reiniciar Cursor

1. Cierra completamente Cursor
2. Vuelve a abrirlo
3. Abre este proyecto en Cursor

### Paso 4: Verificar conexión

En el chat de Cursor, pregunta:

> "¿Qué herramientas MCP tienes disponibles?"

Deberías ver las herramientas del servidor de soporte técnico listadas.

---

## 🎯 Prompts Sugeridos para la Demostración

### Prompt 1: Exploración básica
```
¿Cuántos tickets de soporte tenemos en total? Dame un resumen por prioridad y estado.
```
**Objetivo**: Demostrar cómo la IA usa `obtener_estadisticas` para dar una vista general.

---

### Prompt 2: Filtrado específico
```
Muéstrame todos los tickets urgentes que están abiertos. ¿Cuáles deberíamos atender primero?
```
**Objetivo**: Ver cómo usa `consultar_tickets` con filtros y luego analiza los resultados.

---

### Prompt 3: Análisis de tendencias
```
¿Qué problemas técnicos son los más comunes según los tickets? Identifica los top 3 asuntos recurrentes.
```
**Objetivo**: Demostrar capacidades analíticas sobre datos reales sin tener que pasar todo el dataset.

---

### Prompt 4: Búsqueda contextual
```
Busca todos los tickets relacionados con "Error 500" o problemas de autenticación.
¿Hay algún patrón en los clientes afectados?
```
**Objetivo**: Mostrar `buscar_tickets_por_texto` y análisis cruzado.

---

### Prompt 5: Reporte ejecutivo
```
Genera un reporte ejecutivo para management sobre el estado del sistema de soporte.
Incluye métricas clave, problemas críticos y recomendaciones.
```
**Objetivo**: Capacidad de sintetizar datos de múltiples herramientas en un formato ejecutivo.

---

## 🏗️ Arquitectura del Proyecto

```
mcp_henry_masterclass/
├── src/
│   ├── mcp_server.py          # Servidor MCP con 3 herramientas
│   └── mcp_henry_masterclass/  # Paquete Python principal
├── scripts/
│   └── setup_db.py             # Generador de datos de prueba
├── docs/                       # Documentación adicional
├── soporte.db                  # Base de datos SQLite (generada)
├── pyproject.toml              # Configuración de Poetry
└── README.md                   # Este archivo
```

### Herramientas MCP disponibles

| Herramienta | Descripción | Cuándo usarla |
|-------------|-------------|---------------|
| `consultar_tickets` | Filtra tickets por prioridad/estado | Buscar casos específicos |
| `obtener_estadisticas` | Resúmenes agregados del sistema | Panorama general y métricas |
| `buscar_tickets_por_texto` | Búsqueda de texto libre | Encontrar problemas por palabra clave |

---

## 🧪 Testing Manual

Para probar el servidor directamente sin Cursor:

```bash
# Instalar cliente MCP inspector
npm install -g @modelcontextprotocol/inspector

# Inspeccionar el servidor
mcp-inspector poetry run python src/mcp_server.py
```

Esto abre una interfaz web donde puedes probar las herramientas manualmente.

---

## 📖 Recursos Adicionales

- [Documentación oficial de MCP](https://modelcontextprotocol.io/)
- [Repositorio de FastMCP](https://github.com/jlowin/fastmcp)
- [Ejemplos de servidores MCP](https://github.com/modelcontextprotocol/servers)
- [Cursor IDE Documentation](https://cursor.sh/docs)

---

## 🤝 Contribuciones

Este proyecto es material educativo para la Henry Masterclass. Si encuentras mejoras o bugs:

1. Fork el repositorio
2. Crea una rama con tu feature (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

---

## 📝 Licencia

MIT License - Siéntete libre de usar este código para aprendizaje y enseñanza.

---

## 🎓 Sobre Henry

[Henry](https://www.soyhenry.com/) es una escuela de tecnología líder en Latinoamérica, formando desarrolladores full-stack de clase mundial.

**¿Preguntas sobre el código?** Contáctanos en la clase o abre un issue en GitHub.

---

**Happy Coding! 🚀**
