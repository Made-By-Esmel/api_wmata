const dark_mode_enabled = () =>
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches;

console.log(dark_mode_enabled());

if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  document.querySelector("link[rel*='icon']").href = "https://pub-e0e86bcdb20a447ea11d8706a676342f.r2.dev/metrodark.png";
  document.querySelector("link[rel*='shortcut icon']").href = "https://pub-e0e86bcdb20a447ea11d8706a676342f.r2.dev/metrodark.png";
}