(() => {
  const STORAGE_KEY = "renometric-project-workspace-v1";
  const readItems = () => {
    try {
      const value = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      return Array.isArray(value) ? value : [];
    } catch {
      return [];
    }
  };
  const writeItems = (items) => localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, 50)));
  const esc = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));
  const slugTitle = () => {
    const title = document.querySelector("#tool-title")?.textContent?.trim();
    return title || "Calculator estimate";
  };
  const currentEstimate = () => {
    const result = document.querySelector("#calc-results");
    if (!result) return null;
    const primary = result.querySelector(".big")?.textContent?.trim() || "";
    const summary = result.querySelector(".sub")?.textContent?.trim() || "";
    const rows = [...result.querySelectorAll(".result-row")].map((row) => {
      const parts = [...row.querySelectorAll("span")].map((node) => node.textContent.trim());
      return parts.length > 1 ? { label: parts[0], value: parts.slice(1).join(" ") } : null;
    }).filter(Boolean);
    if (!primary || primary === "—" || /enter measurements/i.test(summary)) return null;
    return { primary, summary, rows };
  };
  const estimateText = (item) => [
    item.title,
    item.primary,
    item.summary,
    ...item.rows.map((row) => row.label + ": " + row.value)
  ].filter(Boolean).join("\n");
  const renderItems = (list, output) => {
    if (!list.length) {
      output.innerHTML = '<p class="workspace-empty">No saved estimates yet. Calculate a material quantity, then save it here.</p>';
      return;
    }
    output.innerHTML = list.map((item) => {
      const rows = item.rows.map((row) =>
        '<li><span>' + esc(row.label) + '</span><b>' + esc(row.value) + '</b></li>'
      ).join("");
      return '<article class="workspace-item">' +
        '<div class="workspace-item-head"><div><b>' + esc(item.title) + '</b><small>' +
        esc(new Date(item.createdAt).toLocaleString()) + '</small></div>' +
        '<button type="button" class="workspace-remove" data-remove="' + esc(item.id) + '">Remove</button></div>' +
        '<strong>' + esc(item.primary) + '</strong>' +
        (item.summary ? '<p>' + esc(item.summary) + '</p>' : "") +
        (rows ? '<ul>' + rows + '</ul>' : "") +
        '</article>';
    }).join("");
  };
  const init = () => {
    const result = document.querySelector("#calc-results");
    const layout = document.querySelector(".calculator-layout");
    if (!result || !layout || document.querySelector("#project-workspace")) return;
    const panel = document.createElement("section");
    panel.id = "project-workspace";
    panel.className = "workspace-panel";
    panel.innerHTML = '<div class="workspace-head"><div><span class="tag">Project workspace</span>' +
      '<h2>Save estimates and build a purchase list</h2><p>Keep this project on this device. No account or upload required.</p></div>' +
      '<button type="button" class="btn" id="workspace-copy">Copy purchase notes</button></div>' +
      '<div class="workspace-save"><label for="workspace-name">Project or estimate name</label>' +
      '<div class="workspace-save-row"><input id="workspace-name" placeholder="e.g. Backyard patio" maxlength="80">' +
      '<button type="button" class="btn primary" id="workspace-save">Save current estimate</button></div></div>' +
      '<div id="workspace-items" class="workspace-items"></div>' +
      '<div class="workspace-foot"><span id="workspace-count"></span>' +
      '<button type="button" class="workspace-clear">Clear saved estimates</button></div>';
    layout.parentNode.insertBefore(panel, layout.nextSibling);
    const itemsOutput = panel.querySelector("#workspace-items");
    const countOutput = panel.querySelector("#workspace-count");
    const refresh = () => {
      const items = readItems();
      renderItems(items, itemsOutput);
      countOutput.textContent = items.length + " saved estimate" + (items.length === 1 ? "" : "s");
    };
    panel.querySelector("#workspace-save").addEventListener("click", () => {
      const estimate = currentEstimate();
      if (!estimate) {
        window.alert("Enter measurements and calculate an estimate first.");
        return;
      }
      const name = panel.querySelector("#workspace-name").value.trim();
      const items = readItems();
      items.unshift({
        id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
        title: name || slugTitle(),
        calculator: document.querySelector("[data-calculator]")?.dataset.calculator || location.pathname,
        createdAt: new Date().toISOString(),
        ...estimate
      });
      writeItems(items);
      panel.querySelector("#workspace-name").value = "";
      refresh();
    });
    itemsOutput.addEventListener("click", (event) => {
      const button = event.target.closest("[data-remove]");
      if (!button) return;
      writeItems(readItems().filter((item) => item.id !== button.dataset.remove));
      refresh();
    });
    panel.querySelector(".workspace-clear").addEventListener("click", () => {
      if (readItems().length && window.confirm("Clear all saved estimates on this device?")) {
        localStorage.removeItem(STORAGE_KEY);
        refresh();
      }
    });
    panel.querySelector("#workspace-copy").addEventListener("click", async () => {
      const items = readItems();
      if (!items.length) {
        window.alert("Save at least one estimate first.");
        return;
      }
      const text = ["RenoMetric purchase notes", ""];
      items.forEach((item, index) => {
        text.push((index + 1) + ". " + estimateText(item), "");
      });
      try {
        await navigator.clipboard.writeText(text.join("\n"));
        window.alert("Purchase notes copied.");
      } catch {
        window.prompt("Copy your purchase notes:", text.join("\n"));
      }
    });
    refresh();
    new MutationObserver(() => {
      const estimate = currentEstimate();
      if (estimate) panel.classList.add("has-estimate");
    }).observe(result, { childList: true, subtree: true, characterData: true });
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();