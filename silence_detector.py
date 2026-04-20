"""
silence_detector.py
Proyecto #2 — Silva Media Demo

Monitorea si Assistable "Mia" está respondiendo leads.
Si no hay actividad en 30 minutos → alerta inmediata.
En producción se conecta al webhook de Assistable/GHL.
"""

import json
import time
from datetime import datetime
from silva_media_data import MIA_ACTIVITY_LOG, MIA_LAST_RESPONSE, NOW

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False

def rojo(t):    return (Fore.RED    + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def verde(t):   return (Fore.GREEN  + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def cyan(t):    return (Fore.CYAN   +                t + Style.RESET_ALL) if COLORS else t
def amarillo(t):return (Fore.YELLOW + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def gris(t):    return (Style.DIM   +                t + Style.RESET_ALL) if COLORS else t

UMBRAL_SILENCIO_MIN = 30  # minutos sin actividad = alerta

def calcular_minutos_silencio():
    return (NOW - MIA_LAST_RESPONSE).total_seconds() / 60

def imprimir_actividad_reciente():
    print(cyan("  📋  ACTIVIDAD RECIENTE DE MIA"))
    print("  " + "─" * 50)
    for entrada in MIA_ACTIVITY_LOG:
        mins = (NOW - entrada["timestamp"]).total_seconds() / 60
        print(f"  {gris(f'hace {mins:.0f} min')}  →  Lead {entrada['lead_id']}  ·  {entrada['mensaje'][:40]}...")
    print()

def imprimir_check(numero, minutos_silencio, es_alerta):
    estado = rojo("🚨 SILENCIO DETECTADO") if es_alerta else verde("✅ MIA ACTIVA")
    print(f"  CHECK #{numero}  —  {estado}")
    print(f"  {gris(f'Última respuesta: hace {minutos_silencio:.0f} minutos')}")
    if not es_alerta:
        print(f"  {gris(f'Umbral: {UMBRAL_SILENCIO_MIN} min  ·  Estado: dentro del límite')}")
    print()

def generar_alerta(minutos_silencio):
    print()
    print(rojo("  ╔══════════════════════════════════════════════════╗"))
    print(rojo("  ║   🚨  ALERTA CRÍTICA — ASSISTABLE MIA OFFLINE   ║"))
    print(rojo("  ╚══════════════════════════════════════════════════╝"))
    print()
    print(f"  {rojo(f'Mia lleva {minutos_silencio:.0f} minutos sin responder ningún lead.')}")
    print(f"  {amarillo('Leads activos en pipeline: sin atención automática.')}")
    print()

    payload = {
        "alerta": "ASSISTABLE_SILENCE",
        "timestamp": NOW.isoformat(),
        "minutos_sin_actividad": round(minutos_silencio),
        "ultima_actividad": MIA_LAST_RESPONSE.isoformat(),
        "acciones": {
            "slack": {
                "canal": "#ops-alerts",
                "mensaje": f"🚨 Mia lleva {round(minutos_silencio)} min offline. Revisión inmediata requerida."
            },
            "clickup": {
                "lista": "Bot Alerts",
                "tarea": "URGENTE: Assistable Mia sin respuesta",
                "prioridad": "URGENTE",
                "asignado": "Oz"
            },
            "ghl": {
                "accion": "Pausar secuencias automáticas hasta restaurar Mia"
            }
        }
    }

    print(cyan("  📤  PAYLOAD → ZAPIER WEBHOOK"))
    print("  " + "─" * 55)
    for linea in json.dumps(payload, indent=4, ensure_ascii=False).split("\n"):
        print("  " + linea)
    print()

    print(cyan("  ⚡  ACCIONES INMEDIATAS:"))
    print("  " + "─" * 40)
    print(f"  {verde('1.')} Slack alert → #ops-alerts  (en segundos)")
    print(f"  {verde('2.')} Tarea urgente creada en ClickUp → asignada a Oz")
    print(f"  {verde('3.')} Secuencias GHL pausadas hasta restaurar Mia")
    print()
    print(amarillo("  ⏱  Tiempo de respuesta humana esperado: < 5 min"))
    print(amarillo("  📉  Sin este detector: el silencio podría durar horas."))
    print()

def main():
    print()
    print(cyan("═" * 62))
    print(cyan("  🤖  SILVA MEDIA — SILENCE DETECTOR"))
    print(cyan(f"  🕐  {NOW.strftime('%Y-%m-%d  %H:%M:%S')}"))
    print(cyan("  📡  Monitoreando Assistable Mia cada 30 minutos"))
    print(cyan("═" * 62))
    print()
    print(gris("  (Producción: webhook Assistable/GHL  ·  Demo: datos sintéticos)\n"))

    imprimir_actividad_reciente()

    # Simulamos 3 checks con pausa visual
    minutos = calcular_minutos_silencio()

    # Check 1 — Mia activa (simulamos como si fuera 10 min atrás)
    print(cyan("  ── Ejecutando checks de monitoreo ──\n"))
    imprimir_check(1, minutos - 31, es_alerta=False)
    time.sleep(1)

    # Check 2 — Mia activa (simulamos como si fuera 5 min atrás)
    imprimir_check(2, minutos - 15, es_alerta=False)
    time.sleep(1)

    # Check 3 — ALERTA (tiempo real actual)
    imprimir_check(3, minutos, es_alerta=(minutos >= UMBRAL_SILENCIO_MIN))

    if minutos >= UMBRAL_SILENCIO_MIN:
        generar_alerta(minutos)
    else:
        print(verde("  ✅  Sistema dentro de parámetros normales."))

    print(cyan("═" * 62))
    print()

if __name__ == "__main__":
    main()
