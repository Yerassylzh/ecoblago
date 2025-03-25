$(".like-section").remove();

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".product-image")) {
        return;
    }

    const productId = e.target.closest(".product-image").previousElementSibling.value;
    window.location.href = `/catalog/product_details/${productId}`;
});
