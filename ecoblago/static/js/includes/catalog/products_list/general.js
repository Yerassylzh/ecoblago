document.addEventListener("click", (e) => {
    if (e.target.closest(".like-empty") != null) {
        let like = e.target.closest(".like-empty");
        addToFavourites(like);
    } else if (e.target.closest(".like-full") != null) {
        let like = e.target.closest(".like-full");
        removeFromFavourites(like);
    }
});

function addToFavourites(like) {
    like.style.display = 'none';
    like.nextElementSibling.style.display = 'block';
    $.ajax({
        type: 'POST',
        url: CATALOG_URL,
        data: {
            "product_id": like.parentElement.parentElement.parentElement.querySelector('.product-id-input').value,
            "csrfmiddlewaretoken": CSRF_TOKEN,
            "action": "add-product-to-favourites",
        },
        success: function(data) {
            const success = data["success"];
            if (success) {
                showToast(gettext("Product was added to favorites"), true);
            } else {
                showToast(gettext("Product was not added to favorites"), false);
            }
        }
    });
}

function removeFromFavourites(like) {
    like.style.display = 'none';
    like.previousElementSibling.style.display = 'block';
    $.ajax({
        type: 'POST',
        url: CATALOG_URL,
        data: {
            "product_id": like.parentElement.parentElement.parentElement.querySelector('.product-id-input').value,
            "csrfmiddlewaretoken": CSRF_TOKEN,
            "action": "remove-product-from-favourites",
        },
        success: function(data) {
            const success = data["success"];
            if (success) {
                showToast(gettext("Product was removed from favorites"), true);
            } else {
                showToast(gettext("Product was not removed from favorites"), false);
            }
        }
    });
}

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".product-image")) {
        return;
    }

    const productId = e.target.closest(".product-image").previousElementSibling.value;
    window.location.href = `/catalog/product_details/${productId}`;
});