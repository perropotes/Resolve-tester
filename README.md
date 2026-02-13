# Resolve Text+ Chain Extender

This repo contains a DaVinci Resolve Python script that automates a common motion-graphics title workflow:

- You select a group of connected **Text+** clips in the Edit page.
- The script optionally places them on consecutive video tracks (`Vx, Vx+1, Vx+2, ...`).
- It extends every selected clip so all of them end on the same frame: the end frame of the latest clip in the selection.

That creates a title chain where each text appears when it starts and stays on screen until the final title ends.

---

## What the script does (exact behavior)

Given selected clips `A, B, C`:

- Starts stay unchanged:
  - `A.start`, `B.start`, `C.start` are preserved.
- Ends are unified:
  - `A.end = max(A.end, B.end, C.end)`
  - `B.end = max(...)`
  - `C.end = max(...)`
- Track layout (default mode):
  - Clips are sorted by start time.
  - They are moved to sequential tracks beginning at the lowest currently used track in your selection.

---

## Files

- `resolve_text_chain.py` — main script.

---

## Requirements

- DaVinci Resolve 18.5+ recommended.
- Python 3.6+.
- Resolve scripting API available as `DaVinciResolveScript`.

> Why 18.5+? This script uses timeline selection (`GetSelectedItems`) so it can work on the clips you highlight in the Edit page.

---

## Install / run inside Resolve (recommended)

1. Copy `resolve_text_chain.py` into Resolve's scripts folder.
   - **Windows:** `%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Edit\`
   - **macOS:** `~/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Edit/`
   - **Linux:** `~/.local/share/DaVinciResolve/Fusion/Scripts/Edit/`
2. Restart Resolve (or refresh scripts).
3. Open your timeline on the **Edit** page.
4. Select the Text+ clips to process.
5. Run script from: `Workspace -> Scripts -> Edit -> resolve_text_chain`.

---

## CLI options

When launched externally (with Resolve API environment configured):

```bash
python3 resolve_text_chain.py [options]
```

Options:

- `--dry-run` : Print what would change, without changing timeline clips.
- `--no-spread-tracks` : Keep current tracks; only extend durations.
- `--all-selected` : Process all selected clips (not just Text+).

---

## Recommended workflow for your use case

1. Create your text sequence in time order.
2. Select the whole group.
3. Run script (default settings).
4. Result: each title appears at its own start time and remains visible until the last title ends.

This is ideal for “build-up” title chains where previous words stay on screen.

---

## Troubleshooting

### `No timeline items selected`

Resolve did not expose selection to the script. Re-select clips in Edit page and retry.

### `GetSelectedItems() not available`

Your Resolve build is too old for selection-based behavior. Update Resolve.

### `Could not move clip to V...`

The current Resolve build/API may not support scripted track moves (`SetTrackIndex`) or destination tracks may be blocked by timeline state.

Use `--no-spread-tracks` to only normalize clip end frames.

### `Could not set clip end frame`

Usually one of these:

- not enough source handles to extend,
- track/item is locked,
- API/property restrictions in current Resolve build.

---

## Notes

- This script is intentionally conservative and fails fast with clear messages when Resolve API methods are unavailable.
- For production use, test first with `--dry-run` and then on a duplicate timeline.
