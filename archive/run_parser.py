import sys
import xml.etree.cElementTree as etree
import os
import glob 
from connection import connect 


      
def miseq(xmlfile,samples):

    def v3(xmlfile, samples):
        start = 1    
        for line in samples:
            if line[0] == '[Data]':
                start = samples.index(line)
    #     print start
         
        inv = samples[2][1]
        pn = samples[3][1]
        en = samples[4][1]
        wf = samples[6][1]
    #       
        data = samples[start + 2:]
         
    #     print data
       # xmlfile = "RunInfo.xml"
          
    #     print xmlfile
          
        run_inf = {}
        read = []
           
        tree = etree.parse(xmlfile)
        root = tree.getroot()
           
        for child in root:
            for k,v in child.attrib.items():
                run_inf[k] = v
            for element in child:
                if element.attrib != {}:
                    for k,v in element.attrib.items():
                        run_inf[k] = v
                run_inf[element.tag] = element.text
                for attrib in element:
                        read.append(attrib.attrib)
          
    #     print read                
        ri = []
          
        for row in read:
            indexed = row['NumCycles'] + '_' + row['IsIndexedRead']
            ri.append(indexed)
    #     print ri    
    #     print "This is len" + str(len(ri))
          
        r1 = ''
        r2 = ''
        i1 = ''
        i2 = ''
          
        if len(ri) == 4:
            r1 = ri[0]
            r2 = ri[3]
            i1 = ri[1]
            i2 = ri[2]
        elif len(ri) ==3:
            r1 = ri[0]
            r2 = ri[2]
            i1 = ri[1]
            i2 = None
              
    #     print r1
                       
        id = run_inf['Id']
        fc = run_inf['Flowcell']
        instr = run_inf['Instrument']
        date = run_inf['Date']
        sc = run_inf['SurfaceCount']
        swc = run_inf['SwathCount']
        tc = run_inf['TileCount']
           
        for line in data:
            line.insert(0, id)
            run_id = line[0]
            sample = line[1]
            sampleName = line[2]
            index = line[6]
            description = line[8]
            each = [run_id, sample, sampleName, index, description]
#             print each
          
            sql = """insert ignore into Sample_Run ( Run_ID, Sample,SampleName, samIndex, 
                    Description) values (%s,%s,%s,%s,%s)"""
            cursor.executemany(sql,[each])
             
        run = [id, fc, instr, date, inv, pn, en, wf, sc, swc,tc, r1, r2, i1, i2]
              
        sql = """ Insert ignore into Run (Run_ID, Flowcell, Instrument, Date, 
        Investigator, ProjectName, ExperimentName, Workflow, SurfaceCount, 
        SwathCount, TileCount, SE_SI, SE_DI, PE_SI, PE_DI) values 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
               
        cursor.executemany(sql,[run])
             
        db.commit()
              
        db.close()
        
    def v4(xmlfile, samples):
        start = 1    
        for line in samples:
            if line[0] == '[Data]':
                start = samples.index(line)
    #     print start
         
        inv = samples[2][1]
        pn = samples[3][1]
        en = samples[4][1]
        wf = samples[6][1]
    #       
        data = samples[start + 2:]
         
    #     print data
           
        #xmlfile = os.path.join(path,"RunInfo.xml")
        #xmlfile = "RunInfo.xml"
          
    #     print xmlfile
          
        run_inf = {}
        read = []
           
        tree = etree.parse(xmlfile)
        root = tree.getroot()
           
        for child in root:
            for k,v in child.attrib.items():
                run_inf[k] = v
            for element in child:
                if element.attrib != {}:
                    for k,v in element.attrib.items():
                        run_inf[k] = v
                run_inf[element.tag] = element.text
                for attrib in element:
                        read.append(attrib.attrib)
          
    #     print read                
        ri = []
          
        for row in read:
            indexed = row['NumCycles'] + '_' + row['IsIndexedRead']
            ri.append(indexed)
    #     print ri    
    #     print "This is len" + str(len(ri))
          
        r1 = ''
        r2 = ''
        i1 = ''
        i2 = ''
          
          
        if len(ri) == 4:
            r1 = ri[0]
            r2 = ri[3]
            i1 = ri[1]
            i2 = ri[2]
        elif len(ri) ==3:
            r1 = ri[0]
            r2 = ri[2]
            i1 = ri[1]
            i2 = None
              
    #     print r1
                       
        id = run_inf['Id']
        fc = run_inf['Flowcell']
        instr = run_inf['Instrument']
        date = run_inf['Date']
        sc = run_inf['SurfaceCount']
        swc = run_inf['SwathCount']
        tc = run_inf['TileCount']
           
        for line in data:
            line.insert(0, id)
            run_id = line[0]
            sample = line[1]
            sampleName = line[2]
            index = line[6]
            description = line[10]
            each = [run_id, sample, sampleName, index, description]
#             print each
          
              
            sql = """insert ignore into Sample_Run ( Run_ID, Sample,SampleName, samIndex, 
                    Description) values (%s,%s,%s,%s,%s)"""
            cursor.executemany(sql,[each])
             
        run = [id, fc, instr, date, inv, pn, en, wf, sc, swc,tc, r1, r2, i1, i2]
              
        sql = """ Insert ignore into Run (Run_ID, Flowcell, Instrument, Date, 
        Investigator, ProjectName, ExperimentName, Workflow, SurfaceCount, 
        SwathCount, TileCount, SE_SI, SE_DI, PE_SI, PE_DI) values 
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
               
        cursor.executemany(sql,[run])
             
        db.commit()
              
        db.close()
        
    if samples[1][1] == '3':
        print samples[1][0] + " 3"
        v3(xmlfile, samples)
    elif samples[1][1] == '4':
        print samples[1][0] + " 4"
        v4(xmlfile, samples)
        
