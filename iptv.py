import pandas as pd
import os
from posixpath import join
import time
import subprocess
import subprocess as sp
import sys
import datetime
args = sys.argv
import pysftp

print("Starting...")
os.system('export DISPLAY=:0.0')
date_now = datetime.datetime.now().strftime("%d-%m-%y-%H-%M")
os.system("sudo sed -i 's/geteuid/getppid/' /usr/bin/vlc")
cwd = os.path.dirname(os.path.abspath(__file__))

work_list = []
audio_dec = []
video_dec = []
res_dt = []
tcp_list = []
tcp_igmp = []
tcp_igmp_2 = []
bitrate = []
working_var = []
audioch = []
audio_lan = []
subtitles = []
encryption = []
csn = []
txtfrmt = []
count = 0
##############################################################
try:
    site_name = args[1]
    interface = args[2]
    filename = args[3]
    
except:
    print("INVALID PARAMETERS WERE LAUNCHED WITH FILE!!!")
    print("Stopped...")
    exit()
print("Parameters are : ", args)
res_file_name = site_name + "-" + date_now + ".xlsx"
##############################################################

try:
    df = pd.read_excel(filename, sheet_name=0, engine='openpyxl') # can also index sheet by name or fetch all sheets
    channel_name = df['CHANNEL NAME'].tolist()
    mylist = df['MULTICAST IP'].tolist()
    port_no = df['PORT'].tolist()
except:
    print("FILE NOT FOUND!! OR DATA IS MISSING!!")
    exit()

#mylist = ['239.255.7.182', '239.255.3.3', '239.255.7.188','239.255.3.2', '239.255.7.190', '239.255.119.35','239.255.7.189','239.255.7.183','239.255.7.191']
print("Got Total : ",len(mylist)," ip")

def tcp_route(ip_add):
    print("Checking for Stream...")
    vlc_play = 'export DISPLAY=:0.0 && cvlc -f -q udp://@' + ip_add
    subprocess.Popen(vlc_play, shell=True)
    ip_with_port = ip_add
    feed_chk(ip_with_port)

def feed_chk(ipWithPort):
    srcp = 'timeout 5 mpv udp://' + ipWithPort + " > sample.txt"
    print("Checking if Feed is Available...")
    subprocess.Popen(srcp, shell=True)
    time.sleep(5)
    y = '(+) Video'
    with open('sample.txt') as f:
        if y in f.read():
            print("Feed Is Available...!!")
            res = 'Working'
            work_list.append(res)
            feed_avi(ipWithPort)
            print("Grabbing The details...")
        else:
            res = 'Not Working'
            work_list.append(res)
            feed_n_avi()

def enc_feed(ipWithPort):
    conv = "timeout 1m cvlc -q udp://@"+ipWithPort+" :demux=dump :demuxdump-file=test.ts"
    os.system(conv)
    
def feed_avi(ipWithPort):
    #conv = "ffmpeg -v error -probesize 30M -analyzeduration 30M -fflags +genpts -re -i udp://"+working_var[-1]+":1234?fifo_size=1000000 -c copy -t 10 -y -f mpegts test.ts"
    conv = "timeout 20s cvlc -q udp://@"+ipWithPort+" :demux=dump :demuxdump-file=test.ts"
    os.system(conv)
    
    enc = sp.getoutput('mediainfo test.ts --Inform='+'"Video;%Encryption%"')
    size = bool(enc)
    if size == False:
        enc = 'Not Encrypted'
    else:
        enc_feed(ipWithPort)
        # enc = enc_feed.enc_final

    bit = sp.getoutput('mediainfo test.ts --Inform='+'"General;%OverallBitRate%"')
    try:
        bitrate_data = str(int(bit)/1000000)+" Mb/s"
    except:
        bitrate_data = bit + " B/s"

    resw = sp.getoutput('mediainfo test.ts --Inform='+'"Video;%Width%"')
    resh = sp.getoutput('mediainfo test.ts --Inform='+'"Video;%Height%"')
    size = bool(resh)
    if size == False:
        resolution = 'N/A'
    else:
        resolution = str(resw)+"x"+str(resh)

    vid_for = sp.getoutput('mediainfo test.ts --Inform='+'"Video;%Format%"')
    if vid_for == "MPEG Video":
        var = "mediainfo test.ts | grep -i 'MPEG Video' -n1 | grep -i 'Format version' |  awk '{print $5}'"
        vid_car = sp.getoutput(var)
        vid_for = vid_for+" Version: "+vid_car
                
    aud_for = sp.getoutput('mediainfo test.ts --Inform='+'"Audio;%Format%, "')
    
    aud_lan = sp.getoutput('mediainfo test.ts --Inform='+'"Audio;%Language%, "')
    
    csn_cap = sp.getoutput('mediainfo test.ts --Inform='+'"Text;%CaptionServiceName%, "') #for caption
    
    txt_for = sp.getoutput('mediainfo test.ts --Inform='+'"Text;%Format%, "') #for format

    sub_tel = sp.getoutput('mediainfo test.ts --Inform='+'"Text;%Language%, "')
    size = bool(sub_tel)
    if size == False:
        tel_sub = 'N/A'
    else:
        tel_sub = sub_tel
        
    aud_ch = sp.getoutput('mediainfo test.ts --Inform='+'"Audio;%Channels%, "')
    size = bool(aud_ch)
    if size == False:
        aud_ch = 'N/A'
    ####################################
    audio_dec.append(aud_for)
    video_dec.append(vid_for)
    res_dt.append(resolution)
    bitrate.append(bitrate_data)
    subtitles.append(tel_sub)
    audioch.append(aud_ch)
    audio_lan.append(aud_lan)
    encryption.append(enc)
    csn.append(csn_cap)
    txtfrmt.append(txt_for)
    

    tcp_info()


