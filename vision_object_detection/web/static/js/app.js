const elements = {
  statusText: document.querySelector("#statusText"),
  cameraState: document.querySelector("#cameraState"),
  startButton: document.querySelector("#startButton"),
  stopButton: document.querySelector("#stopButton"),
  streamImage: document.querySelector("#streamImage"),
  emptyState: document.querySelector("#emptyState"),
  detectionCount: document.querySelector("#detectionCount"),
  detectionsList: document.querySelector("#detectionsList"),
  objectCounter: document.querySelector("#objectCounter"),
  detectorName: document.querySelector("#detectorName"),
  detectorMessage: document.querySelector("#detectorMessage"),
  confidenceSlider: document.querySelector("#confidenceSlider"),
  confidenceValue: document.querySelector("#confidenceValue"),
  drawZoneButton: document.querySelector("#drawZoneButton"),
  clearZoneButton: document.querySelector("#clearZoneButton"),
  zoneStatus: document.querySelector("#zoneStatus"),
  zoneCanvas: document.querySelector("#zoneCanvas"),
  streamStage: document.querySelector(".stream-stage"),
};

let running = false;
let drawZoneMode = false;
let activeDrag = null;
let settings = {
  confidence: 0.35,
  zone: { enabled: false, x1: 0, y1: 0, x2: 1, y2: 1 },
};

function setRunning(value) {
  running = value;
  elements.startButton.disabled = value;
  elements.stopButton.disabled = !value;
  elements.cameraState.textContent = value ? "Running" : "Stopped";
  elements.emptyState.style.display = value ? "none" : "grid";
  if (!value) {
    elements.streamImage.removeAttribute("src");
    elements.detectionCount.textContent = "0 detections";
    elements.detectionsList.textContent = "No detections yet.";
    elements.objectCounter.textContent = "No objects counted yet.";
  }
}

async function postJson(url) {
  const response = await fetch(url, { method: "POST" });
  return response.json();
}

async function postPayload(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return response.json();
}

async function refreshStatus() {
  const response = await fetch("/api/status");
  const status = await response.json();
  elements.statusText.textContent = status.message;
  setRunning(status.running);
  if (status.running) {
    elements.streamImage.src = `/stream?t=${Date.now()}`;
  }
}

async function refreshDetectorStatus() {
  const response = await fetch("/api/detector/status");
  const status = await response.json();
  elements.detectorName.textContent = status.name;
  elements.detectorMessage.textContent = status.message;
}

async function refreshSettings() {
  const response = await fetch("/api/settings");
  settings = await response.json();
  elements.confidenceSlider.value = settings.confidence;
  elements.confidenceValue.textContent = Number(settings.confidence).toFixed(2);
  updateZoneStatus();
  drawZoneOverlay();
}

async function refreshDetections() {
  if (!running) {
    return;
  }

  const response = await fetch("/api/detections");
  if (!response.ok) {
    elements.detectionCount.textContent = "0 detections";
    elements.detectionsList.textContent = "No frame available.";
    elements.objectCounter.textContent = "No objects counted yet.";
    return;
  }

  const result = await response.json();
  elements.detectionCount.textContent = `${result.count} detections`;
  renderObjectCounter(result.object_counts);
  if (!result.detections.length) {
    elements.detectionsList.textContent = "No detections.";
    return;
  }

  elements.detectionsList.replaceChildren(
    ...result.detections.map((detection) => {
      const item = document.createElement("div");
      item.className = "detection-item";
      item.innerHTML = `
        <strong>${detection.label}</strong>
        <span>Confidence: ${Number(detection.confidence).toFixed(2)}</span>
        <span>Box: ${detection.x1}, ${detection.y1}, ${detection.x2}, ${detection.y2}</span>
      `;
      return item;
    }),
  );
}

function renderObjectCounter(counts) {
  const entries = Object.entries(counts || {});
  if (!entries.length) {
    elements.objectCounter.textContent = "No objects counted yet.";
    return;
  }

  elements.objectCounter.replaceChildren(
    ...entries.map(([label, count]) => {
      const item = document.createElement("div");
      item.className = "counter-item";
      item.innerHTML = `<strong>${label}</strong><span>${count}</span>`;
      return item;
    }),
  );
}

