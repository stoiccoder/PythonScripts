from mechanize import Browser
from bs4 import BeautifulSoup
import textwrap
import sys
import os.path
import os

def getTranscript(str):
    br1 = Browser()
    br1.set_handle_robots(False)
    try:
        respo = br1.open(str)
    except Exception as e:
        print e.message
        sys.exit(0)
    sou = BeautifulSoup(respo, "html.parser")
    name = sou.find('title')                       #Video Name =File Name
    name=name.text
    br1.close()

    br = Browser()
    br.set_handle_robots(False)
    str = str.partition("?v=")[2]
    link = "http://video.google.com/timedtext?lang=en&v=" + str
    try:
        response = br.open(link)
    except Exception as e:
        print e.message
        print "Make sure the video has subtitles available!"
        sys.exit(0)
    soup = BeautifulSoup(response , "html.parser")
    data = soup.text
    a = " ".join(data.split())
    br.close()
    return textwrap.fill(a) , name

def getLinks(link):
    br = Browser()
    br.set_handle_robots(False)
    try:
        response = br.open(link)
    except Exception as e:
        print e.message
        sys.exit(0)
    soup = BeautifulSoup(response , "html.parser")
    data = soup.find_all('a',{'class':'pl-video-title-link'})       #links of all videos in the playlist
    arr=[]
    for l in data:
        arr.append(l.get('href'))
    for i in range(len(arr)):
        arr[i] = str(arr[i])
        arr[i] = "https://www.youtube.com" + arr[i]
    br.close()
    return arr

def writeFile(data,name,path):
    cname=os.path.join(path,name+'.txt')
    try:
        f=open(cname, 'w+')
        f.write(data.encode("utf-8"))
    except Exception as e:
        print (e.message)
    finally:
        f.close()

while(True):
    ch = raw_input("\n1-Single Video\n2-Playlist\nX to exit\n")
    if ch=='1':
        link = raw_input("Enter the link of the video:\n")
        path = raw_input("Enter file path without filename.(Leave blank for default)")
        data,name = getTranscript(link)
        writeFile(data,name,path)
        print "Done!"
        print "File with name as video name created."

    elif ch=='2':
        arr2=[]
        link = raw_input("Enter the link of the playlist:\n")
        arr2 = getLinks(link)
        br2=Browser()
        br2.set_handle_robots(False)
        res = br2.open(link)
        sp=BeautifulSoup(res, 'html.parser')
        name=sp.find('title')                     #Folder Name= Channel Name
        name=name.text

        path = raw_input("Enter file path without filename.(Leave blank for default.)")
        l=len(arr2)
        print "Creating folder with channel name.(In case of wrong file path name, check default directory.)"
        path=os.path.join(path,name)
        os.makedirs(path)
        print "The playlist contains {0} videos.".format(l)
        if l>10:
            print "This might take a while, go grab some popcorn!"
        x=1
        for i in arr2:
            sys.stdout.write('\r' +'Done '+ str((x*100)/l)+'%')
            sys.stdout.flush()
            #print "\rDone {0}%".format((x*100)/l),     Not working on Terminal :(
            x+=1
            data, name = getTranscript(i)
            writeFile(data,name, path)


    elif ch=='X' or ch=='x':
        sys.exit(0)

    else:
        print "Invalid Input"


