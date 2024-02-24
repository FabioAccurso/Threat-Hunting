import pandas as pd
import json
import re

#Lettura file Json
eventlog_df = pd.read_json('cmd_psexec_lsa_secrets_dump_2020-10-1903305471.json', lines=True)

#Visualizzare anteprima dataframe
eventlog_df.head()

#Visualizzare elenco dei nomi delle colonne
column_names = eventlog_df.columns
for column_name in column_names:
    print(column_name)

    #inizio della caccia
#Ricerca 1
eventlog_df = eventlog_df.fillna('null')
pattern = r'(psexec)'
for command in eventlog_df['CommandLine']:
    match = re.search(pattern, command, flags = re.IGNORECASE)
    if match:
        print(command)


#Ricerca 2
event_df = eventlog_df.loc[(eventlog_df['EventID'] == 7045) & (eventlog_df['ServiceName'] == 'PSEXESVC')]
for index, row in event_df.iterrows():
    print(f'Hostname = {row["Hostname"]}')
    print(f'TimeCreated = {row["TimeCreated"]}')
    print(f'EventID = {row["EventID"]}')
    print(f'Message = {row["Message"]}')
    print(f'ParentCommandLine = {row["ParentCommandLine"]}')
    print(f'CommandLine = {row["CommandLine"]}')

#Ricerca 3.a
counts = eventlog_df['EventID'].value_counts()
sort_counts = counts.sort_values()
for value, count în sort_counts.items():
	  print(f"EventID: {value} | Occurance: {count}")

#Ricerca 3.b
events_less_than_10 = counts[counts <10].index
stacked_df = eventlog_df[eventlog_df['EventID'].isin(events_less_than_10)]
for _, row in stacked_df.iterrows():
    print(f"EventID: {row['EventID']} - Message: {row['Message']}")

#Ricerca 3.c
writer = pd.ExcelWriter('timeline.xlsx', engine='openpyxl', mode='a')
stacked_df[['Hostname', 'TimeCreated', 'EventID', 'Message', 'ParentCommandLine', 'CommandLine']].to_excel(writer, index=False, header=False, sheet_name='Stacked_Events')
writer.save()







