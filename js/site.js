(function () {
  // Instagram version: keep visitors inside /ig/ and never show the full-version links.
  var ig = false;
  try { ig = /[?&]from=ig\b/.test(location.search) || sessionStorage.getItem('pf-ig') === '1'; if (/[?&]from=ig\b/.test(location.search)) sessionStorage.setItem('pf-ig', '1'); } catch (e) { ig = /[?&]from=ig\b/.test(location.search); }
  if (document.body.dataset.ig === '1') { ig = true; try { sessionStorage.setItem('pf-ig', '1'); } catch (e) {} }
  if (document.body.dataset.ig === '0') { try { sessionStorage.removeItem('pf-ig'); } catch (e) {} ig = false; }
  if (ig) {
    document.querySelectorAll('[data-home]').forEach(function (a) { a.setAttribute('href', a.dataset.igHref); });
    document.querySelectorAll('[data-full-only]').forEach(function (el) { el.remove(); });
  }

  // Galleries: arrow buttons + lightbox
  document.querySelectorAll('.gallery').forEach(function (g) {
    var track = g.querySelector('.track');
    var step = function (d) { var f = track.querySelector('figure'); if (!f) return; track.scrollBy({ left: d * (f.getBoundingClientRect().width + 16), behavior: 'smooth' }); };
    var pv = g.querySelector('.g-prev'), nx = g.querySelector('.g-next');
    if (pv) pv.addEventListener('click', function () { step(-1); });
    if (nx) nx.addEventListener('click', function () { step(1); });
  });

  var dlg = document.querySelector('dialog.lb');
  if (!dlg || !dlg.showModal) return;
  var img = dlg.querySelector('img'), cap = dlg.querySelector('.cap'), list = [], idx = 0;
  var show = function () { var el = list[idx]; img.src = el.currentSrc || el.src; img.alt = el.alt; cap.textContent = (idx + 1) + ' / ' + list.length; };
  document.querySelectorAll('.track img').forEach(function (el) {
    el.addEventListener('click', function () {
      list = Array.prototype.slice.call(el.closest('.track').querySelectorAll('img'));
      idx = list.indexOf(el); show(); dlg.showModal();
    });
  });
  var move = function (d) { idx = (idx + d + list.length) % list.length; show(); };
  dlg.querySelector('.x').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.pv').addEventListener('click', function (e) { e.stopPropagation(); move(-1); });
  dlg.querySelector('.nx').addEventListener('click', function (e) { e.stopPropagation(); move(1); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.classList.contains('lb-in')) dlg.close(); });
  document.addEventListener('keydown', function (e) { if (!dlg.open) return; if (e.key === 'ArrowRight') move(1); if (e.key === 'ArrowLeft') move(-1); });
})();
