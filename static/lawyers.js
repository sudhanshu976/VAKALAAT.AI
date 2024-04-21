// Add your JavaScript code here
// Example JavaScript code
// lawyers.js

function searchLawyers() {
    const searchInput = document.getElementById('searchInput').value;
    fetch(`/search_lawyers?query=${searchInput}`)
        .then(response => response.json())
        .then(data => {
            displayLawyerCards(data.lawyers);
        });
}

function displayLawyerCards(lawyers) {
    const lawyerCardsContainer = document.getElementById('lawyerCards');
    lawyerCardsContainer.innerHTML = '';

    lawyers.forEach(lawyer => {
        const card = document.createElement('div');
        card.classList.add('lawyer-card');

        const image = document.createElement('img');
        image.src = lawyer.image_path;
        card.appendChild(image);

        const content = document.createElement('div');
        content.classList.add('lawyer-card-content');

        const name = document.createElement('h2');
        name.textContent = lawyer.name;
        content.appendChild(name);

        const description = document.createElement('p');
        description.textContent = lawyer.description;
        content.appendChild(description);

        card.appendChild(content);
        lawyerCardsContainer.appendChild(card);
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var joinBtn = document.getElementById('joinBtn');
    var popupForm = document.getElementById('popupForm');
    var closeButton = document.getElementsByClassName('close')[0];

    // Show popup form when "Join as a Lawyer" button is clicked
    joinBtn.addEventListener('click', function () {
        popupForm.style.display = 'block';
    });

    // Close popup form when the close button is clicked
    closeButton.addEventListener('click', function () {
        popupForm.style.display = 'none';
    });

    // Close popup form when the user clicks outside of it
    window.onclick = function (event) {
        if (event.target == popupForm) {
            popupForm.style.display = 'none';
        }
    };
});
