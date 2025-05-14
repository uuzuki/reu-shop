document.addEventListener('DOMContentLoaded', function() {
    const sortContainer = document.getElementById('sortContainer');
    const sortButton = document.getElementById('sortButton');
    const sortDropdown = document.querySelector('.sort-dropdown');
    
    sortButton.addEventListener('click', function(e) {
        e.stopPropagation();
        sortDropdown.style.display = sortDropdown.style.display === 'block' ? 'none' : 'block';
    });
    
    document.addEventListener('click', function() {
        sortDropdown.style.display = 'none';
    });
    
    sortDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
    });
    
    const sortOptions = document.querySelectorAll('.sort-option a');
    sortOptions.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            const sortType = this.getAttribute('href').split('=')[1];
            
            sortButton.innerHTML = 'Загрузка...';
            
            fetch(window.location.pathname + `?sort=${sortType}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('products-container').innerHTML = html;
                
                updateSortButtonText(sortType);
                
                sortDropdown.style.display = 'none';
            })
            .catch(error => {
                console.error('Error:', error);
                window.location.href = this.getAttribute('href');
            });
        });
    });
    
    function updateSortButtonText(sortType) {
        const texts = {
            'newest': 'По новизне',
            'popular': 'По популярности',
            'price_asc': 'Цены: по возрастанию',
            'price_desc': 'Цены: по убыванию',
            'sale': 'SALE'
        };
        sortButton.textContent = texts[sortType] || 'Сортировать';
    }
});