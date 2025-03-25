function getCSRFWidget(token) {
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = token;
    return csrfInput
}

document.addEventListener("click", (e) => {
    if (!e.target.matches("#edit-about-button") && e.target.closest("#edit-about-button") == null) return

    editAboutButton = document.getElementById("edit-about-button")
    editAboutButton.remove()

    aboutText = document.getElementById("about-text")
    aboutTextContent = aboutText.textContent
    aboutText.remove()

    editAboutInput = document.createElement("textarea")
    editAboutInput.setAttribute("class", "edit-about-input")
    editAboutInput.setAttribute("id", "edit-about-input")
    editAboutInput.textContent = aboutTextContent

    submitButton = document.createElement("button")
    submitButton.setAttribute("class", "transparent-button")
    submitButton.setAttribute("id", "edit-about-submit-button")

    editText = document.createElement("a")
    editText.setAttribute("class", "link-text")
    editText.textContent = "Подтвердить"
    submitButton.appendChild(editText)

    aboutSection = document.getElementById("about-section")
    aboutSection.appendChild(editAboutInput)
    aboutSection.appendChild(submitButton)
})

document.addEventListener("click", (e) => {
    if (!e.target.matches("#edit-about-submit-button") && e.target.closest("#edit-about-submit-button") == null) return

    editedAboutTextContent = document.getElementById("edit-about-input").value

    $.ajax({
        url: PROFILEPAGE_URL.replace('0', USER_ID),
        method: "POST",
        dataType: "json",
        data: {
            "action": "edit-about",
            "edited-about-text-content": editedAboutTextContent,
            "csrfmiddlewaretoken": CSRF_TOKEN,
        },
        success: (data) => {
            $("#edit-about-input").remove()
            $("#edit-about-submit-button").remove()

            const addEditAboutLink = () => {
                editAboutLink = document.createElement("a")
                editAboutLink.setAttribute("class", "link-text")
                editAboutLink.setAttribute("id", "edit-about-link")
                editAboutLink.textContent = "Изменить"

                editAboutButton = document.createElement("button")
                editAboutButton.setAttribute("class", "transparent-button")
                editAboutButton.setAttribute("id", "edit-about-button")
                editAboutButton.appendChild(editAboutLink)

                aboutTitle = document.getElementById("about-title")
                aboutTitle.appendChild(editAboutButton)
            }

            const addAboutText = (aboutTextContent) => {
                aboutText = document.createElement("p")
                aboutText.setAttribute("class", "additional-info-text")
                aboutText.setAttribute("id", "about-text")
                aboutText.textContent = aboutTextContent

                aboutSection = document.getElementById("about-section")
                aboutSection.appendChild(aboutText)
            }

            let success = data["success"]
            let aboutTextContent = data["about-text-content"]
            if (success) {
                addEditAboutLink()
                addAboutText(aboutTextContent)
                showToast("Изменения сохранены", true)
            } else {
                addEditAboutLink()
                addAboutText(aboutTextContent)
                showToast(gettext('Произошла ошибка при сохранении изменений'), false)
            }
        },
        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ":" + xhr.responseText)
        }
    })
})

document.addEventListener("click", (e) => {
    if (!e.target.matches("#change-image-button") && e.target.closest("#change-image-button") == null) return

    changeImageButton = document.getElementById("change-image-button")
    changeImageButton.remove()

    form = document.createElement("form")
    form.setAttribute("enctype", "multipart/form-data")
    form.setAttribute("method", "POST")
    form.setAttribute("action", PROFILEPAGE_URL.replace('0', USER_ID))
    form.classList.add("d-flex", "flex-column", "align-items-start", "justify-content-center");
    form.setAttribute("name", "personal-image-upload")

    form.appendChild(getCSRFWidget(CSRF_TOKEN))

    fileInput = document.createElement("input")
    fileInput.setAttribute("type", "file")
    fileInput.setAttribute("value", "Выберите фото")
    fileInput.setAttribute("class", "choose-photo-button")
    fileInput.setAttribute("name", "personal-image")
    form.appendChild(fileInput)

    submitButton = document.createElement("button")
    submitButton.setAttribute("type", "submit")
    submitButton.setAttribute("class", "transparent-button")

    uploadText = document.createElement("a")
    uploadText.setAttribute("class", "link-text")
    uploadText.textContent = "Загрузить"
    submitButton.appendChild(uploadText)

    form.appendChild(submitButton)

    personalImageWrapper = document.getElementById("personal-image-wrapper")
    personalImageWrapper.appendChild(form)
})