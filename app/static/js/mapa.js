document.addEventListener("DOMContentLoaded", () => {
    const gridAsientos = document.getElementById("grid-asientos");

    // Función para consultar los asientos a la API del backend (RF-02)
    function cargarAsientos() {
        fetch('/api/asientos')
            .then(response => {
                if (!response.ok) {
                    throw new Error("No se pudo cargar el aforo.");
                }
                return response.json();
            })
            .then(asientos => {
                gridAsientos.innerHTML = ""; // Limpiar el contenedor

                asientos.forEach(asiento => {
                    // Crear un elemento div por cada asiento
                    const divAsiento = document.createElement("div");
                    divAsiento.classList.add("asiento-box");
                    divAsiento.innerText = asiento.numero_asiento;

                    // Asignar color dinámico basado en el estado (Asignación Cromática en Tiempo Real)
                    if (asiento.estado === "DISPONIBLE") {
                        divAsiento.classList.add("st-disponible");
                        divAsiento.addEventListener("click", () => {solicitarReserva(asiento.id_asiento);
                        });
                    } else if (asiento.estado === "RESERVADO_TEMPORAL") {
                        divAsiento.classList.add("st-reservado");
                    } else if (asiento.estado === "VENDIDO") {
                        divAsiento.classList.add("st-vendido");
                    }

                    gridAsientos.appendChild(divAsiento);
                });
            })
            .catch(error => console.error("Error al pintar el mapa asíncrono:", error));
    }
    
    function solicitarReserva(idAsiento) {
    fetch('/api/reservar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_asiento: idAsiento })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            // AGREGADO: Alerta de éxito y redirección inmediata a la ruta de pagos usando el ID que envió Python
            alert(data.message);
            window.location.href = '/pago/' + data.id_reserva; 
        } else {
            // Si falla por condición de carrera, muestra el error y recarga los colores
            alert("Error: " + data.message);
            cargarAsientos(); 
        }
    })
    .catch(err => console.error("Error en la reserva:", err));
}

    // Cargar los asientos al abrir la página
    cargarAsientos();
});