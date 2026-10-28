(function () {
  var root = document.documentElement;
  var btn = document.getElementById('themeBtn');
  function icon() { if (btn) btn.textContent = root.dataset.theme === 'dark' ? '☀' : '☾'; }
  icon();
  if (btn) btn.addEventListener('click', function () {
    var t = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = t;
    try { localStorage.setItem('theme', t); } catch (e) {}
    icon();
  });

  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    function close() { lb.hidden = true; document.body.style.overflow = ''; }
    document.querySelectorAll('.zoomable').forEach(function (img) {
      img.addEventListener('click', function () {
        lbImg.src = img.src; lb.hidden = false; document.body.style.overflow = 'hidden';
      });
    });
    lb.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  }

  var share = document.getElementById('shareBtn');
  if (share) share.addEventListener('click', function () {
    var data = { title: share.dataset.title, url: location.href };
    if (navigator.share) { navigator.share(data).catch(function () {}); }
    else if (navigator.clipboard) {
      navigator.clipboard.writeText(location.href).then(function () {
        var old = share.textContent; share.textContent = 'تم نسخ الرابط ✓';
        setTimeout(function () { share.textContent = old; }, 1800);
      });
    }
  });
})();
