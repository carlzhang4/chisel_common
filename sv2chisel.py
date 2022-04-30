str="""
	input clk,
		input usr_rst,
		input 	[DEPTH_BIT-1:0]  addr_a,
		input 	[DEPTH_BIT-1:0]  addr_b,
		input 	wr_en_a,
		input 	[DATA_WIDTH-1:0]	data_in_a,
		output 	[DATA_WIDTH-1:0] 	data_out_a,
		output logic	[DATA_WIDTH-1:0] 	data_out_b
"""

def clean_str(line):
	has_width = 0
	has_sub = 0
	line = line.strip()
	if line == "" or line.startswith('/'):
		return None
	if line.find("/")!=-1:
		line = line[0:line.find("//")]
	elif line.find(",")!=-1:
		line = line[0:line.find(",")]
	w_l = line.find("[")
	w_r = line.find("]")
	
	if w_l!=-1 and w_r!=-1:
		width = line[w_l+1:w_r]
		width = width.split(":")[0].strip()
		if '-'in width:
			width = width.split("-")[0].strip()
			has_sub = 1
		line = line[0:w_l]+line[w_r+1:]
		has_width = 1
	
	line = line.replace(',','')
	line = line.replace(';','')
	line = line.replace('wire','')
	line = line.replace('reg','')
	line = line.replace(':',' ')
	v = line.split()
	if has_width==0:
		return [v[0],1,v[1]]
	else:
		if width.isdigit():
			width = str(width+1-has_sub)
		else:
			if has_sub==0:
				width = "("+width+"+1)"
		return [v[0],width,v[-1]]

	return v
for line in str.split("\n"):
	v = clean_str(line)
	if v != None:
		io,width,name = v
		io = io[0].upper()+io[1:]
		print(("val %s "%name).ljust(32)+"= %s(UInt(%s.W))"%(io,width))