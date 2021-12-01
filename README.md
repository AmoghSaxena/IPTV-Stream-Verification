# IPTV Stream Verification

### The program is simple and used to check the working of IPTV Channels. 
#### It takes the Channel List from an Excel file and performs various checks regarding the stream, and grabs the details like:
- Working condition [working/not-working]
- Audio Bit-rate
- Video Bit-rate
- Video Encoding  [H.264/HEVC/etc]
- Audio Encoding [AC3/etc]
- Encryption Status
- Resolution
- Multi-Language Support
- Subtitle
- TCP Source IP
- IGMP v2 and v3 Querry.

###### Just create the excel file in the same directory with the following details:
- Channel Name [CHANNEL NAME]
- Stream IP [MULTICAST IP]
- Port Number [PORT]

It should look like this
![](https://i.ibb.co/8YpNh0z/Screenshot-from-2021-12-01-14-39-37.png)


###### Now just start the program with the following arguments
- your output file name
- interface from which you receive the multicast stream
- and Excel file name

eg: `python iptv.py rexter eth0.100 dataexcel.xlsx`

And you will get the results in an excel file which will look like this.
![](https://i.ibb.co/R0BP597/Screenshot-from-2021-12-01-14-41-57.png)

## Requirements:
- Python 3.8 or above
- Linux OS
- VLC & MPV Media Player
- TCPDUMP Tool

## Installation: 
# "DONT FORGET TO RUN THIS PROGRAM WITH ROOT"
### If you want to create a virtual environment then:If you want to create a virtual environment then:
`virtualenv -p python3 venv`

`source venv/bin/activate`

#### Install Dependencies:
`sudo apt install vlc`

`sudo apt install mpv`

`sudo apt install tcpdump`

#### Install Python Modules:
`pip3 install -r requirements.txt
`
#### Starting the Program
> python3 iptv.py name_of_output_file multicast_stream_interface excel_file_name

eg: 
`python3 iptv.py rexter eth0.100 dataexcel.xlsx
`

For Demo of the Excel sheet I have also uploaded datasheet.xlsx