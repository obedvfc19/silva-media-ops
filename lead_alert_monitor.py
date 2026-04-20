"""
lead_alert_monitor.py
Proyecto #1 — Silva Media Demo

Detecta leads inactivos y críticos en GoHighLevel.
En producción se conecta a la API real de GHL.
Para el demo usa datos sintéticos de silva_media_data.py
"""

import json
from datetime import datetime
from silva_media_data import LEADS, NOW

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS = True
except ImportError:
    COLORS = False

def rojo(t):    return (Fore.RED    + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def amarillo(t):return (Fore.YELLOW + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def verde(t):   return (Fore.GREEN  + Style.BRIGHT + t + Style.RESET_ALL) if COLORS else t
def cyan(t):    return (Fore.CYAN   +                t + Style.RESET_ALL) if COLORS else t
def gris(t):    return (Style.DIM   +                t + Style.RESET_ALL) if COLORS else t

UMBRAL_INACTIVO_H = 48
UMBRAL_CRITICO_H  = 72

def clasificar(lead):
    horas = (NOW - lead["ultimo_contacto"]).total_seconds() / 3600
    if horas >= UMBRAL_CRITICO_H:
        return "CRÍTICO", horas
    elif horas >= UMBRAL_INACTIVO_H:
        return "INACTIVO", horas
    return "ACTIVO", horas

def main():
    linea = "═" * 62
    print()
    print(cyan(linea))
    print(cyan("  🏠  SILVA MEDIA — LEAD ALERT MONITOR"))
    print(cyan(f"  🕐  {NOW.strftime('%Y-%m-%d  %H:%M:%S')}"))
    print(cyan(linea))
    print()
    print(cyan("  📡  Escaneando leads en GoHighLevel..."))
    print(gris("  (Producción: GHL API  ·  Demo: datos sintéticos)\n"))

    # Clasificar
    resultados = [{"lead": l, **dict(zip(["estado","horas"], clasificar(l)))} for l in LEADS]

    # Tabla
    print(f"  {'LEAD':<22} {'AGENTE':<14} {'ESTADO':<10} {'HORAS':<8} STAGE")
    print("  " + "─" * 60)
    for r in resultados:
        n = r["lead"]["nombre"][:21]
        a = r["lead"]["agente"][:13]
        s = r["lead"]["pipeline_stage"]
        h = f"{r['horas']:.0f}h"
        e = r["estado"]
        color = rojo if e == "CRÍTICO" else (amarillo if e == "INACTIVO" else verde)
        print(f"  {n:<22} {a:<14} {color(f'{e:<10}')} {h:<8} {s}")
    print()

    # Resumen
    criticos  = [r for r in resultados if r["estado"] == "CRÍTICO"]
    inactivos = [r for r in resultados if r["estado"] == "INACTIVO"]
    activos   = [r for r in resultados if r["estado"] == "ACTIVO"]
    print(cyan("  RESUMEN"))
    print("  " + "─" * 40)
    print(f"  {rojo('🔴 CRÍTICOS  (72h+)')}  →  {len(criticos)} leads")
    print(f"  {amarillo('🟡 INACTIVOS (48h+)')}  →  {len(inactivos)} leads")
    print(f"  {verde('🟢 ACTIVOS        ')}  →  {len(activos)} leads")
    print()

    # Payload Zapier
    alertas = criticos + inactivos
    if alertas:
        payload = {
            "source": "silva_media_lead_monitor",
            "timestamp": NOW.isoformat(),
            "total_alertas": len(alertas),
            "leads": [{
                "nombre":              r["lead"]["nombre"],
                "agente":              r["lead"]["agente"],
                "estado":              r["estado"],
                "horas_sin_contacto":  round(r["horas"]),
                "pipeline_stage":      r["lead"]["pipeline_stage"],
            } for r in alertas],
            "acciones": {
                "clickup": "Crear tarea urgente por cada lead",
                "slack":   "Notificar al agente responsable",
                "ghl":     "Mover a stage 'Requiere Atención'",
            }
        }
        print(cyan("  📤  PAYLOAD → ZAPIER WEBHOOK"))
        print("  " + "─" * 60)
        for linea_json in json.dumps(payload, indent=4, ensure_ascii=False).split("\n"):
            print("  " + linea_json)
        print()
        print(cyan("  ⚡  ZAPIER EJECUTARÍA:"))
        print("  " + "─" * 40)
        print("     1. Crear tarea en ClickUp por cada lead crítico")
        print("     2. Enviar Slack alert al agente responsable")
        print("     3. Actualizar stage en GoHighLevel")
        print()
        print(verde("  ✅  Ciclo completado. Próximo scan en 4 horas."))
    else:
        print(verde("  ✅  Todos los leads activos. Sin alertas."))

    print(cyan("═" * 62))
    print()

if __name__ == "__main__":
    main()
