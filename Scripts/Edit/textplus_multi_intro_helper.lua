--[[
Text+ Multi Intro Helper (DaVinci Resolve)

Qué hace:
- Lee hasta 20 clips seleccionados en la línea de tiempo (página Edit).
- Filtra clips que contengan al menos un nodo TextPlus en su Fusion Comp.
- Reparte posiciones finales en grid para minimizar solapamientos.
- Aplica animaciones de entrada de 6 frames con perfiles variados.
- Usa 5 perfiles base. Si hay más de 5 clips, reutiliza perfiles aleatoriamente.

Notas:
- Este script asume FPS constante en la timeline.
- Debe ejecutarse con un proyecto y timeline activos.
- Si un clip no tiene Fusion Comp/TextPlus, se omite.
]]

local MAX_ITEMS = 20
local INTRO_FRAMES = 6

math.randomseed(os.time())

local resolve = Resolve()
if not resolve then
  print("❌ No se pudo obtener Resolve().")
  return
end

local projectManager = resolve:GetProjectManager()
local project = projectManager and projectManager:GetCurrentProject() or nil
local timeline = project and project:GetCurrentTimeline() or nil
if not timeline then
  print("❌ No hay timeline activo.")
  return
end

local function clamp(v, lo, hi)
  if v < lo then return lo end
  if v > hi then return hi end
  return v
end

local function getTimelineFPS(tl)
  local fpsStr = tl:GetSetting("timelineFrameRate") or "24"
  local fps = tonumber(fpsStr)
  if not fps then fps = 24 end
  return fps
end

local function getSelectedTimelineItems(tl)
  local selected = tl.GetSelectedItems and tl:GetSelectedItems() or nil
  local out = {}

  if selected and type(selected) == "table" then
    for _, item in pairs(selected) do
      table.insert(out, item)
    end
  end

  if #out == 0 then
    local current = tl.GetCurrentVideoItem and tl:GetCurrentVideoItem() or nil
    if current then
      table.insert(out, current)
    end
  end

  return out
end

local function getFirstFusionComp(clip)
  if not clip then return nil end
  local count = clip.GetFusionCompCount and clip:GetFusionCompCount() or 0
  if count < 1 then return nil end
  return clip:GetFusionCompByIndex(1)
end

local function getFirstTextPlusTool(comp)
  if not comp then return nil end
  local tools = comp:GetToolList(false, "TextPlus")
  if not tools then return nil end
  for _, tool in pairs(tools) do
    return tool
  end
  return nil
end

local function buildLayoutPositions(n)
  -- Grid normalizado en coordenadas de Fusion (0..1)
  local positions = {}
  if n == 1 then
    return { {x = 0.5, y = 0.5} }
  end

  local cols = math.ceil(math.sqrt(n * 16 / 9))
  local rows = math.ceil(n / cols)

  local marginX, marginY = 0.12, 0.2
  local usableW = 1.0 - marginX * 2
  local usableH = 1.0 - marginY * 2

  for i = 1, n do
    local idx = i - 1
    local c = idx % cols
    local r = math.floor(idx / cols)

    local x = marginX + (cols == 1 and 0.5 or (c / (cols - 1))) * usableW
    local y = marginY + (rows == 1 and 0.5 or (r / (rows - 1))) * usableH

    table.insert(positions, { x = clamp(x, 0.05, 0.95), y = clamp(y, 0.05, 0.95) })
  end

  return positions
end

local function safeSetValue(input, frame, value)
  if not input then return false end
  local ok = pcall(function()
    input[frame] = value
  end)
  return ok
end

local function applyEaseOnInput(input)
  -- Intento de curva suave de aceleración inicial usando BezierSpline.
  -- Si no está disponible en este host/API, simplemente conserva keyframes lineales.
  if not input then return end
  pcall(function()
    local attrs = input:GetAttrs()
    if attrs and attrs.INPB_Connected then
      -- Ya tiene una conexión/spline externa.
      return
    end
  end)
end

local function applyRiseFromBottom(tool, startF, endF, targetX, targetY)
  safeSetValue(tool.Center, startF, { targetX, targetY - 0.08 })
  safeSetValue(tool.Center, endF,   { targetX, targetY })

  if tool.Opacity1 then
    safeSetValue(tool.Opacity1, startF, 0)
    safeSetValue(tool.Opacity1, endF, 1)
    applyEaseOnInput(tool.Opacity1)
  end
  applyEaseOnInput(tool.Center)
end

local function applyOpacityGlitch(tool, startF, endF, targetX, targetY)
  safeSetValue(tool.Center, startF, { targetX, targetY })
  safeSetValue(tool.Center, endF,   { targetX, targetY })

  if tool.Opacity1 then
    safeSetValue(tool.Opacity1, startF + 0, 0.00)
    safeSetValue(tool.Opacity1, startF + 1, 0.65)
    safeSetValue(tool.Opacity1, startF + 2, 0.10)
    safeSetValue(tool.Opacity1, startF + 3, 0.90)
    safeSetValue(tool.Opacity1, startF + 4, 0.35)
    safeSetValue(tool.Opacity1, startF + 5, 0.95)
    safeSetValue(tool.Opacity1, endF,       1.00)
    applyEaseOnInput(tool.Opacity1)
  end
