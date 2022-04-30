
str="""
val s_axi_araddr		= Input(UInt(ADDR_WIDTH.W))
val s_axi_arburst		= Input(UInt(2.W))
val s_axi_arcache		= Input(UInt(4.W))
val s_axi_arid			= Input(UInt(ID_WIDTH.W))
val s_axi_arlen			= Input(UInt(8.W))
val s_axi_arlock		= Input(UInt(1.W))
val s_axi_arprot		= Input(UInt(3.W))
val s_axi_arqos			= Input(UInt(4.W))
val s_axi_arregion		= Input(UInt(4.W))
val s_axi_arsize		= Input(UInt(3.W))
val s_axi_aruser		= Input(UInt(USER_WIDTH.W))
val s_axi_arvalid		= Input(UInt(1.W))
val s_axi_arready		= Output(UInt(1.W))

val s_axi_awaddr		= Input(UInt(ADDR_WIDTH.W))
val s_axi_awburst		= Input(UInt(2.W))
val s_axi_awcache		= Input(UInt(4.W))
val s_axi_awid			= Input(UInt(ID_WIDTH.W))
val s_axi_awlen			= Input(UInt(8.W))
val s_axi_awlock		= Input(UInt(1.W))
val s_axi_awprot		= Input(UInt(3.W))
val s_axi_awqos			= Input(UInt(4.W))
val s_axi_awregion		= Input(UInt(4.W))
val s_axi_awsize		= Input(UInt(3.W))
val s_axi_awuser		= Input(UInt(USER_WIDTH.W)))	
val s_axi_awvalid		= Input(UInt(1.W))
val s_axi_awready		= Output(UInt(1.W))

val s_axi_rdata			= Output(UInt(DATA_WIDTH.W))
val s_axi_rid			= Output(UInt(ID_WIDTH.W))
val s_axi_rlast			= Output(UInt(1.W))
val s_axi_rresp			= Output(UInt(2.W))
val s_axi_ruser			= Output(UInt(USER_WIDTH.W))
val s_axi_rvalid		= Output(UInt(1.W))
val s_axi_rready		= Input(UInt(1.W))

val s_axi_wdata			= Input(UInt(DATA_WIDTH.W))
val s_axi_wlast			= Input(UInt(1.W))
val s_axi_wstrb			= Input(UInt((DATA_WIDTH/8).W))
val s_axi_wuser			= Input(UInt(USER_WIDTH.W))
val s_axi_wvalid		= Input(UInt(1.W))
val s_axi_wready		= Output(UInt(1.W))

val s_axi_bid			= Output(UInt(ID_WIDTH.W))
val s_axi_bresp			= Output(UInt(3.W))
val s_axi_buser			= Output(UInt(USER_WIDTH.W))
val s_axi_bvalid		= Output(UInt(1.W))
val s_axi_bready		= Input(UInt(1.W))

val m_axi_araddr		= Output(UInt(ADDR_WIDTH.W))
val m_axi_arburst		= Output(UInt(2.W))
val m_axi_arcache		= Output(UInt(4.W))
val m_axi_arid			= Output(UInt(ID_WIDTH.W))
val m_axi_arlen			= Output(UInt(8.W))
val m_axi_arlock		= Output(UInt(1.W))
val m_axi_arprot		= Output(UInt(3.W))
val m_axi_arqos			= Output(UInt(4.W))
val m_axi_arregion		= Output(UInt(4.W))
val m_axi_arsize		= Output(UInt(3.W))
val m_axi_aruser		= Output(UInt(USER_WIDTH.W))
val m_axi_arvalid		= Output(UInt(1.W))
val m_axi_arready		= Input(UInt(1.W))

val m_axi_awaddr		= Output(UInt(ADDR_WIDTH.W))
val m_axi_awburst		= Output(UInt(2.W))
val m_axi_awcache		= Output(UInt(4.W))
val m_axi_awid			= Output(UInt(ID_WIDTH.W))
val m_axi_awlen			= Output(UInt(8.W))
val m_axi_awlock		= Output(UInt(1.W))
val m_axi_awprot		= Output(UInt(3.W))
val m_axi_awqos			= Output(UInt(4.W))
val m_axi_awregion		= Output(UInt(4.W))
val m_axi_awsize		= Output(UInt(3.W))
val m_axi_awuser		= Output(UInt(USER_WIDTH.W)))	
val m_axi_awvalid		= Output(UInt(1.W))
val m_axi_awready		= Input(UInt(1.W))

val m_axi_rdata			= Input(UInt(DATA_WIDTH.W))
val m_axi_rid			= Input(UInt(ID_WIDTH.W))
val m_axi_rlast			= Input(UInt(1.W))
val m_axi_rresp			= Input(UInt(2.W))
val m_axi_ruser			= Input(UInt(USER_WIDTH.W))
val m_axi_rvalid		= Input(UInt(1.W))
val m_axi_rready		= Output(UInt(1.W))

val m_axi_wdata			= Output(UInt(DATA_WIDTH.W))
val m_axi_wlast			= Output(UInt(1.W))
val m_axi_wstrb			= Output(UInt((DATA_WIDTH/8).W))
val m_axi_wuser			= Output(UInt(USER_WIDTH.W))
val m_axi_wvalid		= Output(UInt(1.W))
val m_axi_wready		= Input(UInt(1.W))

val m_axi_bid			= Input(UInt(ID_WIDTH.W))
val m_axi_bresp			= Input(UInt(3.W))
val m_axi_buser			= Input(UInt(USER_WIDTH.W))
val m_axi_bvalid		= Input(UInt(1.W))
val m_axi_bready		= Output(UInt(1.W))
"""

def clean_str(line):
	s = line
	s = s.replace('=',' ')
	s = s.replace('(',' ')
	s = s.replace(')',' ')
	s = s.replace('.W',' ')
	s = s.replace(',',' ')
	s = s.replace('UInt',' ')
	return s.split()[1:] #eliminate val, hard to directly replace

for line in str.split("\n"):
	if line != "":
		s = clean_str(line)
		if(len(s)==5):#vec
			name	= s[0]
			io		= s[1]
			times	= s[3]
			width 	= s[4]
			if(width.isdigit()):
				width=int(width)-1
			else:
				width=width+"-1"
			for i in range(int(times)):
				if(io=="Input"):
					print("input wire \t", end="")
				elif(io=="Output"):
					print("output wire \t", end="")
				else:
					print("####Error")
				
				print(("[%s:0]"%(width)).ljust(30), end="")
				print(" "+name+"_%d,"%i)
		elif(len(s)==3):
			name	= s[0]
			io		= s[1]
			width 	= s[2]
			if(width.isdigit()):
				width=int(width)-1
			else:
				width=width+"-1"
			if(io=="Input"):
				print("input wire \t", end="")
			elif(io=="Output"):
				print("output wire \t", end="")
			else:
				print("####Error")
			print(("[%s:0]"%(width)).ljust(30), end="")
			print(" "+name+",")
			
