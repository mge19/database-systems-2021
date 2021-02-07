function toggle_password(a,y) {
  var x=$('#'+a);
  if (x.attr('type') == "password") {
    x.attr('type',"text");
    y.className="fa fa-eye-slash eyespan";
  } else {
    x.attr('type',"password");
    y.className="fa fa-eye eyespan";}
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
