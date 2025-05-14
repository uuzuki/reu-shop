document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('filterModal');
    const openBtn = document.getElementById('openFilterModal');
    const closeBtn = document.querySelector('.modal .close');

    openBtn.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});