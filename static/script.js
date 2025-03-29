document.addEventListener("DOMContentLoaded", function () {
    const inkOptions = document.querySelectorAll(".ink-option");

    inkOptions.forEach(option => {
        option.addEventListener("click", function () {
            const checkbox = this.querySelector("input");

            // Zmiana stanu checkboxa
            checkbox.checked = !checkbox.checked;

            // Dodanie/Usunięcie klasy aktywnej
            this.classList.toggle("active");
        });
    });
});