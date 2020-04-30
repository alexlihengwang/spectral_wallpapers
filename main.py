import numpy as np
import numpy.random as npr
import scipy.linalg as la

import svgwrite
from cairosvg import svg2png

import random
import string

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def random_GOE(n):
  A = npr.normal(scale = (1 / np.sqrt(2 * n)),size = (n,n))
  return (A + A.T) / 2

def random_gaussians(title, background_color, colors, alphas, ns, height, width, scale):
  def fmt_pts(x,y):
    return [(width / 2 + scale * x_, height / 2 + scale * y_) for (x_,y_) in zip(x,y)]

  dwg = svgwrite.Drawing(title+'.svg', size=(width, height))
  dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), rx=None, ry=None, fill=background_color))

  for color, alpha, n in zip(colors, alphas, ns):
    A1 = random_GOE(n)
    A2 = random_GOE(n)

    x = []
    y = []
    for theta in np.linspace(0, 2 * np.pi, num = 360):
      cos_t = np.cos(theta)
      sin_t = np.sin(theta)
      length = -1 / la.eigh(cos_t * A1 + sin_t * A2, eigvals_only=True, eigvals=(0,0))[0]
      x.append(length * cos_t)
      y.append(length * sin_t)

    curve = dwg.polygon(points=fmt_pts(x,y), fill=color, fill_opacity=alpha)
    dwg.add(curve)

  # dwg.save()
  svg2png(bytestring=dwg.tostring(),write_to=title+'.png')

if __name__ == '__main__':
  title = randomString(4)

  background_color = '#000'
  colors = ['#ca6ecc', '#7c9cd9', '#dc4596', '#595dc6', '#e4476d', '#5a5ec7', '#6f4cc2', '#595dc6', '#585ec6']
  alphas = [1, 0.8, 0.6, 1, 0.8, 0.6, 1, 0.8, 0.6]
  ns = [20,20,20,25,25,25,30,30,30]

  height = 1600
  width = 2560
  scale = 200

  random_gaussians(title, background_color, colors, alphas, ns, height, width, scale)

