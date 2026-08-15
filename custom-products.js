function loadAllProducts() {
    return fetch('products.js?t=' + Date.now())
        .then(res => res.text())
        .then(data => {
            const match = data.match(/const products = (\[[\s\S]*?\]);/);
            const baseProducts = match ? eval(match[1]) : [];
            const customProducts = JSON.parse(localStorage.getItem('boutique_custom_products') || '[]');
            return baseProducts.concat(customProducts);
        });
}
