(() => {
  const KEY = "renometric-project-workspace-v1";
  const read = () => { try { const v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v : []; } catch { return []; } };
  const write = (items) => localStorage.setItem(KEY, JSON.stringify(items.slice(0, 50)));
  const esc = (v) => String(v ?? "").replace(/[&<>"']/g, (c) => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
  const textOf = (item) => [item.title, item.primary, item.summary, ...(item.rows || []).map((r) => r.label + ": " + r.value)].filter(Boolean).join("\n");
  const render = () => {
    const items = read(), out = document.querySelector("#dashboard-items");
    document.querySelector("#dashboard-count").textContent = items.length + " saved estimate" + (items.length === 1 ? "" : "s");
    if (!items.length) { out.innerHTML = '<p class="workspace-empty">No saved estimates yet. Open a calculator, calculate a quantity, and save it to this project.</p>'; return; }
    out.innerHTML = items.map((item) => '<article class="workspace-item"><div class="workspace-item-head"><div><b>' + esc(item.title) + '</b><small>' + esc(new Date(item.createdAt).toLocaleString()) + '</small></div><button class="workspace-remove" type="button" data-remove="' + esc(item.id) + '">Remove</button></div><strong>' + esc(item.primary) + '</strong>' + (item.summary ? '<p>' + esc(item.summary) + '</p>' : '') + ((item.rows || []).length ? '<ul>' + item.rows.map((r) => '<li><span>' + esc(r.label) + '</span><b>' + esc(r.value) + '</b></li>').join("") + '</ul>' : '') + '</article>').join("");
  };
  const init = () => {
    render();
    document.querySelector("#dashboard-items").addEventListener("click", (e) => { const b = e.target.closest("[data-remove]"); if (!b) return; write(read().filter((i) => i.id !== b.dataset.remove)); render(); });
    document.querySelector("#dashboard-clear").addEventListener("click", () => { if (read().length && confirm("Clear all saved estimates on this device?")) { localStorage.removeItem(KEY); render(); } });
    document.querySelector("#dashboard-copy").addEventListener("click", async () => { const items = read(); if (!items.length) { alert("No saved estimates yet."); return; } const text = ["RenoMetric purchase notes", "", ...items.flatMap((item, i) => [(i + 1) + ". " + textOf(item), ""])].join("\n"); try { await navigator.clipboard.writeText(text); alert("Purchase notes copied."); } catch { prompt("Copy your purchase notes:", text); } });
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();