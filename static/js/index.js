// Define addToCart function
function addToCart() {
    const productId = $("#addtoCartForm input[name='productId']").val();

    const requestBody = {
        productId
    };

    $.ajax({
        type: "POST",
        url: "/addtocart",
        data: JSON.stringify(requestBody),
        contentType: "application/json",
        success: function (response) {
            // Log the server's response to the console
            console.log("Server Response:", response);

            // Update the button appearance or provide feedback as needed
            $("#addToCart").addClass("added-to-cart");
            $("#addToCart").text("Added to Cart");
            $("#addToCart").prop("disabled", true); // Disable the button
        },
        error: function (error) {
            // Handle the error, e.g., display an error message
            console.error("Error:", error);

            // You can still update the button appearance here if needed
            $("#addToCart").addClass("error");
            $("#addToCart").text("Error Adding to Cart");
        }
    });
}

// Checkout
document.addEventListener('DOMContentLoaded', function () {
    // Wait for the DOM to be fully loaded

    // Find the "Proceed to Buy" button
    var proceedToBuyBtn = document.getElementById('proceedToBuyBtn');

    // Check if the cart is empty
    var isCartFull = Math.min(document.getElementById('cartTotalQty'),1)

    if (isCartFull) {
        // Change the label of the button
        proceedToBuyBtn.innerText = 'Go Back to Home';

        // Display a message
        var message = document.createElement('p');
        message.innerText = 'There are no items in your cart.';
        document.body.appendChild(message);

        // Attach a click event listener to the button for redirection to the home page
        proceedToBuyBtn.addEventListener('click', function () {
            // Redirect the user to the home page
            window.location.href = '/index';
        });
    } else {
        // Attach a click event listener to the button for proceeding to buy
        proceedToBuyBtn.addEventListener('click', function () {
            // Redirect the user to the "/checkout" endpoint
            window.location.href = '/checkout';
        });
    }
});

$(document).ready(function(){
    // Add to cart function
    $("#addToCart").click(addToCart);
    
    // banner owl carousel
    $("#banner-area .owl-carousel").owlCarousel({
        dots: true,
        items: 1
    });

    // top sale owl carousel
    $("#top-sale .owl-carousel").owlCarousel({
        loop: true,
        nav: true,
        dots: false,
        responsive : {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000 : {
                items: 5
            }
        }
    });

    // isotope filter
    var $grid = $(".grid").isotope({
        itemSelector : '.grid-item',
        layoutMode : 'fitRows'
    });

    // filter items on button click
    $(".button-group").on("click", "button", function(){
        var filterValue = $(this).attr('data-filter');
        $grid.isotope({ filter: filterValue});
    })


    // new phones owl carousel
    $("#new-phones .owl-carousel").owlCarousel({
        loop: true,
        nav: false,
        dots: true,
        responsive : {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000 : {
                items: 5
            }
        }
    });

    // blogs owl carousel
    $("#blogs .owl-carousel").owlCarousel({
        loop: true,
        nav: false,
        dots: true,
        responsive : {
            0: {
                items: 1
            },
            600: {
                items: 3
            }
        }
    })


    // product qty section
    let $qty_up = $(".qty .qty-up");
    let $qty_down = $(".qty .qty-down");
    let $deal_price = $("#deal-price");
    // let $input = $(".qty .qty_input");

    // click on qty up button
    $qty_up.click(function(e){

        let $input = $(`.qty_input[data-id='${$(this).data("id")}']`);
        let $price = $(`.product_price[data-id='${$(this).data("id")}']`);

        // change product price using ajax call
        $.ajax({url: "template/ajax.php", type : 'post', data : { itemid : $(this).data("id")}, success: function(result){
                let obj = JSON.parse(result);
                let item_price = obj[0]['item_price'];

                if($input.val() >= 1 && $input.val() <= 9){
                    $input.val(function(i, oldval){
                        return ++oldval;
                    });

                    // increase price of the product
                    $price.text(parseInt(item_price * $input.val()).toFixed(2));

                    // set subtotal price
                    let subtotal = parseInt($deal_price.text()) + parseInt(item_price);
                    $deal_price.text(subtotal.toFixed(2));
                }

            }}); // closing ajax request
    }); // closing qty up button

    // click on qty down button
    $qty_down.click(function(e){

        let $input = $(`.qty_input[data-id='${$(this).data("id")}']`);
        let $price = $(`.product_price[data-id='${$(this).data("id")}']`);

        // change product price using ajax call
        $.ajax({url: "template/ajax.php", type : 'post', data : { itemid : $(this).data("id")}, success: function(result){
                let obj = JSON.parse(result);
                let item_price = obj[0]['item_price'];

                if($input.val() > 1 && $input.val() <= 10){
                    $input.val(function(i, oldval){
                        return --oldval;
                    });


                    // increase price of the product
                    $price.text(parseInt(item_price * $input.val()).toFixed(2));

                    // set subtotal price
                    let subtotal = parseInt($deal_price.text()) - parseInt(item_price);
                    $deal_price.text(subtotal.toFixed(2));
                }

            }}); // closing ajax request
    }); // closing qty down button
});