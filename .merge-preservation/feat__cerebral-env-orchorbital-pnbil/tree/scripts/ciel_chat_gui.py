#!/usr/bin/env python3
"""CIEL/Ω cerebral chat surface — no GGUF, no external text backend.

Run from the project root::

    python scripts/ciel_chat_gui.py

The interface talks to ``CerebralLanguageModel``.  The transcript is only a
transcript; semantic state is persisted separately by the cerebral model.
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path

import psutil
from nicegui import ui

from ciel_cerebral_model import CerebralLanguageModel


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL = CerebralLanguageModel(PROJECT_ROOT)
chat_history: list[dict[str, str]] = MODEL.policy.load_transcript(limit=24)


def get_system_resources() -> dict[str, float]:
    vm = psutil.virtual_memory()
    return {
        "ram_pct": float(vm.percent),
        "ram_used": round(vm.used / 1024**3, 1),
        "cpu_pct": float(psutil.cpu_percent(interval=None)),
    }


@ui.page("/")
def index() -> None:
    ui.query("body").style(
        "background: #0f0f1a; color: #e0e0f0; font-family: monospace"
    )

    with ui.column().classes("w-full max-w-5xl mx-auto p-4 gap-3"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column():
                ui.label("CIEL/Ω").style(
                    "font-size:2em; font-weight:bold; color:#7ec8e3"
                )
                ui.label(
                    "CIEL-Cerebral-NeuroSymbolic-v0.4 · lokalny model bez wag autoregresyjnych"
                ).style("color:#a8e6cf; font-size:0.85em")
            model_badge = ui.badge("Cerebral: READY", color="green")

        with ui.card().style(
            "background:#1a1a2e; border:1px solid #333; width:100%"
        ):
            with ui.row().classes("w-full gap-5 p-2 flex-wrap"):
                cycle_lbl = ui.label("Cycle: —").style("color:#7ec8e3")
                phase_lbl = ui.label("phase: —").style("color:#a8e6cf")
                coherence_lbl = ui.label("coherence: —").style("color:#ffd3b6")
                memory_lbl = ui.label("memory: —").style("color:#d7bde2")
                session_lbl = ui.label("session: —").style("color:#c5cae9")
                topic_lbl = ui.label("topic: —").style("color:#b2dfdb")
                ram_lbl = ui.label("RAM: —").style("color:#ffd3b6")
                cpu_lbl = ui.label("CPU: —").style("color:#ffaaa5")

        with ui.card().style(
            "background:#1a1a2e; border:1px solid #333; width:100%; height:520px"
        ):
            chat_scroll = ui.scroll_area().classes("w-full h-full")
            with chat_scroll:
                chat_col = ui.column().classes("w-full gap-2 p-2")

        with ui.row().classes("w-full gap-2"):
            msg_input = ui.input(placeholder="Napisz do CIEL...").classes("flex-1")
            msg_input.style(
                "background:#1a1a2e; color:#e0e0f0; border:1px solid #444"
            )
            send_btn = ui.button("Wyślij", color="blue")
            send_btn.style("background:#2d4a7a")
            new_session_btn = ui.button("Nowa sesja", color="grey")

        status_lbl = ui.label(
            "Warstwa cerebralna gotowa; odpowiedzi są lokalnymi wynikami/draftami."
        ).style("color:#888; font-size:0.8em")

    def add_message(role: str, text: str, color: str = "#e0e0f0") -> None:
        with chat_col:
            with ui.row().classes("w-full"):
                prefix = "Ty" if role == "user" else "CIEL"
                prefix_color = "#7ec8e3" if role == "user" else "#a8e6cf"
                ui.label(f"{prefix}:").style(
                    f"color:{prefix_color}; font-weight:bold; min-width:60px"
                )
                ui.label(text).style(
                    f"color:{color}; white-space:pre-wrap"
                ).classes("flex-1")
        chat_scroll.scroll_to(percent=1.0)

    for item in chat_history:
        add_message(item["role"], item["content"])
    if not chat_history:
        add_message(
            "assistant",
            MODEL.policy.postprocess(
                "[ARTEFAKT] Powierzchnia cerebralna działa bez GGUF: analizuje ramę językową, "
                "fazę, afekt, pamięć semantyczną i lokalny working context.",
                "",
            ),
            "#a8e6cf",
        )

    def reset_session() -> None:
        result = MODEL.new_session(reason="gui_user_requested")
        reply = MODEL.policy.postprocess(
            "[WYNIK] Utworzyłem nową lokalną sesję ciągłości. Transcript pozostaje archiwum, "
            "ale aktywny working context został wyzerowany.",
            "nowa sesja",
        )
        chat_history.append({"role": "assistant", "content": reply})
        MODEL.policy.record_chat("assistant", reply)
        add_message("assistant", reply, "#d7bde2")
        status_lbl.text = f"Nowa sesja: {result['session_id']}"

    new_session_btn.on("click", reset_session)

    async def send() -> None:
        text = (msg_input.value or "").strip()
        if not text:
            return
        msg_input.value = ""
        send_btn.disable()
        add_message("user", text)
        chat_history.append({"role": "user", "content": text})
        MODEL.policy.record_chat("user", text)
        status_lbl.text = "Cerebral cycle: percepcja → znaczenie → pamięć → odpowiedź..."

        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(None, MODEL.process, text)
            reply = str(result.get("reply", "[NIE WIEM] Brak odpowiedzi."))
            chat_history.append({"role": "assistant", "content": reply})
            MODEL.policy.record_chat("assistant", reply)
            add_message("assistant", reply, "#a8e6cf")
        except Exception as exc:  # keep the chat visible even if a module breaks
            reply = MODEL.policy.postprocess(
                "[NIE WIEM] Cerebralny cykl zatrzymał się na granicy modułu. "
                f"Nie oznaczam tego jako PASS: {type(exc).__name__}.",
                text,
            )
            chat_history.append({"role": "assistant", "content": reply})
            MODEL.policy.record_chat("assistant", reply)
            add_message("assistant", reply, "#ffaaa5")
        continuity = MODEL.status()["continuity"]
        status_lbl.text = (
            "Warstwa cerebralna gotowa · "
            f"sesja turn {continuity['turn_index']}"
        )
        send_btn.enable()

    send_btn.on("click", send)
    msg_input.on("keydown.enter", send)

    def update_metrics() -> None:
        state = MODEL.status()
        continuity = state["continuity"]
        resources = get_system_resources()
        cycle_lbl.text = f"Cycle: {state['cycle']}"
        phase_lbl.text = f"phase: {state['phase']:.3f}"
        coherence_lbl.text = f"coherence: {state['coherence']:.3f}"
        memory_lbl.text = f"memory: {state['memory_records']} semantic"
        session_lbl.text = f"session: {str(continuity['session_id'])[:18]}"
        topic = ", ".join(continuity.get("active_topic", [])[:3]) or "—"
        topic_lbl.text = f"topic: {topic}"
        ram_lbl.text = f"RAM: {resources['ram_used']}GB ({resources['ram_pct']:.0f}%)"
        cpu_lbl.text = f"CPU: {resources['cpu_pct']:.0f}%"
        model_badge.text = "Cerebral: READY"
        model_badge.props("color=green")

    ui.timer(3.0, update_metrics)


ui.run(
    title="CIEL/Ω Cerebral",
    host=os.environ.get("CIEL_HOST", "127.0.0.1"),
    port=int(os.environ.get("CIEL_PORT", "8080")),
    reload=False,
    favicon=str(PROJECT_ROOT / "src/ciel-omega-demo-main/main/Logo1.png"),
    dark=True,
)
