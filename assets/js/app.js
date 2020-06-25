'use strict';

const $ = require('jquery');
const tippy = require('tippy.js').default;

function inViewport($el) {
    try {
      let elH = $el.outerHeight(),
        H = $(window).height(),
        r = $el[0].getBoundingClientRect(), t = r.top, b = r.bottom;
      return Math.max(0, t > 0 ? Math.min(elH, H - t) : Math.min(b, H));
    } catch (e) {
      return 0;
    }
}

let hoverTargetEl = null;
let tippyTargetId = null;
let tippyInstances = {};

function getTippyId($el) {
  const targetHashId = $el.attr('href');
  const myHashId = $el.closest('.post-container').attr('id');
  return `${myHashId}:${targetHashId}`;
}

function initTooltips() {
  const qpfl = $('.quoted-post-from-link,.quoted-post-to-link');
  qpfl.each(function () {
    const tippyId = getTippyId($(this));
    tippyInstances[tippyId] = tippy(this, {
      content(reference) {
        const href = reference.getAttribute('href');
        let targetEl = document.querySelector(`.post-container${href} .pseudo-post-container`);
        if (!targetEl) {
          targetEl = document.querySelector(`.post-container.op${href}`);
        }
        return targetEl ? targetEl.innerHTML : null;
      },
      onShow(instance) {
        if (instance.props.content === null) {
          instance.setContent('<b>Loading...</b>');
          console.log('need to load content')
          const href = instance.reference.getAttribute('href');
          const targetPostId = href.split('#p')[1];
          $.ajax({
            url: `/partial/post/${targetPostId}/`,
            method: 'GET',
          }).done(function(data) {
            $('body').append(data);
            const targetEl = document.querySelector(`.post-container${href} .pseudo-post-container`);
            instance.setContent(targetEl ? targetEl.innerHTML : '<b>:(</b>');
          });
        }
      },
      allowHTML: true,
      arrow: false,
      placement: 'right-end',
      theme: 'translucent',
    });
    tippyInstances[tippyId].disable();
  });
  qpfl.on('mouseout', function (e) {
    if (hoverTargetEl) {
      hoverTargetEl.removeClass('highlight');
      hoverTargetEl = null;
    } else if (tippyTargetId && tippyInstances[tippyTargetId]) {
      tippyInstances[tippyTargetId].disable();
      tippyTargetId = null;
    }
  });
  qpfl.on('mouseover', function (e) {
    const href = $(this).attr('href');
    const targetEl = $(href);
    if (targetEl) {
      if (inViewport(targetEl) > 24) {
        hoverTargetEl = targetEl;
        targetEl.addClass('highlight');
      } else {
        const tippyId = getTippyId($(this));
        if (tippyInstances[tippyId]) {
          tippyTargetId = tippyId;
          tippyInstances[tippyTargetId].enable();
        } else {
          console.error('tippy instance not found:', href);
        }
      }
    } else {
      console.error('target not found:', href);
    }
  });
}

$(document).ready(function() {
  $('.link-disabled').on('click', function (e) {
    e.preventDefault();
  });
  $('.scroll-to-bottom, .scroll-to-top').on('click', function (e) {
    e.preventDefault();
    let hash = this.hash;
    $('html, body').animate({
      scrollTop: $(hash).offset().top
    }, 800, function () {
      window.location.hash = hash;
    });
  });
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
  initTooltips();
});

