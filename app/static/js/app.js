(function () {
  'use strict';

  function debounce(fn, delay) {
    var timer;
    return function () {
      var args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () { fn.apply(null, args); }, delay || 250);
    };
  }

  function autoFocus() {
    var target = document.querySelector('[data-autofocus]');
    if (target) { target.focus(); }
  }

  function bindSearchDebounce() {
    document.querySelectorAll('[data-search-debounce]').forEach(function (input) {
      input.addEventListener('input', debounce(function () {
        input.dispatchEvent(new CustomEvent('buvette:search', { bubbles: true, detail: { value: input.value } }));
      }, 300));
    });
  }

  function notify(message, category) {
    var stack = document.querySelector('.flash-stack') || document.createElement('div');
    stack.className = 'flash-stack';
    if (!stack.parentNode) { document.querySelector('.app-main').prepend(stack); }
    var alert = document.createElement('div');
    alert.className = 'alert alert-' + (category || 'info');
    alert.setAttribute('role', 'alert');
    alert.textContent = message;
    stack.appendChild(alert);
  }

  function confirmAction(message) {
    return window.confirm(message || 'Are you sure?');
  }

  window.Buvette = { debounce: debounce, notify: notify, confirmAction: confirmAction };
  document.addEventListener('DOMContentLoaded', function () {
    autoFocus();
    bindSearchDebounce();
  });
}());
