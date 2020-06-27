# Dough hydration
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

# Starter strength factor
Compute starter strength factor (ssf) by mixing a 10% seeded (r_l) levain and measuring the time (t) needed for it (at 25 deg C) to rise to its highest:

ssf = ln(r_l ^ -1) / t

Multiple experiments with multiple seed percentages can be done and an average ssf computed.

After that using the ssf, you can predict the amount of time needed for the levain to rise to its highest based on the seed percentage. You can also use the ssf formula to adjust the seed percentage to shorten or lengthen the levain rise time to match your schedule constraints.

r_l = exp(-ssf * t)

For a starter with a strengths factor of 0.46 per hour, to extend the rising time of the levain to 10 hours:

r_l = exp(-0.46 * 10) = 0.01

you'll need to use 1% seed in your levain. This can be useful if you want to mix the levain the night before and mix the dough in the morning.
