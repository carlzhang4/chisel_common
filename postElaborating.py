import sys
import os
import subprocess
import getopt
import json


class Moniter():
	def __init__(self,name):
		self.name = name
		self.signals = []
		self.widths = []
		if name.startswith("ila"):
			self.type = "ila"
		elif name.startswith("vio"):
			self.type = "vio"
		else:
			print("Error ipType")
			sys.exit(0)

		
configFileName = "config.json"
configFile = open(configFileName)
config = json.load(configFile)
configFile.close()

moniterDepth = 1024
moniterDelay=0

projectName = str(sys.argv[1])
moduleName = str(sys.argv[2])
showTCL = False
postRun = False

argv = sys.argv[3:]

opts, args = getopt.getopt(argv, "tp")  # 短选项模式
for opt, arg in opts:
	if opt in ['-t']:
		showTCL = True
	elif opt in ['-p']:
		postRun = True

moniters = []

destIPRepoPath = ""
destSrcPath = ""

if projectName == "qdma":
	destIPRepoPath = config["qdma"]["destIPRepoPath"]
	destSrcPath = config["qdma"]["destSrcPath"]
elif projectName == "smart_db":
	destIPRepoPath = "/home/amax/cj/smart_db_proj/smart_db_proj.srcs/sources_1/ip"
	destSrcPath = "/home/amax/cj/smart_db_proj/smart_db_proj.srcs/sources_1/new"
else:
	print("No project match")
	sys.exit(0)

def get_width(str):
	l = str.split(' ')
	widthStr = list(filter(None,l))[1]
	if widthStr.startswith("["):
		w = widthStr.split(':')[0].replace('[','')
		return int(w)+1
	else:
		return 1

def append_wrapper_to_sv(wrapper):
	fileName = "Verilog/" + moduleName + ".sv"
	f = open(fileName,'a')
	f.write(wrapper)
	f.close()

def replace_print():
	fileName = "Verilog/" + moduleName + ".sv"
	f = open(fileName,'r')
	lines = f.readlines()
	f.close()

	fileName = destSrcPath+"/%s.sv"%moduleName
	print(fileName)
	f = open(fileName,'w+')
	for line in lines:
		l = line.replace("h80000002", "h80000003") #h80000001
		f.write(l)
	f.close()
	print("Done moving file")

def initial_moniters_from_txt():
	fileName = "Verilog/" + moduleName + ".txt"
	f = None
	try:
		f = open(fileName,'r')
	except IOError:
		return
	lines = f.readlines()
	signals = [] 
	for l in lines:
		line = l.replace("\n","")
		
		if line.endswith(":"):
			moniterName = line[:-1]
			m = Moniter(moniterName)
			m.signals = signals[:]
			moniters.append(m)
			for signal in signals:
				if signal.count(signal) != 1:
					print("signal name conflict!")
					sys.exit(0)
			signals = []
		else:
			signals.append(line)
	f.close()

def parse_verilog():
	fileName = "Verilog/" + moduleName + ".sv"
	f = open(fileName,'r')
	lines = f.readlines()
	for line in lines:
		for moniter in moniters:
			if line.find(moniter.name+" ") != -1: #  ila_control_reg mod1 ( // @[QDMATop.scala 74:26]
				l = line.split(' ')
				instName = list(filter(None,l))[1]
				moniter.instName = instName
	instNames = [moniter.instName for moniter in moniters]
	for instName in instNames:
		if instNames.count(instName) != 1:
			print("instant name conflict!")
			sys.exit(0)
	f.close()

def parse_width():
	fileName = "Verilog/" + moduleName + ".sv"
	f = open(fileName,'r')
	lines = f.readlines()
	for line in lines:
		for moniter in moniters:
			instName = moniter.instName
			signals = moniter.signals
			for i in range(len(signals)):
				wireName = instName+"_data_%d;"%i # must have semicolon, or data_1 would be duplicated by data_11
				if line.find(wireName)!=-1 and line.find("wire")!=-1:
					width = get_width(line)
					moniter.widths.insert(0,width)
	for miniter in moniters:
		if(len(moniter.signals) != len(moniter.widths)):
			print(moniter.signals)
			print(moniter.widths)
		assert(len(moniter.signals) == len(moniter.widths)) # maybe a port is zero and has been optimized!