def hiseq(xmlfile,samples):
    inv = samples[2][1]
    pn = None
    en = samples[3][1]
    wf = samples[5][1]
      
    data = samples[20:]
      
    #fileName = 'tsRunInfo.xml'
      
    run_inf = {}
      
    tree = etree.parse(fileName)
    root = tree.getroot()
      
    for child in root:
        for k,v in child.attrib.items():
            run_inf[k] = v
        for element in child:
            if element.attrib != {}:
                for k,v in element.attrib.items():
                    run_inf[k] = v
            run_inf[element.tag] = element.text
            for attrib in element:
                for k,v in attrib.attrib.items():
                    run_inf[k] = v
                  
    id = run_inf['Id']
    fc = run_inf['Flowcell']
    instr = run_inf['Instrument']
    date = run_inf['Date']
    sc = run_inf['SurfaceCount']
    swc = run_inf['SwathCount']
    tc = run_inf['TileCount']
    run = [id, fc, instr, date, inv, pn, en, wf, sc, swc,tc]
       
    sql = """ Insert ignore into Run (Run_ID, Flowcell, Instrument, Date, 
    Investigator, ProjectName, ExperimentName, Workflow, SurfaceCount, 
    SwathCount, TileCount) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
    cursor.executemany(sql,[run])   
      
    for line in data:
        line.insert(0, id)
        run_id = line[0]
        sample = line[2]
        sampleName = line[3]
        index = line[7]
        description = line[9]
        lane = line[1]
        each = [run_id, sample, sampleName, index, description, lane]
      
          
        sql = """insert ignore into Sample_Run ( Run_ID, Sample,SampleName, samIndex, 
                Description, Lane) values (%s,%s,%s,%s,%s,%s)"""
        cursor.executemany(sql,[each])

    db.commit()
       
    db.close()

if __name__ == "__main__":
	
	import os
	import sys
	import glob

	data = '/media/cf1e95f0-6a68-464e-994b-7565688b6462/home/angie/MiSeq_data_backup/*'


	run_folders = glob.glob(data)

	for run_folder in run_folders:
		fname = os.path.join(run_folder, 'SampleSheet.csv')
		xmlfile = os.path.join(run_folder, 'RunInfo.xml')

		if os.path.exists(fname) and os.path.exists(xmlfile):
			#print rodneys_fucntion(ss)
			
			database = connect()
			cursor = database[0]
			db = database[1]

			#path = os.path.abspath(sys.argv[1])
			#xmlfile = os.path.join(path,"RunInfo.xml")
			#fname = os.path.join(path,"SampleSheet.csv")
			# fname = "SampleSheet.csv"
			# fname = "hiseq.csv"
			
			print fname

			samples = []

			with open(fname,'r') as inp_file:
				for line in inp_file.readlines():
					line = line.strip().split(',')
					samples.append(line)    
				indx = 1
				
				for line in samples:
					if line[0] == 'Lane':
						indx = samples.index(line)
						
				if samples[indx][0] == 'Lane':
					print "This is a Hiseq Samplesheet"
					hiseq(xmlfile,samples)
				else:
					print "This is a Miseq Samplesheet"
					miseq(xmlfile,samples)
