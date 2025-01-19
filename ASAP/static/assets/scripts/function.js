const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sep", "Oct", "Nov", "Dec"
];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = `${dt.getDate()} ${monthNames[dt.getMonth()]} ${dt.getFullYear()}`;

    console.log("AJAX submit triggered");

    $.ajax({
        data: $(this).serialize(),

        method: $(this).attr("method"),

        url: $(this).attr("action"),

        dataType: "json",

        success: function(res){
            console.log("Comment Saved to DB...")
            
            if(res.bool === true){
                $("#review-res").html("Review added successfully.");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let stars = '';
                for(let i = 1; i <= res.context.rating; i++){
                    stars += '<i class="fas fa-star text-warning"></i>';
                }

                const _html = `
                    <div class="review-box p-3 mb-3">
                        <div class="d-flex align-items-center">
                            <img src="{% static 'assets/images/reviewer1.png' %}" alt="User Avatar" class="rounded-circle me-3" style="width: 50px;">
                            <div>
                                <h6> ${res.context.user} <span class="text-muted">${time}</span></h6>
                                <div class="rating">
                                    ${stars}
                                </div>
                                <p>${res.context.review}</p>
                            </div>
                        </div>
                    </div>
                `;

                $(".comment-list").prepend(_html);
            }
        }
    });
});

$(document).ready(function(){
    //Add to Cart Functionality:
    $("#add-to-cart-btn").on("click", function(){
        
        let this_val = $(this)
        let index = this_val.attr("data-index")
    
        let quantity = $(".quantity-"+index).val()
        let product_title = $(".product-title-"+index).val()
        let product_id = $(".product-id-"+index).val()
        let price = $(".current-product-price-"+index).text()
        let product_pid = $(".product-pid-"+index).val()
        let product_image = $(".product-image-"+index).val()
    
        console.log("Quantity: ", quantity);
        console.log("Product Title: ", product_title);
        console.log("Product ID: ", product_id);
        console.log("Price: ", price);
        console.log("image: ", product_image);
        console.log("pid: ", product_pid);
        console.log("Current Element", this_val);
        
        $.ajax({
            url: '/add-to-cart',
            data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'qty': quantity,
            'title': product_title,
            'price': price,
    
            },
            dataType: 'json',
            beforeSend: function(){
            console.log("Adding Product to cart");
            },
            success: function(response){
            this_val.html("Item added to cart");
            console.log("Added Product to cart");
            $(".cart-items-count").text(response.totalcartitems)
            }
        })
    
    })

    $(".delete-product").on("click", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)
    
        console.log("PRODUCT ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data:{
                "id": product_id
            },
            dataType:"json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalcartitems)
                $("#cart-list").html(response.data)
            }
        })
    })
})







