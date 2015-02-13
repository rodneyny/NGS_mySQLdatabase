import sys
import xml.etree.cElementTree as etree
import os
import glob 
from connection import connect 
from illuminate import *
from chris_samples import sample_sheet_dict

      
def data_parser(xmlfile,fname,path):
    # Creates dictionaries from the sample sheet
    samples = sample_sheet_dict(fname)
    h = samples['Header']
    d = samples['Data']

    inv = h['Investigator Name']
# Check which SampleSheet is being used Miseq or Hiseq
# (This might not matter after all as long as the only difference
# is the ProjectName field)
    
    # keys = []
    # for k in d[0]:
    #     keys.append(k)
    # if 'Lane' in keys:
    #     # print "Hiseq"
    # else:
    #     # print "Miseq"

    # Check is the project name is in the SampleSheet file 
    # Hiseq and some Miseq sample sheets do not have Project name
    try:
        pn =  h['Project Name']
    except:
        pn = None

    en = h['Experiment Name']
    wf = h['Workflow']
    
    # Dictionary to contain dictionaries from the 
    # RunInfo.xml file 
    # Consider using xmltodict??? 
    run_inf = {}

    # List of reads found in the RunInfoRead tag 
    read = []
    
    # Parser for the RunInfo.xml file    
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
    ri = []
      
    for row in read:
        indexed = row['NumCycles'] + '_' + row['IsIndexedRead']
        ri.append(indexed)

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

    my_data = InteropDataset(path)
    tilemetrics = my_data.TileMetrics()
    tiledict = tilemetrics.to_dict() 
    clusterdens = str(tiledict['cluster_density'])
    clusterpf = str(tiledict['cluster_density_pf'])
    qualitymetrics = my_data.QualityMetrics()

    metainfo = my_data.meta
    readconfig = metainfo.read_config
    # Number of reads 
    clusters = tilemetrics.num_clusters
    # Length of reads in bp 
    reads = readconfig[0]['cycles']

    clust_run_yield = ((float(reads) * 2) * float(clusters))/10**9

    # print "Clusters yield = ", clust_run_yield

    try:
        indexmetrics = my_data.IndexMetrics()
        indxreads = indexmetrics.total_ix_reads_pf
        indx_run_yield = ((float(reads) * 2) * float(indxreads))/10**9
    except:
        indx_run_yield = None

    # print "Index reads = ", indx_run_yield

    # Some run folders only have one read and no indexes. Take this into account 
    qualdict= qualitymetrics.to_dict()
    try:
        R1qual = str(qualdict[1])
    except:
        R1qual = None
    try:
        I1qual = str(qualdict[2])
    except:
        I1qual = None
    try:
        I2qual = str(qualdict[3])
    except:
        I2qual = None
    try:
        R2qual = str(qualdict[4])
    except:
        R2qual = None


# try:
                   
    run_id = run_inf['Id']
    fc = run_inf['Flowcell']
    instr = run_inf['Instrument']
    date = run_inf['Date']
    sc = run_inf['SurfaceCount']
    swc = run_inf['SwathCount']
    tc = run_inf['TileCount']
    run = [run_id, fc, instr, date, inv, pn, en, wf, sc, swc, tc, r1, R1qual,\
          r2, R2qual, i1, I1qual, i2, I2qual, clusterdens, clust_run_yield,\
          indx_run_yield, clusterpf]
          
    sql = """ Insert ignore into Run (Run_ID, Flowcell, Instrument, Date, 
    Investigator, ProjectName, ExperimentName, Workflow, SurfaceCount, 
    SwathCount, TileCount, Read1, R1qual, Read2, R2qual, Index1, I1qual, Index2,  
    I2qual, ClusterDensity, ClusterYield, IndexPFyield, ClusterPF) values 
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    cursor.executemany(sql,[run])

    db.commit()

    print "Run added"
# except:
    # print "Nothing added to database"

    try:
        for i in d:   
            samid = i['Sample_ID']
            samname = i['Sample_Name']
            samindx = i['index']
            try:
                samindx2 = i['index2']
            except:
                samindx2 = None
            desc = i['Description']
            try:
                samlane = i['Lane']
            except:
                samlane = 1

            each = [run_id, samid, samname, samindx, samindx2, desc, samlane]
          
            sql = """insert ignore into Sample_Run ( Run_ID, Sample,SampleName, Index1, 
                Index2, Description, Lane) values (%s,%s,%s,%s,%s,%s,%s)"""

            cursor.executemany(sql,[each])

            db.commit()
        print "Sample_Run added"
            
    except:
        print "Nothing added to database"

    


if __name__ == "__main__":

    data = '/media/cf1e95f0-6a68-464e-994b-7565688b6462/home/angie/MiSeq_data_backup/*'

    # data = '/home/rodney/testNGSfolders/*'

    run_folders = glob.glob(data)

    database = connect()
    cursor = database[0]
    db = database[1]

    sql = " Select Run_Id from Run"
    # dirls (Directory list) is the list of folders which are not to be parsed by the script.
    # Any folder names in the database are appended to this list. 
    dirls = ['logs', 'Blank_Folders', '140106_M00755_0131_000000000-A60HG', '140813_M00755_0227_000000000-AAU6J']
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        row = row[0]
        item = str(row)
        dirls.append(item)


    for run_folder in run_folders:
        folderID = os.path.basename(run_folder)

        # Check if run folder information has already been added to the database
        if folderID not in dirls:
            fname = os.path.join(run_folder, 'SampleSheet.csv')
            xmlfile = os.path.join(run_folder, 'RunInfo.xml')
            try:
                data_parser(xmlfile,fname,os.path.abspath(run_folder))
            except:
                print "Error:Folder not added to database", '\n', run_folder
                pass
          
    db.close()
                
