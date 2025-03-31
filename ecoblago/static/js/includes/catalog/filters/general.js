let filterSettings = new FilterSettings();
let productsManager = new ProductsManager();
let moreFilters = new DialogMoreFilters();
let dialogsManger = new DialogsManager();

function _onFindProductsClicked(url) {
    const search = $("#filter-text-input").val();
    let region, city;
    if ($("#location-filter-input").val() == '') {
        region = '';
        city = '';
    } else {
        let [first, second] = $("#location-filter-input").val().split(",").map(item => item.trim());
        region = first;
        city = second;
    }

    filterSettings.content = search;
    filterSettings.region = region;
    filterSettings.city = city;

    let data = {
        "csrfmiddlewaretoken": CSRF_TOKEN,
        "city": city,
        "action": "filter-products",
    };

    data = {...data, ...filterSettings.toDict() };

    $.ajax({
        method: "POST",
        url: url,
        data: data,
        dataType: "json",
        beforeSend: () => {
            $("#filter-btn").text(gettext("Подождите") + "...");
            $("#filter-btn").prop('disabled', true);
        },
        success: (data) => {
            const success = data["success"];
            if (!success) {
                showToast(data["error"], false);
                return;
            }

            productsManager.removeAllProducts();
            data["products"].forEach(product => {
                productsManager.addProduct(product);
            });

            if (data["products"].length == 0) {
                showToast(gettext("Не найдено товаров по вашему запросу"), false);
            }
        },
        error: (error) => {
            showToast(gettext("Произошла ошибка при фильтрации товаров"), false);
            console.error("Error fetching products:", error);
        },
        complete: () => {
            $("#filter-btn").text(gettext("Поиск"));
            $("#filter-btn").prop('disabled', false);
        }
    });
}

$("#location-filter-input").on("focus", displayRegions);

function displayRegions() {
    $.ajax({
        type: "GET",
        url: CATALOG_URL,
        data: {
            "action": "get-regions",
        },
        dataType: "json",
        success: (data) => {
            const success = data["success"];
            if (!success) {
                return;
            }

            let main = document.querySelector("main");
            $("main").prepend(dialogsManger.getNewDialogWidget("regions-dialog"));

            let regions = data["regions"];
            dialogsManger.insertLocationOptions(regions, "regions-dialog");
            document.getElementById("regions-dialog").showModal();
        },
        error: function(error) {
            console.error("Error fetching regions:", error);
        }
    });

}

// as soon as the region was selected, we display city options
document.addEventListener("click", (e) => {
    if (!eventMatches(e, "#regions-dialog") || !eventMatches(e, ".select-option")) {
        return;
    }

    let region;
    if (e.target.classList.contains("select-option")) {
        region = e.target.lastElementChild.textContent;
    } else {
        if (e.target.tagName != 'P') {
            region = e.target.nextElementSibling.textContent;
        } else {
            region = e.target.textContent;
        }
    }

    $.ajax({
        method: "GET",
        url: CATALOG_URL,
        data: {
            "action": "get-cities",
            "region": region,
        },
        dataType: "json",
        beforeSend: () => {
            $("#filter-text-input").attr("value", "");
        },
        success: (data) => {
            const success = data["success"];
            if (!success) {
                showToast(gettext("Не удалось получить список городов"), false);
                return;
            }

            $("#location-filter-input").attr("value", region);
            $("#regions-dialog").remove();

            $("main").prepend(dialogsManger.getNewDialogWidget("cities-dialog"));
            let cities = data["cities"];
            dialogsManger.insertLocationOptions(cities, "cities-dialog");
            document.getElementById("cities-dialog").showModal();
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        }
    });
});

// When city option was chosen
document.addEventListener("click", (e) => {
    if (!eventMatches(e, "#cities-dialog") || !eventMatches(e, ".select-option")) {
        return;
    }

    let city;
    if (e.target.classList.contains("select-option")) {
        city = e.target.lastElementChild.textContent;
    } else {
        if (e.target.tagName == 'P') {
            city = e.target.textContent;
        } else {
            city = e.target.closest("i").nextElementSibling.textContent;
        }
    }

    $("#location-filter-input").attr("value", $("#location-filter-input").attr("value") + ", " + city);
    $("#cities-dialog").remove();
});

// more filters
document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".more-filters-btn")) {
        return;
    }

    $.ajax({
        method: "GET",
        url: CATALOG_URL,
        data: {
            "action": "get-categories",
        },
        beforeSend: () => {
            let miniPopup = document.createElement("dialog");
            miniPopup.setAttribute("class", "mini-popup");
            miniPopup.setAttribute("id", "mini-popup");
            $("main").prepend(miniPopup);
        },
        success: (data) => {
            const success = data["success"];
            if (!success) {
                showToast(data["error"], false);
                return;
            }

            $("#mini-popup").html(moreFilters.getDialogInnerHtml(data["categories"]));
            moreFilters.setupCostRegulator();
            moreFilters.recoverSavedSettings();
        },
        error: (error) => {
            showToast(gettext("Произошла ошибка при фильтрации товаров"), false);
            console.error("Error fetching products:", error);
        },
        complete: () => {
            document.getElementById("mini-popup").showModal();
        }
    })
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, "#save-filters-btn")) {
        return;
    }

    let categories = document.querySelector(".filter-categories").querySelectorAll("input");
    let selectedCategories = [];
    for (let category of categories) {
        if (category.checked) {
            selectedCategories.push(category.nextElementSibling.textContent);
        }
    }
    filterSettings.categories = selectedCategories;

    let minPrice = document.getElementById("min-price").value;
    let maxPrice = document.getElementById("max-price").value;
    filterSettings.minCost = minPrice;
    filterSettings.maxCost = maxPrice;

    let sortingRules = document.querySelector(".filter-sortingrules").querySelectorAll("input");
    for (let rule of sortingRules) {
        if (rule.checked) {
            filterSettings.sortingRule = rule.nextElementSibling.textContent;
            break;
        }
    }

    showToast(gettext("Фильтры были сохранены"), true);
    $("#mini-popup").remove();
});

document.addEventListener("click", (e) => {
    if (!eventMatches(e, ".content") || !eventMatches(e, ".radio-container") || !eventMatches(e, "label")) return;

    let content = e.target.closest(".content");
    for (let con of content.children) {
        con.firstElementChild.checked = false;
    }

    let input = e.target.previousElementSibling;
    input.checked = !input.checked;
});