def generate_wrapper(moniter):
	widths = moniter.widths
	signals = moniter.signals
	ip_name = moniter.name
	names = ["data_%d"%i for i in range(len(widths))]
	io = "input" if moniter.type=="ila"  else "output"

	wrapper = "module %s(\n"%(ip_name)
	wrapper += "input clk,\n"

	for i in range(len(names)):
		name = names[i]
		width = widths[i]
		if i != len(names)-1:
			wrapper += "%s [%d:0] %s,\n"%(io,width-1,name)
		else:
			wrapper += "%s [%d:0] %s);\n"%(io,width-1,name)
	
	converts = ""
	if moniter.type=="ila":
		for i in range(len(signals)):
			converts += "wire [%d:0] %s = %s;\n"%(widths[i]-1, signals[i], names[i])
	else:
		for i in range(len(signals)):
			converts += "(* keep = \"true\" *)wire [%d:0] %s;\n"%(widths[i]-1, signals[i])
			converts += "assign %s = %s;\n"%(names[i], signals[i])
	instance = "%s_inner inst_%s(\n.clk(clk),\n"%(ip_name,ip_name)

	for i in range(len(names)):
		name = signals[i]
		width = widths[i]
		if moniter.type=="ila":
			if i != len(names)-1:
				instance += ".probe%d(%s), //[%s:0]\n"%(i,name,width)
			else:
				instance += ".probe%d(%s)); //[%s:0]\n"%(i,name,width)
		else:
			if i != len(names)-1:
				instance += ".probe_out%d(%s), //[%s:0]\n"%(i,name,width)
			else:
				instance += ".probe_out%d(%s)); //[%s:0]\n"%(i,name,width)
	return wrapper + "\n" + converts + "\n" + instance + "endmodule\n"

def generate_tcl(moniter):
	widths = moniter.widths
	signales = moniter.signals
	tcl = ""
	if moniter.type == "ila":
		ip_name = moniter.name+"_inner"
		tcl1 = "create_ip -name ila -vendor xilinx.com -library ip -version 6.2 -module_name "+ip_name
		tcl2 = "set_property -dict [list "
		tcl2 += "CONFIG.C_INPUT_PIPE_STAGES {%d} "%(moniterDelay)
		for i in range(len(widths)):
			tcl2 += "CONFIG.C_PROBE%d_WIDTH {%d} "%(i,widths[i])
		tcl2+="CONFIG.C_DATA_DEPTH {%d} CONFIG.C_NUM_OF_PROBES {%d} ] [get_ips %s]"%(moniterDepth,len(widths),ip_name)
		tcl3 = "generate_target {instantiation_template} [get_files %s/%s/%s.xci]"%(destIPRepoPath,ip_name,ip_name)
		tcl4 = "update_compile_order -fileset sources_1\n\n"
		tcl = tcl1+"\n"+tcl2+"\n"+tcl3+"\n"+tcl4
	else:
		ip_name = moniter.name+"_inner"
		tcl1 = "create_ip -name vio -vendor xilinx.com -library ip -version 3.0 -module_name "+ip_name
		tcl2 = "set_property -dict [list "
		tcl2 += "CONFIG.C_PROBE_OUT0_INIT_VAL {0x0} "
		for i in range(len(widths)):
			tcl2 += "CONFIG.C_PROBE_OUT%d_WIDTH {%d} "%(i,widths[i])
		tcl2+="CONFIG.C_NUM_PROBE_OUT {%d} CONFIG.C_EN_PROBE_IN_ACTIVITY {0} CONFIG.C_NUM_PROBE_IN {0}] [get_ips %s]"%(len(widths),ip_name)
		tcl3 = "generate_target {instantiation_template} [get_files %s/%s/%s.xci]"%(destIPRepoPath,ip_name,ip_name)
		tcl4 = "update_compile_order -fileset sources_1\n\n"
		tcl = tcl1+"\n"+tcl2+"\n"+tcl3+"\n"+tcl4
	return tcl
def post_run():
	initial_moniters_from_txt()
	parse_verilog()
	parse_width()

	wrapperStr = ""
	for moniter in moniters:
		wrapperStr+= generate_wrapper(moniter)
	append_wrapper_to_sv(wrapperStr)

	for moniter in moniters:
		tcl = generate_tcl(moniter)
		if showTCL:
			print(tcl)
	
	replace_print()


try:
	os.remove("Verilog/"+moduleName+".txt")
	print("txt file deleted")
except:
	print("No txt file to be deleted")

print("Running mill " + projectName+" " + moduleName)
p = subprocess.Popen(["mill", projectName, moduleName])
p.wait()
ret = p.returncode

if ret != 0:
	print("Mill compiling error!")
else:
	if postRun == True:
		post_run()
