#!/usr/bin/python

'''
Cranklin's Instagram Bot v.1.0
==============================
Check www.cranklin.com for updates


This bot gets you more likes and followers on your Instagram account.

Requirements:
    - python > 2.6 but < 3.0
    - pycurl library
    - web.stagram.com login prior to using the bot

    Instructions:
        - make sure you have the correct version of Python installed
        - make sure you have the pycurl library installed
        - log into web.stagram.com with your instagram account and approve the app
        - edit between lines 42 and 52
        - from the command line, run "python webstagram.py"
        - enjoy!

    v1.0 updates:
        - added browser agent randomizer
        - added optional sleep timer
        - added optional hashtag limiter
        - added a couple extra additions for some people experiencing SSL errors. (thanks Charlie)
        *** thank you Nick, John, Max, Shahar, Charlie for the help
'''

import os
import pycurl
import cStringIO
import re
import random as r
import time


##### EDIT THESE BELOW

# your instagram username and password instagram
username = ""
password = ""

# replaced the list of hashtags as it is a pain to add new hashtags!
# name of the config file where you have your hashtags
hashTagFile = "config.txt"

# set a sleep timer between each like.  Set value to 0 if you don't want it to sleep at all
sleepTimer = 10

# max number of likes before going to sleep for an hour
maxLikes = 140

# set a like limit per hashtag.  Set value to 0 if you don't want a limit
hashTagLikeLimit = 0

##### NO NEED TO EDIT BELOW THIS LINE

# for user agent strings
browsers = ["IE ","Mozilla/","Gecko/","Opera/","Chrome/","Safari/"]
operatingSystems = ["Windows","Linux","OS X","compatible","Macintosh","Intel"]


def login():
    """
        login using pycurl    
    """
    try:
        os.remove("pycookie.txt")
    except:
        pass

    # Request one to web.stagram.com
    webstagramRequest = sendRequest("http://web.stagram.com", "pycookie.txt", 1, "", 0, 0)

    # Anyone want to refactor this stuff!?!?
    insaneRegEx1 = ur"href=\"https:\/\/api.instagram.com\/oauth\/authorize\/\?client_id=([a-z0-9]*)&redirect_uri=http:\/\/web.stagram.com\/&response_type=code&scope=likes\+comments\+relationships\">LOG IN"
    insaneRegEx2 = ur"href=\"([^\"]*)\">LOG IN"

    clientId = re.findall(insaneRegEx1, webstagramRequest)
    instagramLink = re.findall(insaneRegEx2, webstagramRequest)

    # Request two to instagram.com
    instagramLinkRequest = sendRequest(instagramLink[0], "pycookie.txt", 1, "", 0, 0)

    insaneRegEx3 = ur"action=\"([^\"]*)\""
    insaneReqEx4 = ur"name=\"csrfmiddlewaretoken\" value=\"([^\"]*)\""

    postAction = re.findall(insaneRegEx3, instagramLinkRequest)
    csrfMiddlewareToken = re.findall(insaneReqEx4, instagramLinkRequest)

    postData = "csrfmiddlewaretoken={csrfToken}&username={uname}&password={pword}".format(csrfToken = csrfMiddlewareToken[0], 
                                                                                          uname     = username,
                                                                                          pword     = password)

    insaneUrl = "https://instagram.com/accounts/login/?next=/oauth/authorize/%3Fclient_id%3D" + clientId[0] + "%26redirect_uri%3Dhttp%3A//web.stagram.com/%26response_type%3Dcode%26scope%3Dlikes%2Bcomments%2Brelationships"
    finalRequest = sendReferRequest("https://instagram.com" + postAction[0], "pycookie.txt", 1, "", 0, 0, insaneUrl, 1, postData, len(postData))


