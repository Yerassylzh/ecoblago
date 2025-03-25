class DialogsManager {
    getNewDialogWidget(id) {
        return `
      <dialog class="popup" id="${id}">
        <div style="padding: 1rem;">
          <div class="row options-row">

          </div>
        </div>
      </dialog>
      `;
    }

    insertOption(optionHtml, dialogId) {
        let optionsRow = $("#" + dialogId).children().first().children().first();
        optionsRow.html(optionsRow.html() + optionHtml);
    }

    insertLocationOptions(options, dialogId) {
        let optionsRow = $("#" + dialogId).children().first().children().first();
        for (let i = 0; i < options.length; i++) {
            let option = options[i];

            const optionWidget = `
          <div style="margin-bottom: 0.5rem;" class="col-12 col-md-6 col-xl-4">
            <div class="select-option">
              <i class="fa-solid fa-city" style="color: var(--txt-primary); font-size: 1rem; margin: 0 0.5rem;"></i>
              <p>${option}</p>
            </div>
          </div>
        `;
            optionsRow.html(optionsRow.html() + optionWidget);
        }
    }
}

window.DialogsManager = DialogsManager;