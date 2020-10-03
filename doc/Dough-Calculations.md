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
0.2 = 0.1 * exp(ssf * t)
2 = exp(ssf * t)
ln 2 = ssf * t
t = 
To compute starter strength factor (ssf), mix a 10% seeded (rl1) and a 20% seeded (rl2) levain and measure the time (t1 and t2) needed for each of them (at 25 deg C) to rise to their highest. 

The difference in time accounts is how long it takes the 10% seeded levain to grow to 20%. Assuming the growth to be exponential in time, we have:

rl2 = rl1 * exp(ssf * (t2 - t1))

and therefore

ssf = ln(rl2 / rl1) / (t2 - t1) (starter strength factor)

and 

t2 - t1 = ln(rl2 / rl1) / ssf (time needed for 10% seeded levain to rise to 20%)

So, for instance, if the 10% seeded levain takes 4.25hr and the 20% seeded 3.5hr to rise to highest:
t1 = 4.25hr, t2 = 3.5hr, rl1 = 0.1, rl2 = 0.2 and 
ssf = 0.924 hr^-1

We can see that after 3.5 hours, with rl_i = 20%, we will have an rl_f of:

rl_f = 0.2 * exp(0.924 * 3.5) = 5.08 ~ 5

and this is the rl associated with the highest rise. In other words, we take the highest rise to be the point at which rl becomes almost 5.08. That is, the time needed for a rl seeded levain to rise to highest (rl becoming 5.08) is:

t = ln(5 / rl) / ssf

We can now estimate the amount of time needed for a 10% and 5% seeded levains to rise to highest:

10% : ln(5.08 / 0.1) / 0.924 = 4.25hr
5% : ln(5.08 / 0.05) / 0.924 = 5hr

Multiple experiments with multiple seed percentages can be done and an average ssf computed.

After that using the ssf, you can predict the amount of time needed for the levain to rise to its highest based on the seed percentage. You can also use the ssf formula to adjust the seed percentage to shorten or lengthen the levain rise time to match your schedule constraints.

For a starter with a strengths factor of 0.46 per hour, to extend the rising time of the levain to 10 hours:

r_l = exp(-0.46 * 10) = 0.01

you'll need to use 1% seed in your levain. This can be useful if you want to mix the levain the night before and mix the dough in the morning.
