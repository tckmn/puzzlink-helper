// ==UserScript==
// @name     puzzlink-helper
// @version  1
// @grant    GM.xmlHttpRequest
// @include  https://puzz.link/p*
// ==/UserScript==

var port = 1234;

var timer, pausedTime, cumulPause = 0, sent = false;

window.addEventListener('load', function() {
  timer = document.getElementById('timerpanel');
});

window.addEventListener('keydown', function(e) {
  switch (e.key) {
    case 'o': {
      var notif = document.getElementById('notification'),
          time = timer.textContent.split(' ')[1].split(':');
      if (notif.textContent && !sent) sent = true, GM.xmlHttpRequest({
        method: 'POST',
        url: 'http://localhost:'+port,
        data: JSON.stringify({
          'url': location.search.slice(1),
          't': Math.round(+time[time.length-1] + time[time.length-2]*60 + (time[time.length-3]||0)*3600 - cumulPause/1000)
        }),
        onload: function(r) {
        	notif.textContent = r.responseText;
      	}
      });
      break;
    }
    case 'p':
      if (pausedTime) {
        cumulPause += new Date - pausedTime;
        pausedTime = undefined;
        timer.style.color = '';
      } else {
        pausedTime = new Date;
        timer.style.color = 'red';
      }
      break;
  }
});
