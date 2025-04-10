function removeAll(attrName) {
    document.querySelectorAll(attrName).forEach(item => {
        item.remove()
    })
}

function resetPolicyCheckbox() {
    const checkbox = $("#policy-check").parent();

    if (checkbox.css("display") == "none") {
        checkbox.css("display", "flex");
    } else {
        checkbox.css("display", "none");
    }
}

document.addEventListener("click", e => {
    if (!e.target.matches("#auth-submit") && e.target.closest("#auth-submit") == null) return

    const currentAuthType = document.getElementById("auth-options-container").dataset.currentAuthType
    let isLogin = currentAuthType == "0"
    let isSignup = currentAuthType == "1"

    if (isSignup) {
        if (!$("#policy-check").is(":checked")) {
            showToast(gettext("Вы не можете зарегистрироваться не согласившись условиями использования"), false);
            return;
        }
    }

    let username = $("#username").val()
    let password = $("#password").val()

    let data = {
        "username": username,
        "remember_me": $("#remember-me").is(":checked"),
        "action": "auth-user",
        "auth_type": document.getElementById("auth-options-container").dataset.currentAuthType,
        "csrfmiddlewaretoken": CSRF_TOKEN,
    }

    if (isSignup) {
        let phone_number = $("#phone-number").val()
        let email = $("#email").val()
        let first_name = $("#first_name").val()
        let last_name = $("#last_name").val()
        let password1 = $("#password1").val()
        let password2 = $("#password2").val()

        data["phone_number"] = phone_number
        data["email"] = email
        data["first_name"] = first_name
        data["last_name"] = last_name
        data["password1"] = password1
        data["password2"] = password2
    } else {
        let password = $("#password").val()
        data["password"] = password
    }

    $.ajax({
        method: "POST",
        url: AUTHPAGE_URL,
        data: data,
        dataType: "json",
        beforeSend: () => {
            $("#loading-gif").show();
            $("#arrow-right").hide();
            $("#auth-submit").prop("disabled", true);
        },
        success: function (data) {
            let success = data["success"]
            if (success) {
                window.location.href = $("#next").val()
            } else {
                let [errorWidgetId, errorMessage] = data["error_message"]
                let formId = "auth-form", submitButtonId = "auth-submit", message = errorMessage

                if (document.getElementById(errorWidgetId) != null) {
                    placeholder = $("#" + errorWidgetId).attr("placeholder")
                    message = placeholder + ": " + message
                }
                showToast(message, false)
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        },
        complete: function () {
            $("#loading-gif").hide();
            $("#arrow-right").show();
            $("#auth-submit").prop("disabled", false);
        },
    })
})

document.addEventListener("click", e => {
    if (!e.target.matches("#auth-options-container") && e.target.closest("#auth-options-container") == null) return

    let authOptions = document.getElementById("auth-options-container")
    const currentAuthType = authOptions.dataset.currentAuthType

    let newAuthType
    if (e.target.matches("#auth-login")) {
        newAuthType = "0"
    } else {
        newAuthType = "1"
    }

    if (currentAuthType !== newAuthType) {
        $.ajax({
            method: "GET",
            url: AUTHPAGE_URL,
            data: {
                "auth_type": newAuthType,
                "action": "change-auth-type",
            },
            dataType: "json",
            success: function (data) {
                let beforeButtonId
                let afterButtonId

                if (newAuthType === "0") {
                    beforeButtonId = "auth-signup"
                    afterButtonId = "auth-login"
                } else {
                    beforeButtonId = "auth-login"
                    afterButtonId = "auth-signup"
                }

                document.getElementById(beforeButtonId).classList.remove("auth-type-button-selected")
                document.getElementById(beforeButtonId).classList.toggle("auth-type-button")

                document.getElementById(afterButtonId).classList.remove("auth-type-button")
                document.getElementById(afterButtonId).classList.toggle("auth-type-button-selected")

                authOptions.dataset.currentAuthType = newAuthType

                let inputFields = document.getElementById("input-fields-container")
                while (inputFields.lastChild != null) {
                    inputFields.lastChild.remove()
                }

                for (let i = 0; i < data["input_fields"].length; i++) {
                    let input_widget = data["input_fields"][i][0]
                    let input_placeholder = data["input_fields"][i][1]
                    let input_field_wrapper = document.createElement("div")
                    input_field_wrapper.classList.add("input-field-wrapper")

                    input_field_wrapper.innerHTML = input_widget;
                    input_field_wrapper.innerHTML += `<div>${input_placeholder}</div>`

                    inputFields.appendChild(input_field_wrapper)
                }
                resetPolicyCheckbox();
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ":" + xhr.responseText)
            }
        })
    }
});