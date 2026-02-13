"""Helpers para animaciones de clips en línea de tiempo.

Este módulo define una utilidad para crear/aplicar una entrada/salida por empuje
usando keyframes de recorte lateral.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Protocol


CUBIC_SPLINE = "cubic"


@dataclass(frozen=True)
class Keyframe:
    """Representa un keyframe para un parámetro animable."""

    frame: int
    value: float
    in_spline: str = CUBIC_SPLINE
    out_spline: str = CUBIC_SPLINE


class AnimatableClip(Protocol):
    """Interfaz mínima para aplicar keyframes a un clip."""

    def set_keyframe(
        self,
        parameter: str,
        frame: int,
        value: float,
        in_spline: str,
        out_spline: str,
    ) -> None:
        ...

    def set_value(self, parameter: str, value: float) -> None:
        ...


@dataclass(frozen=True)
class SidePushConfig:
    """Configuración de la animación de empuje lateral."""

    side_crop_pixels: int = 1920
    transition_frames: int = 12
    blur_amount: float = 0.2


def build_side_push_keyframes(
    clip_start_frame: int,
    clip_duration_frames: int,
    config: SidePushConfig | None = None,
) -> Dict[str, List[Keyframe]]:
    """Construye los keyframes para el efecto de entrada/salida por empuje.

    - En el primer frame del clip, `crop_left = 1920`.
    - En `frame 12` desde el inicio, `crop_left = 0`.
    - En los últimos 12 frames, `crop_right` anima `0 -> 1920`.
    - Todos los keyframes usan spline cúbico.
    """

    cfg = config or SidePushConfig()
    minimum_duration = cfg.transition_frames * 2
    if clip_duration_frames <= minimum_duration:
        raise ValueError(
            "La duración del clip debe ser mayor a 2 * transition_frames para evitar solapamiento de entradas/salidas."
        )

    start = clip_start_frame
    end = clip_start_frame + clip_duration_frames - 1

    crop_left = [
        Keyframe(frame=start, value=float(cfg.side_crop_pixels)),
        Keyframe(frame=start + cfg.transition_frames, value=0.0),
    ]

    crop_right = [
        Keyframe(frame=end - cfg.transition_frames, value=0.0),
        Keyframe(frame=end, value=float(cfg.side_crop_pixels)),
    ]

    blur = [Keyframe(frame=start, value=cfg.blur_amount)]

    return {
        "crop_left": crop_left,
        "crop_right": crop_right,
        "blur": blur,
    }


def apply_side_push_to_clip(
    clip: AnimatableClip,
    clip_start_frame: int,
    clip_duration_frames: int,
    config: SidePushConfig | None = None,
) -> Dict[str, List[Keyframe]]:
    """Aplica al clip los keyframes del efecto y retorna la data aplicada."""

    keyframes = build_side_push_keyframes(
        clip_start_frame=clip_start_frame,
        clip_duration_frames=clip_duration_frames,
        config=config,
    )

    for parameter, frames in keyframes.items():
        if parameter == "blur":
            clip.set_value(parameter, frames[0].value)

        for kf in frames:
            clip.set_keyframe(
                parameter=parameter,
                frame=kf.frame,
                value=kf.value,
                in_spline=kf.in_spline,
                out_spline=kf.out_spline,
            )

    return keyframes
