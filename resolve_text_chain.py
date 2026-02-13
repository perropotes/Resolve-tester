#!/usr/bin/env python3
"""DaVinci Resolve script: cascade selected Text+ clips and extend all to the same end frame.

Workflow:
1. Select a group of connected Text+ clips in the Edit page.
2. Run this script from Resolve's script menu (or external Python with Resolve env set).
3. The script moves each selected clip to consecutive video tracks and extends every clip
   so they all end at the last selected clip's end frame.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class ClipInfo:
    item: object
    name: str
    start: int
    end: int
    track_index: int


class ResolveScriptError(RuntimeError):
    pass


def _import_resolve_module():
    try:
        import DaVinciResolveScript as dvr  # type: ignore
    except ImportError as exc:  # pragma: no cover - depends on Resolve environment
        raise ResolveScriptError(
            "Could not import DaVinciResolveScript. Run inside Resolve, or configure "
            "PYTHONPATH/RESOLVE_SCRIPT_API as described in README.md."
        ) from exc
    return dvr


def _selected_items(timeline: object) -> Sequence[object]:
    getter = getattr(timeline, "GetSelectedItems", None)
    if getter is None:
        raise ResolveScriptError(
            "Your Resolve version does not expose Timeline.GetSelectedItems(). "
            "Update Resolve (18.5+) to use selection-based automation."
        )

    raw = getter()
    if isinstance(raw, dict):
        return list(raw.values())
    if isinstance(raw, list):
        return raw
    return []


def _is_text_plus(item: object) -> bool:
    media_pool_item = getattr(item, "GetMediaPoolItem", lambda: None)()
    if media_pool_item is not None:
        props = media_pool_item.GetClipProperty()
        if isinstance(props, dict):
            clip_type = str(props.get("Type", "")).lower()
            clip_name = str(props.get("Clip Name", "")).lower()
            if "fusion title" in clip_type or "text+" in clip_name:
                return True

    # Fallback heuristic: Text+ is usually a fusion-enabled timeline item.
    get_comp_count = getattr(item, "GetFusionCompCount", None)
    if callable(get_comp_count):
        try:
            return int(get_comp_count() or 0) > 0
        except Exception:
            return False

    return False


def _item_track_index(item: object) -> int:
    getter = getattr(item, "GetTrackIndex", None)
    if not callable(getter):
        raise ResolveScriptError("Timeline item does not expose GetTrackIndex() in this Resolve build.")
    return int(getter())


def _clip_infos(items: Iterable[object], text_only: bool) -> List[ClipInfo]:
    clips: List[ClipInfo] = []
    for item in items:
        if text_only and not _is_text_plus(item):
            continue

        name = str(getattr(item, "GetName", lambda: "<unnamed>")())
        start = int(getattr(item, "GetStart")())
        end = int(getattr(item, "GetEnd")())
        track_index = _item_track_index(item)
        clips.append(ClipInfo(item=item, name=name, start=start, end=end, track_index=track_index))

    clips.sort(key=lambda c: (c.start, c.track_index, c.end, c.name))
    return clips


def _move_clip_to_track(item: object, track_index: int) -> None:
    setter = getattr(item, "SetTrackIndex", None)
    if not callable(setter):
        raise ResolveScriptError(
            "TimelineItem.SetTrackIndex() is not available in this Resolve build. "
            "Track spreading cannot be done by script in this version."
        )
    ok = bool(setter(track_index))
    if not ok:
        raise ResolveScriptError(f"Could not move clip to V{track_index}.")


def _set_clip_end(item: object, end_frame: int) -> None:
    set_property = getattr(item, "SetProperty", None)
    if not callable(set_property):
        raise ResolveScriptError("Timeline item has no SetProperty(); cannot change clip duration.")

    # Resolve accepts numeric frame values for many timeline-item properties.
    ok = bool(set_property("End", int(end_frame)))
    if not ok:
        raise ResolveScriptError(
            "Could not set clip end frame via SetProperty('End', ...). "
            "Check timeline lock state and ensure clip has enough source media handles."
        )


def run(spread_tracks: bool, text_only: bool, dry_run: bool) -> int:
    dvr = _import_resolve_module()
    resolve = dvr.scriptapp("Resolve")
    if resolve is None:
        raise ResolveScriptError("Could not connect to DaVinci Resolve.")

    project = resolve.GetProjectManager().GetCurrentProject()
    if project is None:
        raise ResolveScriptError("No active Resolve project.")

    timeline = project.GetCurrentTimeline()
    if timeline is None:
        raise ResolveScriptError("No active timeline.")

    items = _selected_items(timeline)
    if not items:
        raise ResolveScriptError("No timeline items selected.")

    clips = _clip_infos(items, text_only=text_only)
    if not clips:
        raise ResolveScriptError("No matching clips in selection (Text+ filter removed everything).")

    target_end = max(c.end for c in clips)
    base_track = min(c.track_index for c in clips)

    print(f"Selected clips: {len(clips)}")
    print(f"Target end frame: {target_end}")

    for offset, clip in enumerate(clips):
        new_track = base_track + offset if spread_tracks else clip.track_index
        print(
            f"- {clip.name}: start={clip.start} end={clip.end} "
            f"track V{clip.track_index} -> V{new_track}, end -> {target_end}"
        )

        if dry_run:
            continue

        if spread_tracks and new_track != clip.track_index:
            _move_clip_to_track(clip.item, new_track)
        if clip.end != target_end:
            _set_clip_end(clip.item, target_end)

    print("Done.")
    return 0


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-spread-tracks",
        action="store_true",
        help="Keep clips on their current tracks (only normalize end frame).",
    )
    parser.add_argument(
        "--all-selected",
        action="store_true",
        help="Process all selected clips, not just Text+ clips.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print planned edits without writing changes.")
    return parser.parse_args(argv)


def main(argv: Sequence[str]) -> int:
    args = parse_args(argv)
    try:
        return run(
            spread_tracks=not args.no_spread_tracks,
            text_only=not args.all_selected,
            dry_run=args.dry_run,
        )
    except ResolveScriptError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
