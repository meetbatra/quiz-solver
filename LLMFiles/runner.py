
cutoff = 54623
sum_of_numbers_gt_eq_cutoff = 0
with open("demo-audio-data.csv", "r") as f:
    for line in f:
        try:
            number = int(line.strip())
            if number >= cutoff:
                sum_of_numbers_gt_eq_cutoff += number
        except ValueError:
            continue
print(sum_of_numbers_gt_eq_cutoff)
