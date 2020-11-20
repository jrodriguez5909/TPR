#                                                                                                    
#                 ``                                                                        ```.`    
#               `+/                                                                 ``.-/+o+:-.      
#             `/mo                                                          ``.-:+syhdhs/-`          
#            -hMd                                                    `..:+oyhmNNmds/-`               
#          `oNMM/                                            ``.-/oyhdmMMMMNdy+:.                    
#         .hMMMM-                                     `.-/+shdmNMMMMMMNdy+:.                         
#        :mMMMMM+                             `.-:+sydmNMMMMMMMMMNmho:.`                             
#       :NMMMMMMN:                    `.-:/oyhmmNMMMMMMMMMMMNmho:.`                                  
#      .NMMMMMMMMNy:`          `.-/oshdmNMMMMMMMMMMMMMMMmhs/-`                                       
#      hMMMMMMMMMMMMmhysooosyhdmNMMMMMMMMMMMMMMMMMMmds/-`                                            
#     .MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNdy+-.`                                                
#     -MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNdy+-.`                                                     
#     `NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMmyo:.`                                                          
#      /NMMMMMMMMMMMMMMMMMMMMMMMmho:.`                                                               
#       .yNMMMMMMMMMMMMMMMMmhs/.`                                                                    
#         ./shdmNNmmdhyo/-``                                                                         
#              `````                 
#                                     
###   Created By: Jutiliano Rodriguez   
###   Last Modified By: Jutiliano Rodriguez 
#####################################################################################################


#####################################################
###                                               ###
###   Import packages and set working directory   ###
###                                               ###
#####################################################

import re
import time # Tracks time a script takes to run
import pandas as pd # For numerical analysis in tabular forms

StartTime = time.time()

######################
###                ###
###   Parameters   ###
###                ###
######################

# COPA_MTD = pd.read_csv('TPR_COPA_2020.11.16.csv') # MTD COPA file
Month = ['202011'] # Set the calendar month you're performing the TPR calculation for
Period = ['06'] # Set the FY period you're performing the TPR calculation for

##############################
###                        ###
###   Pull data together   ###
###                        ###
##############################

dataJul1 = pd.read_csv('TPR Materials_GPC_2020.07.06_01.csv')
dataJul2 = pd.read_csv('TPR Materials_GPC_2020.07.06_02.csv')

dataOct1 = pd.read_csv('TPR Materials_GPC_2020.10.14_01.csv')
dataOct2 = pd.read_csv('TPR Materials_GPC_2020.10.14_02.csv')

dataJul1.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', '202006', '01', '202007', '02', '202008', '03', '202009', '04', '202010', '05', 
                 '202011', '06', '202012', '07', '202101', '08', '202102', '09', '202103', '10', '202104', '11', '202105', '12']
dataJul2.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', '202006', '01', '202007', '02', '202008', '03', '202009', '04', '202010', '05', 
                 '202011', '06', '202012', '07', '202101', '08', '202102', '09', '202103', '10', '202104', '11', '202105', '12']

dataOct1.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', '202006', '01', '202007', '02', '202008', '03', '202009', '04', '202010', '05', 
                 '202011', '06', '202012', '07', '202101', '08', '202102', '09', '202103', '10', '202104', '11', '202105', '12']
dataOct2.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', '202006', '01', '202007', '02', '202008', '03', '202009', '04', '202010', '05', 
                 '202011', '06', '202012', '07', '202101', '08', '202102', '09', '202103', '10', '202104', '11', '202105', '12']

combinedJul = [dataJul1, dataJul2]
combinedOct = [dataOct1, dataOct2]

TPRDataJul = pd.concat(combinedJul) # Concatenates data frames into one
TPRDataOct = pd.concat(combinedOct) # Concatenates data frames into one

Columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', Month[0], Period[0]]
TPRDataJul = TPRDataJul[Columns]
TPRDataOct = TPRDataOct[Columns]
TPRDataJul['Material'] = TPRDataJul['STYLENUMBER'].astype(str) + "-" + TPRDataJul['CLRCD'].astype(str).str.zfill(3)
TPRDataOct['Material'] = TPRDataOct['STYLENUMBER'].astype(str) + "-" + TPRDataOct['CLRCD'].astype(str).str.zfill(3)
TPRDataJul.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', 'TPR', 'TYPE', 'Material']
TPRDataOct.columns = ['GPCD', 'STYLENUMBER', 'CLRCD', 'STYLEDESCRIPTION', 'TPR', 'TYPE', 'Material']

