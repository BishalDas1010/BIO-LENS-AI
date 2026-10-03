const API = window.API_URL || "http://localhost:8000";
const $ = (id) => document.getElementById(id);
let imageBlob = null;
let stream = null;

//  sidebar navigation 
document.querySelectorAll("nav a").forEach((a) => {
  a.onclick = () => {
    document.querySelectorAll("nav a").forEach((x) => x.classList.remove("active"));
    a.classList.add("active");
    $(a.dataset.target).scrollIntoView({ behavior: "smooth" });
    if (a.dataset.target === "history") loadHistory();
  };
});

// image upload 
const drop = $("drop"), file = $("file");
drop.onclick = () => file.click();
file.onchange = () => file.files[0] && setImage(file.files[0]);
drop.ondragover = (e) => { e.preventDefault(); drop.classList.add("over"); };
drop.ondragleave = () => drop.classList.remove("over");
drop.ondrop = (e) => {
  e.preventDefault(); drop.classList.remove("over");
  e.dataTransfer.files[0] && setImage(e.dataTransfer.files[0]);
};

async function setImage(blob) {
  $("error").textContent = "";
  if (!["image/jpeg", "image/png"].includes(blob.type)) return ($("error").textContent = "Only JPG or PNG allowed.");
  if (blob.size > 5 * 1024 * 1024) return ($("error").textContent = "Image must be 5MB or smaller.");
  stopCamera();
  imageBlob = blob;
  $("img").src = URL.createObjectURL(blob);
  $("img").hidden = false;
  $("video").hidden = true;
  $("previewMsg").hidden = true;
  $("box").hidden = true;
  await detectFace(blob);
}

async function detectFace(blob) {
  try {
    const fd = new FormData();
    fd.append("image", blob, "face.jpg");
    const r = await fetch(`${API}/api/detect-face`, { method: "POST", body: fd });
    if (!r.ok) throw new Error((await r.json()).detail || "Detection failed");
    const d = await r.json();
    if (!d.detected) { $("error").textContent = "No face detected. Try another image."; return; }
    drawBox(d.box);
  } catch (e) {
    $("error").textContent = "Face detection error: " + e.message;
  }
}

// the image uses object-fit: cover, so map the box into the displayed area
function drawBox(b) {
  const img = $("img"), pv = $("preview");
  const W = pv.clientWidth, H = pv.clientHeight;
  const nw = img.naturalWidth, nh = img.naturalHeight;
  const scale = Math.max(W / nw, H / nh);
  const offX = (W - nw * scale) / 2, offY = (H - nh * scale) / 2;
  const box = $("box");
  box.style.left = offX + b.x * nw * scale + "px";
  box.style.top = offY + b.y * nh * scale + "px";
  box.style.width = b.w * nw * scale + "px";
  box.style.height = b.h * nh * scale + "px";
  box.hidden = false;
}

// camera
$("tabUpload").onclick = () => { setTab("upload"); stopCamera(); };
$("tabCamera").onclick = async () => {
  setTab("camera");
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    $("video").srcObject = stream;
    $("video").hidden = false;
    $("img").hidden = true;
    $("box").hidden = true;
    $("previewMsg").hidden = true;
    $("snap").hidden = false;
  } catch (e) {
    $("error").textContent = "Camera unavailable: " + e.message;
    setTab("upload");
  }
};
$("snap").onclick = () => {
  const v = $("video"), c = document.createElement("canvas");
  c.width = v.videoWidth; c.height = v.videoHeight;
  c.getContext("2d").drawImage(v, 0, 0);
  c.toBlob((b) => setImage(b), "image/jpeg", 0.92);
};
function setTab(t) {
  $("tabUpload").classList.toggle("active", t === "upload");
  $("tabCamera").classList.toggle("active", t === "camera");
}
function stopCamera() {
  if (stream) stream.getTracks().forEach((t) => t.stop());
  stream = null;
  $("snap").hidden = true;
}

// ---------- analyze ----------
$("analyze").onclick = async () => {
  $("error").textContent = "";
  const btn = $("analyze");
  const fd = new FormData();
  
  fd.append("age", $("age").value);
  fd.append("gender", $("gender").value);
  fd.append("height", $("height").value);
  fd.append("weight", $("weight").value);
  if ($("hr").value) fd.append("heart_rate", $("hr").value);
  if ($("spo2").value) fd.append("spo2", $("spo2").value);
  if ($("temp").value) fd.append("temperature", $("temp").value);
  const syms = [...document.querySelectorAll(".checks input:checked")].map((c) => c.value);
  fd.append("symptoms", syms.join(","));
  if (imageBlob) fd.append("image", imageBlob, "face.jpg");

  btn.disabled = true; btn.textContent = "Analyzing...";
  try {
    const r = await fetch(`${API}/api/analyze`, { method: "POST", body: fd });
    if (!r.ok) throw new Error(JSON.stringify((await r.json()).detail));
    showResults(await r.json());
  } catch (e) {
    $("error").textContent = "Analysis failed: " + e.message;
  } finally {
    btn.disabled = false; btn.textContent = "📈 Analyze My Health";
  }
};

function showResults(d) {
  $("results").hidden = false;
  const label = { normal: "No concerning indicators", watch: "Some indicators to watch", attention: "Some indicators need attention" };
  $("overall").className = "s-" + d.overall;
  $("overall").textContent = label[d.overall];
  $("indicators").innerHTML = d.indicators
    .map((i) => `<div class="s-${i.status}"><strong>${esc(i.name)}: ${esc(i.value)}</strong><small>${esc(i.note)}</small></div>`)
    .join("");
  $("recs").innerHTML = d.recommendations.map((r) => `<li>${esc(r)}</li>`).join("");
  $("disc").textContent = d.disclaimer;
  $("results").scrollIntoView({ behavior: "smooth" });
  loadHistory();
}

// ---------- history ----------
async function loadHistory() {
  try {
    const items = await (await fetch(`${API}/api/history`)).json();
    $("historyList").innerHTML = items.length
      ? items.map((h) => `<div class="hrow"><span>#${h.id} · ${esc(h.time)}</span><span class="s-${h.overall}" style="padding:2px 10px;border-radius:12px">${h.overall}</span></div>`).join("")
      : "<small>No analyses yet.</small>";
  } catch {
    $("historyList").innerHTML = "<small>Backend not reachable.</small>";
  }
}

// ---------- chat ----------
function addMsg(text, me) {
  const p = document.createElement("p");
  p.textContent = text;
  if (me) p.className = "me";
  $("chatLog").appendChild(p);
  $("chatLog").scrollTop = $("chatLog").scrollHeight;
}
async function sendChat() {
  const text = $("chatInput").value.trim();
  if (!text) return;
  $("chatInput").value = "";
  addMsg(text, true);
  try {
    const r = await fetch(`${API}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });
    addMsg((await r.json()).reply, false);
  } catch {
    addMsg("Backend not reachable.", false);
  }
}
$("chatSend").onclick = sendChat;
$("chatInput").onkeydown = (e) => e.key === "Enter" && sendChat();

function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

addMsg("Hi! Ask me about SpO2, heart rate, BMI, temperature or fatigue.", false);
loadHistory();
