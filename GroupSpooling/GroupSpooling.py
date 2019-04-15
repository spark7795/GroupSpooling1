import urllib
import urllib.request 
import os
import json
import time

SearchingUserID = 119827962
GroupID = "-28627911" # or smthng else. Group with '-' at begin of string. Users without.
access_token = ""
VersionAPI = "5.92"
#MaxSubsLimit = 200
UnProcessedPhotos = 0
MaxPhotosLimit = 1000
PhotosOffset = str(0)
#global PhotosInAlbum
#PhotosInAlbum = str(0)
AlbumsJSON_filename = "Albums.json"
AlbumsJSON_counter = "alcounter.json"
urllib.request.urlretrieve("https://api.vk.com/method/photos.getAlbums?owner_id="+GroupID+"&params[need_system]=0&params[need_covers]=0&params[photo_sizes]=0&access_token="+access_token+"&v="+VersionAPI+"", AlbumsJSON_filename)
urllib.request.urlretrieve("https://api.vk.com/method/photos.getAlbumsCount?user_id="+GroupID+"&access_token="+access_token+"&v="+VersionAPI+"", AlbumsJSON_counter)

with open(AlbumsJSON_filename, encoding='utf-8') as f:
    albumsid_dict = json.load(f)

#print (albumsid_dict["response"]["count"])
internalCounter = 0

while internalCounter < albumsid_dict["response"]["count"]:
    secondCounter = 0
    album_id = str(albumsid_dict["response"]["items"][internalCounter]["id"])
    time.sleep(1)
    urllib.request.urlretrieve("https://api.vk.com/method/photos.get?owner_id="+GroupID+"&album_id="+album_id+"&access_token="+access_token+"&v="+VersionAPI+"", "AlbumsJSON_Album_"+album_id+"")
    with open("AlbumsJSON_Album_"+album_id+"", encoding='utf-8') as fr:
        album_info = json.load(fr)
    PhotosInAlbum = int(album_info["response"]["count"])
    #print(PhotosInAlbum)
    if PhotosInAlbum < 1000:
        PhotosInAlbum = str(album_info["response"]["count"])
        urllib.request.urlretrieve("https://api.vk.com/method/photos.get?owner_id="+GroupID+"&album_id="+album_id+"&count="+PhotosInAlbum+"&access_token="+access_token+"&v="+VersionAPI+"", "AlbumsJSON_Album1_"+album_id+"")
        with open("AlbumsJSON_Album1_"+album_id+"", encoding='utf-8') as fr:
            album_info = json.load(fr)
        PhotosInAlbum = int(PhotosInAlbum)
        #while secondCounter < PhotosInAlbum:
        for X in album_info["response"]["items"]:        
            Userin = X["user_id"]
            if SearchingUserID == Userin:
                ClubID = str(X["owner_id"])
                PhotoID = str(X["id"])
                print("https://vk.com/photo"+ClubID+"_"+PhotoID)
            #secondCounter = secondCounter + 1
    else:
        UnProcessedPhotos = int(PhotosInAlbum)
        PhotosOffset = str(0)
        PhotosInAlbum = int(PhotosInAlbum)
        UnProcessedPhotos = PhotosInAlbum
        Max = 1000
        while UnProcessedPhotos > 1000:
            #if UnProcessedPhotos 
            secondCounter = 0
            PhotosInAlbum = str(album_info["response"]["count"])
            urllib.request.urlretrieve("https://api.vk.com/method/photos.get?owner_id="+GroupID+"&album_id="+album_id+"&offset="+PhotosOffset+"&count=1000"+"&access_token="+access_token+"&v="+VersionAPI+"", "AlbumsJSON_Album1_"+album_id+"")
            with open("AlbumsJSON_Album1_"+album_id+"", encoding='utf-8') as fr:
                album_info = json.load(fr)
            PhotosInAlbum = int(PhotosInAlbum)
            #while secondCounter < Max:
            for X in album_info["response"]["items"]:
                Userin = X["user_id"]
                if SearchingUserID == Userin:
                    ClubID = str(X["owner_id"])
                    PhotoID = str(X["id"])
                    print("https://vk.com/photo"+ClubID+"_"+PhotoID)
                #secondCounter = secondCounter + 1
            PhotosOffset = int(PhotosOffset) + 1000
            PhotosOffset = str(PhotosOffset)
            UnProcessedPhotos = UnProcessedPhotos-1000    
    internalCounter = internalCounter + 1

