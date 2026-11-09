/** Navigation owns scroll; focusing a heading must not hide the top bar. */
export function resetAppScroll() {
  for (const element of [document.getElementById("root"), document.scrollingElement, document.documentElement, document.body]) {
    if (element) element.scrollTop = 0;
  }
}