function updateZoneStatus() {
  if (drawZoneMode) {
    elements.zoneStatus.textContent = "Drag on the video to draw a zone.";
    elements.streamStage.classList.add("zone-armed");
    return;
  }

  elements.streamStage.classList.remove("zone-armed");
  elements.zoneStatus.textContent = settings.zone.enabled
    ? "Zone filter is active."
    : "Zone filter is off.";
}

function canvasPoint(event) {
  const rect = elements.zoneCanvas.getBoundingClientRect();
  return {
    x: Math.max(0, Math.min(rect.width, event.clientX - rect.left)),
    y: Math.max(0, Math.min(rect.height, event.clientY - rect.top)),
    width: rect.width,
    height: rect.height,
  };
}

function normalizeZone(start, end) {
  return {
    enabled: true,
    x1: start.x / start.width,
    y1: start.y / start.height,
    x2: end.x / end.width,
    y2: end.y / end.height,
  };
}

function drawZoneOverlay(previewZone = settings.zone) {
  const canvas = elements.zoneCanvas;
  const rect = canvas.getBoundingClientRect();
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.round(rect.width * scale));
  canvas.height = Math.max(1, Math.round(rect.height * scale));

  const context = canvas.getContext("2d");
  context.setTransform(scale, 0, 0, scale, 0, 0);
  context.clearRect(0, 0, rect.width, rect.height);

  if (!previewZone.enabled) {
    return;
  }

  const x = previewZone.x1 * rect.width;
  const y = previewZone.y1 * rect.height;
  const width = (previewZone.x2 - previewZone.x1) * rect.width;
  const height = (previewZone.y2 - previewZone.y1) * rect.height;

  context.fillStyle = "rgba(61, 165, 255, 0.12)";
  context.strokeStyle = "#3da5ff";
  context.lineWidth = 2;
  context.fillRect(x, y, width, height);
  context.strokeRect(x, y, width, height);
}

elements.startButton.addEventListener("click", async () => {
  const status = await postJson("/api/camera/start");
  elements.statusText.textContent = status.message;
  setRunning(status.running);
  if (status.running) {
    elements.streamImage.src = `/stream?t=${Date.now()}`;
  }
});

elements.stopButton.addEventListener("click", async () => {
  const status = await postJson("/api/camera/stop");
  elements.statusText.textContent = status.message;
  setRunning(false);
});

elements.confidenceSlider.addEventListener("input", () => {
  elements.confidenceValue.textContent = Number(elements.confidenceSlider.value).toFixed(2);
});

elements.confidenceSlider.addEventListener("change", async () => {
  settings = await postPayload("/api/settings/confidence", {
    confidence: Number(elements.confidenceSlider.value),
  });
  elements.confidenceValue.textContent = Number(settings.confidence).toFixed(2);
});

elements.drawZoneButton.addEventListener("click", () => {
  drawZoneMode = true;
  updateZoneStatus();
});

elements.clearZoneButton.addEventListener("click", async () => {
  drawZoneMode = false;
  settings = await postPayload("/api/settings/zone", { enabled: false });
  updateZoneStatus();
  drawZoneOverlay();
});

elements.zoneCanvas.addEventListener("pointerdown", (event) => {
  if (!drawZoneMode || !running) {
    return;
  }
  elements.zoneCanvas.setPointerCapture(event.pointerId);
  activeDrag = canvasPoint(event);
});

elements.zoneCanvas.addEventListener("pointermove", (event) => {
  if (!activeDrag) {
    return;
  }
  drawZoneOverlay(normalizeZone(activeDrag, canvasPoint(event)));
});

elements.zoneCanvas.addEventListener("pointerup", async (event) => {
  if (!activeDrag) {
    return;
  }

  const zone = normalizeZone(activeDrag, canvasPoint(event));
  activeDrag = null;
  drawZoneMode = false;
  settings = await postPayload("/api/settings/zone", zone);
  updateZoneStatus();
  drawZoneOverlay();
});

window.addEventListener("resize", drawZoneOverlay);

setInterval(refreshDetections, 1000);
refreshStatus();
refreshDetectorStatus();
refreshSettings();
