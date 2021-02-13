import bs4 as bs
import os
from datetime import date
import urllib.request
from urllib.request import Request, urlopen

#get link and clean
inUserLink = input("Link the 4chan thread: ")
userLink = inUserLink.split('#', 1)[0]
print(userLink)


req = Request(userLink, headers={'User-Agent': 'Mozilla/5.0'})  #bypass 403 error

source = urllib.request.urlopen(req).read()
soup = bs.BeautifulSoup(source, 'lxml')


#retrieves all href links in replys
path = []
for child in soup.find_all('a', class_="fileThumb"):
    path.append(child.get('href'))


#prepends "https:" to plain links
http = "https:"
links = [http + p for p in path]    
print("There are " + str(len(links)) + " files.")


#mkdir with thread title + date
spChars = ['/', '\\', ':', '*', '?', "\"", '<', '>', '|'] #unallowed dir chars

threadTitle = soup.find('blockquote', class_="postMessage")
threadText = threadTitle.text

for i in spChars:
    threadText = threadText.replace(i, ' ') #replace special chars

dirName = threadText + " " + str(date.today())

if not os.path.isdir(dirName):
    print("Creating directory: ", dirName)
    os.mkdir(dirName)
else:
    print("E: Directory already present: ", dirName)
    

#sets file name and downloads every file in links list
fileName = ""
fNum = 1 
for link in links:
    fileName = link.split('/', 4)[4]    

    print("Downloading file: ", str(fNum), "-", fileName)
    urllib.request.urlretrieve(link, './' + dirName + '/' + str(fileName))
    fNum += 1
    fileName = ''

