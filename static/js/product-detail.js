// ============================================
// PRODUCT DETAIL PAGE JAVASCRIPT
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    'use strict';

    // ============================================
    // IMAGE GALLERY
    // ============================================
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainProductImage');

    thumbnails.forEach(thumb => {
        thumb.addEventListener('click', function() {
            // Update active thumbnail
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Update main image
            const imageUrl = this.dataset.image;
            if (mainImage) {
                mainImage.src = imageUrl;
            }
        });
    });

    // ============================================
    // QUANTITY CONTROL
    // ============================================
    const quantityInput = document.getElementById('quantity');
    const maxQuantity = productData.maxQuantity || 0;

    window.updateQuantity = function(change) {
        let currentValue = parseInt(quantityInput.value) || 1;
        let newValue = currentValue + change;
        
        if (newValue < 1) newValue = 1;
        if (newValue > maxQuantity && maxQuantity > 0) newValue = maxQuantity;
        
        quantityInput.value = newValue;
        
        // Update button states
        document.getElementById('decrementQty').disabled = newValue <= 1;
        document.getElementById('incrementQty').disabled = newValue >= maxQuantity;
    };

    // Validate quantity input
    quantityInput.addEventListener('change', function() {
        let value = parseInt(this.value) || 1;
        
        if (value < 1) value = 1;
        if (value > maxQuantity && maxQuantity > 0) value = maxQuantity;
        
        this.value = value;
    });

    // ============================================
    // ADD TO CART
    // ============================================
    window.addToCart = function(productId) {
        const quantity = parseInt(quantityInput.value) || 1;
        const btn = document.querySelector('.add-to-cart-btn');
        
        if (btn.disabled) {
            showToast('This product is out of stock!', 'error');
            return;
        }
        
        // Animate button
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
        btn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-check"></i> Added!';
            btn.classList.add('added');
            
            showToast(`"${productData.name}" added to cart! 🛒`, 'success');
            
            setTimeout(() => {
                btn.innerHTML = '<i class="fas fa-shopping-cart"></i> Add to Cart';
                btn.classList.remove('added');
                btn.disabled = false;
            }, 2000);
        }, 800);
    };
});
