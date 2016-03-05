# coding: utf-8
"""将ip地址换算成int，或者将int换算成ip
"""


def ip2int(ip):
    ip_parts = ip.split('.')
    parts = ip_parts[::-1]
    ipsum = 0
    for index, part in enumerate(parts):
        ipsum += int(part) * (256 ** (index))
    return ipsum


def int2ip(integer):
    parts = []
    for exp in range(3, -1, -1):
        exp_val = 256 ** exp
        part = integer / exp_val
        parts.append(str(part))
        integer = integer % exp_val
    return '.'.join(parts)


if __name__ == "__main__":
    ip = '163.177.158.77'
    intip = ip2int(ip)
    ipint = int2ip(intip)
    print '{} ==> {}'.format(ip, intip)
    print '{} ==> {}'.format(intip, ipint)
