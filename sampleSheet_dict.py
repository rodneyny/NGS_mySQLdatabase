#Function to get sample sheet data below - let me know if you have any problems 

def sample_sheet_dict(sample_sheet):

    """ returns dictionary of data from the sample sheet 

    Info['Data'] = list of the sample data in the sample sheet 
    E.g. 

    Info['Data'][0]['Sample_Name'] = the name of the first sample in the sample sheet
    Info['Data'][1]['Sample_Name'] = the name of the second sample in the sample sheet 
    etc... """

   
    Info = {}

    Tag = None

    with open(sample_sheet,'r') as inp_file:

        for record in inp_file:
            record = record.strip().split(",")
            if record[0].startswith("["):
                Tag       = record[0][1:-1]
                
                Info[Tag] = {}; continue

            # Header/Setting appear to be two-columns describing key/value ...
            if Tag in [ "Header", "Settings","Manifests" ]:
                if len(record)>1:
                    Info[Tag][record[0]] = record[1]

            # Reads appears to be one row/column describing the number of reads in the data ...
            if Tag == "Reads":
                Info[Tag] = record[0]

            if Tag == "Data":
                Info[Tag] = []
                
                # save the data header(s) i.e. column names
                Header    = record

                
                # perform a second iteration across the remaining records
                # note: once this is done, the file should have been processed
                n = 0
                for record in inp_file:
                    record = record.strip().split(",")
                    n += 1
                    # assign data to the corresponding header
                    tmp = {}
                    for p, q in zip(Header, record):
                        tmp[p] = q  
                    Info[Tag].append(tmp)

    return Info



