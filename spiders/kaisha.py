import urllib
from urllib import parse

def str2url(s):
    num_loc = s.find('h')
    rows = int(s[0:num_loc])
    strlen = len(s) - num_loc
    cols = int(strlen/rows)
    right_rows = strlen % rows
    new_s = list(s[num_loc:])
    output = ''
    for i in range(len(new_s)):
        x = i % rows
        y = i / rows
        p = 0
        if x <= right_rows:
            p = x * (cols + 1) + y
        else:
            p = right_rows * (cols + 1) + (x - right_rows) * cols + y
        output += new_s[int(p)]
    return parse.unquote(output).replace('^', '0')


def main():
    s = "6hAFxn321%5E525_7%puy445-383Eb1Et%mie2192E%EF71753t%%8E%5a%fafct21at316F25%1646E%h35%-5e%54b54pF2m%%%327E5778143_DE5%E85E8c9%%8i22521%3E9684.Fk19E5-9E%69%32..FFE3%5%%5516mae55%Eb715275"
    result_str = str2url(s)
    print(result_str)

main()
