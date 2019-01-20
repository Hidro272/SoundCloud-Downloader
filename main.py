import sys
import os
import requests
import json
from urllib.request import urlopen
import bs4

os.system("title Xequinox's Soundcloud Downloader");
Version = 1.1
LatestVer = requests.get('https://pastebin.com/raw/QDzApaBF').text
DownloadLink = requests.get('https://pastebin.com/raw/BbTKyDni').text


if float(LatestVer) > Version:
    print("Current Version: " + str(Version))
    print("Latest Version: " + str(LatestVer))
    print("Download Link: "+ str(DownloadLink))
    input("\nPress any key to continue.\n")


clientid = "tgoEjKtQsCqtiffoqeHxtnND4Lx7zBqV"
def getDlUrl(TrackId):
    try:
        response = requests.get('https://api.soundcloud.com/i1/tracks/' + TrackId + '/streams?client_id=' + clientid)
        downloadUrl = json.loads(response.text)['http_mp3_128_url']
    except:
        print("[Error] - GetDlUrl")
        input("Press any key to return.\n")
        menu()
    return downloadUrl


def saveFile(name,url,dest):
    os.system("cls")
    print("Downloading: "+name)
    mp3file = urlopen(url)
    with open(dest,'wb') as output:
      output.write(mp3file.read())
    print("Finished Downloading: "+name)
    return


def PlaylistURL():
    os.system("cls")
    x = input("Enter A Playlist Url: ")
    response = requests.get(x)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    metas = soup.select("meta")
    PlaylistID = (str(metas[30]).split("\"")[1])[23:len(str(metas[30]).split("\"")[1])]
    response = requests.get("http://api.soundcloud.com/playlists/"+PlaylistID+"?client_id="+clientid)
    PlaylistName = json.loads(response.text)['title']
    if not os.path.isdir("Downloads/"):
        os.mkdir("Downloads/")
    if not os.path.isdir("Downloads/"+PlaylistName):
        os.mkdir("Downloads/"+PlaylistName)
    for i in range(0,len(json.loads(response.text)['tracks'])):
        title = json.loads(response.text)['tracks'][i]['title']
        saveFile(title,getDlUrl(str(json.loads(response.text)['tracks'][i]['id'])),"Downloads/" + PlaylistName + "/" + title + ".mp3")
    menu()


def TrackURL():
    os.system("cls")
    x = input("Enter A Track Url: ")
    os.system("cls")
    print("Loading...")
    try:
        response = requests.get(x)
        text = response.text
        soup = bs4.BeautifulSoup(text,"html.parser")
        metas = soup.select("meta")
        TrackId = str(metas[30]).split("\"")[1][20:len(str(metas[30]).split("\"")[1])]
    except:
        os.system("cls")
        print("[Error] - TrackURL")
        input("Press any key to return.\n")
        TrackURL()
    links = soup.select('link')
    link = str(links[17])[12:61]
    Author = str(metas[63]).split("\"")[1]
    Title = str(metas[38]).split("\"")[1]
    os.system("cls")
    print("TrackId: " + TrackId)
    print("Title: " + Title)
    print("Author: " + Author)
    if not os.path.isdir("Downloads/"):
        os.mkdir("Downloads/")
    saveFile(Title,getDlUrl(TrackId),"Downloads/"+Title+".mp3")
    input("Finished!, press any key to continue to the menu.")
    menu()


def menu():
    os.system("cls")
    print("Xequinox's Soundcloud Downloader")
    print("#"*35)
    print("[1] - Download Playlist From Url")
    print("[2] - Download Track From Url")
    print("#"*35)
    chc = input("#>")
    chc = chc[0]
    if chc == "1":
        PlaylistURL()
    elif chc == "2" :
        TrackURL()
    else:
        menu()
menu()
