function eventMatches(e, selector) {
    return e.target.matches(selector) || e.target.closest(selector) != null;
}

function switchTheme(theme) {
    htmlElement.setAttribute('data-theme', theme);

    const navbar = document.getElementById("navbar");
    if (theme == "dark") {
        navbar.classList.remove("bg-light");
        navbar.classList.add("bg-dark");
    } else {
        navbar.classList.remove("bg-dark");
        navbar.classList.add("bg-light");
    }
}

function showToast(text, isSuccess) {
    let messagesContainer = document.getElementById('messages-container');
    let message = document.createElement('div');
    let messageBody = document.createElement('div');

    messageBody.className = 'message-body';
    messageBody.innerHTML = text;

    message.className = 'message show ' + (isSuccess ? 'success' : 'failure');
    message.appendChild(messageBody);
    messagesContainer.appendChild(message);

    setTimeout(() => {
        message.className = "message hide " + (isSuccess ? 'success' : 'failure');
        setTimeout(() => {
            messagesContainer.removeChild(message);
        }, 500);
    }, 3000);
}

// Example usage:
// showToast('Operation successful!', true);
// showToast('Operation failed!', false);
