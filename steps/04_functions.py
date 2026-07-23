def calc_net(in_count, out_count):
    net = in_count - out_count
    return net


result = calc_net(53281, 59566)
print(result)

print(calc_net(100, 80))
print(calc_net(30, 45))

in_counts = [53281, 21497]
out_counts = [59566, 22697]

for i in range(len(in_counts)):
    net = calc_net(in_counts[i], out_counts[i])
    print(net)


def describe_net(in_count, out_count):
    net = calc_net(in_count, out_count)
    if net >= 0:
        return "転入超過"
    else:
        return "転出超過"


print(describe_net(53281, 59566))
print(describe_net(100, 80))