def like():
    """
        like a random instagram photo which contains a hashtag from config.txt
    """
    likeCount = 0
    sleepCount = 0
    for tag in getHashTags(hashTagFile):
        hashTagLikes = 0
        nextPage = "http://web.stagram.com/tag/"+ tag + "/?vm=list"

        while nextPage and (hashTagLikeLimit == 0 or (hashTagLikeLimit > 0 and hashTagLikes < hashTagLikeLimit)):

            req = sendRequest(nextPage, "pycookie.txt", 1, "", 0, 0)

            anotherRegEx1 = ur"<a href=\"([^\"]*)\" rel=\"next\">Earlier<\/a>"
            nextPageLink = re.findall(anotherRegEx1, req)
            
            if len(nextPageLink) > 0:
                nextPage = "http://web.stagram.com" + nextPageLink[0]
            else:
                nextPage = False

            anotherRegEx2 = ur"<span class=\"like_button\" id=\"like_button_([^\"]*)\">"
            likeData = re.findall(anotherRegEx2, req )

            if len(likeData) > 0:
                for imageId in likeData:

                    if hashTagLikeLimit > 0 and hashTagLikes >= hashTagLikeLimit:
                        break

                    repeat = True

                    while repeat:
                        rand = r.randint(1000,9999)

                        postData = "pk={imgId}&t={rand}".format(imgId=imageId, rand=rand)
                        status = sendReferRequest("http://web.stagram.com/do_like/", "pycookie.txt", 1, "", 0, 0, "", 1, postData, len(postData))

                        print status
                        if status == '''{"status":"OK","message":"LIKED"}''':
                            print "You liked #"+tag+" image "+ imageId + "! Like count: "+str(likeCount)

                            repeat = False

                            likeCount += 1
                            hashTagLikes += 1
                            sleepCount = 0

                            # sleep for an hour when you have liked 'maxlike' images
                            if likeCount > 0 and likeCount == maxLikes:
                                print "liked " + maxLikes + " times, now going to sleep for an hour"
                                time.sleep(3600)

                            if sleepTimer > 0:
                                time.sleep(sleepTimer)
                        else:
                            sleepCount += 1
                            print "You've been rate limited. Sleeping on {tag} for {sleepCount} min(s). Liked {likeCount} photo(s)".format(tag=tag, sleepCount=sleepCount, likeCount=likeCount)
                            time.sleep(60)


def sendRequest(url, cookieFn, follow, encoding, vPeer, vHost):
    """
        send a pycurl request
    """
    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.COOKIEFILE, cookieFn)
    c.setopt(pycurl.COOKIEJAR, cookieFn)
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, follow)
    c.setopt(pycurl.ENCODING, encoding)
    c.setopt(pycurl.SSL_VERIFYPEER, vPeer)
    c.setopt(pycurl.SSL_VERIFYHOST, vHost)
    c.setopt(pycurl.USERAGENT, randomUserAgent())
    c.perform()

    curlData = buf.getvalue()
    buf.close()
    return curlData


def sendReferRequest(url, cookieFn, follow, encoding, vPeer, 
                     vHost, ref, post, postF, postFs):
    """
        send pycurl request with extra options
    """
    buf = cStringIO.StringIO()
    c = pycurl.Curl()

    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.COOKIEFILE, cookieFn)
    c.setopt(pycurl.COOKIEJAR, cookieFn)
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, follow)
    c.setopt(pycurl.ENCODING, encoding)
    c.setopt(pycurl.SSL_VERIFYPEER, vPeer)
    c.setopt(pycurl.SSL_VERIFYHOST, vHost)
    c.setopt(pycurl.REFERER, ref)
    c.setopt(pycurl.USERAGENT, randomUserAgent())
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, postF)
    c.setopt(pycurl.POSTFIELDSIZE, postFs)
    c.perform()

    curlData = buf.getvalue()
    buf.close()
    return curlData


def getHashTags(fn):
    """
        a list of hashtags from a config file
    """
    with open(fn) as f:
        return [tag.strip() for tag in f.readlines()]


def randomUserAgent():
    """
        a user agent string created from a list of browsers
    """
    return "{os1} {vnum1}.{vnum2} ({os2}; {os3}; rv:{v1}.{v2}.{v3}.{v4})".format( os1   = r.choice(browsers),
                                                                                  vnum1 = str(r.randrange(1,9)),
                                                                                  vnum2 = str(r.randrange(0,50)),
                                                                                  os2   = r.choice(operatingSystems),
                                                                                  os3   = r.choice(operatingSystems),
                                                                                  v1    = str(r.randrange(1,9)),
                                                                                  v2    = str(r.randrange(1,9)),
                                                                                  v3    = str(r.randrange(1,9)),
                                                                                  v4    = str(r.randrange(1,9)))

def main():
    login()
    like()

if __name__ == "__main__":
    main()
