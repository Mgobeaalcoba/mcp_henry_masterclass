"""
Servidor MCP para Sistema de Soporte Técnico
=============================================

Este servidor MCP (Model Context Protocol) proporciona herramientas para
que un LLM pueda consultar y analizar tickets de soporte técnico de manera
eficiente y contextual.

Diseñado para demostrar cómo MCP permite que las IAs accedan a datos
empresariales de forma estructurada y semántica.
"""
import sqlite3
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP

# Inicializar el servidor MCP
mcp = FastMCP("Sistema de Soporte Técnico")

# Ruta a la base de datos
DB_PATH = Path(__file__).parent.parent / "soporte.db"


def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Base de datos no encontrada en {DB_PATH}. "
            "Ejecuta 'poetry run python scripts/setup_db.py' primero."
        )
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def consultar_tickets(
    prioridad: Optional[str] = None,
    estado: Optional[str] = None,
    limite: int = 20
) -> list[dict]:
    """
    Consulta tickets de soporte técnico con filtros opcionales.

    Esta herramienta permite buscar tickets específicos según criterios
    de filtrado. Úsala cuando necesites revisar tickets individuales,
    buscar problemas específicos, o analizar casos particulares.

    Args:
        prioridad: Filtra por prioridad. Valores: "baja", "media", "alta", "urgente"
        estado: Filtra por estado. Valores: "abierto", "cerrado"
        limite: Número máximo de tickets a retornar (default: 20, max: 100)

    Returns:
        Lista de tickets con todos sus detalles (id, cliente, asunto,
        descripción, estado, prioridad, fechas)

    Ejemplos de uso:
        - "Muéstrame los tickets urgentes abiertos"
        - "¿Qué problemas de alta prioridad tiene TechCorp?"
        - "Lista los últimos 10 tickets cerrados"
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Construir query dinámica según filtros
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []

    if prioridad:
        prioridad = prioridad.lower()
        if prioridad not in ["baja", "media", "alta", "urgente"]:
            conn.close()
            raise ValueError(
                f"Prioridad inválida: {prioridad}. "
                "Usa: baja, media, alta, urgente"
            )
        query += " AND prioridad = ?"
        params.append(prioridad)

    if estado:
        estado = estado.lower()
        if estado not in ["abierto", "cerrado"]:
            conn.close()
            raise ValueError(
                f"Estado inválido: {estado}. "
                "Usa: abierto, cerrado"
            )
        query += " AND estado = ?"
        params.append(estado)

    # Limitar resultados (seguridad)
    limite = min(max(1, limite), 100)
    query += " ORDER BY fecha_creacion DESC LIMIT ?"
    params.append(limite)

    cursor.execute(query, params)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    tickets = []
    for row in rows:
        ticket = dict(zip(columns, row))
        tickets.append(ticket)

    conn.close()

    return tickets


@mcp.tool()
def obtener_estadisticas(agrupar_por: str = "estado") -> dict:
    """
    Obtiene estadísticas agregadas del sistema de soporte.

    Esta herramienta proporciona resúmenes y métricas de alto nivel sobre
    todos los tickets. Úsala cuando necesites entender el panorama general,
    identificar tendencias, o responder preguntas sobre volúmenes y distribución.

    Args:
        agrupar_por: Criterio de agrupación. Valores: "estado", "prioridad", "cliente"

    Returns:
        Diccionario con estadísticas completas incluyendo:
        - total_tickets: Número total de tickets en el sistema
        - distribucion: Conteo agrupado según el criterio especificado
        - metricas_adicionales: Estadísticas complementarias

    Ejemplos de uso:
        - "¿Cuántos tickets tenemos en total?"
        - "Dame un resumen de tickets por prioridad"
        - "¿Qué clientes tienen más tickets abiertos?"
        - "Muéstrame las estadísticas generales del sistema"
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    agrupar_por = agrupar_por.lower()
    if agrupar_por not in ["estado", "prioridad", "cliente"]:
        conn.close()
        raise ValueError(
            f"Criterio inválido: {agrupar_por}. "
            "Usa: estado, prioridad, cliente"
        )

    # Total de tickets
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total_tickets = cursor.fetchone()[0]

    # Distribución según agrupación solicitada
    cursor.execute(
        f"SELECT {agrupar_por}, COUNT(*) as cantidad "
        f"FROM tickets GROUP BY {agrupar_por} ORDER BY cantidad DESC"
    )
    distribucion = {}
    for row in cursor.fetchall():
        distribucion[row[0]] = row[1]

    # Métricas adicionales útiles
    cursor.execute("SELECT COUNT(*) FROM tickets WHERE estado = 'abierto'")
    tickets_abiertos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE prioridad = 'urgente'")
    tickets_urgentes = cursor.fetchone()[0]

    cursor.execute(
        "SELECT cliente, COUNT(*) as cantidad FROM tickets "
        "GROUP BY cliente ORDER BY cantidad DESC LIMIT 5"
    )
    top_clientes = [
        {"cliente": row[0], "tickets": row[1]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return {
        "total_tickets": total_tickets,
        "distribucion": distribucion,
        "metricas_adicionales": {
            "tickets_abiertos": tickets_abiertos,
            "tickets_urgentes": tickets_urgentes,
            "top_5_clientes": top_clientes
        }
    }


@mcp.tool()
def buscar_tickets_por_texto(
    busqueda: str,
    campo: str = "asunto",
    limite: int = 20
) -> list[dict]:
    """
    Busca tickets que contengan un texto específico.

    Herramienta especializada para búsquedas de texto libre dentro de
    los tickets. Útil para encontrar problemas específicos, errores
    recurrentes, o menciones de tecnologías particulares.

    Args:
        busqueda: Texto a buscar (case-insensitive)
        campo: Campo donde buscar. Valores: "asunto", "descripcion", "ambos"
        limite: Número máximo de resultados (default: 20, max: 100)

    Returns:
        Lista de tickets que coinciden con la búsqueda

    Ejemplos de uso:
        - "Busca todos los tickets relacionados con 'Error 500'"
        - "¿Hay tickets sobre problemas de 'autenticación'?"
        - "Muéstrame menciones de 'PostgreSQL' en las descripciones"
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    campo = campo.lower()
    if campo not in ["asunto", "descripcion", "ambos"]:
        conn.close()
        raise ValueError(
            f"Campo inválido: {campo}. "
            "Usa: asunto, descripcion, ambos"
        )

    # Construir query según campo
    if campo == "ambos":
        query = """
            SELECT * FROM tickets
            WHERE asunto LIKE ? OR descripcion LIKE ?
            ORDER BY fecha_creacion DESC
            LIMIT ?
        """
        pattern = f"%{busqueda}%"
        params = [pattern, pattern, min(max(1, limite), 100)]
    else:
        query = f"""
            SELECT * FROM tickets
            WHERE {campo} LIKE ?
            ORDER BY fecha_creacion DESC
            LIMIT ?
        """
        params = [f"%{busqueda}%", min(max(1, limite), 100)]

    cursor.execute(query, params)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()

    tickets = []
    for row in rows:
        ticket = dict(zip(columns, row))
        tickets.append(ticket)

    conn.close()

    return tickets


if __name__ == "__main__":
    # Ejecutar el servidor MCP
    mcp.run()
