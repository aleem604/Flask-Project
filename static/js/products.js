// ============================================
// PRODUCTS PAGE - JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ============================================
    // FILTER FUNCTIONALITY
    // ============================================
    const filterBtns = document.querySelectorAll('.filter-btn');
    const productsGrid = document.getElementById('productsGrid');
    const productCards = document.querySelectorAll('.product-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const filter = this.dataset.filter;
            
            productCards.forEach(card => {
                if (filter === 'all' || card.dataset.category === filter) {
                    card.style.display = '';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });

            // Show toast notification
            showToast(`Showing ${filter === 'all' ? 'all' : filter} products`, 'info');
        });
    });

    // ============================================
    // SORT FUNCTIONALITY
    // ============================================
    const sortSelect = document.getElementById('sortSelect');
    
    sortSelect.addEventListener('change', function() {
        const sortBy = this.value;
        const cards = Array.from(productCards);
        
        cards.sort((a, b) => {
            switch(sortBy) {
                case 'newest':
                    return new Date(b.dataset.date) - new Date(a.dataset.date);
                case 'popular':
                    return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);
                case 'price-low':
                    return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
                case 'price-high':
                    return parseFloat(b.dataset.price) - parseFloat(a.dataset.price);
                case 'rating':
                    return parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating);
                default:
                    return 0;
            }
        });

        // Reorder cards
        cards.forEach(card => {
            productsGrid.appendChild(card);
        });

        showToast('Products sorted!', 'success');
    });

    // ============================================
    // VIEW TOGGLE (Grid/List)
    // ============================================
    const viewBtns = document.querySelectorAll('.view-btn');
    
    viewBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            viewBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');

            const view = this.dataset.view;
            productsGrid.className = 'products-grid';
            
            if (view === 'list') {
                productsGrid.classList.add('list-view');
                showToast('List view enabled', 'info');
            } else {
                showToast('Grid view enabled', 'info');
            }
        });
    });

    // ============================================
    // WISHLIST TOGGLE
    // ============================================
    const wishlistBtns = document.querySelectorAll('.wishlist-btn');
    
    wishlistBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            const icon = this.querySelector('i');
            
            if (icon.classList.contains('far')) {
                icon.classList.remove('far');
                icon.classList.add('fas');
                this.classList.add('active');
                showToast('Added to wishlist! ❤️', 'success');
                
                // Add animation
                this.style.animation = 'pulse 0.5s ease';
                setTimeout(() => {
                    this.style.animation = '';
                }, 500);
            } else {
                icon.classList.remove('fas');
                icon.classList.add('far');
                this.classList.remove('active');
                showToast('Removed from wishlist', 'info');
            }
        });
    });

    // ============================================
    // ADD TO CART
    // ============================================
    const addToCartBtns = document.querySelectorAll('.add-to-cart');
    
    addToCartBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            
            const productId = this.dataset.productId;
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-title').textContent.trim();
            
            // Animate button
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
            this.disabled = true;
            
            // Simulate adding to cart
            setTimeout(() => {
                this.innerHTML = '<i class="fas fa-check"></i> Added!';
                this.style.background = '#2ecc71';
                
                showToast(`"${productName}" added to cart! 🛒`, 'success');
                
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                    this.style.background = '';
                    this.disabled = false;
                }, 2000);
            }, 500);
        });
    });

    // ============================================
    // BUY NOW
    // ============================================
    const buyNowBtns = document.querySelectorAll('.buy-now');
    
    buyNowBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (this.disabled) return;
            
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-title').textContent.trim();
            
            showToast(`Redirecting to checkout for "${productName}"...`, 'info');
            
            setTimeout(() => {
                // Simulate redirect
                window.location.href = '/checkout';
            }, 1000);
        });
    });

    // ============================================
    // QUICK VIEW MODAL
    // ============================================
    const quickViewBtns = document.querySelectorAll('.quick-view-btn');
    const modal = document.getElementById('quickViewModal');
    const closeModal = document.getElementById('closeModal');
    
    quickViewBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const productCard = this.closest('.product-card');
            
            // Get product data
            const title = productCard.querySelector('.product-title').textContent.trim();
            const category = productCard.querySelector('.product-category').textContent.trim();
            const description = productCard.querySelector('.product-description').textContent.trim();
            const price = productCard.querySelector('.current-price').textContent.trim();
            const originalPrice = productCard.querySelector('.original-price');
            const rating = productCard.dataset.rating || '0';
            const reviewCount = productCard.querySelector('.rating-count').textContent.trim();
            const stockStatus = productCard.querySelector('.stock-status');
            const imageElement = productCard.querySelector('.product-image img');
            const placeholder = productCard.querySelector('.image-placeholder');
            
            // Populate modal
            document.getElementById('modalTitle').textContent = title;
            document.getElementById('modalCategory').textContent = category;
            document.getElementById('modalDescription').textContent = description;
            
            // Price
            const modalPrice = document.getElementById('modalPrice');
            if (originalPrice) {
                modalPrice.innerHTML = `
                    <span class="original-price">${originalPrice.textContent}</span>
                    <span class="current-price">${price}</span>
                `;
            } else {
                modalPrice.innerHTML = `
                    <span class="current-price">${price}</span>
                `;
            }
            
            // Rating
            const modalStars = document.getElementById('modalStars');
            modalStars.innerHTML = generateStars(parseFloat(rating));
            document.getElementById('modalReviewCount').textContent = reviewCount;
            
            // Stock
            const modalStock = document.getElementById('modalStock');
            if (stockStatus) {
                modalStock.innerHTML = stockStatus.innerHTML;
            }
            
            // Image
            const modalImage = document.getElementById('modalProductImage');
            const modalIcon = document.getElementById('modalProductIcon');
            
            if (imageElement) {
                modalImage.src = imageElement.src;
                modalImage.style.display = 'block';
                modalIcon.style.display = 'none';
            } else {
                modalImage.style.display = 'none';
                modalIcon.style.display = 'block';
                modalIcon.className = placeholder ? placeholder.querySelector('i').className : 'fas fa-image';
            }
            
            // Show modal
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        });
    });
    
    // Close modal
    closeModal.addEventListener('click', closeQuickView);
    modal.addEventListener('click', function(e) {
        if (e.target === this) {
            closeQuickView();
        }
    });
    
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) {
            closeQuickView();
        }
    });
    
    function closeQuickView() {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
    
    function generateStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= Math.floor(rating)) {
                stars += '<i class="fas fa-star"></i>';
            } else if (i - 0.5 <= rating) {
                stars += '<i class="fas fa-star-half-alt"></i>';
            } else {
                stars += '<i class="far fa-star"></i>';
            }
        }
        return stars;
    }

    // ============================================
    // TOAST NOTIFICATION
    // ============================================
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toastMessage');
    const toastIcon = document.getElementById('toastIcon');
    let toastTimeout;

    function showToast(message, type = 'success') {
        toastMessage.textContent = message;
        toast.className = 'toast';
        toast.classList.add(type);
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        toastIcon.className = icons[type] || icons.success;
        toast.classList.add('show');
        
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    // ============================================
    // KEYBOARD SHORTCUTS
    // ============================================
    document.addEventListener('keydown', function(e) {
        // Ctrl + F for filter focus
        if (e.ctrlKey && e.key === 'f') {
            e.preventDefault();
            const filterInput = document.querySelector('.filter-group input');
            if (filterInput) filterInput.focus();
        }
        
        // Ctrl + S for sort focus
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            sortSelect.focus();
        }
    });

    // ============================================
    // SCROLL TO TOP BUTTON (if not in base.html)
    // ============================================
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-top';
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        left: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        z-index: 1000;
        display: none;
        align-items: center;
        justify-content: center;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    `;
    
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 400) {
            scrollBtn.style.display = 'flex';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ============================================
    // PRODUCT CARD IMAGE ZOOM ON HOVER
    // ============================================
    document.querySelectorAll('.product-image').forEach(imageContainer => {
        const img = imageContainer.querySelector('img');
        if (img) {
            imageContainer.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = (e.clientX - rect.left) / rect.width * 100;
                const y = (e.clientY - rect.top) / rect.height * 100;
                img.style.transformOrigin = `${x}% ${y}%`;
            });
        }
    });

    // ============================================
    // INFINITE SCROLL (Optional)
    // ============================================
    // Uncomment if you want infinite scroll
    /*
    let loading = false;
    let page = 1;
    const loadMoreBtn = document.querySelector('.load-more-btn');
    
    window.addEventListener('scroll', function() {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
            if (!loading) {
                loading = true;
                page++;
                // Fetch more products via AJAX
                fetch(`/api/products?page=${page}`)
                    .then(response => response.json())
                    .then(data => {
                        // Append products
                        loading = false;
                    });
            }
        }
    });
    */

    console.log('🚀 Products page initialized successfully!');
});