def feed_n_avi():
    no_data = '-'
    audio_dec.append(no_data)
    video_dec.append(no_data)
    res_dt.append(no_data)
    tcp_list.append(no_data)
    if count == 0:
        print("First Time")
        igmp()
    else:
        tcp_igmp.append(no_data)
        tcp_igmp_2.append(no_data)
    bitrate.append(no_data)
    subtitles.append(no_data)
    audioch.append(no_data)
    audio_lan.append(no_data)
    encryption.append(no_data)
    csn.append(no_data)
    txtfrmt.append(no_data)
    cles()

def tcp_info():
    line2 = "'/"+working_var[-1]+"/ && /length/ && /UDP/'"
    scp_tcp = 'timeout 5s tcpdump -ni ' + interface + ' | awk '+line2+' > sample1.txt'
    print(scp_tcp)
    os.popen(scp_tcp).read()
    time.sleep(5)
    tcp_file = os.popen('cat sample1.txt | head -1').read()
    print(tcp_file)
    tcpr = tcp_file.split()
    crp_tcp = str(tcpr[2])
    tcpsrp = ".".join(crp_tcp.split(".")[:4])
    tcp_list.append(tcpsrp)
    if count==0:
        igmp()
    else:
        tcp_igmp.append('-')
        tcp_igmp_2.append('-')
        cles()

def cles():
    os.system('killall vlc')

def igmp():
    phrase = "224.0.0.1: igmp query v2"
    scp_igp = 'timeout 180s tcpdump -ni ' + interface +" 'igmp'"+' > sample2.txt'
    print(scp_igp)
    os.popen(scp_igp).read()
    line_number = "Phrase not found"
    a_file = open("sample2.txt","r")
    b_file = open("sample2.txt","r")
    for number, line in enumerate(a_file):
      if phrase in line:
        line_number = number
        break
    a_file.close()
    content = b_file.readlines()
    if line_number == 'Phrase not found':
        print("##########################################")
        print("IGMP NOT FOUND")
        print("##########################################")
        data_fill = pd.DataFrame({'STATUS':["IGMP NOT FOUND :("]})
        data_sheet = {'Sheet1': data_fill}
        writer = pd.ExcelWriter(res_file_name, engine='xlsxwriter')
        for sheet_name in data_sheet.keys():
                data_sheet[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
        writer.save()
        result_final_ig = pd.read_excel (res_file_name, engine='openpyxl')
        print(result_final_ig)
        os.system('rm sample.txt')
        os.system('rm sample1.txt')
        os.system('rm sample2.txt')
        os.system('rm test.ts')
        exit()
    else:
        global count
        first_line = content[line_number].split()
        tcp_igmp.append(first_line[2])
        count = 1
        
        #########################################
        
        phrase = "224.0.0.1: igmp query v3"
        line_number = "Phrase not found"
        a_file = open("sample2.txt","r")
        b_file = open("sample2.txt","r")
        for number, line in enumerate(a_file):
            if phrase in line:
                line_number = number
                break
        a_file.close()
        content = b_file.readlines()
        if line_number == 'Phrase not found':
            no_data = "-"
            tcp_igmp_2.append(no_data)
        else:
            first_line = content[line_number].split()
            tcp_igmp_2.append(first_line[2])
            
        
        #########################################
        
        cles()


def upload(uploaded_file):
    cwd_loc = cwd + "/" + uploaded_file
    path = '/var/www/html/result/' + uploaded_file
    with pysftp.Connection(host, username=username, password=password, port=35222, cnopts=cnopts) as sftp:
        sftp.put(cwd_loc, path)
    print("Uploaded File to server")
    print("++++++++++++++++++++++++++++++")
    print("DIRECT DOWNLOAD LINK : https://feedchecker.digivalet.com/result/" + uploaded_file)




##########PROGRAM STARTING###########################
for j in range(0,len(mylist)):
        working_var.append(mylist[j])
        ip_port = str(mylist[j]) + ":" + str(port_no[j])
        print("Checking feed on : " + ip_port)
        tcp_route(ip_port)
#####################################################




###################DATA WRITTEN IN EXCEL#############
data_fill = pd.DataFrame({'Channel Name':channel_name,'IP': mylist,'Port': port_no,'Feed':work_list,'Encryption': encryption,'Video Encoding':video_dec,'Bitrate':bitrate,'Audio Channels':audioch,'Audio Language':audio_lan,'Video Resolution':res_dt,'Audio Encoding':audio_dec,'Subtitiles':subtitles,'CaptionService':csn,'Text Format':txtfrmt,'TCP Source IP':tcp_list,'IGMP v2':tcp_igmp,'IGMP v3':tcp_igmp_2})
data_sheet = {'Sheet1': data_fill}
writer = pd.ExcelWriter(res_file_name, engine='xlsxwriter')
for sheet_name in data_sheet.keys():
    data_sheet[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
writer.save()
os.system('rm sample.txt')
os.system('rm sample1.txt')
os.system('rm sample2.txt')
os.system('rm test.ts')
print("Program completed With 0 Error")
result_final = pd.read_excel(res_file_name, engine='openpyxl')
print(result_final)
print("Excel file saved as: " + res_file_name)
try:
    upload(res_file_name)
except:
    pass
