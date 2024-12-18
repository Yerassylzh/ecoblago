function get_error_p(content) {
    let message = document.createElement("p")
    message.setAttribute("class", "error-message")
    message.textContent = content
    setTimeout(() => {
        message.style.opacity = 0
        setTimeout(() => {
        message.remove()
        }, 200);
    }, 2000);
    return message
}

function get_success_p(content) {
    let message = document.createElement("p")
    message.setAttribute("class", "success-message")
    message.textContent = content
    setTimeout(() => {
        message.style.opacity = 0
        setTimeout(() => {
        message.remove()
        }, 200);
    }, 2000);
    return message
}

function removeAll(attrName) {
    document.querySelectorAll(attrName).forEach(item => {
        item.remove()
    })
}

document.addEventListener("click", e => {
    if (!e.target.matches("#auth-submit") && e.target.closest("#auth-submit") == null) return
    const currentAuthType = document.getElementById("auth-options-container").dataset.currentAuthType
    let isLogin = currentAuthType == "0"
    let isSignup = currentAuthType == "1"

    let username = $("#username").val()
    let password = $("#password").val()

    console.log(document.getElementById("auth-options-container").dataset.currentAuthType);

    let data = {
        "username": username,
        "password": password,
        "remember_me": $("#remember-me").val() == "on",
        "action": "auth-user",
        "auth_type": document.getElementById("auth-options-container").dataset.currentAuthType,
        "csrfmiddlewaretoken": CSRF_TOKEN,
    }

    if (isSignup) {
        let phone_number = $("#phone-number").val()
        let email = $("#email").val()

        data["phone_number"] = phone_number
        data["email"] = email
    }

    $.ajax({
        method: "POST",
        url: AUTHPAGE_URL,
        data: data,
        dataType: "json",
        success: function(data) {
            if (data["has_error_message"]) {
            const errorMessage = get_error_p(data["error_message"]);

            let formId = "auth-form"
            let submitButtonId = "auth-submit"

            let submitButton = document.getElementById(submitButtonId)
            document.getElementById(formId).insertBefore(errorMessage, submitButton)
            } else if (data["success"]) {
                window.location.href = data["redirect_to"]
            } else {
                alert("Got an unexpected error while loggining")
            }
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        }
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
            success: function(data) {
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

                console.log(data["input_fields"])
                for (let i = 0; i < data["input_fields"].length; i++) {
                let input_field = data["input_fields"][i]
                let input_field_container = document.createElement("div")
                input_field_container.innerHTML = input_field
                inputFields.appendChild(input_field_container.firstChild)
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ":" + xhr.responseText)
            }
        })
    }
})
