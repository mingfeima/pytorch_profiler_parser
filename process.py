################################################################
# This file is used to process the profile files resulted by 
# autoprofiler of pytorch
# The following is a example :

# import torch
# x = torch.randn((1, 1), requires_grad=True)
# with torch.autograd.profiler.profile() as prof:
#     y=x ** 2
#     y.backward()

# print(prof)
# prof.export_chrome_trace("result.json")


# After get a json file, you can run the file on terminal
# python process.py --input result.json --output result.xlsx

################################################################

import json
import xlsxwriter
import argparse
from  tqdm import tqdm
def main(args):

	f=open(args.input_file_name,encoding='utf-8')
	#setting is a array of one dim
	setting=json.load(f)
	# getting the total opt name
	opt_name=[]
	# save unique opt data
	dic_unique={}
	keys=['name','ph','ts','dur','tid','pid']
	for i in tqdm(range(len(setting))):
		if 'cat' not in setting[i]:
			if setting[i]['name']+setting[i]['pid'] not in opt_name:
				opt_name.append(setting[i]['name']+setting[i]['pid'])
				dic_unique[setting[i]['name']+setting[i]['pid']]=setting[i]
				dic_unique[setting[i]['name']+setting[i]['pid']]['call_num']=1
			else:
				dic_unique[setting[i]['name']+setting[i]['pid']]['call_num']+=1
				for key in keys:
					if isinstance(setting[i][key],float):
						dic_unique[setting[i]['name']+setting[i]['pid']][key]+=setting[i][key]

	keys.append('call_num') #the call_num is the numbers calls of a function
	Values=[dic_unique[x] for x in opt_name]

	workbook = xlsxwriter.Workbook(args.out_file_name)
	worksheet = workbook.add_worksheet()

	for j in range(len(keys)):
		worksheet.write(0,j,keys[j])
		for i in range(len(Values)):
			worksheet.write(i+1,j,Values[i][keys[j]])

	workbook.close()


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='manual to this script')
	parser.add_argument('--input', type=str, default=None)
	parser.add_argument('--output', type=str, default=None)
	args = parser.parse_args()
	main(args)
