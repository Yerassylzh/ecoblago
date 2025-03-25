class FilterSettings {
    sortingRules = {
        POPULAR: "popular",
        FROMCHEAP: "from-cheap",
        FROMEXPENSIVE: "from-expensive",
        HIGHRATING: "high-rating",
        NEW: "new",
    };

    constructor() {
        this.content = "";
        this.region = null;
        this.city = null;

        this.maxCost = 480000;
        this.minCost = 500;
        this.categories = [];
        this.sortingRule = this.sortingRules.POPULAR;
    }

    toDict() {
        return {
            "content": this.content,
            "region": this.region,
            "city": this.city,
            "max-cost": this.maxCost,
            "min-cost": this.minCost,
            "categories": this.categories,
            "sorting-rule": this.sortingRule
        };
    }
};

window.FilterSettings = FilterSettings;