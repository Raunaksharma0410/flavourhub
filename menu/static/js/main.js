/* ==========================================================
                    FLAVORHUB
                    MAIN JAVASCRIPT
========================================================== */

document.addEventListener("DOMContentLoaded", function () {

  /* ==========================================================
                AUTO HIDE DJANGO MESSAGES
========================================================== */

const alerts = document.querySelectorAll(".alert");

alerts.forEach(function(alert){

    setTimeout(function(){

        alert.style.transition = "all .5s ease";

        alert.style.opacity = "0";

        alert.style.transform = "translateY(-15px)";

        setTimeout(function(){

            alert.remove();

        },500);

    },3000);

});


    /* ======================================================
                    SMOOTH SCROLL
    ====================================================== */

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(

                this.getAttribute("href")

            );

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });


    /* ======================================================
                    SCROLL TO TOP BUTTON
    ====================================================== */

    const scrollBtn = document.getElementById("scrollTopBtn");

    if (scrollBtn) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 400) {

                scrollBtn.style.display = "flex";

            }

            else {

                scrollBtn.style.display = "none";

            }

        });

        scrollBtn.addEventListener("click", function () {

            window.scrollTo({

                top: 0,

                behavior: "smooth"

            });

        });

    }

});




/* ==========================================================
                SHOW / HIDE PASSWORD
========================================================== */

const passwordFields = document.querySelectorAll(

    'input[type="password"]'

);

passwordFields.forEach(function(field){

    const wrapper = document.createElement("div");

    wrapper.style.position = "relative";

    wrapper.style.width = "100%";

    field.parentNode.insertBefore(wrapper, field);

    wrapper.appendChild(field);

    const toggle = document.createElement("span");

    toggle.innerHTML = "👁";

    toggle.classList.add("password-toggle");

    wrapper.appendChild(toggle);

    toggle.addEventListener("click", function(){

        if(field.type === "password"){

            field.type = "text";

            toggle.innerHTML = "🙈";

        }

        else{

            field.type = "password";

            toggle.innerHTML = "👁";

        }

    });

});


/* ==========================================================
                PROFILE IMAGE PREVIEW
========================================================== */

const profileImage = document.querySelector(

    'input[type="file"]'

);

if(profileImage){

    profileImage.addEventListener(

        "change",

        function(e){

            const file = e.target.files[0];

            if(!file) return;

            const reader = new FileReader();

            reader.onload = function(event){

                let preview = document.querySelector(

                    "#profilePreview"

                );

                if(!preview){

                    preview = document.createElement("img");

                    preview.id = "profilePreview";

                    preview.classList.add("profile-preview");

                    profileImage.parentNode.appendChild(preview);

                }

                preview.src = event.target.result;

            };

            reader.readAsDataURL(file);

        }

    );

}


/* ==========================================================
                TRIM ALL INPUTS
========================================================== */

document.querySelectorAll(

    "input[type='text'], input[type='email'], textarea"

).forEach(function(input){

    input.addEventListener("blur", function(){

        this.value = this.value.trim();

    });

});


/* ==========================================================
            REMOVE EXTRA SPACES
========================================================== */

document.querySelectorAll(

    "input[type='text'], textarea"

).forEach(function(input){

    input.addEventListener("input", function(){

        this.value = this.value.replace(

            /\s{2,}/g,

            " "

        );

    });

});


/* ==========================================================
                SMART LOADING BUTTONS
========================================================== */

