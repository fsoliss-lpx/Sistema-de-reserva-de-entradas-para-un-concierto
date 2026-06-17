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
                        // Evento click provisional para el Sprint 3
                        divAsiento.addEventListener("click", () => {
                            alert(`Seleccionaste el asiento ${asiento.numero_asiento}. El control optimista se aplicará en el Sprint 3.`);
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

    // Cargar los asientos al abrir la página
    cargarAsientos();
});