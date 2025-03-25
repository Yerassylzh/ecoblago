document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".edit-product-btn")) return;

    const productId = PRODUCT_ID;
    window.location.href = EDIT_PRODUCT_URL.replace('0', productId);
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".delete-product-btn")) return;

    const productId = PRODUCT_ID;
    $.ajax({
        type: "POST",
        url: PRODUCT_DETAILS_URL.replace('0', productId),
        data: {
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "delete",
            product_id: productId
        },
        success: (data) => {
            showToast(gettext('Продукт успешно удален'), true);
            setTimeout(() => {
                window.location.href = CATALOG_URL;
            }, 2000);
        },
        error: (err) => {
            showToast(gettext("Произошла ошибка при удалении продукта"), false);
        }
    })
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".seller-profile")) return;

    const sellerProfile = e.target.closest(".seller-profile");
    const sellerId = parseInt(sellerProfile.querySelector(".seller-id-input").value);
    window.location.href =  PROFILEPAGE_URL.replace('0', sellerId);
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".right-arrow")) return;

    const imageContainer = e.target.closest(".images-container");
    const currentInd = parseInt(imageContainer.firstElementChild.dataset.imageIndex);
    const images = imageContainer.lastElementChild.children;
    const nextInd = (currentInd + 1) % images.length;

    imageContainer.firstElementChild.setAttribute("src", images[nextInd].getAttribute("src"));
    imageContainer.firstElementChild.dataset.imageIndex = nextInd;
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".left-arrow")) return;

    const imageContainer = e.target.closest(".images-container");
    const currentInd = parseInt(imageContainer.firstElementChild.dataset.imageIndex);
    const images = imageContainer.lastElementChild.children;
    const nextInd = (currentInd - 1 + images.length) % images.length;

    imageContainer.firstElementChild.setAttribute("src", images[nextInd].getAttribute("src"));
    imageContainer.firstElementChild.dataset.imageIndex = nextInd;
});
