const API = '';  // same origin — change to 'http://localhost:8000' if different

let images = [];
let currentImage = null;
let showingAnnotated = false;

// ── Init ──────────────────────────────────────────────────────────────
async function init() {
  await loadImages();
  setupDrag();
}

// ── Drag & drop ───────────────────────────────────────────────────────
function setupDrag() {
  const zone = document.getElementById('uploadZone');
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('drag');
    uploadFiles(e.dataTransfer.files);
  });
  document.getElementById('fileInput').addEventListener('change', e => {
    uploadFiles(e.target.files);
    e.target.value = '';
  });
}

// ── Load image list ───────────────────────────────────────────────────
async function loadImages() {
  try {
    const res = await fetch(`${API}/images`);
    images = await res.json();
    renderList();
  } catch { toast('Could not reach server.', 'error'); }
}

function renderList() {
  const list = document.getElementById('imageList');
  if (!images.length) {
    list.innerHTML = '<div style="padding:12px 10px;color:var(--muted);font-size:12px;">No images yet.</div>';
    return;
  }
  list.innerHTML = images.map(img => `
    <div class="image-item ${currentImage?.id === img.id ? 'active' : ''}"
         onclick="selectImage(${img.id})">
      <div class="thumb">🖼</div>
      <div class="info">
        <div class="name">${esc(img.title || img.filename)}</div>
        <div class="date">${formatDate(img.uploaded_at)}</div>
      </div>
      <button class="del-btn" onclick="deleteImage(event, '${esc(img.filename)}')">✕</button>
    </div>
  `).join('');
}

// ── Upload ────────────────────────────────────────────────────────────
async function uploadFiles(files) {
  for (const file of files) {
    const form = new FormData();
    form.append('file', file);
    try {
      const res = await fetch(`${API}/images`, { method: 'POST', body: form });
      if (!res.ok) throw new Error();
      toast(`Uploaded ${file.name}`, 'success');
    } catch { toast(`Failed to upload ${file.name}`, 'error'); }
  }
  await loadImages();
}

// ── Select image ──────────────────────────────────────────────────────
async function selectImage(id) {
  currentImage = images.find(i => i.id === id);
  showingAnnotated = false;

  document.getElementById('emptyState').classList.add('hidden');
  document.getElementById('imageView').classList.remove('hidden');

  // Set preview
  document.getElementById('previewImg').src = `${API}/uploads/${currentImage.filename}`;
  document.getElementById('titleInput').value = currentImage.title || currentImage.filename;
  document.getElementById('notesInput').value = currentImage.notes || '';

  // Reset sections
  document.getElementById('captionSection').classList.add('hidden');
  document.getElementById('detectionsSection').classList.add('hidden');
  document.getElementById('toggleAnnotated').classList.add('hidden');

  // Load chat
  await loadChat();
  renderList();
}

// ── Delete ────────────────────────────────────────────────────────────
async function deleteImage(e, filename) {
  e.stopPropagation();
  if (!confirm(`Delete "${filename}"?`)) return;
  await fetch(`${API}/images/${filename}`, { method: 'DELETE' });
  if (currentImage?.filename === filename) {
    currentImage = null;
    document.getElementById('emptyState').classList.remove('hidden');
    document.getElementById('imageView').classList.add('hidden');
  }
  await loadImages();
  toast('Image deleted');
}

