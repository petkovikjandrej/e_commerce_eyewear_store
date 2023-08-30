function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast Notification for Color Selection
let colorToast = document.getElementById('colorToast');
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(colorToast);

function showToast(message) {
    let toastElement = document.getElementById('colorToast');
    let toastInstance = bootstrap.Toast.getOrCreateInstance(toastElement);
    let toastBodyElement = toastElement.querySelector('.toast-body');
    toastBodyElement.innerHTML = message;
    toastInstance.show();
}

// Your existing code for color selection
function selectColor(colorId) {
    const images = document.querySelectorAll('.color-image');
    images.forEach(image => image.classList.remove('selected'));
    const selectedImage = document.querySelector(`.color-image[data-color-id="${colorId}"]`);
    selectedImage.classList.add('selected');
    const hiddenField = document.getElementById('selected-color');
    hiddenField.value = colorId;
}

document.addEventListener("DOMContentLoaded", function () {
    const colorImages = document.querySelectorAll('.color-image');
    colorImages.forEach(function (image) {
        image.addEventListener('click', function () {
            const colorId = image.getAttribute("data-color-id");
            selectColor(colorId);
        });
    });

    // Add event listener to the Add to Cart button to validate color selection
    const addToCartForm = document.querySelector('#add-to-cart-form');
    const productId = addToCartForm.getAttribute('data-product-id');

    const addToCartButton = document.querySelector('#add-to-cart-form button[type="submit"]');
    addToCartButton.addEventListener('click', function (e) {
        const hiddenField = document.getElementById('selected-color');
        const colorId = hiddenField.value;
        const quantity = document.querySelector('input[name="quantity"]').value;
        e.preventDefault();

        if (!colorId) {
            showToast("Please select a color before adding to cart.");
            return;
        }

        const addToCartUrl = '/add_to_cart/' + productId + '/'; // Replace `productId` with the actual product ID
        const csrftoken = getCookie('csrftoken');

        $.ajax({
            url: addToCartUrl,
            type: 'POST',
            headers: {
                "X-CSRFToken": csrftoken
            },
            data: {
                'color_choice': colorId,
                'quantity': quantity,
            },
            success: function (data) {
                if (data.status === 'success') {  // Changed from data.success to data.status === 'success'
                    showToast("Product Added to Your Cart.");  // I've removed the second argument
                } else {
                    showToast(data.message);
                }
            },
            error: function () {
                showToast("Network error. Please try again.");
            }
        });
    });
});
