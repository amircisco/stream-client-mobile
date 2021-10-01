center_ip="192.168.2.3"
sender_ip="192.168.2.3"
camera_name_1="1::@@::1::@@::1"
camera_name_2="2::@@::2::@@::2"
camera_name_3="3::@@::3::@@::3"
camera_name_4="4::@@::4::@@::4"
show_camera="0"
key="100"



br=""


def_width=480
def_height=320
motion_sound="Assets/sound/motion-sound.mp3"
area_sound="Assets/sound/area-detection-sound.mp3"
start_spl="@#q49#32###AvnB@@@#"
end_spl="@Rt56##@anm@#@lP"

show_img_fps=30
communicate_spliter="!@#$%^&*"
port_rec_video_frame=52110
port_rec_detect_frame=52120
port_communicate=52220
socket_port_handle_ip=5050
port_cam1=":8181"
port_cam2=":8282"
port_cam3=":8383"
port_cam4=":8484"
port_cam_all=":8585"
addr_base="http://"+sender_ip
address1=addr_base+port_cam1
address2=addr_base+port_cam2
address3=addr_base+port_cam3
address4=addr_base+port_cam4

font_farsi="Assets/Fonts/BTitrBd.ttf"

chunk_size=1024*10
url_video_all='http://'+sender_ip+port_cam_all+'/video'

url_video_auth='http://'+sender_ip+port_cam_all+'/auth'
url_video_get_video='http://'+sender_ip+port_cam_all+'/get_video'

url_video1='http://'+sender_ip+port_cam1+'/video_1'
url_video2='http://'+sender_ip+port_cam2+'/video_2'
url_video3='http://'+sender_ip+port_cam3+'/video_3'
url_video4='http://'+sender_ip+port_cam4+'/video_4'

tak_frame_size=(800,600)

state_icon_red="Assets/icons/state_red.png"
state_icon_green="Assets/icons/state_green.png"
state_icon_yellow="Assets/icons/state_yellow.png"
state_icon_silver="Assets/icons/state_silver.png"

first_video_tizer="Assets/video/1.mp4"
img_none="Assets/icons/none.jpg"

video_alt="Assets/icons/video_alt.jpg"