// ── Save meta ─────────────────────────────────────────────────────────
async function saveMeta() {
  if (!currentImage) return;
  const title = document.getElementById('titleInput').value;
  const notes = document.getElementById('notesInput').value;
  try {
    await fetch(`${API}/images/${currentImage.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, notes })
    });
    currentImage.title = title;
    currentImage.notes = notes;
    images = images.map(i => i.id === currentImage.id ? { ...i, title, notes } : i);
    renderList();
    toast('Saved', 'success');
  } catch { toast('Save failed', 'error'); }
}

// ── Detect ────────────────────────────────────────────────────────────
async function runDetect() {
  if (!currentImage) return;
  const btn = document.getElementById('detectBtn');
  setLoading(btn, true, '🔍 Detecting…');

  try {
    const res = await fetch(`${API}/detect/${currentImage.id}`, { method: 'POST' });
    const detections = await res.json();

    // Show annotated image
    const ts = Date.now();
    const annotatedSrc = `${API}/annotated/${currentImage.id}_detected.jpg?t=${ts}`;
    const img = document.getElementById('previewImg');

    // Preload then switch
    const tmp = new Image();
    tmp.onload = () => {
      img.src = annotatedSrc;
      showingAnnotated = true;
      document.getElementById('toggleAnnotated').classList.remove('hidden');
      document.getElementById('toggleAnnotated').textContent = 'Show original';
    };
    tmp.onerror = () => {
      // annotated file not accessible via /annotated — show detections as tags only
    };
    tmp.src = annotatedSrc;

    // Render detection tags
    const list = document.getElementById('detectionsList');
    if (!detections.length) {
      list.innerHTML = '<div style="color:var(--muted);font-size:12px;">No objects detected.</div>';
    } else {
      list.innerHTML = detections.map(d => `
        <div class="detection-tag">
          <div>
            <div class="label">${esc(d.label)}</div>
            <div class="conf-bar"><div class="conf-bar-fill" style="width:${(d.confidence*100).toFixed(0)}%"></div></div>
          </div>
          <div class="conf">${(d.confidence*100).toFixed(1)}%</div>
        </div>
      `).join('');
    }
    document.getElementById('detectionsSection').classList.remove('hidden');
    toast(`Found ${detections.length} object${detections.length !== 1 ? 's' : ''}`, 'success');
  } catch (err) {
    toast('Detection failed', 'error');
  } finally {
    setLoading(btn, false, '🔍 Detect objects');
  }
}

// ── Toggle annotated / original ───────────────────────────────────────
function toggleAnnotated() {
  const img = document.getElementById('previewImg');
  const btn = document.getElementById('toggleAnnotated');
  if (showingAnnotated) {
    img.src = `${API}/uploads/${currentImage.filename}`;
    btn.textContent = 'Show annotated';
    showingAnnotated = false;
  } else {
    const ts = Date.now();
    img.src = `${API}/annotated/${currentImage.id}_detected.jpg?t=${ts}`;
    btn.textContent = 'Show original';
    showingAnnotated = true;
  }
}

// ── Caption ───────────────────────────────────────────────────────────
async function runCaption() {
  if (!currentImage) return;
  const btn = document.getElementById('captionBtn');
  setLoading(btn, true, '✨ Generating…');

  try {
    const res = await fetch(`${API}/caption/${currentImage.id}`, { method: 'POST' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    document.getElementById('captionText').textContent = data.caption;
    document.getElementById('captionSection').classList.remove('hidden');
    toast('Caption ready', 'success');
  } catch (err) {
    toast('Caption failed — check server logs', 'error');
    console.error(err);
  } finally {
    setLoading(btn, false, '✨ Generate caption');
  }
}

// ── Chat ──────────────────────────────────────────────────────────────
async function loadChat() {
  if (!currentImage) return;
  try {
    const res = await fetch(`${API}/chat/${currentImage.id}`);
    const msgs = await res.json();
    const box = document.getElementById('chatMessages');
    box.innerHTML = msgs.map(m => `<div class="msg ${m.role}">${esc(m.message)}</div>`).join('');
    box.scrollTop = box.scrollHeight;
  } catch {}
}

async function sendChat() {
  if (!currentImage) return;
  const input = document.getElementById('chatInput');
  const q = input.value.trim();
  if (!q) return;

  const box = document.getElementById('chatMessages');
  box.innerHTML += `<div class="msg user">${esc(q)}</div>`;
  input.value = '';
  autoResize(input);
  box.scrollTop = box.scrollHeight;

  // Thinking indicator
  const thinkId = 'think-' + Date.now();
  box.innerHTML += `<div class="msg assistant" id="${thinkId}" style="color:var(--muted)">…</div>`;
  box.scrollTop = box.scrollHeight;

  try {
    const res = await fetch(`${API}/chat/${currentImage.id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    document.getElementById(thinkId).outerHTML = `<div class="msg assistant">${esc(data.answer)}</div>`;
  } catch {
    document.getElementById(thinkId).outerHTML = `<div class="msg assistant" style="color:var(--danger)">Error — could not get a response.</div>`;
  }
  box.scrollTop = box.scrollHeight;
}

function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendChat(); }
}

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}

// ── Helpers ───────────────────────────────────────────────────────────
function setLoading(btn, loading, label) {
  btn.disabled = loading;
  btn.innerHTML = loading
    ? `<span class="spinner"></span> ${label}`
    : label;
}

function toast(msg, type = '') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = 'toast show' + (type ? ' ' + type : '');
  clearTimeout(el._t);
  el._t = setTimeout(() => el.classList.remove('show'), 3000);
}

function formatDate(iso) {
  if (!iso) return '';
  try { return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' }); }
  catch { return ''; }
}

function esc(str) {
  return String(str ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

init();