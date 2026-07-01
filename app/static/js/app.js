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


  function bindQuantityButtons() {
    document.querySelectorAll('[data-step]').forEach(function (button) {
      button.addEventListener('click', function () {
        var target = document.getElementById(button.getAttribute('data-target'));
        var step = parseInt(button.getAttribute('data-step'), 10);
        var value = Math.max(0, (parseInt(target.value || '0', 10) || 0) + step);
        target.value = value;
      });
    });
  }

  function bindNumericKeypad() {
    var amount = document.querySelector('.keypad-field input');
    if (!amount) { return; }
    document.querySelectorAll('.numeric-keypad button').forEach(function (button) {
      button.addEventListener('click', function () {
        var key = button.textContent.trim();
        var value = amount.value || '';
        if (button.hasAttribute('data-clear-amount')) { amount.value = ''; return; }
        if (button.hasAttribute('data-backspace-amount')) { amount.value = value.slice(0, -1); return; }
        if (key === '.') {
          if (value.indexOf('.') !== -1) { return; }
          amount.value = value ? value + '.' : '0.';
          return;
        }
        if (/^[0-9]$/.test(key)) { amount.value = value + key; }
      });
    });
  }

  window.Buvette = { debounce: debounce, notify: notify, confirmAction: confirmAction };
  document.addEventListener('DOMContentLoaded', function () {
    autoFocus();
    bindSearchDebounce();
    bindQuantityButtons();
    bindNumericKeypad();
  });
}());
