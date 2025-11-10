document.addEventListener("DOMContentLoaded", async () => {
try {
    const response = await fetch("/api/reclamos/director");
    const reclamos = await response.json();
    const contenedor = document.getElementById("reclamosComunidad");
    contenedor.innerHTML = "";

    reclamos.forEach((reclamo) => {
      const fotoUrl = reclamo.foto
        ? `${reclamo.foto}`
        : "/static/images/tureclamo.png";

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

    // 👇 El listener va dentro del try
    contenedor.addEventListener("click", async (e) => {
      if (e.target.classList.contains("btn-borrar")) {
        const id = e.target.getAttribute("data-id");

        if (!confirm("¿Seguro que deseas borrar este reclamo?")) return;

        try {
          const respuesta = await fetch(`/api/reclamos/borrar/${id}`, {
            method: "DELETE",
          });

          if (respuesta.ok) {
            alert("Reclamo eliminado correctamente");
            e.target.closest(".reclamo-card").remove();
          } else {
            const error = await respuesta.json();
            alert("Error al borrar: " + (error.error || "Error desconocido"));
          }
        } catch (error) {
          console.error("Error al borrar reclamo:", error);
          alert("Error de conexión con el servidor");
        }
      }
    });
  } catch (error) {
    console.error("Error cargando reclamos:", error);
  }
});