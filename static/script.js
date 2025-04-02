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
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.add-to-collection').forEach(button => {
        button.addEventListener('click', function () {
            const cardElement = this.closest('.card');
            const cardId = cardElement.dataset.cardId; // Pobieramy ID karty z atrybutu data-card-id
            window.location.href = `/add_to_collection/${cardId}`;
        });
    });

    document.querySelectorAll('.remove-from-collection').forEach(button => {
        button.addEventListener('click', function () {
            const cardElement = this.closest('.card');
            const cardId = cardElement.dataset.cardId; // Pobieramy ID karty
            window.location.href = `/remove_from_collection/${cardId}`;
        });
    });
});