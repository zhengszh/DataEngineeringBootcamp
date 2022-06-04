import pandas as pd
import numpy as np
import scipy.stats as stats
# url='https://drive.google.com/file/d/1PCJ7ltluquoXKi6MYTPMfwZQNI_-MIFP/view?usp=sharing'
# url='https://drive.google.com/uc?id=' + url.split('/')[-2]
# df = pd.read_csv(url)


fileObj = open("data_dict.txt", "r")
di = eval(fileObj.read())
fileObj.close()

# dataset = {}
# for key, key_dict in di.iteritems():
# 	for idx, val in key_dict.iteritems():
# 		td = dataset.setdefault(idx, {})
# 		td[key] = val

# fileObj = open("data_dict.txt", "w")
# fileObj.write("%s" % dataset)
# fileObj.close()


def f1(di):
	emiss_list = []

	for item in di.itervalues():
		if item['Make'] != 'Volkswagen':
			continue
		emiss_list.append(item['CO2 Emission Grams/Mile'])

	return sum(emiss_list) / len(emiss_list)

def f2(di):
	brand_dict = {}

	for item in di.itervalues():
		name_set = brand_dict.setdefault(item['Make'], set())
		name_set.add(item['Model'])

	brand_list = brand_dict.items()
	brand_list = [[t[0], len(t[1])] for t in brand_list]
	brand_list = sorted(brand_list, key=lambda t: t[1], reverse=True)

	return brand_list[:5]

def f3(di):
	fuel_set = set()
	for item in di.itervalues():
		fuel_set.add(item['Fuel Type'])

	return sorted(list(fuel_set))


def f4(di):
	toyota_list = []

	fuel_list = []

	for item in di.itervalues():
		if item['Make'] != 'Toyota':
			continue
		toyota_list.append(item)
		fuel_list.append(item['Fuel Barrels/Year'])

	fuel_list = np.array(fuel_list)
	fuel_z_list = list(stats.zscore(fuel_list))

	res_list = []

	for toyota, fuel_z in zip(toyota_list, fuel_z_list):
		res_list.append([toyota['Model'], int(item['Year']), fuel_z])

	def cmp_func(t1, t2):
		abs1 = abs(t1[-1])
		abs2 = abs(t2[-1])
		if abs1 == abs2:
			y1 = t1[1]
			y2 = t2[1]
			if y1 == y2:
				return 0
			return -1 if y1 > y2 else 1
		return -1 if abs1 > abs2 else 1
	res_list = sorted(res_list, cmp=cmp_func)
	return res_list[:9]


def f5(di):
	golf_list = []
	for item in di.itervalues():
		if item['Model'] != 'Golf':
			continue
		if item['Fuel Type'] != 'Regular':
			continue
		if item['Transmission'] != 'Manual 5-spd':
			continue
		golf_list.append([int(item['Year']), int(item['Combined MPG'])])
	res_list = []
	res_list.append([golf_list[0][0], golf_list[0][1], 0.0])
	for golf_car in golf_list[1:]:
		res_list.append([golf_car[0], golf_car[1], float(golf_car[1] - res_list[-1][1])])
	return res_list


def f6(di):
	brand_set = ['Toyota', 'Ford', 'Volkswagen', 'Nissan', 'Honda']
	brand_dict = {}
	for item in di.itervalues():
		if item['Make'] not in brand_set:
			continue
		li = brand_dict.setdefault(item['Make'], [])
		li.append(item['CO2 Emission Grams/Mile'])
	for brand in brand_dict.keys():
		li = brand_dict[brand]
		brand_dict[brand] = sorted(li)[:5]
	res = []
	for brand in brand_set:
		res.append([brand] + brand_dict[brand])
	return res


def f7(di):
	start_year = 1984
	group_dict = {}
	year_dict = {}
	for item in di.itervalues():
		group = (item['Year'] - start_year) / 5
		year_dict.setdefault(group, set())
		group_list = group_dict.setdefault(group, [])
		group_list.append(item['Combined MPG'])
		year_dict[group].add(item['Year'])
	res = []
	for group_id in group_dict.keys():
		a = np.array(group_dict[group_id])
		s_year = int(start_year + group_id * 5)
		e_year = s_year + 4
		res.append([(s_year, e_year), np.median(a)])
	return res

answer_dict = {
	"Q1": f1(di), "Q2": f2(di), "Q3": f3(di), "Q4": f4(di), "Q5": f5(di), "Q6": f6(di),
}