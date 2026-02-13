# Fusion Compatibility Guidelines

Use this checklist for any programming added to this repo.

## 1) Runtime and script conventions

- Prefer native Fusion macro `.setting` patterns for parameter wiring.
- Keep parameter names stable and predictable (`Size`, `CenterX`, `CenterY`, `Strength`, etc.).
- Use Resolve/Fusion-supported expression syntax only.
- Avoid dependencies on external runtimes for core macro behavior.

## 2) Expression requirements

- Expressions must be deterministic and frame-safe.
- Use straightforward math operations for maintainability:
  - `+`, `-`, `*`, `/`, `%`
  - `min(a,b)`, `max(a,b)`, `abs(x)`
  - `clamp(x, lo, hi)` style patterns using `max(lo, min(hi, x))`
- Guard against divide-by-zero when using user controls:
  - `value / max(0.0001, denom)`

## 3) Macro variable design

- Every exposed user control should include:
  - clear display name,
  - default value,
  - sensible min/max bounds,
  - optional step/increment.
- Use normalized ranges where possible (for example, 0..1 for percentages).
- Document control intent directly in macro comments/docs.

## 4) Tool-chain compatibility (Fusion tools)

- Verify expressions correctly drive common tools used in macro graphs (Transform, Blur, Merge, ColorCorrector, etc.).
- Keep links between controls and tool inputs explicit.
- Ensure defaults produce visible output without user adjustment.

## 5) Validation checklist

Before accepting a macro/tool update:

1. Macro loads in Resolve Fusion page without errors.
2. Published controls appear and update downstream tools.
3. Expressions evaluate across multiple frames.
4. Extreme values (min/max) do not break output.
5. No unresolved control links.
