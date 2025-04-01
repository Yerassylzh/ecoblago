class ProductsManager {
    getProductWidget(product) {
        function formatCost(cost) {
            return cost.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
        }

        return `
        <div class="col-6 col-md-4 col-xl-3">
          <div class="product">
            <input type="hidden" class="product-id-input" value="${product.id}">
            <div class="product-image">
              <img src="${product.main_image.url}" alt="product">
            </div>
            <div class="product-info">
              <div class="text-section">
                <h3 class="product-title">${product.title.slice(0, 30)}</h3>
                <p class="product-price">${formatCost(product.cost)} тг</p>
              </div>
              <div class="like-section">
                <i class="fa-regular fa-heart like-empty" style="display: ${product.is_liked ? 'none' : 'block'};"></i>
                <i class="fa-solid fa-heart like-full" style="display: ${product.is_liked ? 'block' : 'none'};"></i>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    addProduct(product) {
        const productWidget = this.getProductWidget(product);
        document.querySelector('.products').insertAdjacentHTML('beforeend', productWidget);
    }

    removeAllProducts() {
        document.querySelector('.products').innerHTML = '';
    }
};


window.ProductsManager = ProductsManager;
