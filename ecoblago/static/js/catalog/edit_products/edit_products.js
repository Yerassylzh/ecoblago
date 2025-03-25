function recoverData() {
    const imagesJson = JSON.parse(document.getElementById('image_urls').textContent);
    const imageUrls = Array.from(imagesJson);

    for (let i = 0; i < imageUrls.length; i++) {
        const imageInput = document.getElementById("add-image-input" + (i + 1));
        const imageContainer = imageInput.closest(".image-container");
        const addImageLabel = imageInput.nextElementSibling;

        fetch(imageUrls[i])
            .then(response => response.blob())
            .then(blob => {
                const fileName = imageUrls[i].split("/").pop();
                const file = new File([blob], fileName, { type: blob.type });

                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);
                imageInput.files = dataTransfer.files;

                const reader = new FileReader();
                reader.onload = (e) => {
                    imageContainer.style.backgroundImage = `url(${e.target.result})`;
                    imageContainer.style.backgroundSize = 'cover';
                    imageContainer.dataset.hasImage = 'true';
                    addImageLabel.textContent = '';
                    imageInput.setAttribute('disabled', 'true');
                };

                reader.onerror = (e) => {
                    console.error("Error reading file:", e.target.error);
                };

                reader.readAsDataURL(blob);
            })
            .catch(error => {
                console.error("Fetch failed:", error);
            });
    }

    $("#product-name-input").val(title);
    $("#product-description-input").val(description);
    $("#product-cost-input").val(cost);
    $("#product-region-input").val(region);
    $("#product-city-input").val(city);
    $("#product-category-input").val(category);
    $("#product-phone-number-input").val(phoneNumber);
    $("#product-email-input").val(email);
}

function init() {
    document.title = gettext('Редактирование обявления');
    $(".profile-bar").children().first().text(gettext('Редактирование обявления'));

    $("#product-city-input").parent().parent().css("display", "block");
    recoverData();

    $("#publish-btn").attr("id", "save-btn");
    $("#save-btn").text(gettext('Сохранить изменения'));
}

init();

const regionsJson = JSON.parse(document.getElementById('regions-data').textContent);
const regions = Array.from(regionsJson);

const categoriesJson = JSON.parse(document.getElementById('categories-data').textContent);
const categories = Array.from(categoriesJson);

// Sending request to save the changes
function saveChanges() {
    let formData = getProductFormData();
    console.log(formData["gallery_images"]);
    formData.append("csrfmiddlewaretoken", CSRF_TOKEN);
    formData.append("action", "edit");

    $.ajax({
        method: "POST",
        url: EDIT_PRODUCT_URL.replace('0', PRODUCT_ID),
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $("#save-btn").text(gettext("Подождите") + "...");
            $("#save-btn").attr("disabled", "true");
        },
        success: (data) => {
            const success = data["success"];
            if (success) {
                showToast(gettext("Изменения успешно сохранены"), true);
                setTimeout(() => {
                    window.location.href = CATALOG_URL;
                }, 3000);
            } else {
                showToast(data["error"], false);
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
            showToast(gettext("Произошла ошибка при добавлении обявления"), false);
        },
        complete: function () {
            $("#save-btn").text(gettext("Сохранить изменения"));
            $("#save-btn").removeAttr("disabled");
        }
    })
}

$("#save-btn").on("click", saveChanges);
