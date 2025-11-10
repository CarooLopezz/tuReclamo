

document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/reclamos/director");
  const reclamos = await res.json();

  const tbody = document.getElementById("tbodyReclamos");
  tbody.innerHTML = "";

  if (reclamos.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="7" class="text-center text-muted">No hay reclamos cargados aún.</td>
      </tr>`;
    return;
  }

  reclamos.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td>${r.usuario}</td>
        <td>${r.categoria}</td>
        <td>${r.direccion}</td>
        <td>
          <img src="${r.foto ?? '/static/images/tureclamo.png'}" style="height:60px; border-radius:6px;">
        </td>
        <td>${r.descripcion}</td>
        <td>
          <button onclick="borrar(${r.id})" class="btn btn-danger btn-sm">Borrar</button>
        </td>
      </tr>
    `;
  });
});

async function borrar(id){
  if (!confirm("¿Seguro que querés borrar este reclamo?")) return;

  try {
    const res = await fetch(`/api/reclamos/director/borrar/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const errorText = await res.text();
      alert("Error al borrar el reclamo: " + errorText);
      return;
    }

    // Si se borró correctamente, eliminar la fila sin recargar toda la página
    document.getElementById(`reclamo-${id}`).remove();
  } catch (error) {
    console.error("Error al eliminar:", error);
    alert("Error al intentar borrar el reclamo.");
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("/api/reclamos/director");
  const reclamos = await res.json();
  const tbody = document.getElementById("tbodyReclamos");

  tbody.innerHTML = "";

  if (reclamos.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No hay reclamos cargados aún.</td></tr>`;
    return;
  }

  reclamos.forEach(r => {
    tbody.innerHTML += `
      <tr id="reclamo-${r.id}">
        <td>${r.usuario}</td>
        <td>${r.categoria}</td>
        <td>${r.direccion}</td>
        <td><img src="${r.foto ?? '/static/images/tureclamo.png'}" style="height:60px; border-radius:6px;"></td>
        <td>${r.descripcion}</td>
        <td>
          <select id="estado-${r.id}" class="form-select form-select-sm">
            <option value="pendiente">Pendiente</option>
            <option value="en proceso">En proceso</option>
            <option value="resuelto">Resuelto</option>
          </select>
        </td>
        <td>
          <button onclick="notificar(${r.id}, '${r.usuario}')" class="btn btn-warning btn-sm">Notificar</button>
        </td>
        <td>
          <button onclick="borrar(${r.id})" class="btn btn-danger btn-sm">🗑️</button>
        </td>
      </tr>
    `;
  });
});



// 📨 Función para notificar por correo
async function notificar(id, usuario) {
  const estado = document.getElementById(`estado-${id}`).value;

  const res = await fetch(`/api/reclamos/${id}/notificar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ estado }),
  });

  const data = await res.json();
  if (res.ok) {
    alert(`Se notificó a ${usuario}: el reclamo está "${estado}".`);
  } else {
    alert("Error al notificar: " + data.error);
  }


}
