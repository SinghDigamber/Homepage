document.addEventListener("DOMContentLoaded", function() {
    var lazyloadImages = document.querySelectorAll("img.lazy-load");
    var lazyloadThrottleTimeout;

    function lazyload () {
    if(lazyloadThrottleTimeout) {
        clearTimeout(lazyloadThrottleTimeout);
    }

    lazyloadThrottleTimeout = setTimeout(function() {
        var scrollTop = window.pageYOffset;
        lazyloadImages.forEach(function(img) {
            if(img.offsetTop < (window.innerHeight + scrollTop)) {
                img.src = img.dataset.src;
                img.classList.remove('lazy-load');
            }
        });
    }, 20);
  }
});