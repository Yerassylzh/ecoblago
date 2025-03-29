const regionsJson = JSON.parse(document.getElementById('regions-data').textContent);
const regions = Array.from(regionsJson);

const categoriesJson = JSON.parse(document.getElementById('categories-data').textContent);
const categories = Array.from(categoriesJson);

// Sending request to create a product
function createProduct() {
    let formData = getProductFormData();
    formData.append("csrfmiddlewaretoken", CSRF_TOKEN);
    formData.append("action", "create-product");

    $.ajax({
        method: "POST",
        url: CREATE_PRODUCT_URL,
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $("#publish-btn").text(gettext("Подождите") + "...");
            $("#publish-btn").attr("disabled", "true");
        },
        success: (data) => {
            const success = data["success"];
            if (success) {
                showToast(gettext('Объявление успешно добавлено'), true);
                setTimeout(() => {
                    window.location.href = CATALOG_URL;
                }, 3000);
            } else {
                showToast(data["error"], false);
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
            showToast(gettext('Произошла ошибка при добавлении обявления'), false);
        },
        complete: function () {
            $("#publish-btn").text(gettext('Подать объявление'));
            $("#publish-btn").removeAttr("disabled");
        }
    })
}

$("#publish-btn").on("click", createProduct);