
function matches(e, name) {
    if (!e.target.matches(name) && e.target.closest(name) == null) {
        return false;
    }
    return true;
}

function logout() {
    if (confirm("Вы точно хотите выйти c аккаунта?")) {
        $.ajax({
            method: "POST",
            url: SETTINGSPAGE_URL,
            data: {
                "csrfmiddlewaretoken": CSRF_TOKEN,
                "action": "logout"
            },
            dataType: "json",
            success: function (data) {
                if (data["success"]) {
                    window.location.href = AUTHPAGE_URL;
                } else {
                    showToast("Ошибка при выходе", false);
                }
            },
            error: function (xhr, errmsg, err) {
                showToast("Произошла ошибка", false);
                console.log(xhr.status + ":" + xhr.responseText);
            }
        });
    }
}

function deleteAccount() {
    if (confirm("Вы точно хотите удалить аккаунт?")) {
        $.ajax({
            method: "POST",
            url: SETTINGSPAGE_URL,
            data: {
                "csrfmiddlewaretoken": CSRF_TOKEN,
                "action": "delete-account"
            },
            dataType: "json",
            success: function (data) {
                if (data["success"]) {
                    window.location.href = AUTHPAGE_URL;
                } else {
                    showToast("Ошибка при удалении аккаунта", false);
                }
            },
            error: function (xhr, errmsg, err) {
                showToast("Произошла ошибка", false);
                console.log(xhr.status + ":" + xhr.responseText);
            }
        });
    }
}

function changePassword() {
    let password1 = document.getElementById("new-password").value
    let password2 = document.getElementById("new-password-confirm").value
    if (password1 == "") {
        showToast("Введите пароль", false)
        return
    }
    console.log(password1)
    if (password1 != password2) {
        showToast("Пароли не совпадают", false)
        return
    }

    $.ajax({
        method: "POST",
        url: SETTINGSPAGE_URL,
        data: {
            "csrfmiddlewaretoken": CSRF_TOKEN,
            "action": "change-password",
            "new_password": password1
        },
        dataType: "json",
        beforeSend: () => {
            $("#loading-gif").show();
            $("#arrow-right").hide();
            $("#confirm-new-password-btn").prop("disabled", true);
        },
        success: function (data) {
            let success = data["success"]
            if (success) {
                showToast("Пароль успешно изменен", true)
                return;
            }

            showToast(data["error_message"], false)
        },
        error: function (xhr, errmsg, err) {
            showToast("Произошла ошибка", false);
            console.log(xhr.status + ":" + xhr.responseText)
        },
        complete: function () {
            $("#loading-gif").hide();
            $("#arrow-right").show();
            $("#confirm-new-password-btn").prop("disabled", false);
            password1 = ""
            password2 = ""
        },
    })
}

document.addEventListener("change", (e) => {
    if (!matches(e, ".radio-input-wrapper")) return

    const selectedId = e.target.getAttribute("id")

    let multipleChoiceSection = e.target.closest(".radio-input-wrapper").closest(".multiple-choice-actions");
    let inputs = multipleChoiceSection.querySelectorAll(".radio-input-wrapper > input");
    inputs.forEach(input => {
        input.checked = false;
    });

    document.getElementById(selectedId).checked = true;
});

document.addEventListener("change", (e) => {
    if (!matches(e, "#lang-kk") && !matches(e, "#lang-ru") && !matches(e, "#lang-en")) return

    const selectedId = e.target.getAttribute("id")
    let lang;
    if (selectedId == "lang-kk") {
        lang = "kk";
    } else if (selectedId == "lang-ru") {
        lang = "ru";
    } else {
        lang = "en";
    }

    $.ajax({
        method: "POST",
        url: SETTINGSPAGE_URL,
        data: {
            "csrfmiddlewaretoken": CSRF_TOKEN,
            "action": "change-lang",
            "lang": lang
        },
        dataType: "json",
        success: function (data) {
            if (data["success"]) {
                location.reload();
            } else {
                showToast("Ошибка при изменении языка", false);
            }
        },
        error: function (xhr, errmsg, err) {
            showToast("Произошла ошибка", false);
            console.log(xhr.status + ":" + xhr.responseText);
        }
    });
})

document.addEventListener("change", (e) => {
    if (!matches(e, "#light-theme") && !matches(e, "#dark-theme")) return

    const selectedId = e.target.getAttribute("id")
    let theme = (selectedId == "light-theme" ? "light" : "dark");

    if (theme == htmlElement.getAttribute('data-theme')) {
        return;
    }

    $.ajax({
        method: "POST",
        url: SETTINGSPAGE_URL,
        data: {
            "csrfmiddlewaretoken": CSRF_TOKEN,
            "action": "change-theme",
            "theme": theme
        },
        dataType: "json",
        success: function (data) {
            if (data["success"]) {
                switchTheme(theme);
                showToast("Тема успешно изменена", true);
            } else {
                showToast("Ошибка при изменении темы", false);
            }
        },
        error: function (xhr, errmsg, err) {
            showToast("Произошла ошибка", false);
            console.log(xhr.status + ":" + xhr.responseText);
        }
    });
});

document.addEventListener("click", (e) => {
    if (!e.target.matches(".popup-header-btn") && e.target.closest(".popup-header-btn") == null) return

    let button = e.target.closest(".popup-header-btn")
    let img = button.querySelector("i")

    const state = button.dataset.state
    const bodyElement = button.closest(".popup-action").querySelector(".body");
    if (state == "hidden") {
        button.dataset.state = "visible";
        img.style.animation = "rotateTo180 0.5s forwards"
        bodyElement.style.display = "flex"
        bodyElement.style.animation = "makeVisible 0.5s forwards"
    } else {
        button.dataset.state = "hidden";
        img.style.animation = "rotateTo0 0.5s forwards"
        bodyElement.style.animation = "hide 0.5s forwards"
        setTimeout(() => {
            bodyElement.style.display = "none";
        }, 500);
    }
});