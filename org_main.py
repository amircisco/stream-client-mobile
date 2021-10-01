from kivy.app import App
import time
from kivy.uix.image import Image
from kivy.core.window import Window
import cv2
from kivy.graphics.texture import Texture
import threading
from popup import PopUp

import config
import base64
import numpy as np

import os
from queue import Queue
from Encoding import encrypt_cisco
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.clock import Clock


from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import arabic_reshaper
import bidi.algorithm

import socket
from messagebox import MessageBox

import translate
from initConfig import initConfig
import traceback



class VideoPlayerNoCrl(Image):
    def __init__(self, **kwargs):
        super(VideoPlayerNoCrl, self).__init__(**kwargs)
        self.start()
    def pr1(self):
        Clock.schedule_interval(self.update,1.0/30)

    def start(self):
        self.capture=cv2.VideoCapture("Assets/video/1.mp4")
        th1=threading.Thread(target=self.pr1)
        th1.daemon=True
        th1.start()

    def update(self,dt):
        ret,frame=self.capture.read()
        if ret:
            frame=cv2.resize(frame,(self.width,self.height))
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()
        else:
            time.sleep(2)
            Clock.unschedule(self.update)
            self.source="none.jpg"
            Window.maximize()
            MainKivyApp.my_screenmanager.current="KivyShowVideoFrames"

class DataViewItem():

    def get_layout(self,crp_img,org_img,date_time,camera_number,camera_name):
        self.layout=BoxLayout()
        self.layout.orientation="vertical"
        self.layout.size_hint_x=1
        self.layout.spacing=7
        self.layout.padding=14

        self.cam_name=Label()
        self.cam_name.size_hint_x=1
        self.cam_name.size_hint_y=0.15
        self.cam_name.text=MainKivyApp.app.init_persian_text(camera_name)
        self.cam_name.font_name="Assets/Fonts/BKoodakBold.ttf"
        self.cam_name.font_size=18
        self.layout.add_widget(self.cam_name)

        self.img=Image()
        self.img.size_hint_x=1
        self.img.size_hint_y=0.7
        self.img.source=crp_img
        self.layout.add_widget(self.img)

        self.date_time=Label()
        self.date_time.size_hint_x=1
        self.date_time.size_hint_y=0.15
        self.date_time.text=date_time
        self.layout.add_widget(self.date_time)

        self.btn=Button(on_press=lambda *args: self.clicked_btn(self.btn))
        self.btn.font_name="Assets/Fonts/BKoodakBold.ttf"
        self.btn.size_hint_x=1
        self.btn.size_hint_y=0.20
        self.btn.id=org_img
        self.btn.text=MainKivyApp.app.init_persian_text("مشاهده تصویر اصلی")
        self.layout.add_widget(self.btn)

        return self.layout

    def clicked_btn(self,instance):
        org_img=instance.id
        frame=cv2.imread(org_img)
        frame=cv2.resize(frame,(640,480))
        name=os.path.dirname(__file__)+"/"+org_img
        cv2.imshow(name,frame)

class IconButtonZoom(ButtonBehavior, Image):

    def __init__(self, angle=0, **kwargs):
        super(IconButtonZoom, self).__init__(**kwargs)

    def on_press(self):
        print("from on_press Zoom")

class IconButtonArrow(ButtonBehavior, Image):

    def __init__(self, angle=0, **kwargs):
        super(IconButtonArrow, self).__init__(**kwargs)

    def on_press(self):
        print("from on_press Arrow")

class IconButtonFullScreen(ButtonBehavior, Image):
    def __init__(self, angle=0, **kwargs):
        super(IconButtonFullScreen, self).__init__(**kwargs)

    def on_press(self):
        try:
            if self.id_id.startswith("full_screen"):
                if self.id_id=="full_screen1":
                    ret=1
                    MainKivyApp.my_screenmanager.ids.qrcam.handle_full_screen_frame(ret)
                elif self.id_id=="full_screen2":
                    ret=2
                    MainKivyApp.my_screenmanager.ids.qrcam.handle_full_screen_frame(ret)
                elif self.id_id=="full_screen3":
                    ret=3
                    MainKivyApp.my_screenmanager.ids.qrcam.handle_full_screen_frame(ret)
                elif self.id_id=="full_screen4":
                    ret=4
                    MainKivyApp.my_screenmanager.ids.qrcam.handle_full_screen_frame(ret)
        except:
            pass


