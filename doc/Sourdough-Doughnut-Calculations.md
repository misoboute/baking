# Known
T : total dough
H : dough hydration
h : levain hydration
sd : seed ratio
rs : sugar to total flour ratio
rst : salt to total flour ratio
rb : butter to total flour ratio
re : egg to total flour ratio
wb : butter water content ratio
we : egg water content ratio
wm : milk water content ratio

# Unknown
l : total levain in final dough
m : total milk in final dough
st : total salt in final dough
s : total sugar in final dough
b : total butter in final dough
e : total egg in final dough
f : total flour without the levain

# Compute
F = T / (sd * (1 + h) + (H - h * sd - wb * rb - we * re) / wm + rs + rst + re + rb + (1 - sd))
l = sd * (1 + h) * F
m = (H - h * sd - wb * rb - we * re) * F / wm
st = rst * F
s = rs * F
b = rb * F
e = re * F
f = (1 - sd) * F

W : total water in the final dough
F : total flour in the final dough
wl : levain water content ratio
fl : levain flour content ratio
f : added flour

T = l + m + s + b + e + f 
T = (sd * (1 + h) + (H - h * sd - wb * rb - we * re) / wm + rs + re + rb + (1 - sd)) * F
F = T / (sd * (1 + h) + (H - h * sd - wb * rb - we * re) / wm + rs + re + rb + (1 - sd))
wl = h / (1 + h)
fl = 1 / (1 + h)
W = h / (1 + h) * l + wm * m + wb * b + we * e
F = f / (1 - sd)

F = fl * l + f
fl * l / F = sd
l = sd * F / fl
l = sd * (1 + h) * F

F - fl * l = f
1 - fl * l / F = f / F
1 - sd = f / F
f = (1 - sd) * F
F = f / (1 - sd)

H = W / F = (h / (1 + h) * l + wm * m + wb * b + we * e) / F
H * F = h / (1 + h) * l + wm * m + wb * b + we * e
H * F = wl * sd * (1 + h) * F + wm * m + wb * rb * F + we * re * F
H * F = h * sd * F + wm * m + wb * rb * F + we * re * F
H = h * sd + wb * rb + we * re + wm * m / F
m = (H - h * sd - wb * rb - we * re) * F / wm

F = (h / l + (1 + h) * wm * m + (1 + h) * wb * b + (1 + h) * we * e) / (2 * H)
sd = fl / F
h = wl / fl = wl * l / (l - wl * l) = wl / (1 - wl)
h = wl / (1 - wl)
h * (1 - wl) = wl = h - h * wl
(1 + h) * wl = h
wl = h / (1 + h)

fl = wl / h = 1 / (1 + h)

W = h / (1 + h) * l + wm * m + wb * b + we * e
F = f * (1 + 1 / (1 + h)) = 2 * f / (1 + h)
l = f * sd * (1 + h) / (1 - sd)
s = f * rs
b = f * rb
e = f * re
T = f * (sd / ((1 - sd) * (1 - h)) + rs + rb + re) + m
F = f * (1 + sd / (1 - sd))
H = (wm * m + h * l + wb * b + we * e) / f * (1 + sd / (1 - sd))
T = l + m + s + b + e + f
