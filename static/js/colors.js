
function hsv_to_rgb(h, s, v) {
  var r, g, b, i, f, p, q, t;
  i = Math.floor(h * 6);
  f = h * 6 - i;
  p = v * (1 - s);
  q = v * (1 - f * s);
  t = v * (1 - (1 - f) * s);
  switch (i % 6) {
    case 0: r = v, g = t, b = p; break;
    case 1: r = q, g = v, b = p; break;
    case 2: r = p, g = v, b = t; break;
    case 3: r = p, g = q, b = v; break;
    case 4: r = t, g = p, b = v; break;
    case 5: r = v, g = p, b = q; break;
  }
  return [
    Math.round(r * 255),
    Math.round(g * 255),
    Math.round(b * 255)
  ];
}

function get_rainbow_steps(length) {
  var colors = [];
  var step = 1/length;
  for (i = 0; i < length; i++) {
    var h = i * step;
    var [r,g,b] = hsv_to_rgb(h, 1, 1);
    var solid = `rgba(${r},${g},${b},1)`;
    colors.push(solid);
  }
  return colors
}