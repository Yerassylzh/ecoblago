document.addEventListener('DOMContentLoaded', function () {
	const dropdowns = document.querySelectorAll('.dropdown');

	dropdowns.forEach(dropdown => {
		dropdown.addEventListener('mouseenter', function () {
			if (window.innerWidth >= 992) {
				this.querySelector('.dropdown-toggle').click();
			}
		});

		dropdown.addEventListener('mouseleave', function () {
			if (window.innerWidth >= 992) {
				const dropdownMenu = this.querySelector('.dropdown-menu');
				if (dropdownMenu.classList.contains('show')) {
					this.querySelector('.dropdown-toggle').click();
				}
			}
		});
	});
});
