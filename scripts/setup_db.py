"""
Script para configurar la base de datos de demostración de soporte técnico.
Genera una BD SQLite con tickets realistas para la Masterclass de MCP.
"""
import sqlite3
import random
from datetime import datetime, timedelta
from pathlib import Path


# Configuración de datos realistas
CLIENTES = [
    "TechCorp S.A.", "Innovatech", "Digital Solutions Ltd.", "CloudBase Inc.",
    "DataStream Corp", "SoftWarehouse", "AppDev Studios", "WebMaster Co.",
    "Cyber Systems", "NetWork Solutions", "InfoTech Group", "CodeFactory",
    "SmartBiz Ltd.", "Enterprise Solutions", "Global Tech", "FastServe Inc.",
    "ApiFirst Corp", "MicroServices S.A.", "DevOps Central", "CloudNative",
    "SecureNet", "DataVision", "TechHub", "InnovateSoft", "SystemCore"
]

ASUNTOS_TECNICOS = [
    "Error 500 en endpoint de pagos",
    "Fallo en autenticación OAuth2",
    "Timeout en conexión a base de datos",
    "Error de memoria en servidor de aplicaciones",
    "Certificado SSL expirado",
    "API Gateway retornando 503",
    "Fallo en sincronización de caché Redis",
    "Error de permisos en bucket S3",
    "Lentitud en queries de PostgreSQL",
    "Webhook no recibiendo eventos",
    "Error de CORS en frontend",
    "Fallo en proceso de deployment",
    "Inconsistencia en datos de usuarios",
    "Error 404 en recursos estáticos",
    "Problema de rate limiting en API",
    "Fallo en job de cron nocturno",
    "Error de validación en formulario de registro",
    "Problema con cola de mensajes RabbitMQ",
    "Sesiones de usuario expirando prematuramente",
    "Error al procesar archivos CSV grandes",
    "Fallo en integración con pasarela de pago",
    "Problema de encodificación UTF-8",
    "Error en pipeline CI/CD",
    "Logs no apareciendo en CloudWatch",
    "Problema de concurrencia en transacciones",
    "Error en migración de base de datos",
    "Fallo en backup automático",
    "Problema de conectividad VPN",
    "Error en generación de reportes PDF",
    "Fallo en servicio de notificaciones push"
]

ESTADOS = ["abierto", "cerrado"]
PRIORIDADES = ["baja", "media", "alta", "urgente"]


def create_database(db_path: Path):
    """Crea la base de datos y la tabla de tickets."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Crear tabla tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT NOT NULL,
            asunto TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT NOT NULL,
            prioridad TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL,
            fecha_actualizacion TEXT NOT NULL
        )
    """)

    conn.commit()
    return conn


