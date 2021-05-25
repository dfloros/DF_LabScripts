


def fraglist_clearner(fraglist):
	
	if is_number(fraglist]) == True:
			fraglist = [fraglist]
	else: 
		fraglist = [i.strip("?!. ,") for i in fraglist.split(',')]
	
	
	
	for frag in fraglist:
		n=0
		
		if is_number(frag):
			if pd.isna(frag):
				fraglist.remove(frag)
		elif is_string_dtype(frag):
			try:
				float(frag)
			except: 
				#print('2', fraglist)
				fraglist.remove(frag)    
		else:
			try:
				frag = float(frag.strip("?. ,!"))
			except: 
				#print('3', fraglist)
				continue
					
		else: 
			fraglist.remove(frag)
			#print('4', fraglist)
					
	if len(fraglist) >= 1:
		return fraglist
	elif len(fraglist) == 1:
		return [fraglist]
	else:
		return None

def stringify(a):
		if is_number(a):
			b = str(int(round(a,0)))
		elif type(a) == type([]):
			b = [str(int(round(i,0))) for i in a]
		return b


def fraglist_combiner(fraglists, pick_best_by_order = True, maxfrags = None)
	"""fraglists should be 2 lists of fragment masses in increasing CE voltage - outputs [low, high, both, best] lists"""
	fl = fraglists[0]
	fh = fraglists[1]
	fboth = []
	best_list = []
	
	fraglists = [fl,fh, fboth, best_list]
	
	
	flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
	
	for frag in fl:
		frtoken = stringify(frag)
		if frtoken in fhset:
			fboth.append(frag)
			fl.remove(frag)
			fh.remove(frag)
			flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
		elif frtoken in fbset:
			fl.remove()
		
		else:
			if frag == fl[0]:
				best_list.append(frag)
			pass
	
	flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
	
	for frag in fh:
		frtoken = stringify(frag)
		if frtoken in flset:
			fboth.append(frag)
			fh.remove(frag)
			fl.remove(frag)
			flset, fhset, fbset = set(stringify(fl)), set(stringify(fh)), set(stringify(fboth))
		elif frtoken in fbset:
			fh.remove()
		else:
			if frag == fh[0]:
				best_list.append(frag)
			pass
	
	if fboth:
		best_list.append(fboth[0])

	for frag in 
	
	
	for fraglist in fraglists:
		if fraglist:
			pass
		else:
			fraglist = []
	if maxfrags:
		if sum([len(i) for i in a]) > maxfrags:
			r = maxfrags
			while r > 0:
				for fraglist in fraglists: 
				
		else:
			pass
	else:
		pass
	
	if pick_best_by_order:	
		return fraglists
	else:
		return fraglists[:3]
	



##########



				for Q3, CE in make_CE_MRMs(frag, range(40,90, 5)):
					try: 
						Q3s = str(int(Q3))
					except:
						continue


					ID = f'%s_%s_%s_%s_DP%s_CE%s' %(inhouse, chemname, Q1s, Q3s, DP, CE)


					lowfstr = '\t'.join([str(x) for x in (round(Q1,2),round(Q3,3),Time,ID,DP,EP,CE,CXP)])
					method_string = method_string + lowfstr + '\n'
					#print((method_string))
			else: pass
			CEDP_methods[method_name] = method_string
		