function changeImage(src, element) {
    const mainImg = document.getElementById('mainImage');
    
    mainImg.style.opacity = '0';
    
    setTimeout(() => {
        mainImg.src = src;
        mainImg.style.opacity = '1';

        const thumbnails = document.querySelectorAll('.thumbnails img');
        thumbnails.forEach(thumb => thumb.classList.remove('active'));

        element.classList.add('active');
    }, 300);
}

function selectSize(element) {
    const sizes = document.querySelectorAll('.size-option');
    sizes.forEach(size => size.classList.remove('selected'));

    element.classList.add('selected');
}

document.addEventListener('DOMContentLoaded', function() {
    const firstThumbnail = document.querySelector('.thumbnails img');
    if (firstThumbnail) {
        firstThumbnail.classList.add('active');
    }
});