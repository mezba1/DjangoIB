$(document).ready(function() {
  $('.post-image-link').on('click', function (e) {
    e.preventDefault();
    const imgEl = $(this).children(':first');
    const containerEl = $(this).parent();
    const fullSrcUrl = $(this).data('full-src');
    const thumbSrcUrl = $(this).data('thumb-src');
    if (containerEl.hasClass('expanded')) {
      containerEl.removeClass('expanded');
      imgEl.attr('src', thumbSrcUrl);
    } else {
      containerEl.addClass('expanded');
      imgEl.attr('src', fullSrcUrl);
    }
  });
});
