import re, urllib, urllib2
import codecs
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context
#####################  MAIN PAGE ############################

print "KLAS Main"

url = "https://klas.khu.ac.kr/main/viewMainIndex.do"
req = urllib2.Request(url)
#read =urllib2.urlopen(req,timeout=5).read()

#print read

#####################  LOGIN FORM ############################
user_id = raw_input("KLAS ID: ")
PASSWORD = raw_input("KLAS password: ")
#login_form = {'USER_ID': user_id, 'PASSWORD': user_password}

PASSWORD={'PASSWORD':PASSWORD}
PASSWORD=urllib.urlencode(PASSWORD)



#####################  Login And Get Cookie ############################
#url = "http://klas.khu.ac.kr/user/loginUser.do"
#url = "http://klas.khu.ac.kr//user/loginUser.do"
url = "https://klas.khu.ac.kr/user/loginUser.do?USER_ID="+str(user_id)+"&"+PASSWORD
print url
#request = urllib2.Request(url, data)
#response = urllib2.urlopen(request)
#print response.headers
#cookie = response.headers.get('Set-Cookie')
#html = response.read()
#print cookie
request = urllib2.Request(url)
response = urllib2.urlopen(request)
cookie = response.headers.get('Set-Cookie')
request.add_header('Cookie',cookie)
print response.headers

#print html    #  Main Page

course_ID_list = []         # for class ID
course_name_list = []    # for class name
totalPageNumber = 0;

#####################  GO CLASSROOM MAIN ############################

url = "http://klas.khu.ac.kr/classroom/viewClassroomMain.do"

request = urllib2.Request(url)
request.add_header('Cookie',cookie)
print response.headers
read =urllib2.urlopen(request).read()
#print read         # Classroom Page


#####################  FIND TOTAL PAGE ############################

index = read.find("<div class=\"paging\">")
index = read.find("</span></a></span>",index)
totalPageNumber = read[index-1]
totalPageNum = int(totalPageNumber)

#####################  FIND COURSE ID ############################

for pageNum in range(1,totalPageNum+1):

    url = "http://klas.khu.ac.kr/classroom/viewClassroomMain.do?coursePageIndex=" + str(pageNum)
    request = urllib2.Request(url)
    request.add_header('Cookie',cookie)
    read =urllib2.urlopen(request).read()
    #print read         # Classroom Page

    first_index = read.find("/classroom/viewClassroomCourseMoreList.do?courseType=ing")
    final_index = read.find("paging",first_index)
    course_number = read.count("</dl>",first_index,final_index)
    course_number = int(course_number)
    for i in range(0,course_number):
        first_index = read.find("<dt><strong>",first_index)
        first_index += 11
        second_index = read.find("</strong>",first_index)

        course_name = read[first_index+1:second_index]
        course_name_list.append(course_name)

        second_index = read.find("/course/viewCourseClassroom.do?COURSE_ID",second_index)
        second_index = read.find("=",second_index)
        third_index = read.find("\"",second_index)
        
        course_ID= read[second_index+1:third_index]
        course_ID_list.append(course_ID)
        
    
        #print course_name
        #print course_ID

i = 1
for name in course_name_list:
    print str(i) + " : " + name
    i += 1
    

    

##################### ADD COURSE LIST############################





#####################  ENTER SPECIFIC CLASSROOM ############################

#url = "http://klas.khu.ac.kr/course/viewCourseClassroom.do?COURSE_ID=2016_20_EE20700"
course_ID = raw_input("Enter Course Number: ")
url = "http://klas.khu.ac.kr/course/viewCourseClassroom.do?COURSE_ID=" + course_ID_list[int(course_ID)-1]
request = urllib2.Request(url)
request.add_header('Cookie',cookie)
reponse = urllib2.urlopen(request)


#read = response.read()
read =urllib2.urlopen(request).read()

#print read          # ClassRoom #1 Page


