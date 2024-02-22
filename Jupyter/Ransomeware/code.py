import os
import pandas as pd 
from subprocess import check_output
mft_path = "\"C:\\kape\\collected\\2021-06-01T151604\\C\\$MFT\""
mftexplorer_path = "\"C:\\MFTExplorer\\MFTECmd.exe\""
output_folder = "C:\\Documents\\test"
output_filename = "MyOutputFile.csv"
command = "{0} -f {1} --csv \"{2}\" --csvf \"{3}\"".format(mftexplorer_path, mft_path, output_folder, output_filename)
print(command)
output = os.popen(command).read()

pd.set_option('display.max_columns', 500)
data = pd.read_csv(output_folder + "\\" + output_filename)

data.set_index("EntryNumber", inplace=True)
data['Created0x10'] =  pd.to_datetime(data['Created0x10'], format='%Y-%m-%d %H:%M:%S.%f')
data['Created0x30'] =  pd.to_datetime(data['Created0x30'], format='%Y-%m-%d %H:%M:%S.%f')
data['LastModified0x10'] =  pd.to_datetime(data['LastModified0x10'], format='%Y-%m-%d %H:%M:%S.%f')
data['LastModified0x30'] =  pd.to_datetime(data['LastModified0x30'], format='%Y-%m-%d %H:%M:%S.%f')
data['LastRecordChange0x10'] =  pd.to_datetime(data['LastRecordChange0x10'], format='%Y-%m-%d %H:%M:%S.%f')
data['LastRecordChange0x30'] =  pd.to_datetime(data['LastRecordChange0x30'], format='%Y-%m-%d %H:%M:%S.%f')

#Analisi 1
dates = data["LastRecordChange0x10"]
dates.index = dates.dt.to_period('d')
s = dates.groupby(level=0).size()
s.sort_values(ascending=False).head(10)

#Analisi 2
data_filtered = data[(data['LastModified0x10'] > "2021-01-01") & (data['LastModified0x10'] < "2021-05-30")]
names = data_filtered["FileName"].value_counts()
names.nlargest()
names_plot = names.to_frame().head(5).sort_values(by="FileName", ascending=False)
fig = px.bar(names_plot, x="FileName", "title=Files with more entries")
fig.show()

#Visualizzazione piu nel dettaglio di Analisi 2
#readme = data[data["FileName"].str.contains("_readme_.txt")]
#redme.sort_values(by="LastModified0x10", ascending=True).head()

#Analisi 3
first_note = readme1.sort_values(by="LastModified0x10", ascending=True).iloc[0]["LastModified0x10"]
range_exe = first_note + pd.offsets.Hour(-12)
data_filtered = data[(data['Created0x10'] > "2021-05-22") & (data['Created0x10'] < "2021-05-25")]
files = data_filtered[data_filtered["FileName"].str.contains("\.exe|\.ps1|\.msi|\.vba", regex=True)]
