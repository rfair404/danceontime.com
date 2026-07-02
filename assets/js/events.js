/*!
 * Dance On Time — Events list (vanilla JS, no dependencies, no Jekyll required).
 *
 * Usage in ANY web app:
 *   <div data-events data-src="/assets/data/events.json" data-print></div>
 *   <script src="/assets/js/events.js"></script>
 *
 * Attributes on the container:
 *   data-src   URL to the events JSON (default: /assets/data/events.json)
 *   data-print add a "Print this list" button
 *   data-limit max number of events to show (optional)
 *
 * JSON shape: an array of events. See _data/events.json for the schema.
 */
(function () {
  "use strict";

  var STYLE_ID = "dot-events-style";
  var CSS = [
    ".dot-events{font-family:Helvetica,Arial,sans-serif;color:#2f2f41;line-height:1.35;max-width:760px}",
    ".dot-events__toolbar{margin:0 0 1.25rem}",
    ".dot-events__btn{background:#e5261f;color:#fff;border:0;border-radius:4px;padding:.55rem 1.1rem;font:inherit;font-weight:700;cursor:pointer}",
    ".dot-events__btn:hover{background:#a01b16}",
    ".dot-events__empty{color:#5c5a5a}",
    ".dot-events__list{list-style:none;margin:0;padding:0}",
    ".dot-event{display:flex;gap:1.25rem;padding:1.25rem 0;border-top:1px solid rgba(47,47,65,.12)}",
    ".dot-event:last-child{border-bottom:1px solid rgba(47,47,65,.12)}",
    ".dot-event__date{flex:0 0 64px;text-align:center;line-height:1.1;color:#e5261f}",
    ".dot-event__month{display:block;text-transform:uppercase;font-size:.8rem;letter-spacing:.06em;font-weight:700}",
    ".dot-event__day{display:block;font-family:'Playfair Display',Georgia,serif;font-size:2rem;color:#2f2f41}",
    ".dot-event__weekday{display:block;font-size:.75rem;color:#5c5a5a;text-transform:uppercase}",
    ".dot-event__body{flex:1 1 auto}",
    ".dot-event__head{display:flex;align-items:baseline;flex-wrap:wrap;gap:.5rem .75rem}",
    ".dot-event__title{font-family:'Playfair Display',Georgia,serif;font-size:1.35rem;margin:0}",
    ".dot-event--featured .dot-event__title{color:#e5261f}",
    ".dot-event__cat{font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700;color:#e5261f;border:1px solid #e5261f;border-radius:999px;padding:.1rem .6rem}",
    ".dot-event__meta{margin:.35rem 0 .5rem;color:#5c5a5a;font-size:.95rem}",
    ".dot-event__meta span+span:before{content:'\\2022';margin:0 .5rem;color:rgba(47,47,65,.35)}",
    ".dot-event__desc{margin:0;color:#2f2f41}",
    ".dot-event__links{margin:.6rem 0 0}",
    ".dot-event__link{color:#e5261f;font-weight:700;margin-right:1rem;text-decoration:none}",
    ".dot-event__link:hover{text-decoration:underline}",
    "@media print{.dot-events__toolbar,.dot-event__links{display:none!important}",
    ".dot-events{max-width:none;color:#000}",
    ".dot-event{break-inside:avoid;page-break-inside:avoid;border-color:#999}",
    ".dot-event__title,.dot-event__day,.dot-event--featured .dot-event__title{color:#000}",
    ".dot-event__cat{color:#000;border-color:#000}}"
  ].join("");

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement("style");
    s.id = STYLE_ID;
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function esc(v) {
    return String(v == null ? "" : v).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function parseDate(s) {
    if (!s) return null;
    var d = new Date(s);
    return isNaN(d) ? null : d;
  }

  var MON = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  var DOW = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

  function fmtTime(d) {
    var h = d.getHours(), m = d.getMinutes();
    var ap = h >= 12 ? "PM" : "AM";
    h = h % 12; if (h === 0) h = 12;
    return h + ":" + (m < 10 ? "0" + m : m) + " " + ap;
  }

  function loc(l) {
    if (!l || !l.name) return "";
    var out = l.name;
    if (l.city) out += ", " + l.city;
    if (l.city && l.state) out += ", " + l.state;
    return out;
  }

  function renderEvent(ev) {
    var start = parseDate(ev.start), end = parseDate(ev.end);
    var time = ev.allDay ? "All day"
      : (start ? fmtTime(start) + (end ? " – " + fmtTime(end) : "") : "");

    var meta = [];
    if (time) meta.push('<span>' + esc(time) + '</span>');
    var lc = loc(ev.location); if (lc) meta.push('<span>' + esc(lc) + '</span>');
    if (ev.price) meta.push('<span>' + esc(ev.price) + '</span>');

    var links = [];
    if (ev.registerUrl) links.push('<a class="dot-event__link" href="' + esc(ev.registerUrl) + '">Register</a>');
    if (ev.url) links.push('<a class="dot-event__link" href="' + esc(ev.url) + '">Details</a>');

    return '' +
      '<li class="dot-event' + (ev.featured ? ' dot-event--featured' : '') + '">' +
        '<div class="dot-event__date">' +
          (start
            ? '<span class="dot-event__month">' + MON[start.getMonth()] + '</span>' +
              '<span class="dot-event__day">' + start.getDate() + '</span>' +
              '<span class="dot-event__weekday">' + DOW[start.getDay()] + '</span>'
            : '') +
        '</div>' +
        '<div class="dot-event__body">' +
          '<div class="dot-event__head">' +
            '<h3 class="dot-event__title">' + esc(ev.title) + '</h3>' +
            (ev.category ? '<span class="dot-event__cat">' + esc(ev.category) + '</span>' : '') +
          '</div>' +
          (meta.length ? '<p class="dot-event__meta">' + meta.join('') + '</p>' : '') +
          (ev.description ? '<p class="dot-event__desc">' + esc(ev.description) + '</p>' : '') +
          (links.length ? '<p class="dot-event__links">' + links.join('') + '</p>' : '') +
        '</div>' +
      '</li>';
  }

  function render(container, events) {
    events = (events || []).slice().sort(function (a, b) {
      return (parseDate(a.start) || 0) - (parseDate(b.start) || 0);
    });
    var limit = parseInt(container.getAttribute("data-limit"), 10);
    if (!isNaN(limit)) events = events.slice(0, limit);

    var html = '<div class="dot-events">';
    if (container.hasAttribute("data-print")) {
      html += '<div class="dot-events__toolbar">' +
        '<button type="button" class="dot-events__btn" onclick="window.print()">Print this list</button></div>';
    }
    html += events.length
      ? '<ul class="dot-events__list">' + events.map(renderEvent).join("") + "</ul>"
      : '<p class="dot-events__empty">No upcoming events right now. Check back soon.</p>';
    html += "</div>";
    container.innerHTML = html;
  }

  function init(container) {
    var src = container.getAttribute("data-src") || "/assets/data/events.json";
    fetch(src, { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (data) { injectStyle(); render(container, data); })
      .catch(function (e) {
        injectStyle();
        container.innerHTML = '<div class="dot-events"><p class="dot-events__empty">Unable to load events (' + esc(e.message) + ').</p></div>';
      });
  }

  // Expose for manual/framework use: DanceOnTimeEvents.render(el, eventsArray)
  window.DanceOnTimeEvents = { render: function (el, evs) { injectStyle(); render(el, evs); }, init: init };

  function boot() {
    var nodes = document.querySelectorAll("[data-events]");
    for (var i = 0; i < nodes.length; i++) init(nodes[i]);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
