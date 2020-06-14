Based on the desired final amount of dough (T), desired dough hydration (H), levain hydration (h), levain-sourced flour to total flour ratio AKA seed (r_l), and ratio of salt to total flour (r_s), we can calculate the amount of levain (l), water (w), and flour (f) to mix:

Ratio of levain to flour:
c_l = r_l * (1 + h) / (h * (1 - r_l))

Ratio of water to flour:
c_w = (H * h - r_l) / (h * (1 - r_l))

Ratio of salt to flour:
c_s = (1 + h + c_l) * r_s / (1 + h)

And
f = T / (1 + c_w + c_l + c_s)
l = c_l * f
w = c_w * f
s = c_s * f

For 100% hydrated levain (h = 1) and a 10% ratio of levain-sourced to total flour (r_l = 0.1)
c_l = 2 / 9
c_w = (10 * H - 1) / 9
c_s = 10 * r_s / 9
f = T / (1 + c_w + c_l + c_s)
l = c_l * f
w = c_w * f
s = c_s * f

For 1kg of 75% hydrated dough with 1.8% salt:
c_l = 2 / 9
c_w = 2 / 3
c_s = 0.02
flour: 509g
levain: 113g
water: 368g
salt: 10g