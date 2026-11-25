// 브라우저에서 HTML 로 해석하는 API
import DOMPurify from 'dompurify';

function render() {
  const q = new URLSearchParams(location.search).get('q');
  // ruleid: mois-1-04-xss-js
  document.getElementById('out').innerHTML = '<b>' + q + '</b>';
  const box = document.querySelector('#box');
  // ruleid: mois-1-04-xss-js
  box.outerHTML = location.hash.slice(1);
  // ruleid: mois-1-04-xss-js
  box.insertAdjacentHTML('beforeend', document.referrer);
  // ruleid: mois-1-04-xss-js
  document.write('<p>' + window.name + '</p>');
  // ruleid: mois-1-04-xss-js
  box.innerHTML += decodeURIComponent(location.hash);
  const frame = document.createElement('iframe');
  // ruleid: mois-1-04-xss-js
  frame.srcdoc = document.URL;
}

window.addEventListener('message', (event) => {
  // ruleid: mois-1-04-xss-js
  $('#chat').append(event.data);
  // ruleid: mois-1-04-xss-js
  $(event.data);
  const list = jQuery('#list');
  // ruleid: mois-1-04-xss-js
  list.html(event.data.text);
});

// 속이는 예: DOMPurify 결과를 속성 값 안에 넣음 (따옴표를 바꾸지 않는다)
function title() {
  const t = DOMPurify.sanitize(location.hash);
  // ruleid: mois-1-04-xss-js
  document.body.innerHTML = '<div title="' + t + '">x</div>';
}