TPR_Merged_Jul = pd.merge(TPRDataJul, COPA_MTD[['Material', 'NetSales', 'Units', 'Category', 'PE']], on='Material', how="left")
TPR_Merged_Oct = pd.merge(TPRDataOct, COPA_MTD[['Material', 'NetSales', 'Units', 'Category', 'PE']], on='Material', how="left")
TPR_Merged_Jul = TPR_Merged_Jul[TPR_Merged_Jul.TYPE != 'B'] # Removes rows with labeled as having both per unit and % of sales TPR since already captured individually in duplicate rows labeled "S" or "U"
TPR_Merged_Oct = TPR_Merged_Oct[TPR_Merged_Oct.TYPE != 'B'] # Removes rows with labeled as having both per unit and % of sales TPR since already captured individually in duplicate rows labeled "S" or "U"

Category = {'ACTION OUTDOOR':'',
            'ACTION SPORTS':'NIKE SB',
            'OUTDOOR':'OTHER FIELD SPORTS',
            'BASKETBALL':'',
            'JORDAN BRAND':'JORDAN BRAND',
            'NIKE BASKETBALL':'NIKE BASKETBALL',
            'FOOTBALL, BASEBALL, AT':'',
            'AMERICAN FOOTBALL':'AMERICAN FOOTBALL',
            'BASEBALL OTH FIELD SPORTS':'OTHER FIELD SPORTS',
            'MEN TRAINING':"MEN'S TRAINING'",
            'WOMEN TRAINING':"WOMEN'S TRAINING",
            'FOOTBALL/SOCCER':'GLOBAL FOOTBALL',
            'NIKE GOLF':'GOLF',
            'HURLEY':'HURLEY',
            'NIKE SPORTSWEAR':'',
            'NSW BASKETBALL':"MEN'S NSW",
            'NSW FOOTBALL/SOCCER':"MEN'S NSW",
            'NSW OTHER SPORTS':"MEN'S NSW",
            'NSW RUNNING':"MEN'S NSW",
            'Not assigned':'Not assigned',
            'OTHER':'',
            'ALL OTHER':'OTHER',
            'TENNIS':'TENNIS',
            'RUNNING':"MEN'S RUNNING",
            'WOMEN TRAINING':"WOMEN'S TRAINING",
            'YOUNG ATHLETES':'YOUNG ATHLETES'}

PE = {'20':'FW',
      '10':'AP',
      '30':'EQ'}

#############################
###                       ###
###   Calculate MTD TPR   ###
###                       ###
#############################

def TPR_calc(row): # This function calculates TPR as % of net sales or per unit based on the "S" or "U" flag in the "TYPE" vector 
    if row['TYPE'] == 'S':
        royalty = (row['NetSales'] * row['TPR'])/100 # Divides the TPR column by 100 to make it % since "S" denotes materials for which royalties are paid as % of net sales
    else:
        royalty = row['Units'] * row['TPR'] # Calculates per unit TPRs for rows labeled "U"
    return royalty

TPR_Merged_Jul['TPR_Paid'] = TPR_Merged_Jul.apply(TPR_calc, axis = 1) # Applies the above function to all rows in the dataframe
TPR_Merged_Oct['TPR_Paid'] = TPR_Merged_Oct.apply(TPR_calc, axis = 1) # Applies the above function to all rows in the dataframe

TPR_Merged_Jul['dup'] = TPR_Merged_Jul.groupby(['Material']).cumcount() + 1 # Creates duplicate flag just in case it's needed for further analysis
TPR_Merged_Oct['dup'] = TPR_Merged_Oct.groupby(['Material']).cumcount() + 1 # Creates duplicate flag just in case it's needed for further analysis
TPR_Merged_Jul = TPR_Merged_Jul[TPR_Merged_Jul['TPR_Paid'].notna()] # Removes materials not sold during the month and hence no TPR is incurred for
TPR_Merged_Oct = TPR_Merged_Oct[TPR_Merged_Oct['TPR_Paid'].notna()] # Removes materials not sold during the month and hence no TPR is incurred for

TPR_Jul = TPR_Merged_Jul["TPR_Paid"].sum() # Sum all TPR in one float variable
TPR_Oct = TPR_Merged_Oct["TPR_Paid"].sum() # Sum all TPR in one float variable

ExecutionTime = (time.time() - StartTime)

print('MTD TPR based on the prior listing is ' + str('${:,.0f}'.format(TPR_Jul)) + '. ' +
      'MTD TPR based on the new listing is ' + str('${:,.0f}'.format(TPR_Oct)) + '. ' +      
      'This script took ' + format(str(round(ExecutionTime, 1))) + ' seconds to run.')