def generate_tickets(conn, num_tickets: int = 50):
    """Genera tickets realistas en la base de datos."""
    cursor = conn.cursor()

    # Calcular fechas para la última semana
    hoy = datetime.now()
    hace_una_semana = hoy - timedelta(days=7)
    
    # Generar primero 5 tickets urgentes de hoy
    print("  Generando 5 tickets urgentes de hoy...")
    for i in range(5):
        cliente = random.choice(CLIENTES)
        asunto = random.choice(ASUNTOS_TECNICOS)
        prioridad = "urgente"
        estado = "abierto"  # Tickets urgentes de hoy están abiertos
        
        # Fecha de creación: hoy con hora aleatoria
        fecha_creacion = hoy.replace(
            hour=random.randint(0, 23),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
        
        descripcion = f"URGENTE: {asunto}. Cliente reporta impacto crítico en producción. Requiere atención inmediata."
        
        # Actualización reciente (1-3 horas después de creación)
        fecha_actualizacion = fecha_creacion + timedelta(
            hours=random.randint(1, 3)
        )
        
        cursor.execute("""
            INSERT INTO tickets
            (cliente, asunto, descripcion, estado, prioridad, fecha_creacion, fecha_actualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente,
            asunto,
            descripcion,
            estado,
            prioridad,
            fecha_creacion.isoformat(),
            fecha_actualizacion.isoformat()
        ))
    
    # Generar el resto de tickets de la última semana
    print(f"  Generando {num_tickets - 5} tickets de la última semana...")
    for i in range(num_tickets - 5):
        cliente = random.choice(CLIENTES)
        asunto = random.choice(ASUNTOS_TECNICOS)
        prioridad = random.choices(
            PRIORIDADES,
            weights=[30, 40, 20, 10]  # Más tickets de baja/media prioridad
        )[0]

        # Fecha de creación aleatoria en la última semana (0-7 días atrás)
        dias_atras = random.uniform(0, 7)
        fecha_creacion = hoy - timedelta(days=dias_atras)
        dias_desde_creacion = (hoy - fecha_creacion).days

        # El estado depende de la antigüedad y prioridad (ajustado para última semana)
        if prioridad in ["urgente", "alta"]:
            estado = "cerrado" if dias_desde_creacion > 2 else "abierto"
        elif prioridad == "media":
            estado = "cerrado" if dias_desde_creacion > 5 else random.choice(ESTADOS)
        else:  # baja
            estado = random.choice(ESTADOS)

        # Generar descripción contextual
        descripciones = {
            "urgente": f"URGENTE: {asunto}. Cliente reporta impacto crítico en producción. Requiere atención inmediata.",
            "alta": f"Prioridad Alta: {asunto}. Afectando a múltiples usuarios. Necesita resolución pronto.",
            "media": f"{asunto}. Cliente solicita revisión. Impacto moderado en operaciones.",
            "baja": f"{asunto}. Consulta de cliente. Sin impacto crítico en servicio."
        }
        descripcion = descripciones[prioridad]

        # Actualización dentro de un rango razonable
        max_horas = min(int(dias_desde_creacion * 24), 72)
        fecha_actualizacion = fecha_creacion + timedelta(
            hours=random.randint(1, max(1, max_horas))
        )

        cursor.execute("""
            INSERT INTO tickets
            (cliente, asunto, descripcion, estado, prioridad, fecha_creacion, fecha_actualizacion)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente,
            asunto,
            descripcion,
            estado,
            prioridad,
            fecha_creacion.isoformat(),
            fecha_actualizacion.isoformat()
        ))

    conn.commit()


def main():
    """Función principal para configurar la base de datos."""
    # Ruta a la base de datos en la raíz del proyecto
    project_root = Path(__file__).parent.parent
    db_path = project_root / "soporte.db"

    # Eliminar BD existente si hay una
    if db_path.exists():
        print(f"⚠️  Eliminando base de datos existente: {db_path}")
        db_path.unlink()

    print(f"🔧 Creando nueva base de datos: {db_path}")
    conn = create_database(db_path)

    print("📊 Generando 60 tickets de soporte de la última semana...")
    generate_tickets(conn, num_tickets=60)

    # Verificar datos
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT prioridad, COUNT(*) FROM tickets GROUP BY prioridad")
    stats_prioridad = cursor.fetchall()

    cursor.execute("SELECT estado, COUNT(*) FROM tickets GROUP BY estado")
    stats_estado = cursor.fetchall()
    
    # Verificar tickets urgentes de hoy
    hoy = datetime.now().date().isoformat()
    cursor.execute("""
        SELECT COUNT(*) FROM tickets 
        WHERE prioridad = 'urgente' 
        AND DATE(fecha_creacion) = ?
    """, (hoy,))
    urgentes_hoy = cursor.fetchone()[0]

    conn.close()

    print(f"\n✅ Base de datos creada exitosamente!")
    print(f"   Total de tickets: {total}")
    print(f"   🔥 Tickets urgentes de hoy: {urgentes_hoy}")
    print(f"\n   Distribución por prioridad:")
    for prioridad, count in stats_prioridad:
        print(f"     - {prioridad}: {count}")
    print(f"\n   Distribución por estado:")
    for estado, count in stats_estado:
        print(f"     - {estado}: {count}")
    print(f"\n🎯 Todos los tickets son de la última semana. Listo para la Masterclass!\n")


if __name__ == "__main__":
    main()