class KivyCamera(Image):
    def init_data(self,url):
        try:
            key=config.key
            self.encoding=encrypt_cisco(key)
            self.url=url
            self.q_show=Queue()
            self.th_start=True
            self.wait=0.020
            self.i=0
            HOST = config.sender_ip
            PORT = config.port_rec_video_frame
            self.ip_port=(HOST,PORT)
            self.buf_size=1024*60
            self.w=config.def_width
            self.h=config.def_height
            none_frame=cv2.imread(config.img_none)
            self.none_frame=cv2.resize(none_frame,(config.def_width,config.def_height))
            self.stop_tcp=False
            self.stop_rec_data=False
            self.show_tak_frame=0
        except:
            traceback.print_exc()
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)

    def pr1(self):
        Clock.schedule_interval(self.show_images,0.009)

    def pr2(self):
        self.run()

    def start(self):
        th1=threading.Thread(target=self.pr1)
        th1.daemon=True
        th2=threading.Thread(target=self.pr2)
        th2.daemon=True
        th1.start()
        th2.start()
        return self

    def stop(self):
        try:
            title='ارتباط با فرستنده قطع شد'
            print("stop connection...")
            self.stop_rec_data=True
            self.stop_tcp=True
            self.socket.close()
            Clock.unschedule(self.show_images)
            messagebox=MessageBox('توجه',title,MainKivyApp.app)
            messagebox.show_message_box()
        except:
            print("error inside stop def")
            traceback.print_exc()

    def communicate(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip=MainKivyApp.conf.get_update_config('center_ip')
        port=config.port_communicate
        address=(ip,port)
        s.connect(address)
        data="user!@#$%^&*get_sender_ip"
        data=data.encode('utf-8')
        data=self.encoding.encrypt(data)
        s.sendall(data)
        do=True
        while do==True:
            recive=s.recv(1024)
            recive=self.encoding.decrypt(recive)
            recive=recive.decode('utf-8')
            if recive.find(config.communicate_spliter)>-1:
                arr=recive.split(config.communicate_spliter)
                if arr[0]=="ok":
                    ip=arr[1]
                    data=MainKivyApp.conf.get_data()
                    old='sender_ip="'+MainKivyApp.conf.get_update_config('sender_ip')+'"'
                    new_data='sender_ip="'+ip+'"'
                    data=data.replace(old,new_data)
                    MainKivyApp.conf.write_data(data)
                    do=False
                    ret=True
                elif arr[0]=="not":
                    if arr[1]=="no_your_ip_in_server":
                        msg=MessageBox(translate.mytr.get('warning'),translate.mytr.get(''),MainKivyApp.app)
                        msg.show_message_box()
                    ret=False
                    do=False
        return ret
    def init_and_connect_socket(self):
        ret=False
        if self.communicate()==True:
            data="abcdef".encode(encoding='utf-8')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.ip_port)
            self.socket.sendall(data)
            while True:
                data = self.socket.recv(1024)
                data=data.decode()
                if(data=="rtxz" or data=="bqyu"):
                    ret=True
                    break
            self.socket.close()
        return ret

    def run(self):
        title=MainKivyApp.app.init_persian_text("برقراری ارتباط با فرستنده")
        self.popup=PopUp(title,"pleas wait...",MainKivyApp.app)
        self.popup.show_popup_loading()
        self.flg_popup=True
        if(self.init_and_connect_socket()==True):
            timer=3
            print('connect after {} secondes'.format(timer))
            while timer>0:
                print(timer)
                time.sleep(1)
                timer-=1
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.ip_port)
            self.socket.sendall(str("zxcvbn+"+config.show_camera).encode())
            tmp=""
            start=config.start_spl
            end=config.end_spl
            frm_num=0
            while self.stop_rec_data==False:
                try:
                    data=self.socket.recv(self.buf_size)
                    rec=data.decode('utf-8')
                    tmp+=rec
                    if tmp.find(end) > -1:
                        frm_num+=1
                        spl=tmp.split(end)
                        source=spl[0].split(start)[1]
                        tmp=spl[1]
                        enc_frm=base64.b64decode(source)
                        frame=self.encoding.decrypt(enc_frm)
                        #nparr=np.frombuffer(frame,np.uint8)
                        nparr=np.fromstring(frame, dtype='int8')
                        frame=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
                        self.q_show.put(frame)
                except:
                    continue

        else:
            self.popup.close()

    def handle_full_screen_frame(self, ret):
        if self.show_tak_frame==0:
            self.show_tak_frame=ret
            self.hide_visible_frames()
        elif self.show_tak_frame>0:
            self.check_visible_frames()
            self.show_tak_frame=0

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.show_tak_frame>0:
                self.handle_full_screen_frame(None)


    def show_motion_detection(self):
        pass

    def show_normal(self,frame):
        if self.show_tak_frame==0:
            if MainKivyApp.conf.get_update_config('show_camera')=="1":
                tm0=frame
                tm1=np.concatenate((self.none_frame,self.none_frame),axis=1)
                frame=np.concatenate((tm0,tm1),axis=0)
            if MainKivyApp.conf.get_update_config('show_camera')=="2":
                tm0=np.concatenate((self.none_frame,self.none_frame),axis=1)
                tm1=frame
                frame=np.concatenate((tm0,tm1),axis=0)
            frame=cv2.resize(frame,(int(self.width),int(self.height)))


        elif self.show_tak_frame>0:
            self.hide_visible_frames()
            if self.show_tak_frame==1:
                a="a"
            elif self.show_tak_frame==2:
                a="b"
            elif self.show_tak_frame==3:
                a="c"
            elif self.show_tak_frame==4:
                a="d"
            az_x,ta_x,az_y,ta_y=self.crop_img_for_sections(a)
            frame=frame[az_y:ta_y,az_x:ta_x]
            frame=cv2.resize(frame,config.tak_frame_size)

        if len(frame):
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

    def show_images(self,dt):
        if(self.q_show.qsize()>0):

            if(self.flg_popup):
                self.flg_popup=False
                self.popup.close()
                self.check_visible_frames()
            frame=self.q_show.get()

            self.show_normal(frame)



    def crop_img_for_sections(self,t):
        ret=""
        if t == "a":
            az_x=0
            ta_x=int(config.def_width)
            az_y=0
            ta_y=int(config.def_height)
            ret= az_x,ta_x,az_y,ta_y
        elif t== "b":
            az_x=int(config.def_width)
            ta_x=int(config.def_width*2)
            az_y=0
            ta_y=int(config.def_height)
            ret= az_x,ta_x,az_y,ta_y
        elif t== "c":
            az_x=0
            ta_x=int(config.def_width)
            az_y=int(config.def_height)
            ta_y=int(config.def_height*2)
            ret= az_x,ta_x,az_y,ta_y
        elif t== "d":
            az_x=int(config.def_width)
            ta_x=int(config.def_width*2)
            az_y=int(config.def_height)
            ta_y=int(config.def_height*2)
            ret= az_x,ta_x,az_y,ta_y

        return ret

    def hide_visible_frames(self):
        MainKivyApp.my_screenmanager.ids.grid_box_1.opacity=0
        MainKivyApp.my_screenmanager.ids.grid_box_2.opacity=0
        MainKivyApp.my_screenmanager.ids.grid_box_3.opacity=0
        MainKivyApp.my_screenmanager.ids.grid_box_4.opacity=0

    def check_visible_frames(self):
        if MainKivyApp.conf.get_update_config('show_camera')=="1":
            MainKivyApp.my_screenmanager.ids.grid_box_1.opacity=1
            MainKivyApp.my_screenmanager.ids.grid_box_2.opacity=1

        elif MainKivyApp.conf.get_update_config("show_camera")=="2":
            MainKivyApp.my_screenmanager.ids.grid_box_3.opacity=1
            MainKivyApp.my_screenmanager.ids.grid_box_4.opacity=1

        elif MainKivyApp.conf.get_update_config("show_camera")=="0":
            MainKivyApp.my_screenmanager.ids.grid_box_1.opacity=1
            MainKivyApp.my_screenmanager.ids.grid_box_2.opacity=1
            MainKivyApp.my_screenmanager.ids.grid_box_3.opacity=1
            MainKivyApp.my_screenmanager.ids.grid_box_4.opacity=1

    def get_click(self):
        print("ssss")

