export default {
  mounted(el) {
    const setTarget = (element) => {
      element.querySelectorAll("a").forEach((anchor) => {
        anchor.setAttribute("target", "_blank");
        anchor.setAttribute("rel", "noopener noreferrer");
      });
    };

    setTarget(el);

    const observer = new MutationObserver(() => setTarget(el));
    observer.observe(el, { childList: true, subtree: true });
  },
};
