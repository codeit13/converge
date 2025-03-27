const THEME_KEY = "theme-mode";

export const getTheme = () => {
  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme) return savedTheme;

  // Check system preference
  if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
    return "dark";
  }
  return "light";
};

export const setTheme = (theme) => {
  const root = document.documentElement;
  const isDark =
    theme === "dark" ||
    (theme === "system" &&
      window.matchMedia("(prefers-color-scheme: dark)").matches);

  const body = document.body;
  if (isDark) {
    if (!body.classList.contains("dark")) {
      body.classList.add("dark");
    }
  } else {
    if (body.classList.contains("dark")) {
      body.classList.remove("dark");
    }
  }

  localStorage.setItem(THEME_KEY, theme);
};

// Listen for system theme changes
export const initTheme = () => {
  const savedTheme = localStorage.getItem(THEME_KEY);
  if (savedTheme === "system") {
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", ({ matches }) => {
        if (matches) {
          document.documentElement.classList.add("dark");
        } else {
          document.documentElement.classList.remove("dark");
        }
      });
  }
  setTheme(savedTheme || getTheme());
};
