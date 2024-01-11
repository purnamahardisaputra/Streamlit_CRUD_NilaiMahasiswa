# Installasi Depedency
# pip install streamlit
# pip install pandas
# pip install openpyxl
# pip install plotly-express

# Import Library
import streamlit as stream
import pandas as pd
import plotly.express as px
from PIL import Image

# Title Aplikasi
stream.title("Sistem Informasi Nilai Pengolahan Citra Kelas IF-3")

# Dataframe 
df = pd.read_excel("data/dataset.xlsx")
dfTampilData = pd.read_excel("data/dataset.xlsx", usecols='A:F')
dfAngkatan = pd.read_excel("data/dataset.xlsx", usecols='D:F')
dfNilai = pd.read_excel("data/dataset.xlsx", usecols='D:H')
dfJumlahMhs = df.groupby('Prodi').size().reset_index(name='Jumlah Mahasiswa')
df['HasilAkhir'] = df.apply(lambda row: (row['UTS'] + row['UAS']) / 2, axis=1)

def klasifikasikan_nilai(rata_rata):
    if rata_rata >= 95:
        return 'A'
    elif rata_rata >= 90:
        return 'AB'
    elif rata_rata >= 85:
        return 'B'
    elif rata_rata >= 80:
        return 'C'
    elif rata_rata >= 70:
        return 'D'
    else:
        return 'E'
df['KlasifikasiNilai'] = df['HasilAkhir'].apply(klasifikasikan_nilai)

# Stream Tampil Data
stream.write(dfTampilData)

# Stream Sidebar Tambah Data
stream.sidebar.header("Tambah Data Nilai")
formTmbhMhs = stream.sidebar.form("Tambah _Mahasiswa")
tmbhNamaMhs = formTmbhMhs.text_input("Nama")
tmbhEmailMhs = formTmbhMhs.text_input("Email")
tmbhNimMhs = formTmbhMhs.text_input("NIM")
tmbhProdiMhs = formTmbhMhs.text_input("Program Studi")
tmbhFakultasMhs = formTmbhMhs.text_input("Fakultas")
tmbhAngkatanMhs = formTmbhMhs.text_input("Angkatan")
tmbhNilaiUTSMhs = formTmbhMhs.text_input("Nilai UTS")
tmbhNilaiUASMhs = formTmbhMhs.text_input("Nilai UAS")
tmbhStatusMhs = formTmbhMhs.radio(
    label="Status Mahasiswa",
    options=("Aktif", "Pasif")
)
tambahData = formTmbhMhs.form_submit_button("Tambah Data")

# Stream Sidebar 
checkBoxTampilJumlahMhs = stream.sidebar.checkbox("Tampil Jumlah Mahasiswa Masing-Masing Prodi")
def sidebarMhs():
    stream.sidebar.header("Jumlah Mahasiswa")
    stream.sidebar.write(dfJumlahMhs)

if checkBoxTampilJumlahMhs:
    sidebarMhs()

# Fungsi Tambah Data
if tambahData:
    dataBaru = {"Name" : tmbhNamaMhs, "Email" : tmbhEmailMhs, "NIM": tmbhNimMhs, "Prodi": tmbhProdiMhs, "Fakultas": tmbhFakultasMhs, "Angkatan": tmbhAngkatanMhs, "UTS": tmbhNilaiUTSMhs, "UAS": tmbhNilaiUASMhs, "Status Mahasiswa": tmbhStatusMhs}
    df = pd.concat([df, pd.DataFrame([dataBaru])], ignore_index=True)
    df.to_excel("data/dataset.xlsx", index=False)

# Pie Chart
pieChartAngkatan = px.pie(dfAngkatan, 
                          title='Jumlah angkatan masing-masing Fakultas kelas IF-3', 
                          values='Angkatan',
                          names='Prodi'
                          )

# Bar Chart
barChartNilaiUTS = px.bar(dfNilai,
                          title="Jumlah Nilai UTS Masing Prodi",
                          x= 'Prodi',
                          y= 'UTS',
                          text='UTS',
                          color_discrete_sequence=['#005866']*len(dfNilai),
                          template='plotly_white'
                          )

barChartNilaiUAS = px.bar(dfNilai,
                          title="Jumlah Nilai UAS Masing Prodi",
                          x= 'Prodi',
                          y= 'UAS',
                          text='UAS',
                          color_discrete_sequence=['#eb4034']*len(dfNilai),
                          template='plotly_white'
                          )

# Stream Chart
stream.plotly_chart(pieChartAngkatan)
stream.plotly_chart(barChartNilaiUTS)
stream.plotly_chart(barChartNilaiUAS)

stream.header("Data Mahasiswa dan Klasifikasi Nilai")
stream.dataframe(df[['Name', 'HasilAkhir', 'KlasifikasiNilai']])

stream.header("Our Teams")
pur = Image.open("data/pur.jpg")
pur.resize(size=[100, 100])
ray = Image.open("data/ray.png")
ray.resize(size=[150, 100])
han = Image.open("data/han.png")
han.resize(size=[150, 100])
col1, col2, col3 = stream.columns(3)
col1.image(pur, caption="Purnama Hardi Saputra - 20102123")
col2.image(han, caption="Hanin Salsabila - 20102149")
col3.image(ray, caption="Rayhan Hafidh Wiarso - 20102138")
