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
         
        </div>
      `;

      contenedor.appendChild(card);
    });
  } catch (error) {
    console.error("Error cargando reclamos:", error);
  }
});

document.getElementById("loginForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const data = {
        email: form.email.value,
        password: form.password.value
    };
    console.log("Datos enviados:", data);
    const res = await fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    const result = await res.json();
    console.log(result);

    if (res.ok) {
        localStorage.setItem("token", result.token);
        localStorage.setItem("role", result.role);
        localStorage.setItem("username", result.username);
        window.location.href = "/dashboard";
    } else {
        alert(result.message);
    }
});



async function borrar(id) {
  await fetch(`/api/reclamos/borrar/${id}`, { 
      method: "DELETE",
      headers: { "Authorization": "Bearer " + localStorage.getItem("token") }
  });
  location.reload();
}