# all screens sort ......

class Tizer(Screen):
    pass

class CustomSetting(Screen):
    def on_enter(self, *args):
        self.init_lbl_text()
        self.fill_data()
        self.old_camera1=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_1').split('::@@::')[1])
        self.old_camera2=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_2').split('::@@::')[1])
        self.old_camera3=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_3').split('::@@::')[1])
        self.old_camera4=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_4').split('::@@::')[1])

    def init_lbl_text(self):
        MainKivyApp.my_screenmanager.ids.btn_save_lsetting.text=MainKivyApp.app.init_persian_text('ذخیره')
        MainKivyApp.my_screenmanager.ids.btn_exit_lsetting.text=MainKivyApp.app.init_persian_text('بازگشت')
        MainKivyApp.my_screenmanager.ids.lbl_center_ip.text=MainKivyApp.app.init_persian_text('آیپی مرکز کنترل')
        MainKivyApp.my_screenmanager.ids.lbl_enbale_3g.text=MainKivyApp.app.init_persian_text('فعال کردن حالت 3 جی')
        MainKivyApp.my_screenmanager.ids.lbl_show_camera.text=MainKivyApp.app.init_persian_text('کدام دوربین ها در حالت 3 جی نمایش داده شوند')
        MainKivyApp.my_screenmanager.ids.lbl_ch_box_show_camera1.text=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_1').split('::@@::')[1]+' - '+MainKivyApp.conf.get_update_config('camera_name_2').split('::@@::')[1])
        MainKivyApp.my_screenmanager.ids.lbl_ch_box_show_camera2.text=MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_3').split('::@@::')[1]+' - '+MainKivyApp.conf.get_update_config('camera_name_4').split('::@@::')[1])

    def fill_data(self):
        if len(MainKivyApp.conf.get_update_config('center_ip'))>1:
            MainKivyApp.my_screenmanager.ids.txt_center_ip.text=MainKivyApp.conf.get_update_config('center_ip')
        if MainKivyApp.conf.get_update_config('show_camera')=="0":
            MainKivyApp.my_screenmanager.ids.txt_enbale_3g.active=False
            MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera1.active=False
            MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera2.active=False
        else:
            MainKivyApp.my_screenmanager.ids.txt_enbale_3g.active=True
            if MainKivyApp.conf.get_update_config('show_camera')=="1":
                MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera1.active=True
            elif MainKivyApp.conf.get_update_config('show_camera')=="2":
                MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera2.active=True

        MainKivyApp.my_screenmanager.ids.txt_key.text=MainKivyApp.conf.get_update_config('key')

    def clicked_btn_save(self):
        if MainKivyApp.my_screenmanager.ids.txt_enbale_3g.active==True and MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera1.active==False and MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera2.active==False:
            msg=MessageBox('ذخیره نشد','وقتی حالت 3 جی فعال است باید مشخص شود کدام دوربین ها نمایش داده شوند',MainKivyApp.app)
            msg.show_message_box()
        else:
            data=MainKivyApp.conf.get_data()
            last=data.split('br=""')[1]
            change_data=""
            txt_center_ip=MainKivyApp.my_screenmanager.ids.txt_center_ip.text
            if len(txt_center_ip)>1:
                change_data+='center_ip="'+txt_center_ip+'"'
                change_data+='\n'
            txt_sender_ip=MainKivyApp.conf.get_update_config('sender_ip')
            change_data+='sender_ip="'+txt_sender_ip+'"'
            change_data+='\n'
            txt_camera_name_1=MainKivyApp.conf.get_update_config('camera_name_1')
            change_data+='camera_name_1="1::@@::'+txt_camera_name_1+'"'
            change_data+='\n'
            txt_camera_name_2=MainKivyApp.conf.get_update_config('camera_name_2')
            change_data+='camera_name_2="2::@@::'+txt_camera_name_2+'"'
            change_data+='\n'
            txt_camera_name_3=MainKivyApp.conf.get_update_config('camera_name_3')
            change_data+='camera_name_3="3::@@::'+txt_camera_name_3+'"'
            change_data+='\n'
            txt_camera_name_4=MainKivyApp.conf.get_update_config('camera_name_4')
            change_data+='camera_name_4="4::@@::'+txt_camera_name_4+'"'
            change_data+='\n'
            if MainKivyApp.my_screenmanager.ids.txt_enbale_3g.active==False:
                change_data+='show_camera="0"'
                change_data+='\n'
            elif MainKivyApp.my_screenmanager.ids.txt_enbale_3g.active==True:
                if MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera1.active==True:
                    change_data+='show_camera="1"'
                    change_data+='\n'
                elif MainKivyApp.my_screenmanager.ids.txt_ch_box_show_camera2.active==True:
                    change_data+='show_camera="2"'
                    change_data+='\n'
            change_data+='key="'+MainKivyApp.my_screenmanager.ids.txt_key.text+'"'
            change_data+='\n'

            data=change_data+'\n\n\n'+'br=""'+last
            MainKivyApp.conf.write_data(data)
            msg=MessageBox('انجام شد','ذخیره تنظیمات با موفقیت انجام شد',MainKivyApp.app)
            msg.show_message_box()
            MainKivyApp.app.change_screen_for_refresh("KivyShowVideoFrames","customsetting")
    def clicked_btn_exit(self):
        MainKivyApp.my_screenmanager.current="KivyShowVideoFrames"



