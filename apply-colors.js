fetch('colors.json?t=' + Date.now())
  .then(res => res.json())
  .then(colors => {
    const root = document.documentElement;
    Object.keys(colors).forEach(key => {
      root.style.setProperty(key, colors[key]);
    });
  })
  .catch(() => {});
