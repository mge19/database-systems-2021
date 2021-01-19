function toggle_password(x,y) {
  var z = document.getElementById(x);
  if (z.type == "password") {
    z.type = "text";
    y.className="far fa-eye-slash";
  } else {
    z.type = "password";
    y.className="far fa-eye";}
}
$(document).ready(function () {
    $('.form').find('input, textarea').on('keyup keydown blur focus', function (e) {

        var $this = $(this),
            label = $this.prev('label');
        if (e.type === 'keyup') {
            if ($this.val() === '') {
                label.removeClass('highlight');
            } else {
                label.addClass('highlight');
            }
        } else if (e.type === 'blur') {
            if ($this.val() === '') {
                label.removeClass('highlight');
            } else {
                label.addClass('highlight');
            }
        } else if (e.type === 'focus') {

            if ($this.val() === '') {
                label.removeClass('highlight');
            }
            else if ($this.val() !== '') {
                label.addClass('highlight');
            }
        } else if (e.type === 'keydown') {
            if ($this.val() === '') {
                label.removeClass('highlight');
            } else {
                label.addClass('highlight');
            }
        } 
    });
});



$(document).ready(function () {
    $('.tab a').on('click', function (e) {
        e.preventDefault();

        $(this).parent().addClass('active');
        $(this).parent().siblings().removeClass('active');

        target = $(this).attr('href');
        $('.tab-content > div').not(target).hide();

        $(target).fadeIn(600);
        $('.Result p').text(target);
    });
});