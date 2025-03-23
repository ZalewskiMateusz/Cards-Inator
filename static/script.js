document.addEventListener('click', function(event) {
    if (event.target.classList.contains('add-to-collection')) {
        const cardId = event.target.closest('.card').querySelector('h2').textContent;
        fetch(`/add_to_collection/${cardId}`)
            .then(() => location.reload());
    } else if (event.target.classList.contains('remove-from-collection')) {
        const cardId = event.target.closest('.card').querySelector('h2').textContent;
        fetch(`/remove_from_collection/${cardId}`)
            .then(() => location.reload());
    }
});