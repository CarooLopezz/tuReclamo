document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/reclamos");
    const reclamos = await response.json();

    const contenedor = document.getElementById("reclamosComunidad");
    contenedor.innerHTML = "";

    reclamos.forEach((reclamo) => {
      // Si hay imagen, usar su ruta; si no, usar una por defecto
      const fotoUrl = reclamo.foto
        ? `/${reclamo.foto}`  // 👈 asegurate de poner el slash inicial
        : "/static/images/tureclamo.png"; // imagen default

      const card = document.createElement("div");
      card.classList.add("reclamo-card");

      card.innerHTML = `
        <img src="${fotoUrl}" alt="Imagen del reclamo" class="reclamo-foto">
        <div class="reclamo-info">
          <h3>${reclamo.categoria}</h3>
          <p><strong>Dirección:</strong> ${reclamo.direccion}</p>
          <p>${reclamo.descripcion}</p>
          <p class="usuario">Reportado por: ${reclamo.usuario}</p>
          <button class="btn-borrar" data-id="${reclamo.id}">🗑️ Borrar</button>
        </div>
      `;

      contenedor.appendChild(card);
    });
  } catch (error) {
    console.error("Error cargando reclamos:", error);
  }
});

contenedor.addEventListener("click", async (e) => {
  if (e.target.classList.contains("btn-borrar")) {
    const id = e.target.getAttribute("data-id");

    // Opcional: borrar del servidor también
    await fetch(`/api/reclamos/${id}`, { method: "DELETE" });

    // Borrar visualmente del DOM
    e.target.closest(".reclamo-card").remove();
  }
});