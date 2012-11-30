#!/usr/bin/python
import os
import pycurl
import cStringIO
import re
import random
import time

username = "username"
password = "password"
hashtags = ["love","instagood","me","cute","photooftheday","tbt","instamood","iphonesia","picoftheday","igers","girl","beautiful","instadaily","tweegram","summer","instagramhub","follow","bestoftheday","iphoneonly","igdaily","happy","picstitch","webstagram","fashion","sky","nofilter","jj","followme","fun","smile","sun","pretty","instagramers","food","like","friends","lol","hair","nature","swag","onedirection","bored","funny","life","cool","beach","blue","dog","pink","art","hot","my","family","sunset","photo","versagram","instahub","amazing","statigram","girls","cat","awesome","throwbackthursday","repost","clouds","baby","red","music","party","black","instalove","night","textgram","followback","all_shots","jj_forum","igaddict","yummy","white","yum","bestfriend","green","school","likeforlike","eyes","sweet","instago","tagsforlikes","style","harrystyles","2012","foodporn","beauty","ignation","niallhoran","i","boy","nice","halloween","instacollage"]

def login():
    try:
        os.remove("pycookie.txt")
    except:
        pass

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://web.stagram.com")
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
    c.perform()
    curlData = buf.getvalue()
    buf.close()

    clientid = re.findall(ur"href=\"https:\/\/api.instagram.com\/oauth\/authorize\/\?client_id=([a-z0-9]*)&redirect_uri=http:\/\/web.stagram.com\/&response_type=code&scope=likes\+comments\+relationships\">LOG IN",curlData)
    instagramlink = re.findall(ur"href=\"([^\"]*)\">LOG IN",curlData)




    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, instagramlink[0])
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
    c.perform()
    curlData = buf.getvalue()
    buf.close()

    postaction = re.findall(ur"action=\"([^\"]*)\"",curlData)
    csrfmiddlewaretoken = re.findall(ur"name=\"csrfmiddlewaretoken\" value=\"([^\"]*)\"",curlData)





    postdata = 'csrfmiddlewaretoken='+csrfmiddlewaretoken[0]+'&username='+username+'&password='+password

    buf = cStringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, "https://instagram.com"+postaction[0])
    c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
    c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
    c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.ENCODING, "")
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.REFERER, "https://instagram.com/accounts/login/?next=/oauth/authorize/%3Fclient_id%3D"+clientid[0]+"%26redirect_uri%3Dhttp%3A//web.stagram.com/%26response_type%3Dcode%26scope%3Dlikes%2Bcomments%2Brelationships")
    c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, postdata)
    c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
    #c.setopt(pycurl.VERBOSE, True)
    c.perform()
    curlData = buf.getvalue()
    buf.close()



def like():
    likecount = 0
    sleepcount = 0
    for tag in hashtags:
        nextpage = "http://web.stagram.com/tag/"+tag+"/?vm=list"
        #enter infinite poke loop
        while nextpage != False:
            buf = cStringIO.StringIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, nextpage)
            c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
            c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
            c.setopt(pycurl.WRITEFUNCTION, buf.write)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            c.setopt(pycurl.ENCODING, "")
            c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
            c.perform()
            curlData = buf.getvalue()
            buf.close()

            nextpagelink = re.findall(ur"<a href=\"([^\"]*)\" rel=\"next\">Earlier<\/a>",curlData)
            if len(nextpagelink)>0:
                nextpage = "http://web.stagram.com"+nextpagelink[0]
            else:
                nextpage = False

            likedata = re.findall(ur"<span class=\"like_button\" id=\"like_button_([^\"]*)\">",curlData)
            if len(likedata)>0:
                for imageid in likedata:
                    repeat = True
                    while repeat:
                        randomint = random.randint(1000,9999)

                        postdata = 'pk='+imageid+'&t='+str(randomint)
                        buf = cStringIO.StringIO()
                        c = pycurl.Curl()
                        c.setopt(pycurl.URL, "http://web.stagram.com/do_like/")
                        c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
                        c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
                        c.setopt(pycurl.WRITEFUNCTION, buf.write)
                        c.setopt(pycurl.FOLLOWLOCATION, 1)
                        c.setopt(pycurl.ENCODING, "")
                        c.setopt(pycurl.USERAGENT, "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6 (.NET CLR 3.5.30729)")
                        c.setopt(pycurl.POST, 1)
                        c.setopt(pycurl.POSTFIELDS, postdata)
                        c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
                        #c.setopt(pycurl.VERBOSE, True)
                        c.perform()
                        postData = buf.getvalue()
                        buf.close()
                        if postData == '''{"status":"OK","message":"LIKED"}''':
                            likecount += 1
                            print "You liked #"+tag+" image "+imageid+"! Like count: "+str(likecount)
                            repeat = False
                            sleepcount = 0
                        else:
                            sleepcount += 1
                            print "Your account has been rated. Sleeping on "+tag+" for "+str(sleepcount)+" minute(s). Liked "+str(likecount)+" photo(s)..."
                            time.sleep(60)

def main():
    login()
    like()

if __name__ == "__main__":
    main()
