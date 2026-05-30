const state = {
  bills: [],
  assumptions: [],
};

const fileInput = document.getElementById("fileInput");
const extractButton = document.getElementById("extractButton");
const resetButton = document.getElementById("resetButton");
const generateButton = document.getElementById("generateButton");
const previewGrid = document.getElementById("previewGrid");
const resultsRoot = document.getElementById("resultsRoot");
const statusBox = document.getElementById("statusBox");
const assumptionBox = document.getElementById("assumptionBox");
const panelWattage = document.getElementById("panelWattage");

fileInput.addEventListener("change", renderPreviews);
extractButton.addEventListener("click", handleExtract);
resetButton.addEventListener("click", resetAll);
generateButton.addEventListener("click", handleGenerate);

function renderPreviews() {
  previewGrid.innerHTML = "";
  const files = Array.from(fileInput.files || []);
  files.forEach((file) => {
    const tile = document.createElement("div");
    tile.className = "preview-tile";

    if (file.type.startsWith("image/")) {
      const img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      img.alt = file.name;
      tile.appendChild(img);
    } else {
      const placeholder = document.createElement("div");
      placeholder.className = "preview-caption";
      placeholder.style.minHeight = "220px";
      placeholder.style.display = "grid";
      placeholder.style.placeItems = "center";
      placeholder.textContent = "PDF preview";
      tile.appendChild(placeholder);
    }

    const caption = document.createElement("div");
    caption.className = "preview-caption";
    caption.textContent = file.name;
    tile.appendChild(caption);
    previewGrid.appendChild(tile);
  });
}

async function handleExtract() {
  const files = Array.from(fileInput.files || []);
  if (!files.length) {
    setStatus("Upload at least one file first.", true);
    return;
  }

  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));

  setStatus("Extracting bill data with AI...");
  extractButton.disabled = true;

  try {
    const response = await fetch("/api/extract", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || "Extraction failed.");
    }

    state.bills = data.bills || [];
    state.assumptions = data.assumptions || [];
    renderAssumptions();
    renderResults();
    setStatus("Extraction completed. Review the fields below before export.");
    generateButton.disabled = state.bills.length === 0;
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    extractButton.disabled = false;
  }
}

function renderAssumptions() {
  assumptionBox.innerHTML = "";
  if (!state.assumptions.length) {
    return;
  }
  const list = document.createElement("ul");
  state.assumptions.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    list.appendChild(li);
  });
  assumptionBox.appendChild(list);
}

function renderResults() {
  resultsRoot.innerHTML = "";
  state.bills.forEach((bill, index) => {
    const card = document.createElement("section");
    card.className = "bill-card";
    card.dataset.billIndex = String(index);

    const cardHeader = document.createElement("div");
    cardHeader.className = "bill-card-header";
    cardHeader.innerHTML = `
      <div>
        <h3>Bill ${index + 1}</h3>
        <p>${escapeHtml(bill.source_name || `Upload ${index + 1}`)}</p>
      </div>
      <div class="confidence-pill">${overallConfidence(bill)} confidence</div>
    `;
    card.appendChild(cardHeader);

    const fieldGrid = document.createElement("div");
    fieldGrid.className = "field-grid";

    const fields = [
      ["utility_name", "Utility Name"],
      ["consumer_name", "Consumer Name"],
      ["consumer_number", "Consumer Number"],
      ["address", "Address"],
      ["mobile_number", "Mobile Number"],
      ["meter_number", "Meter Number"],
      ["bill_month_label", "Billing Month"],
      ["bill_year", "Billing Year"],
      ["bill_date", "Bill Date"],
      ["due_date", "Due Date"],
      ["payable_amount", "Payable Amount"],
      ["payable_after_due", "Amount After Due Date"],
      ["fixed_charges", "Fixed Charges"],
      ["excel_bill_amount", "Excel Bill Amount"],
      ["sanctioned_load_text", "Sanctioned Load"],
      ["connection_type", "Connection Type"],
      ["tariff_category", "Tariff Category"],
      ["previous_reading", "Previous Reading"],
      ["current_reading", "Current Reading"],
      ["units_consumed", "Units Consumed"],
    ];

    fields.forEach(([key, label]) => {
      fieldGrid.appendChild(renderInputGroup(index, key, label, bill[key] ?? ""));
    });

    card.appendChild(fieldGrid);

    const monthTable = document.createElement("div");
    monthTable.className = "month-table";
    const title = document.createElement("h3");
    title.textContent = "12-Month Usage History";
    monthTable.appendChild(title);

    (bill.monthly_history || []).forEach((item, monthIndex) => {
      const row = document.createElement("div");
      row.className = "month-row";
      row.innerHTML = `
        <div class="field-group">
          <label>Month</label>
          <input type="text" data-kind="month-label" data-bill-index="${index}" data-month-index="${monthIndex}" value="${escapeAttribute(item.month_label || "")}">
        </div>
        <div class="field-group">
          <label>Units</label>
          <input type="number" step="0.01" data-kind="month-units" data-bill-index="${index}" data-month-index="${monthIndex}" value="${escapeAttribute(item.units ?? "")}">
        </div>
      `;
      monthTable.appendChild(row);
    });

    card.appendChild(monthTable);

    if ((bill.validation_issues || []).length) {
      const issueList = document.createElement("ul");
      issueList.className = "issue-list";
      bill.validation_issues.forEach((issue) => {
        const li = document.createElement("li");
        li.textContent = `${issue.field}: ${issue.message}`;
        issueList.appendChild(li);
      });
      card.appendChild(issueList);
    }

    if ((bill.raw_notes || []).length) {
      const noteList = document.createElement("ul");
      noteList.className = "issue-list";
      bill.raw_notes.forEach((note) => {
        const li = document.createElement("li");
        li.textContent = note;
        noteList.appendChild(li);
      });
      card.appendChild(noteList);
    }

    resultsRoot.appendChild(card);
  });
}