class KivyShowVideoFrames(Screen):

    def clicked_setting(self):
        MainKivyApp.my_screenmanager.current="customsetting"

    def clicked_dissconnect(self):
        MainKivyApp.my_screenmanager.ids.qrcam.stop()

    def clicked_connect(self):
        MainKivyApp.my_screenmanager.ids.qrcam.init_data(config.url_video_all)
        MainKivyApp.my_screenmanager.ids.qrcam.start()

    def on_enter(self, *args):
        MainKivyApp.my_screenmanager.ids.cam1_name1.text= MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_1').split('::@@::')[1])
        MainKivyApp.my_screenmanager.ids.cam2_name2.text= MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_2').split('::@@::')[1])
        MainKivyApp.my_screenmanager.ids.cam3_name3.text= MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_3').split('::@@::')[1])
        MainKivyApp.my_screenmanager.ids.cam4_name4.text= MainKivyApp.app.init_persian_text(MainKivyApp.conf.get_update_config('camera_name_4').split('::@@::')[1])

        MainKivyApp.my_screenmanager.ids.menu_btn_connect.text= MainKivyApp.app.init_persian_text("اتصال")
        MainKivyApp.my_screenmanager.ids.menu_btn_disconnect.text= MainKivyApp.app.init_persian_text("قطع اتصال")
        MainKivyApp.my_screenmanager.ids.menu_btn_setting.text= MainKivyApp.app.init_persian_text("تنظیمات")



