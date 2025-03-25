class DialogsManager {
    static getRegionsDialogWidget() {
        let widget =
            `<dialog class="popup" id="regions-dialog">
        <div style="padding: 1rem;">
          <div class="row options-row">     
      `;

        for (let region of regions) {
            widget +=
                `<div style="margin-bottom: 0.5rem;" class="col-12 col-md-6 col-xl-4">
          <div class="select-option">
            <i class="fa-solid fa-city" style="color: var(--txt-primary); font-size: 1rem; margin: 0 0.5rem;"></i>
            <p>${region}</p>
          </div>
        </div>`;
        }

        widget +=
            ` </div>
        </div>
        </dialog>`;

        return widget;
    };

    static getCitiesDialogWidget(cities) {
        let widget =
            `<dialog class="popup" id="cities-dialog">
        <div style="padding: 1rem;">
          <div class="row options-row">     
      `;

        for (let city of cities) {
            widget +=
                `<div style="margin-bottom: 0.5rem;" class="col-12 col-md-6 col-xl-4">
          <div class="select-option">
            <i class="fa-solid fa-city" style="color: var(--txt-primary); font-size: 1rem; margin: 0 0.5rem;"></i>
            <p>${city}</p>
          </div>
        </div>`;
        }

        widget +=
            ` </div>
        </div>
        </dialog>`;

        return widget;
    };

    static getCategoriesDialogWidget() {
        let widget =
            `<dialog class="popup" id="categories-dialog">
        <div style="padding: 1rem;">
          <div class="row options-row">     
      `;

        for (let category of categories) {
            widget +=
                `<div style="margin-bottom: 0.5rem;" class="col-12 col-md-6 col-xl-4">
          <div class="select-option">
            <i class="fa-solid fa-list" style="color: var(--txt-primary); font-size: 1rem; margin: 0 0.5rem;"></i>
            <p>${category}</p>
          </div>
        </div>`;
        }

        widget +=
            ` </div>
        </div>
        </dialog>`;
        return widget;
    };
}

function displayCitiesDialog(region) {
    $.ajax({
        method: "POST",
        url: CREATE_PRODUCT_URL,
        data: {
            "region": region,
            "action": "get-cities-by-region",
            "csrfmiddlewaretoken": CSRF_TOKEN,
        },
        dataType: "json",
        beforeSend: () => {
            $(".popup").remove();
        },
        success: (data) => {
            const success = data["success"];
            if (!success) {
                showToast(gettext('Произошла ошибка при получении городов'), false);
                return;
            }

            const cities = data["cities"];
            const citiesDialogWidget = DialogsManager.getCitiesDialogWidget(cities);
            $("main").prepend(citiesDialogWidget);
        },
        error: (xhr, errmsg, err) => {
            showToast(gettext("Произошла ошибка при получении городов"), false);
            console.log(xhr.status + ":" + xhr.responseText)
        },
        complete: () => {
            const dialog = document.querySelector("dialog");
            dialog.showModal();
        }
    })
}

// Displaying categories dialog
document.addEventListener("click", (e) => {
    if (document.querySelector(".popup") != null || !eventMatches(e, "#product-category-input")) return;
    console.log("here");


    $("main").prepend(DialogsManager.getCategoriesDialogWidget());
    const dialog = document.querySelector(".popup");
    dialog.showModal();
});

// Displaying regions dialog
document.addEventListener("click", (e) => {
    if (document.querySelector(".popup") != null || !eventMatches(e, "#product-region-input")) return;

    $("main").prepend(DialogsManager.getRegionsDialogWidget());
    const dialog = document.querySelector(".popup");
    dialog.showModal();
});

// Displaying cities dialog
document.addEventListener("click", (e) => {
    if (document.querySelector(".popup") != null || !eventMatches(e, "#product-city-input")) return;

    displayCitiesDialog(document.querySelector("#product-region-input").value);
});

// Choosing category
document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".select-option") || !eventMatches(e, "#categories-dialog")) return;

    const category = e.target.closest(".select-option").querySelector("p").textContent;
    $("#product-category-input").val(category);
    $(".popup").remove();
});

// Choosing region
document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".select-option") || !eventMatches(e, "#regions-dialog")) return;

    const region = e.target.closest(".select-option").querySelector("p").textContent;
    $("#product-region-input").val(region);
    $(".popup").remove();

    $("#product-city-input").parent().parent().css("display", "block");
});

// Choosing city
document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".select-option") || !eventMatches(e, "#cities-dialog")) return;

    const city = e.target.closest(".select-option").querySelector("p").textContent;
    $("#product-city-input").val(city);
    $(".popup").remove();
});

function getProductFormData() {
    const title = $("#product-name-input").val();
    const category = $("#product-category-input").val();
    const region = $("#product-region-input").val();
    const city = $("#product-city-input").val();
    const phone_number = $("#product-phone-number-input").val();
    const cost = $("#product-cost-input").val();
    const description = $("#product-description-input").val();
    const email = $("#product-email-input").val();

    let images = [];
    addImageInputs.forEach((imageInput) => {
        if (imageInput.files.length > 0) {
            images.push(imageInput.files[0]);
        }
    });

    let formData = new FormData();
    formData.append("title", title);
    formData.append("category_name", category);
    formData.append("region_name", region);
    formData.append("city_name", city);
    formData.append("phone_number", phone_number);
    formData.append("cost", cost);
    formData.append("description", description);
    formData.append("email", email);
    images.forEach((image, index) => {
        formData.append('gallery_images', image);
    });

    return formData;
}

// Adding images to the image containers
const addImageInputs = document.querySelectorAll('.add-image-input');
addImageInputs.forEach((imageInput) => {
    imageInput.onchange = () => {
        const imageContainer = imageInput.closest(".image-container");
        const hasImage = imageContainer.getAttribute('data-has-image');
        const addImageLabel = imageInput.nextElementSibling;

        if (hasImage === 'false') {
            const reader = new FileReader();
            reader.onload = (e) => {
                imageContainer.style.backgroundImage = `url(${e.target.result})`
                imageContainer.style.backgroundSize = 'cover';
                imageContainer.dataset.hasImage = 'true';
                addImageLabel.textContent = '';
                imageInput.setAttribute('disabled', 'true');
            }
            reader.readAsDataURL(imageInput.files[0]);
        }
    };
});