##################  GET LECTURE LIST ####################################
#counter = read.count("onclick=\"fn_Join('content',")
counter = read.count("word-break:break-all;") + 1
lecture_name_list = []
lecture_period_list = []
lecture_recommend_list = []
lecture_current_list = []
first_index = 0
for i in range(0,counter):

    #index = read.find("<ul style=\"word-break:break-all;\">",first_index)
    index = read.find("word-break:break-all;",first_index)

    img_index = read.find("<img src=",index)
    img_index = read.find("\"",img_index)
    sec_img_index = read.find("\"",img_index+1)
    #print read[img_index+1:sec_img_index]

    if(read[img_index+1:sec_img_index]=="/webdata/ko/images/common/myclass/btn_mycl_continfo_05.gif"):
        img_index = read.find("<img src=",img_index+1)
        img_index = read.find("\"",img_index)
        sec_img_index = read.find("\"",img_index+1)
        #print read[img_index+1:sec_img_index]
    
    if(read[img_index+1:sec_img_index]=="/webdata/ko/images/common/myclass/btn_mycl_continfo_01.gif"):
        #print "good"
        #print read[img_index+1:sec_img_index]

        first_index = read.find("<b>",index)
        first_index += 3
        second_index = read.find("</b>",first_index)
        lecture_name = read[first_index:second_index]
        lecture_name_list.append(lecture_name)


        first_index = read.find("<li><span>",second_index)
        second_index = read.find("</span></li>",second_index)
        first_index += 10
        lecture_period = read[first_index:second_index]
        lecture_period_list.append(lecture_period)

        first_index = read.find("<li",second_index)
        first_index = read.find(">",first_index)
        second_index = read.find("</li>",first_index)
        first_index += 1
        lecture_recommend = read[first_index:second_index]
        lecture_recommend_list.append(lecture_recommend)



        first_index = read.find("studytime",second_index)
        first_index = read.find(">",first_index)
        second_index = read.find("</li>",first_index)
        first_index += 1
        lecture_current = read[first_index:second_index]
        lecture_current = lecture_current.strip()
        lecture_current_list.append(lecture_current)

    else:                         
    
        first_index = read.find("word-break:break-all;",first_index+1)



counter = read.count("onclick=\"fn_Join('content',")
for count in range(0,counter):
    print "Lecture " + str(count+1) + " : " + lecture_name_list[count]
    print "            " + lecture_period_list[count]
    print "            " + lecture_recommend_list[count]
    print "            " + lecture_current_list[count]
    print " "

content_list = []
activity_list = []

first_index = 0
for count in range(0,counter):
    first_index = read.find("onclick=\"fn_Join('content',",first_index)
    first_index = read.find("','",first_index)
    first_index += 3
    second_index = read.find("','",first_index)
    content_name = read[first_index:second_index]
    content_list.append(content_name)
    first_index = read.find("','",first_index)
    first_index += 3
    second_index = read.find("','",first_index)
    activity_name = read[first_index:second_index]
    activity_list.append(activity_name)
    
temp = raw_input("Select Lecture Number : ")
url = "http://klas.khu.ac.kr/study/viewStudyFrame.do?CONTENTS_ID=" + content_list[int(temp)-1]+ "&ACTIVITY_ID=" + activity_list[int(temp)-1]

#--ClassRoom Html--#
#http://klas.khu.ac.kr/course/viewCourseClassroom.do?COURSE_ID=2016_20_EE20700
#--Cookie Form--#
#Cookie: COURSE_MENU_NAME=%uAC15%uC758%uC2E4; OPEN_2016122017=Y; LMS_JSESSIONID=skZ3YQwps4vwvp8fnr23H7L3MqdQp0LYKCxSrWXMCQ2P0Jg9237p!-827476922!-1548459817!7001!-1; OPEN_20161214=Y; OPEN_20991230=Y



##################### MANIPULATE LECTURE TIME ############################
#/study/viewStudyFrame.do?CONTENTS_ID=CNT_1612020636171199419d&ACTIVITY_ID=LES_1612020635481199419c
#url = "http://klas.khu.ac.kr/study/viewStudyFrame.do?CONTENTS_ID=CNT_16090114231756884b3a&ACTIVITY_ID=LES_16090114231756884b20"

#url = "http://klas.khu.ac.kr/study/viewStudyFrame.do?CONTENTS_ID=CNT_16090114231756884b3e&ACTIVITY_ID=LES_16090114231756884b2c"
request = urllib2.Request(url)
request.add_header('Cookie',cookie)
response = urllib2.urlopen(request)
read = urllib2.urlopen(request).read()



#print read 





# POST http://klas.khu.ac.kr/dwr/call/plaincall/StudyWork.addRecordWeb.dwr
# Referer: http://klas.khu.ac.kr/study/viewStudyFrame.do?CONTENTS_ID=CNT_1612020636171199419d&ACTIVITY_ID=LES_1612020635481199419c
# Cookie: COURSE_MENU_NAME=%uAC15%uC758%uC2E4; OPEN_2016122017=Y; LMS_JSESSIONID=skZ3YQwps4vwvp8fnr23H7L3MqdQp0LYKCxSrWXMCQ2P0Jg9237p!-827476922!-1548459817!7001!-1; OPEN_20161214=Y; OPEN_20991230=Y
#####################  Login And Get Cookie ############################

index = read.find("studyVO.RECORD_ID")
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e1 = str(read[first_index:second_index])

