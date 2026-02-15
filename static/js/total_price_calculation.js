document.addEventListener("DOMContentLoaded", () => {
  const qtySelect = document.getElementById("id_quantity");
  const unitPrice = parseFloat(document.getElementById("unit-price").dataset.price);
  const totalEl = document.getElementById("total-price");

  qtySelect.addEventListener("change", () => {
    totalEl.textContent = (qtySelect.value * unitPrice).toFixed(2);
  });
});