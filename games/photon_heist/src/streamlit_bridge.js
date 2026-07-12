(function () {
  "use strict";

  const SHARED_LANGUAGE_KEY = "photonHeistLanguage";
  const embedded = window.parent !== window;
  let heightFrame = null;

  function normalizeLanguage(value) {
    return value === "en" ? "en" : "ko";
  }

  function queryLanguage() {
    const queryLanguage = new URLSearchParams(window.location.search).get("lang");
    if (queryLanguage === "ko" || queryLanguage === "en") return queryLanguage;
    return null;
  }

  function readLanguage() {
    const urlLanguage = queryLanguage();
    if (urlLanguage) return urlLanguage;
    try {
      return normalizeLanguage(localStorage.getItem(SHARED_LANGUAGE_KEY));
    } catch (_) {
      return normalizeLanguage(document.documentElement.lang);
    }
  }

  function saveLanguage(value) {
    const lang = normalizeLanguage(value);
    document.documentElement.lang = lang;
    try {
      localStorage.setItem(SHARED_LANGUAGE_KEY, lang);
      localStorage.setItem("photonHeistHubLanguage", lang);
    } catch (_) {}
    return lang;
  }

  function withLanguage(path, value = readLanguage()) {
    try {
      const url = new URL(path, window.location.href);
      url.searchParams.set("lang", normalizeLanguage(value));
      return url.pathname.split("/").pop() + url.search + url.hash;
    } catch (_) {
      const separator = path.indexOf("?") === -1 ? "?" : "&";
      return `${path}${separator}lang=${normalizeLanguage(value)}`;
    }
  }

  function postToStreamlit(message) {
    if (!embedded) return;
    window.parent.postMessage({ isStreamlitMessage: true, ...message }, "*");
  }

  function reportHeight() {
    if (!embedded) return;
    if (heightFrame !== null) window.cancelAnimationFrame(heightFrame);
    heightFrame = window.requestAnimationFrame(function () {
      heightFrame = null;
      const height = Math.max(
        720,
        document.body ? document.body.scrollHeight : 0,
        document.documentElement.scrollHeight
      );
      postToStreamlit({ type: "streamlit:setFrameHeight", height: height + 8 });
    });
  }

  window.PhotonHeistBridge = {
    getLanguage: readLanguage,
    saveLanguage: saveLanguage,
    withLanguage: withLanguage,
    reportHeight: reportHeight
  };

  saveLanguage(readLanguage());

  window.addEventListener("message", function (event) {
    const message = event.data;
    if (!message || message.type !== "streamlit:render") return;
    const lang = saveLanguage(message.args && message.args.lang);
    window.dispatchEvent(new CustomEvent("photonheist:language", { detail: { lang: lang } }));
    reportHeight();
  });

  if (embedded) {
    postToStreamlit({ type: "streamlit:componentReady", apiVersion: 1 });
    if ("ResizeObserver" in window) {
      const resizeObserver = new ResizeObserver(reportHeight);
      resizeObserver.observe(document.documentElement);
    }
    window.addEventListener("load", reportHeight, { once: true });
    reportHeight();
  }
})();