index = read.find("studyVO.STUDY_RECORD_ID",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e2 = str(read[first_index:second_index])

index = read.find("studyVO.LEARNER_ID ",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e3 = str(read[first_index:second_index])

index = read.find("studyVO.CONTENTS_ID",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e4 = str(read[first_index:second_index])

index = read.find("studyVO.ACTIVITY_ID",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e5 = str(read[first_index:second_index])

index = read.find("studyVO.COURSE_ID",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e6 = str(read[first_index:second_index])

index = read.find("studyVO.START_TIME",index)
first_index = read.find("\"",index)
first_index += 1
second_index = read.find("\"",first_index)
temp_e16 = str(read[first_index:second_index])

temp_user_param1 = str(int(temp_e16)+100)

temp_e9 = raw_input("How Much Do you wanna? Enter in seconds : ")


user_contents_ID=temp_e4#CONTENTS ID                             #DONE
user_activity_ID=temp_e5#ACTIVITY ID                            #DONE
user_session_ID="2630D4F73B71F80F4C9885B25A24A936792"#IDON'TKNOW                                 #NOT YET
user_e1=temp_e1#RECORD_ID                                       #DONE
user_e2=temp_e2#STUDY_RECORD_ID                                #DONE
user_e3=temp_e3#LEARNER_ID                                    #DONE
user_e4=user_contents_ID#CONTENTS_ID                        #DONE
user_e5=user_activity_ID#ACTIVITY_ID                        #DONE
user_e6=temp_e6#COURSE_ID                                    #DONE
user_e7="1"#CONNECT_NUM                                       #DONE
user_e8="0"#STUDY_TIME                                        #DONE
user_e9=temp_e9#TOTAL_STUDY_TIME                                   #DONE
user_e10="0"#STUDY_AFTER_TIME                                 #DONE
user_e11="0"#STUDY_LOCATION                                   #DONE
user_e16=temp_e16#START_TIME                              #DONE
user_param1=temp_user_param1#IDON'T KNOW                  #NOT YET

"""
print user_contents_ID
print user_activity_ID
print user_session_ID
print user_e1
print user_e2
print user_e3
print user_e4
print user_e5
print user_e6
print user_e7
print user_e8
print user_e9
print user_e10
print user_e11
print user_e16
print user_param1
"""
#data = "callCount=1&page=/study/viewStudyFrame.do?CONTENTS_ID=CNT_16090114231756884b3e&ACTIVITY_ID=LES_16090114231756884b2c&httpSessionId=&scriptSessionId=2630D4F73B71F80F4C9885B25A24A936792&c0-scriptName=StudyWork&c0-methodName=addRecordWeb&c0-id=0&c0-e1=string:RCD_161027105208086b0744&c0-e2=string:RCD_160913230350724c018e&c0-e3=string:201620_GEE1287G01_2009104162&c0-e4=string:CNT_16090114231756884b3e&c0-e5=string:LES_16090114231756884b2c&c0-e6=string:2016_20_GEE1287G01&c0-e7=string:19&c0-e8=string:0&c0-e9=string:3607&c0-e10=string:272&c0-e11=string:0&c0-e12=string:completed&c0-e13=string:0.0&c0-e14=string:50&c0-e15=string:N&c0-e16=string:1482011541&c0-param0=Object_Object:{RECORD_ID:reference:c0-e1, STUDY_RECORD_ID:reference:c0-e2, LEARNER_ID:reference:c0-e3, CONTENTS_ID:reference:c0-e4, ACTIVITY_ID:reference:c0-e5, COURSE_ID:reference:c0-e6, CONNECT_NUM:reference:c0-e7, STUDY_TIME:reference:c0-e8, TOTAL_STUDY_TIME:reference:c0-e9, STUDY_AFTER_TIME:reference:c0-e10, STUDY_LOCATION:reference:c0-e11, STUDY_STATE:reference:c0-e12, STUDY_SCORE:reference:c0-e13, LESSON_TIME:reference:c0-e14, ON_STUDY_YN:reference:c0-e15, START_TIME:reference:c0-e16}&c0-param1=number:1328045125299&c0-param2=string:end&c0-param3=boolean:false&batchId=0"
data = "callCount=1&page=/study/viewStudyFrame.do?CONTENTS_ID="+user_contents_ID+"&ACTIVITY_ID="+user_activity_ID+"&httpSessionId=&scriptSessionId=" + user_session_ID + "&c0-scriptName=StudyWork&c0-methodName=addRecordWeb&c0-id=0&c0-e1=string:" + user_e1 + "&c0-e2=string:" + user_e2  + "&c0-e3=string:" + user_e3 + "&c0-e4=string:" + user_e4 + "&c0-e5=string:" + user_e5 + "&c0-e6=string:" + user_e6 + "&c0-e7=string:" + user_e7 + "&c0-e8=string:" + user_e8 + "&c0-e9=string:" + user_e9 + "&c0-e10=string:" + user_e10 + "&c0-e11=string:" + user_e11 + "&c0-e12=string:completed&c0-e13=string:0.0&c0-e14=string:50&c0-e15=string:N&c0-e16=string:" + user_e16 + "&c0-param0=Object_Object:{RECORD_ID:reference:c0-e1, STUDY_RECORD_ID:reference:c0-e2, LEARNER_ID:reference:c0-e3, CONTENTS_ID:reference:c0-e4, ACTIVITY_ID:reference:c0-e5, COURSE_ID:reference:c0-e6, CONNECT_NUM:reference:c0-e7, STUDY_TIME:reference:c0-e8, TOTAL_STUDY_TIME:reference:c0-e9, STUDY_AFTER_TIME:reference:c0-e10, STUDY_LOCATION:reference:c0-e11, STUDY_STATE:reference:c0-e12, STUDY_SCORE:reference:c0-e13, LESSON_TIME:reference:c0-e14, ON_STUDY_YN:reference:c0-e15, START_TIME:reference:c0-e16}&c0-param1=number:" + user_param1 + "&c0-param2=string:end&c0-param3=boolean:false&batchId=0"
#print data
#url = "http://klas.khu.ac.kr/dwr/call/plaincall/StudyWork.addRecordWeb.dwr"
url = "http://klas.khu.ac.kr/dwr/call/plaincall/StudyWork.addRecordWeb.dwr?" + str(data) 
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)
cookie = response.headers.get('Set-Cookie')
html = response.read()

"""
#request = urllib2.Request(url)
#response = urllib2.urlopen(request)
#cookie = response.headers.get('Set-Cookie')

#print cookie

url = "http://klas.khu.ac.kr/dwr/call/plaincall/StudyWork.addRecordWeb.dwr"

T_callCount = "1"
T_page = "/study/viewStudyFrame.do?CONTENTS_ID=CNT_16090114231756884b3e&ACTIVITY_ID=LES_16090114231756884b2c"
T_httpSessionId =""
T_scriptSessionId = "2630D4F73B71F80F4C9885B25A24A936707"
scriptName = "StudyWork"
methodName = "addRecordWeb"
#c0 param0
T_id = "0"
e1 = "string:RCD_161027105208086b0744"
e2 = "string:RCD_160913230350724c018e"
e3 = "string:201620_GEE1287G01_2009104162"
e4 = "string:CNT_16090114231756884b3e"
e5 = "string:LES_16090114231756884b2c"
e6 = "string:2016_20_GEE1287G01"
e7 = "string:15"
e8 = "string:0"
e9 = "string:3700"
e10 = "string:91"
e11 = "string:0"
e12 = "string:completed"
e13 = "string:0.0"
e14 = "string:50"
e15 = "string:N"
e16 = "string:1482004311"
param0 = "Object_Object:{RECORD_ID:reference:c0-e1, STUDY_RECORD_ID:reference:c0-e2, LEARNER_ID:reference:c0-e3, CONTENTS_ID:reference:c0-e4, ACTIVITY_ID:reference:c0-e5, COURSE_ID:reference:c0-e6, CONNECT_NUM:reference:c0-e7, STUDY_TIME:reference:c0-e8, TOTAL_STUDY_TIME:reference:c0-e9, STUDY_AFTER_TIME:reference:c0-e10, STUDY_LOCATION:reference:c0-e11, STUDY_STATE:reference:c0-e12, STUDY_SCORE:reference:c0-e13, LESSON_TIME:reference:c0-e14, ON_STUDY_YN:reference:c0-e15, START_TIME:reference:c0-e16}"

#c0 param
param1 = "number:754887436879"
param2 = "string:end"
param3 = "boolean:false"
T_batchId = "0"

lecture_form = {'c0-param0' : param0,
                'callCount': T_callCount ,
                'page' : T_page,
                'httpSessionId' : T_httpSessionId,
                'scriptSessionId' : T_scriptSessionId,
                'c0-scriptName' : scriptName,
                'c0-methodName' : methodName,
                'c0-id' : T_id,
                'c0-e1' : e1,
                'c0-e2' : e2,
                'c0-e3' : e3,
                'c0-e4' : e4,
                'c0-e5' : e5,
                'c0-e6' : e6,
                'c0-e7' : e7,
                'c0-e8' : e8,
                'c0-e9' : e9,
                'c0-e10' : e10,
                'c0-e11' : e11,
                'c0-e12' : e12,
                'c0-e13' : e13,
                'c0-e14' : e14,
                'c0-e15' : e15,
                'c0-e16' : e16,
                'c0-param1' : param1,
                'c0-param2' : param2,
                'batchId' : T_batchId}
                
                


"""
