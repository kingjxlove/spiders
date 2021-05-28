import json



with open('one_m.json','r',encoding='utf8')as fp:
    one_m = json.load(fp)
    print(len(one_m))

with open('one_y.json','r',encoding='utf8')as fp:
    one_y = json.load(fp)
    print(len(one_y))

with open('three_m.json','r',encoding='utf8')as fp:
    three_m = json.load(fp)
    print(len(three_m))

with open('six_m.json','r',encoding='utf8')as fp:
    six_m = json.load(fp)
    print(len(six_m))

with open('two_y.json','r',encoding='utf8')as fp:
    two_y = json.load(fp)
    print(len(two_y))

with open('three_y.json','r',encoding='utf8')as fp:
    three_y = json.load(fp)
    print(len(three_y))

a_top_dict = []
b_top_dict = []
c_top_dict = []
d_top_dict = []
e_top_dict = []
f_top_dict = []

a_top_list = []
b_top_list = []
c_top_list = []
d_top_list = []
e_top_list = []
f_top_list = []

print(one_m[0].split(',')[0])
# top 2366 (1/3)
for i in range(2366):
	one_m_top = {"code":one_m[i].split(',')[0], "name": one_m[i].split(',')[1]}
	three_m_top = {"code":three_m[i].split(',')[0], "name": three_m[i].split(',')[1]}
	six_m_top = {"code":six_m[i].split(',')[0], "name": six_m[i].split(',')[1]}

	a_top_dict.append(one_m_top)
	a_top_list.append(one_m[i].split(',')[0])
	b_top_dict.append(three_m_top)
	b_top_list.append(three_m[i].split(',')[0])
	c_top_dict.append(six_m_top)
	c_top_list.append(six_m[i].split(',')[0])

# top 1775 (1/4)
for i in range(1775):
	one_y_top = {"code":one_y[i].split(',')[0], "name": one_y[i].split(',')[1]}
	two_y_top = {"code":two_y[i].split(',')[0], "name": two_y[i].split(',')[1]}
	three_y_top = {"code":three_y[i].split(',')[0], "name": three_y[i].split(',')[1]}

	d_top_dict.append(one_y_top)
	d_top_list.append(one_y[i].split(',')[0])
	e_top_dict.append(two_y_top)
	e_top_list.append(two_y[i].split(',')[0])
	f_top_dict.append(three_y_top)
	f_top_list.append(three_y[i].split(',')[0])

top_1_4 = []
for item in a_top_dict:
	if item["code"] in a_top_list and item["code"] in b_top_list and item["code"] in c_top_list and item["code"] in d_top_list and item["code"] in e_top_list and item["code"] in f_top_list:
		print("综合TOP3344:",item)
		top_1_4.append(item)

print(len(top_1_4))