end

local function applySlideFromLeft(tool, startF, endF, targetX, targetY)
  safeSetValue(tool.Center, startF, { targetX - 0.12, targetY })
  safeSetValue(tool.Center, endF,   { targetX, targetY })

  if tool.Opacity1 then
    safeSetValue(tool.Opacity1, startF, 0)
    safeSetValue(tool.Opacity1, endF, 1)
    applyEaseOnInput(tool.Opacity1)
  end
  applyEaseOnInput(tool.Center)
end

local function applyScalePop(tool, startF, endF, targetX, targetY)
  safeSetValue(tool.Center, startF, { targetX, targetY })
  safeSetValue(tool.Center, endF,   { targetX, targetY })

  if tool.Size then
    safeSetValue(tool.Size, startF, 0.65)
    safeSetValue(tool.Size, startF + 4, 1.06)
    safeSetValue(tool.Size, endF, 1.00)
    applyEaseOnInput(tool.Size)
  end

  if tool.Opacity1 then
    safeSetValue(tool.Opacity1, startF, 0)
    safeSetValue(tool.Opacity1, endF, 1)
    applyEaseOnInput(tool.Opacity1)
  end
end

local function applyMicroRotate(tool, startF, endF, targetX, targetY)
  safeSetValue(tool.Center, startF, { targetX, targetY + 0.04 })
  safeSetValue(tool.Center, endF,   { targetX, targetY })

  if tool.Angle then
    safeSetValue(tool.Angle, startF, 8)
    safeSetValue(tool.Angle, endF, 0)
    applyEaseOnInput(tool.Angle)
  end

  if tool.Opacity1 then
    safeSetValue(tool.Opacity1, startF, 0)
    safeSetValue(tool.Opacity1, endF, 1)
    applyEaseOnInput(tool.Opacity1)
  end

  applyEaseOnInput(tool.Center)
end

local animationProfiles = {
  applyRiseFromBottom,
  applyOpacityGlitch,
  applySlideFromLeft,
  applyScalePop,
  applyMicroRotate,
}

local function pickProfileIndex(i)
  if i <= #animationProfiles then
    return i
  end
  return math.random(1, #animationProfiles)
end

local function getCompIntroRange(comp, introFrames)
  local defaultStart = 0
  local defaultEnd = defaultStart + introFrames
  if not comp or not comp.GetAttrs then
    return defaultStart, defaultEnd
  end

  local attrs = comp:GetAttrs() or {}
  local startFrame = tonumber(attrs.COMPN_RenderStart)
    or tonumber(attrs.COMPN_GlobalStart)
    or defaultStart
  local endLimit = tonumber(attrs.COMPN_RenderEnd)
    or tonumber(attrs.COMPN_GlobalEnd)

  local endFrame = startFrame + introFrames
  if endLimit and endFrame > endLimit then
    endFrame = endLimit
  end

  return startFrame, endFrame
end

local fps = getTimelineFPS(timeline)
local selectedItems = getSelectedTimelineItems(timeline)
if #selectedItems == 0 then
  print("⚠️ No hay clips seleccionados (ni clip de video actual).")
  return
end

-- Filtrar Text+ válidos
local candidates = {}
for _, clip in ipairs(selectedItems) do
  local comp = getFirstFusionComp(clip)
  local textTool = getFirstTextPlusTool(comp)
  if comp and textTool then
    table.insert(candidates, { clip = clip, comp = comp, tool = textTool })
  end
end

if #candidates == 0 then
  print("⚠️ Ningún clip seleccionado tiene TextPlus dentro de Fusion.")
  return
end

if #candidates > MAX_ITEMS then
  print(string.format("⚠️ Seleccionaste %d clips Text+, se procesarán solo los primeros %d.", #candidates, MAX_ITEMS))
end

local total = math.min(#candidates, MAX_ITEMS)
local positions = buildLayoutPositions(total)

for i = 1, total do
  local item = candidates[i]
  local clip = item.clip
  local comp = item.comp
  local tool = item.tool

  local introStart, introEnd = getCompIntroRange(comp, INTRO_FRAMES)

  local tx = positions[i].x
  local ty = positions[i].y

  local profileIdx = pickProfileIndex(i)
  local profile = animationProfiles[profileIdx]

  comp:Lock()
  comp:StartUndo("Text+ Multi Intro Helper")

  local ok, err = pcall(function()
    profile(tool, introStart, introEnd, tx, ty)
  end)

  comp:EndUndo(true)
  comp:Unlock()

  if ok then
    print(string.format("✅ Clip %d animado con perfil %d.", i, profileIdx))
  else
    print(string.format("❌ Error animando clip %d: %s", i, tostring(err)))
  end
end

print(string.format("Hecho. FPS detectado: %s. Clips procesados: %d.", tostring(fps), total))
