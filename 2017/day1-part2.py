captcha = file("day1-input.txt").read()

half = len(captcha) / 2
rotated = captcha[half:] + captcha[:half] 
total = 0

for (a,b) in zip(captcha, rotated):
    if a == b:
        total += int(a)

print total
