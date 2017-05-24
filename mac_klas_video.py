import re, urllib, urllib2
import codecs
import ssl
import os

cookie = ""
course_ID_list = []         # for class ID
course_name_list = []    # for class name
lecture_name_list = []
lecture_CNT_list = []
lecture_LES_list = []

totalPageNumber = 0;
html = ""

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context



def Login():
    global html
    global cookie
    url = "https://klas.khu.ac.kr/mmain/viewMainIndex.do"
    req = urllib2.Request(url)
    user_id = raw_input("KLAS ID: ")
    PASSWORD = raw_input("KLAS password: ")
    PASSWORD={'PASSWORD':PASSWORD}
    PASSWORD=urllib.urlencode(PASSWORD)

    url = "https://klas.khu.ac.kr/muser/loginUser.do?USER_ID="+str(user_id)+"&"+PASSWORD
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    cookie = response.headers.get('Set-Cookie')
    request.add_header('Cookie',cookie)
    #print response.headers
    html = response.read()
    #print html

def FindCourse():
    global html
    global course_ID_list
    #print html
    course_number = html.count("/mcourse/viewCourseClassroom.do")
    first_index = 0
    for i in range(0,course_number):
        
        index = html.find("/mcourse/viewCourseClassroom.do",first_index+1)
        first_index = html.find("/mcourse/viewCourseClassroom.do",index)
        first_index = html.find("=",first_index)
        second_index = html.find("\"",first_index)
        course_ID = html[first_index+1:second_index]
        #print course_ID
        course_ID_list.append(course_ID)

        first_index = html.find("<h3>",second_index)
        second_index = html.find("</h3>",second_index)

        course_name = html[first_index+4:second_index]
        course_name_list.append(course_name)
        print str(i+1) +". "+ course_name
        

def EnterCourse():
    global cookie
    global course_ID_list
    global lecture_CNT_list
    global lecture_LES_list
    global lecture_name_list
     
    course_ID = raw_input("Enter Course Number: ")
    url = "http://klas.khu.ac.kr/mcourse/viewCourseClassroomInto.do?COURSE_ID=" + course_ID_list[int(course_ID)-1]
    request = urllib2.Request(url)
    request.add_header('Cookie',cookie)
    response = urllib2.urlopen(request)
    html = response.read()
    #print html
    lecture_count2 = html.count("<font size=\"3\" style=\"padding-left:50px;\">")
    lecture_count = html.count("onclick=\"fn_Join('content',")
    #first_index = html.find("<font size="3" style="padding-left:50px;">",first_index)
    #print lecture_count
    #print lecture_count2
    first_index = 0
    for i in range(0,lecture_count):
        first_index = html.find("onclick=\"fn_Join('content',",first_index+1)
        first_index = html.find(",",first_index)
        first_index = html.find("'",first_index)
        second_index = html.find("'",first_index+1)
        CNT_ID = html[first_index+1:second_index]
        lecture_CNT_list.append(CNT_ID)
        #print CNT_ID
        first_index = html.find("'",second_index+1)
        second_index = html.find("'",first_index+1)
        LES_ID = html[first_index+1:second_index]
        lecture_LES_list.append(LES_ID)
        #print LES_ID

        first_index = html.find("<font size=\"3\" style=\"padding-left:50px;\">",second_index)
        first_index = html.find("]",first_index)
        second_index = html.find("</font>",first_index)

        lecture_name = html[first_index+5:second_index]
        print str(i+1) + lecture_name
        lecture_name_list.append(lecture_name)


    #https://klas.khu.ac.kr/mstudy/viewStudyFrame.do?CONTENTS_ID=CNT_1702261137203fdf0a41&ACTIVITY_ID=LES_1702261137193fdf09ce&isClassroom=Y

def OpenLecture():
    global cookie
    global course_ID_list
    global lecture_CNT_list
    global lecture_LES_list
    global lecture_name_list
    temp = raw_input("Select Lecture Number : ")
    url = "http://klas.khu.ac.kr/mstudy/viewStudyFrame.do?CONTENTS_ID=" + lecture_CNT_list[int(temp)-1]+ "&ACTIVITY_ID=" + lecture_LES_list[int(temp)-1] + "&isClassroom=Y"
    request = urllib2.Request(url)
    request.add_header('Cookie',cookie)
    response = urllib2.urlopen(request)
    read = urllib2.urlopen(request).read()
    #print read
    first_index = read.find("<source")
    first_index = read.find("src",first_index)
    first_index = read.find("'",first_index)
    second_index = read.find("'",first_index+1)
    video_url = read[first_index+1:second_index]

    slash_count = video_url.count("/")
    index = 0
    for i in range(0,slash_count-1):
        index = video_url.find("/",index+1)
    second_index = video_url.find(".",index)
    
    video_name = video_url[index+1:second_index]
    
    print video_name
    video_name = {'video_url':video_name}
    video_name = urllib.urlencode(video_name)
    name_index = video_name.find("=")
    video_name = video_name[name_index+1:]

    video_url = video_url[:index+1] + video_name + video_url[second_index:]
    print video_url
    command = 'mplayer %s 1>/dev/null 2>&1' % video_url
    os.system(command)

Login()
FindCourse()
EnterCourse()
OpenLecture()
