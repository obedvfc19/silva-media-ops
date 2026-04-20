"""
silva_media_data.py
Base de datos sintética de Silva Media.
Usada por los 3 proyectos del demo.
"""

from datetime import datetime, timedelta

# Hora actual de referencia
NOW = datetime.now()

# ─────────────────────────────────────────
# LEADS SINTÉTICOS  (simulan contactos GHL)
# ─────────────────────────────────────────
LEADS = [
    {
        "id": "lead_001",
        "nombre": "Juan García",
        "telefono": "+52 55 1234 5678",
        "agente": "Carlos Vega",
        "pipeline_stage": "Calificando",
        "ultimo_contacto": NOW - timedelta(hours=130),   # CRÍTICO
        "fuente": "Facebook Ad",
        "interes": "Comprar",
        "presupuesto": "$250,000 USD",
    },
    {
        "id": "lead_002",
        "nombre": "María López",
        "telefono": "+52 55 2345 6789",
        "agente": "Sofía Reyes",
        "pipeline_stage": "Nuevo",
        "ultimo_contacto": NOW - timedelta(hours=75),    # CRÍTICO
        "fuente": "Referido",
        "interes": "Vender",
        "presupuesto": "N/A",
    },
    {
        "id": "lead_003",
        "nombre": "Carlos Rodríguez",
        "telefono": "+52 55 3456 7890",
        "agente": "Luis Mora",
        "pipeline_stage": "Seguimiento",
        "ultimo_contacto": NOW - timedelta(hours=52),    # INACTIVO
        "fuente": "Google Ad",
        "interes": "Comprar",
        "presupuesto": "$180,000 USD",
    },
    {
        "id": "lead_004",
        "nombre": "Ana Martínez",
        "telefono": "+52 55 4567 8901",
        "agente": "Carlos Vega",
        "pipeline_stage": "Demo Agendada",
        "ultimo_contacto": NOW - timedelta(hours=30),    # INACTIVO
        "fuente": "Instagram Ad",
        "interes": "Comprar",
        "presupuesto": "$320,000 USD",
    },
    {
        "id": "lead_005",
        "nombre": "Roberto Sánchez",
        "telefono": "+52 55 5678 9012",
        "agente": "Sofía Reyes",
        "pipeline_stage": "Calificando",
        "ultimo_contacto": NOW - timedelta(hours=8),     # ACTIVO
        "fuente": "Referido",
        "interes": "Comprar",
        "presupuesto": "$400,000 USD",
    },
    {
        "id": "lead_006",
        "nombre": "Laura Herrera",
        "telefono": "+52 55 6789 0123",
        "agente": "Luis Mora",
        "pipeline_stage": "Nuevo",
        "ultimo_contacto": NOW - timedelta(hours=3),     # ACTIVO
        "fuente": "Facebook Ad",
        "interes": "Vender",
        "presupuesto": "N/A",
    },
]

# ─────────────────────────────────────────
# HISTORIAL DE ACTIVIDAD DE ASSISTABLE MIA
# ─────────────────────────────────────────
MIA_ACTIVITY_LOG = [
    {"timestamp": NOW - timedelta(minutes=48), "lead_id": "lead_005", "mensaje": "Hola Roberto, soy Mia de Silva Media..."},
    {"timestamp": NOW - timedelta(minutes=44), "lead_id": "lead_006", "mensaje": "Hola Laura, gracias por tu interés..."},
    {"timestamp": NOW - timedelta(minutes=41), "lead_id": "lead_003", "mensaje": "Carlos, te contactamos para agendar..."},
    # — Después de este punto Mia dejó de responder —
]

# Última vez que Mia respondió algo
MIA_LAST_RESPONSE = MIA_ACTIVITY_LOG[-1]["timestamp"]

# ─────────────────────────────────────────
# AGENTES ACTIVOS
# ─────────────────────────────────────────
AGENTES = [
    {"nombre": "Carlos Vega",  "leads_activos": 18, "closings_mes": 2},
    {"nombre": "Sofía Reyes",  "leads_activos": 24, "closings_mes": 3},
    {"nombre": "Luis Mora",    "leads_activos": 15, "closings_mes": 1},
]
