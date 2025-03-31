class DialogMoreFilters {
    constructor() {
        this.maxPrice = 480000;
        this.sliderStep = 60;

        this.updateSlider = this.updateSlider.bind(this);
        this.updateInput = this.updateInput.bind(this);
        this.updateTrackBackground = this.updateTrackBackground.bind(this);
    }

    // Make sure widgets exist in document
    setupCostRegulator() {
        this.minSlider = document.getElementById('min-slider');
        this.maxSlider = document.getElementById('max-slider');
        this.minPriceInput = document.getElementById('min-price');
        this.maxPriceInput = document.getElementById('max-price');
        this.sliderTrack = document.querySelector('.slider-track');

        this.minSlider.addEventListener('input', this.updateSlider);
        this.maxSlider.addEventListener('input', this.updateSlider);
        this.minPriceInput.addEventListener('input', this.updateInput);
        this.maxPriceInput.addEventListener('input', this.updateInput);

        this.updateTrackBackground(this.minSlider.value, this.maxSlider.value);
    }

    _getCategoriesSectionWidget(categories) {
        let categoryWidget = `
        <div class="filter-categories">
          <div class="header">${gettext("Категории")}</div>
          <div class="content">
      `;
        for (let category of categories) {
            categoryWidget += `
          <div class="checkbox-container">
            <input type="checkbox">
            <label class="text">${category}</label>
          </div>
        `;
        }
        categoryWidget += '</div></div>';
        return categoryWidget;
    }

    _getCostRegulatorSectionWidget() {
        return `
        <div class="cost-regulator">
          <div class="header">${gettext("Цена")}</div>
          <div class="content">
            <div class="price-inputs">
                <div class="field">
                    <label for="min-price">${gettext("Min Price")}:</label>
                    <input type="number" id="min-price" value="1000">
                </div>
                <div class="field">
                    <label for="max-price">${gettext("Max Price")}:</label>
                    <input type="number" id="max-price" value="20000">
                </div>
            </div>
            <div class="slider-container">
                <div class="slider-track"></div>
                <input type="range" id="min-slider" min="0" max="${this.maxPrice}" value="1000" step="${this.sliderStep}">
                <input type="range" id="max-slider" min="0" max="${this.maxPrice}" value="20000" step="${this.sliderStep}">
            </div>
          </div>
        </div>
      `;
    }

    _getSortingRulesWidget() {
        let options = Object.values(new FilterSettings().sortingRules);
        let sortingRulesWidget = `
        <div class="filter-sortingrules" style="display: none;">
          <div class="header">${gettext("Сортировка")}</div>
          <div class="content">
      `;
        for (let option of options) {
            sortingRulesWidget += `
          <div class="radio-container">
            <input type="radio" data-sorting-rule=${option}>
            <label class="text">${option}</label>
          </div>
        `;
        }
        sortingRulesWidget += '</div></div>';
        return sortingRulesWidget;
    }

    _getSaveButtonWidget() {
        return `<button class="save-btn" id="save-filters-btn">${gettext('Сохранить')}</button>`;
    }

    // High level function
    getDialogInnerHtml(categories) {
        let categoriesWidget = this._getCategoriesSectionWidget(categories);
        let costRegulatorWidget = this._getCostRegulatorSectionWidget();
        let sortingRulesWidget = this._getSortingRulesWidget();
        let saveButtonWidget = this._getSaveButtonWidget();
        return categoriesWidget + costRegulatorWidget + sortingRulesWidget + saveButtonWidget;
    }

    _recoverCategoriesSection() {
        let chosenCategories = new Set(filterSettings.categories);
        let checkboxes = document.querySelector(".filter-categories").querySelectorAll("input");
        for (let category of checkboxes) {
            if (chosenCategories.has(category.nextElementSibling.textContent)) {
                category.checked = true;
            }
        }
    }

    _recoverSortingRulesSection() {
        let sortingRule = filterSettings.sortingRule;
        let sortingRules = document.querySelector(".filter-sortingrules").querySelectorAll("input");
        for (let rule of sortingRules) {
            if (rule.dataset.sortingRule == sortingRule) {
                rule.checked = true;
                break;
            }
        }
    }

    _recoverCostRegulatorSection() {
        document.getElementById("min-price").value = filterSettings.minCost;
        document.getElementById("max-price").value = filterSettings.maxCost;
        document.getElementById("min-slider").value = filterSettings.minCost;
        document.getElementById("max-slider").value = filterSettings.maxCost;
        this.updateTrackBackground(filterSettings.minCost, filterSettings.maxCost);
    }

    // High level function
    recoverSavedSettings() {
        this._recoverCategoriesSection();
        this._recoverCostRegulatorSection();
        this._recoverSortingRulesSection();
    }

    updateSlider() {
        const minValue = parseInt(this.minSlider.value);
        const maxValue = parseInt(this.maxSlider.value);

        if (maxValue - minValue < this.sliderStep) {
            if (this.id === 'min-slider') {
                this.minSlider.value = maxValue - this.sliderStep;
            } else {
                this.maxSlider.value = minValue + this.sliderStep;
            }
        }

        this.minPriceInput.value = this.minSlider.value;
        this.maxPriceInput.value = this.maxSlider.value;
        this.updateTrackBackground(this.minSlider.value, this.maxSlider.value);
    }

    updateInput() {
        let minValue = parseInt(minPriceInput.value);
        let maxValue = parseInt(maxPriceInput.value);

        if (maxValue - minValue >= this.sliderStep && maxValue <= this.maxPrice) {
            this.minSlider.value = minValue;
            this.maxSlider.value = maxValue;
            this.updateTrackBackground(minSlider.value, maxSlider.value);
        }
    }

    updateTrackBackground(minValue, maxValue) {
        const sliderContainer = document.querySelector('.slider-container');
        const sliderTrack = document.querySelector('.slider-track');
        const minPercent = (minValue / this.maxPrice) * 100;
        const maxPercent = (maxValue / this.maxPrice) * 100;

        sliderTrack.style.color = "var(--green-primary);";
        sliderTrack.style.left = `${minPercent}%`;
        sliderTrack.style.width = `${maxPercent - minPercent}%`;
    }
};

window.DialogMoreFilters = DialogMoreFilters;
