function getCSRFWidget(token) {
	const csrfInput = document.createElement('input');
	csrfInput.type = 'hidden';
	csrfInput.name = 'csrfmiddlewaretoken';
	csrfInput.value = token;
	return csrfInput
}

document.addEventListener("click", (e) => {
	if (!e.target.matches("#edit-about-button") && e.target.closest("#edit-about-button") == null) return

	editAboutButton = document.getElementById("edit-about-button");
	editAboutButton.remove();

	aboutText = document.getElementById("about-section").lastElementChild;
	aboutTextContent = (aboutText.getAttribute("id") == "about-text" ? aboutText.textContent : "");
	aboutText.remove();

	editAboutInput = document.createElement("textarea")
	editAboutInput.setAttribute("class", "edit-about-input")
	editAboutInput.setAttribute("id", "edit-about-input")
	editAboutInput.textContent = aboutTextContent

	submitButton = document.createElement("button")
	submitButton.setAttribute("class", "transparent-button")
	submitButton.setAttribute("id", "edit-about-submit-button")

	editText = document.createElement("a")
	editText.setAttribute("class", "link-text")
	editText.textContent = gettext("Подтвердить")
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
				editAboutLink.textContent = gettext("Изменить")

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
				showToast(gettext("Изменения сохранены"), true)
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
	fileInput.setAttribute("value", gettext("Выберите фото"))
	fileInput.setAttribute("class", "choose-photo-button")
	fileInput.setAttribute("name", "personal-image")
	form.appendChild(fileInput)

	submitButton = document.createElement("button")
	submitButton.setAttribute("type", "submit")
	submitButton.setAttribute("class", "transparent-button")

	uploadText = document.createElement("a")
	uploadText.setAttribute("class", "link-text")
	uploadText.textContent = gettext("Загрузить")
	submitButton.appendChild(uploadText)

	form.appendChild(submitButton)

	personalImageWrapper = document.getElementById("personal-image-wrapper")
	personalImageWrapper.appendChild(form)
})

function getEditableFeedbackHtml() {
	return `
	<div class="feedback-bar">
		<h6>${gettext('Your feedback')}</h6>
		<hr class="additional-info-hr" />
		<div class="feedback-content">
			<div id="leave-feedback-star-rating" class="star-rating animated-stars">
				<input type="radio" id="star5" name="rating" value="5">
				<label for="star5" class="bi bi-star-fill"></label>
				<input type="radio" id="star4" name="rating" value="4">
				<label for="star4" class="bi bi-star-fill"></label>
				<input type="radio" id="star3" name="rating" value="3">
				<label for="star3" class="bi bi-star-fill"></label>
				<input type="radio" id="star2" name="rating" value="2">
				<label for="star2" class="bi bi-star-fill"></label>
				<input type="radio" id="star1" name="rating" value="1">
				<label for="star1" class="bi bi-star-fill"></label>
			</div>
			<textarea class="form-control" rows="4" id="leave-feedback-textarea" placeholder=${gettext('Feedback')}></textarea>
			<button id="leave-feedback-btn" type="button" class="btn btn-success">${gettext('Submit')}</button>
            <style>
                #leave-feedback-textarea {
                    background-color: var(--widget-color);
                    color: var(--txt-primary);
                }
                #leave-feedback-textarea::placeholder {
                    color: var(--txt-secondary);
                }
            </style>
		</div>
	</div>
	`;
}

document.addEventListener("click", (e) => {
	if (!eventMatches(e, "#add-feedback-btn")) {
		return;
	}

	let addFeedbackBtn = $("#add-feedback-btn");
	addFeedbackBtn.css("display", "none");

	let con = addFeedbackBtn.parent();
	con.html(con.html() + getEditableFeedbackHtml());
});

document.querySelectorAll('.star-rating:not(.readonly) label').forEach(star => {
	star.addEventListener('click', function() {
			this.style.transform = 'scale(1.2)';
			setTimeout(() => {
					this.style.transform = 'scale(1)';
			}, 200);
	});
});

document.addEventListener("click", (e) => {
	if (!eventMatches(e, "#leave-feedback-btn")) {
		return;
	}

	const selectedRating = $("#leave-feedback-star-rating input:checked").attr("value");
	const feedback = $("#leave-feedback-textarea").val().trim();
	if (feedback.length == 0) {
		showToast(gettext("Please, write down your feedback"), false);
		return;
	}

	$.ajax({
		method: "POST",
		url: PROFILEPAGE_URL.replace("0", USER_ID),
		data: {
			"csrfmiddlewaretoken": CSRF_TOKEN,
			"action": "save-feedback",
			"rating": selectedRating,
			"feedback": feedback,
		},
		success: (data) => {
			$("#leave-feedback-btn").closest(".feedback-bar").remove();
			showToast(gettext("Your feedback was successfully saved"), true);
			setTimeout(() => {
				window.location = PROFILEPAGE_URL.replace("0", USER_ID);
			}, 1000);
		},
		error: (xhr, errmsg, err) => {
			console.log(xhr.status + ":" + xhr.responseText)
			showToast(gettext("Произошла ошибка"), false);
		},
	})
});
