import glob
import os
#print glob.glob('/home/jayati/Documents/sarcasmdet/sarcastic_with_past/*.')
for f in glob.glob('*.csv'):
	#print f
	for f2 in glob.glob('*.csv'):
		#print f2
		if f!=f2 and os.path.isfile(f) and os.path.isfile(f2):
			with open(f, 'r') as file1:
				with open(f2, 'r') as file2:
					for i, x in enumerate(file1):
						if i==1:
							for i1, x1 in enumerate(file2):
								if i1==1:
									if x==x1:
										#os.remove(f2)
										print f+f2
								elif i1>1:
									break
						elif i>1:
							break
        
			
