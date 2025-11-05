console.log("Dashboard cargado correctamente.");

async function cargarReclamos() {
  try {
    const response = await fetch("/api/reclamos");
    const reclamos = await response.json();

    const container = document.getElementById("reclamosComunidad");
    if (!container) {
      console.error("No se encontró el contenedor de reclamos");
      return;
    }

    container.innerHTML = "";

    reclamos.forEach(r => {
      const card = document.createElement("div");
      card.classList.add("reclamo-card");

      // Imagen por defecto
      let fotoSrc = "/static/images/tureclamo.png";

      if (r.foto) {
        if (r.foto.startsWith("data:image")) {
          // viene en base64 completa
          fotoSrc = r.foto;
        } else if (r.foto.startsWith("/static/")) {
          // imagen guardada en static
          fotoSrc = r.foto;
        } else if (r.foto.startsWith("images/")) {
          // si se guardó en carpeta
          fotoSrc = `/${r.foto}`;
        } else if (r.foto.match(/\.(png|jpg|jpeg)$/)) {
          // si solo vino el nombre de la imagen
          fotoSrc = `/static/images/${r.foto}`;
        } else {
          // si vino base64 sin prefijo
          fotoSrc = `data:image/jpeg;base64,${r.foto}`;
        }
      }

      // Crear card
      card.innerHTML = `
        <img src="${fotoSrc}" alt="Imagen del reclamo" onerror="this.src='/static/images/tureclamo.png'">
        <div class="reclamo-info">
          <h3>${r.categoria || "Sin categoría"}</h3>
          <p><strong>Dirección:</strong> ${r.direccion || "No especificada"}</p>
          <p>${r.descripcion || ""}</p>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (err) {
    console.error("Error al cargar los reclamos:", err);
    const container = document.getElementById("reclamosComunidad");
    if (container) container.innerHTML = `<p>Error al cargar los reclamos.</p>`;
  }
}

document.addEventListener("DOMContentLoaded", cargarReclamos);