document.querySelectorAll("form").forEach(function(form){

    form.addEventListener("submit", function(e){

        /*
        ------------------------------------------------------
        Get the EXACT button that was clicked.
        This is important when a form has multiple buttons.
        ------------------------------------------------------
        */

        const submitButton = e.submitter;

        if(!submitButton) return;


        /*
        ------------------------------------------------------
        Don't run loading state twice.
        ------------------------------------------------------
        */

        if(submitButton.disabled){

            e.preventDefault();

            return;

        }


        /*
        ------------------------------------------------------
        Disable only the button that was clicked.
        ------------------------------------------------------
        */

        submitButton.disabled = true;


        /*
        ------------------------------------------------------
        Save original button text.
        ------------------------------------------------------
        */

        submitButton.dataset.originalText =
            submitButton.innerHTML;


        /*
        ------------------------------------------------------
        Detect which action was clicked.
        ------------------------------------------------------
        */

        if(submitButton.classList.contains("buy-btn")){

            submitButton.innerHTML =
                '<span class="loader"></span> Please Wait...';

        }

        else if(
            submitButton.classList.contains("add-cart-btn")
        ){

            submitButton.innerHTML =
                '<span class="loader"></span> Adding...';

        }

        else if(
            submitButton.classList.contains("place-order-btn")
        ){

            submitButton.innerHTML =
                '<span class="loader"></span> Placing Order...';

        }

        else if(
            submitButton.classList.contains("login-btn")
        ){

            submitButton.innerHTML =
                '<span class="loader"></span> Logging In...';

        }

        else if(
            submitButton.classList.contains("register-btn")
        ){

            submitButton.innerHTML =
                '<span class="loader"></span> Creating Account...';

        }

        else{

            submitButton.innerHTML =
                '<span class="loader"></span> Please Wait...';

        }

    });

});
/* ==========================================================
                LOGOUT CONFIRMATION
========================================================== */

document.querySelectorAll('a[href*="logout"]').forEach(function(link){

    link.addEventListener("click", function(e){

        const confirmLogout = confirm(

            "Are you sure you want to logout?"

        );

        if(!confirmLogout){

            e.preventDefault();

        }

    });

});


/* ==========================================================
            REMOVE FROM CART CONFIRMATION
========================================================== */

document.querySelectorAll(".remove-btn").forEach(function(button){

    button.addEventListener("click", function(e){

        const confirmDelete = confirm(

            "Remove this item from your cart?"

        );

        if(!confirmDelete){

            e.preventDefault();

        }

    });

});


/* ==========================================================
                RIPPLE EFFECT
========================================================== */

document.querySelectorAll(

    "button"

).forEach(function(button){

    button.addEventListener("click", function(e){

        const ripple = document.createElement("span");

        ripple.classList.add("ripple");

        this.appendChild(ripple);

        const rect = this.getBoundingClientRect();

        ripple.style.left =

            e.clientX - rect.left + "px";

        ripple.style.top =

            e.clientY - rect.top + "px";

        setTimeout(function(){

            ripple.remove();

        },600);

    });

});


/* ==========================================================
                INPUT FOCUS EFFECT
========================================================== */

document.querySelectorAll(

    "input, textarea, select"

).forEach(function(input){

    input.addEventListener("focus", function(){

        this.parentElement.classList.add(

            "input-active"

        );

    });

    input.addEventListener("blur", function(){

        this.parentElement.classList.remove(

            "input-active"

        );

    });

});

/* ==========================================================
                FOOD DETAIL QUANTITY
========================================================== */

const minusBtn = document.getElementById("minusBtn");

const plusBtn = document.getElementById("plusBtn");

const quantityInput = document.getElementById("quantity");

if(minusBtn && plusBtn && quantityInput){

    minusBtn.addEventListener("click", function(){

        let quantity = parseInt(quantityInput.value);

        if(quantity > 1){

            quantity--;

            quantityInput.value = quantity;

        }

    });

    plusBtn.addEventListener("click", function(){

        let quantity = parseInt(quantityInput.value);

        quantity++;

        quantityInput.value = quantity;

    });

}
/* ==========================================================
        RESET BUTTONS WHEN RETURNING TO PAGE
========================================================== */

window.addEventListener("pageshow", function(){

    /*
    ------------------------------------------------------
    Reset Add To Cart buttons
    ------------------------------------------------------
    */

    document.querySelectorAll(".add-cart-btn").forEach(
        function(button){

            button.disabled = false;

            button.classList.remove("loading");

            button.innerHTML = "🛒 Add To Cart";

        }
    );


    /*
    ------------------------------------------------------
    Reset Buy Now buttons
    ------------------------------------------------------
    */

    document.querySelectorAll(".buy-btn").forEach(
        function(button){

            button.disabled = false;

            button.classList.remove("loading");

            button.innerHTML = "⚡ Buy Now";

        }
    );


    /*
    ------------------------------------------------------
    Reset Checkout button
    ------------------------------------------------------
    */

    document.querySelectorAll(".place-order-btn").forEach(
        function(button){

            button.disabled = false;

        }
    );

});
