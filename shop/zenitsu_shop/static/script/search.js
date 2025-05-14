document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchBtn = document.getElementById('searchBtn');
    const closeBtn = document.getElementById('closeBtn');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchTrigger = document.getElementById('searchTrigger');

    if (!searchInput || !searchResults || !searchBtn || !closeBtn || !searchOverlay || !searchTrigger) {
        console.error('Не найдены необходимые элементы поиска');
        return;
    }

    searchTrigger.addEventListener('click', function() {
        searchOverlay.style.display = 'block';
        searchInput.focus();
    });

    closeBtn.addEventListener('click', closeSearch);
    
    function closeSearch() {
        searchOverlay.style.display = 'none';
        searchResults.innerHTML = '';
        searchInput.value = '';
    }

    searchBtn.addEventListener('click', performSearch);
    searchInput.addEventListener('input', debounce(performSearch, 300));
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (query.length < 2) {
            searchResults.innerHTML = '<div class="no-results">Введите минимум 2 символа</div>';
            return;
        }
        
        searchResults.innerHTML = '<div class="loading">Поиск...</div>';
        
        fetch(`/api/search/?q=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.length > 0) {
                    renderResults(data);
                } else {
                    searchResults.innerHTML = '<div class="no-results">Ничего не найдено</div>';
                }
            })
            .catch(error => {
                console.error('Ошибка поиска:', error);
                searchResults.innerHTML = '<div class="no-results">Ошибка поиска</div>';
            });
    }

    function renderResults(products) {
        let html = '<div class="results-list">';
        
        products.forEach(product => {
            html += `
                <div class="result-item">
                    <a href="${product.url}" class="product-link">
                        <img src="${product.img_1}" alt="${product.name}" class="product-image">
                        <div class="product-details">
                            <span class="product-name">${product.name}</span>
                            <span class="product-price">${product.price} ₽</span>
                        </div>
                    </a>
                </div>
            `;
        });
        
        html += '</div>';
        searchResults.innerHTML = html;
    }

    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
});