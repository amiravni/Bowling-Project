import urllib
import urllib2
import json
import os

RESOURCES_PATH = "./resources/"
USER_PROFILE_PATH = RESOURCES_PATH  + "users/profile/"
USER_PROFILE_PICTURE_PATH = RESOURCES_PATH  + "users/profile_pic/"
DEBUG = True

def print_debug(str):
    if DEBUG:
        print str

#Notes
#1. if no user with that username use the username as a name
def get_user_data(username):
    try:
        if not os.path.exists(USER_PROFILE_PATH + username):
            print_debug("saving profile of : %s" % username)
            user_data_json = urllib2.urlopen("http://graph.facebook.com/%s" % username).read()
            user_profile_fd = open(USER_PROFILE_PATH + username,'w')
            print >> user_profile_fd, user_data_json
        else:
            user_data_json =  open(USER_PROFILE_PATH + username,'r').read()
    except:
        print 'Error fetching user data'
        return {'username':username,'name':username}

    user_data_dic = json.loads(user_data_json)    
    return user_data_dic

#TODO
#1. if no user use some anonymous picture
def get_user_picture_path(username):
    try:
        profile_pic_path = USER_PROFILE_PICTURE_PATH + username+".jpg"
        if not os.path.exists(profile_pic_path):
            print_debug("downloading profile photo : %s" % username)
            urllib.urlretrieve("http://graph.facebook.com/%s/picture?type=large" % username, profile_pic_path)
        return profile_pic_path
    except:
        print 'Error fetching user profile photo'
        return USER_PROFILE_PICTURE_PATH + 'anonymous.png'

def get_user_count():
    return len(os.listdir(USER_PROFILE_PATH))