function renderInputGroup(index, key, label, value) {
  const wrapper = document.createElement("div");
  wrapper.className = "field-group";
  wrapper.innerHTML = `
    <label>${label}</label>
    <input
      type="${inputTypeFor(key)}"
      step="${inputStepFor(key)}"
      data-kind="field"
      data-bill-index="${index}"
      data-key="${key}"
      value="${escapeAttribute(value)}"
    >
  `;
  return wrapper;
}

async function handleGenerate() {
  const payload = {
    panel_wattage: Number(panelWattage.value || 600),
    bills: collectBills(),
  };

  generateButton.disabled = true;
  setStatus("Generating Excel workbook...");

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Excel generation failed.");
    }

    const blob = await response.blob();
    const downloadUrl = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    const disposition = response.headers.get("content-disposition") || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    anchor.href = downloadUrl;
    anchor.download = match ? match[1] : "energybae_output.xlsx";
    anchor.click();
    URL.revokeObjectURL(downloadUrl);
    setStatus("Excel file generated and download started.");
  } catch (error) {
    setStatus(error.message, true);
  } finally {
    generateButton.disabled = false;
  }
}

function collectBills() {
  return state.bills.map((bill, index) => {
    const copy = structuredClone(bill);
    document.querySelectorAll(`[data-bill-index="${index}"][data-kind="field"]`).forEach((input) => {
      copy[input.dataset.key] = castValue(input.dataset.key, input.value);
    });
    document.querySelectorAll(`[data-bill-index="${index}"][data-kind="month-label"]`).forEach((input) => {
      const monthIndex = Number(input.dataset.monthIndex);
      copy.monthly_history[monthIndex].month_label = input.value;
    });
    document.querySelectorAll(`[data-bill-index="${index}"][data-kind="month-units"]`).forEach((input) => {
      const monthIndex = Number(input.dataset.monthIndex);
      copy.monthly_history[monthIndex].units = input.value === "" ? null : Number(input.value);
    });
    return copy;
  });
}

function inputTypeFor(key) {
  return ["bill_year", "payable_amount", "payable_after_due", "fixed_charges", "excel_bill_amount", "previous_reading", "current_reading", "units_consumed"].includes(key)
    ? "number"
    : "text";
}

function inputStepFor(key) {
  return inputTypeFor(key) === "number" ? "0.01" : "any";
}

function castValue(key, value) {
  if (value === "") {
    return null;
  }
  if (inputTypeFor(key) === "number") {
    return Number(value);
  }
  return value;
}

function overallConfidence(bill) {
  const values = Object.values(bill.confidence || {});
  if (!values.length) {
    return "Review";
  }
  const avg = values.reduce((sum, value) => sum + value, 0) / values.length;
  return `${Math.round(avg * 100)}%`;
}

function resetAll() {
  fileInput.value = "";
  previewGrid.innerHTML = "";
  resultsRoot.innerHTML = "";
  assumptionBox.innerHTML = "";
  state.bills = [];
  state.assumptions = [];
  generateButton.disabled = true;
  setStatus("");
}

function setStatus(message, isError = false) {
  statusBox.textContent = message;
  statusBox.style.color = isError ? "var(--warn)" : "var(--muted)";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('"', "&quot;");
}
