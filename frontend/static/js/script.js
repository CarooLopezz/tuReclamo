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

        // 🔥 Redirección según el rol
        window.location.href = result.redirect; 
    } else {
        alert(result.message);
    }

});

/* manejo de peteciones post en el register y guarda el token en local storage */