class WindowManager(ScreenManager):
    def __init__(self):
        super(WindowManager, self).__init__()
        #self.add_widget(Tizer(name='Tizer'))
        #self.add_widget(KivyShowVideoFrames(name='KivyShowVideoFrames'))

# end all screens sort .........

class MainKivyApp(App):
    my_screenmanager=None
    app=None
    conf=initConfig()
    def build(self):
        MainKivyApp.app=self
        self.icon="Assets/icons/logo.jpg"
        MainKivyApp.my_screenmanager=WindowManager()
        return MainKivyApp.my_screenmanager

    def init_persian_text(self,text):
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = bidi.algorithm.get_display(reshaped_text)
        return bidi_text

    def convert_code_string(self,key):
        return self.init_persian_text(translate.mytr.get(key))

    def change_screen_for_refresh(self,first,second):
        MainKivyApp.my_screenmanager.current=first
        MainKivyApp.my_screenmanager.current=second

    def check_persian_char(self,body):
        ret=""
        for x in body:
            if 0>ord(x) > 500 :
                ret="en"
                break
            elif 1500>ord(x)>2000:
                ret="fa"
                break
            elif 60000>ord(x)<70000:
                ret="fa_k"
                break

        return ret

if __name__=="__main__":
    main=MainKivyApp()
    main.run()

