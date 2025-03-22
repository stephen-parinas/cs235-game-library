// set height up to a max of 260px (at which a 'Read more' button is added
document.addEventListener("DOMContentLoaded", function () {
    const description = document.querySelector('.description-text-box');
    if (!document.querySelector('.read-more-btn') && description.scrollHeight > 260) {
        const readMoreButton = document.createElement("button");
        readMoreButton.textContent = "Read more";
        readMoreButton.classList.add("read-more-btn");
        readMoreButton.addEventListener("click", toggleGameDescription);
        description.parentNode.insertBefore(readMoreButton, description.nextSibling);
    } else if (!document.querySelector('.read-more-btn')) {
        description.style.height = '100%'
    }
})

// shows or hides description when 'Read more' button clicked
function toggleGameDescription() {
    const description = document.querySelector('.description-text-box');
    const button = document.querySelector('.read-more-btn');
    if (description.style.height !== '100%') {
        description.style.height = '100%';
        button.innerHTML = 'Read less';
    } else {
        description.style.height = '260px';
        button.innerHTML = 'Read more';
    }
}

// 'add a review' button to open or close the modal for writing a review
// if game has >3 reviews, 'view all reviews' button to open or close modal for showing all reviews
document.addEventListener("DOMContentLoaded", function () {

    if (document.querySelector(".add-review-btn")) {
        const formModal = document.querySelector(".review-modals .review-form");
        const addReviewButton = document.querySelector(".add-review-btn");
        const closeFormButton = document.querySelector(".close-form-btn");
        const formOverlay = document.querySelector(".form-modal-background-overlay");

        addReviewButton.onclick = function () {
            formModal.style.display = "block";
            formOverlay.style.display = "block";
        }

        closeFormButton.onclick = function () {
            formModal.reset();
            formModal.style.display = "none";
            formOverlay.style.display = "none";
        }

        formOverlay.onclick = function () {
            formModal.reset();
            formModal.style.display = "none";
            formOverlay.style.display = "none";
        }
    }

    if (document.querySelector(".view-reviews-btn")) {
        const displayModal = document.querySelector(".review-modals .review-display");
        const viewReviewsButton = document.querySelector(".view-reviews-btn");
        const closeDisplayButton = document.querySelector(".close-display-btn");
        const displayOverlay = document.querySelector(".display-modal-background-overlay");

        viewReviewsButton.onclick = function () {
            displayModal.style.display = "block";
            displayOverlay.style.display = "block";
        }

        closeDisplayButton.onclick = function () {
            displayModal.style.display = "none";
            displayOverlay.style.display = "none";
        }

        displayOverlay.onclick = function () {
            displayOverlay.style.display = "none";
            displayModal.style.display = "none";
        }
    }
});

// validate the review form
document.addEventListener("DOMContentLoaded", function () {
    const reviewForm = document.querySelector(".review-modals .review-form");
    const rating = document.querySelectorAll(".review-rating input[type='radio']");
    const comment = document.querySelector(".review-comment textarea");
    const errorMessage = document.querySelector(".form-error-message");

    reviewForm.addEventListener('submit', function (event) {
        let ratingAdded = false;
        for (const star of rating) {
            if (star.checked) {
                ratingAdded = true;
                break;
            }
        }

        if (!ratingAdded || (comment.value.trim() === '')) {
            event.preventDefault();
            errorMessage.style.display = 'block'
            reviewForm.style.height = '420px'
        }
    })

    reviewForm.addEventListener('reset', function (event) {
        errorMessage.style.display = 'none'
        reviewForm.style.height = '400px'
    })
});
