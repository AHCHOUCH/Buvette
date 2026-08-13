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
    return window.confirm(message || 'Confirmer ?');
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

  function applyNumericKey(value, key) {
    value = value || '';
    if (key === 'clear') { return ''; }
    if (key === 'backspace') { return value.slice(0, -1); }
    if (key === '.') { return value.indexOf('.') !== -1 ? value : (value ? value + '.' : '0.'); }
    if (/^[0-9]$/.test(key)) { return value + key; }
    return value;
  }

  function bindNumericKeypad() {
    document.querySelectorAll('.numeric-keypad').forEach(function (keypad) {
      var amount = document.querySelector(keypad.getAttribute('data-target')) || keypad.closest('form') && keypad.closest('form').querySelector('.keypad-field input') || document.querySelector('.keypad-field input');
      if (!amount) { return; }
      keypad.querySelectorAll('button').forEach(function (button) {
        button.addEventListener('click', function () {
          var key = button.hasAttribute('data-clear-amount') ? 'clear' : button.hasAttribute('data-backspace-amount') ? 'backspace' : button.textContent.trim();
          amount.value = applyNumericKey(amount.value, key);
        });
      });
    });
  }

  function bindClientSelector() {
    document.querySelectorAll('[data-client-search]').forEach(function (input) {
      input.addEventListener('input', function () {
        var q = input.value.toLowerCase();
        document.querySelectorAll('[data-client-card]').forEach(function (card) {
          card.hidden = card.getAttribute('data-search').toLowerCase().indexOf(q) === -1;
        });
      });
    });
    document.querySelectorAll('[data-client-card]').forEach(function (card) {
      card.addEventListener('click', function () {
        document.querySelectorAll('[data-client-card]').forEach(function (c) { c.classList.remove('selected'); });
        card.classList.add('selected');
        var input = document.querySelector('[data-selected-client]');
        if (input) { input.value = card.getAttribute('data-client-id'); }
      });
    });
    document.querySelectorAll('[data-plate-id][data-variant-id]').forEach(function (button) {
      button.addEventListener('click', function () {
        document.querySelectorAll('[data-plate-id][data-variant-id]').forEach(function (b) { b.classList.remove('selected'); });
        button.classList.add('selected');
        document.querySelector('[data-selected-plate]').value = button.getAttribute('data-plate-id');
        document.querySelector('[data-selected-variant]').value = button.getAttribute('data-variant-id');
      });
    });
  }



  function bindLunchForm() {
    var form = document.getElementById('lunch-charge-form');
    if (!form) { return; }
    var client = form.querySelector('#client_id');
    var plate = form.querySelector('#plate_id');
    var variant = form.querySelector('#variant_id');
    var confirm = form.querySelector('#lunch-confirm');
    function sync() {
      var plateId = plate ? plate.value : '';
      if (variant) {
        variant.querySelectorAll('option[data-plate]').forEach(function (option) {
          option.hidden = option.getAttribute('data-plate') !== plateId;
        });
        if (variant.selectedOptions.length && variant.selectedOptions[0].hidden) { variant.value = ''; }
      }
      if (confirm) { confirm.disabled = !(client && client.value && plate && plate.value && variant && variant.value) || plate.disabled || variant.disabled; }
    }
    [client, plate, variant].forEach(function (el) { if (el) { el.addEventListener('change', sync); } });
    sync();
  }

  function bindPageScrollButtons() {
    document.querySelectorAll('[data-scroll-page]').forEach(function (button) {
      button.addEventListener('click', function () {
        var direction = button.getAttribute('data-scroll-page') === 'up' ? -1 : 1;
        window.scrollBy({ top: direction * Math.max(320, window.innerHeight * 0.72), behavior: 'smooth' });
      });
    });
  }

  function bindNavigationDropdowns() {
    var groups = Array.prototype.slice.call(document.querySelectorAll('.app-topnav details.nav-group'));
    groups.forEach(function (group) {
      group.addEventListener('toggle', function () {
        if (!group.open) { return; }
        groups.forEach(function (other) { if (other !== group) { other.open = false; } });
      });
    });
    document.addEventListener('click', function (event) {
      if (!event.target.closest('.app-topnav')) { groups.forEach(function (group) { group.open = false; }); }
    });
  }

  window.Buvette = { debounce: debounce, notify: notify, confirmAction: confirmAction, applyNumericKey: applyNumericKey };
  document.addEventListener('DOMContentLoaded', function () {
    autoFocus();
    bindSearchDebounce();
    bindQuantityButtons();
    bindNumericKeypad();
    bindClientSelector();
    bindLunchForm();
    bindPageScrollButtons();
    bindNavigationDropdowns();
  });
}());
