captcha = file("day1-input.txt").read()

prev = captcha[0]
captcha += prev
total = 0

for c in captcha[1:]:
    curr = int(c)
    if curr == prev:
       total += curr
    prev = curr

print total
