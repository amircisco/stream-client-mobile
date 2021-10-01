from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class PopUp():
    def __init__(self,title,content,instance):
        self.title=instance.init_persian_text(title)
        self.content=content
        self.instance=instance
    def show_popup(self):
        layout=BoxLayout(padding=10,orientation="vertical")
        self.text_loading=self.instance.init_persian_text(self.content)
        self.popupLabel= Label(self.text_loading,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.7))
        layout.add_widget(self.popupLabel)
        self.popup = Popup(title=self.title,content=layout,size=(300,200),auto_dismiss = False,size_hint= (None, None))
        self.popup.title_font="Assets/Fonts/BKoodakBold.ttf"
        self.popup.title_size=20
        self.popup.title_align="right"
        self.popup.open()

    def show_popup_loading_dynamic(self):
        layout=BoxLayout(padding=10,orientation="vertical")
        self.text_loading=self.instance.init_persian_text(self.content)
        self.popupLabel= Label(text="...."+self.text_loading,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.7))
        layout.add_widget(self.popupLabel)
        text_btn=self.instance.init_persian_text("انصراف")
        self.btn=Button(text=text_btn,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.3))
        self.btn.on_press=self.click_enseraf
        layout.add_widget(self.btn)
        self.popup = Popup(title=self.title,content=layout,size=(300,200),auto_dismiss = False,size_hint= (None, None))
        self.popup.title_font="Assets/Fonts/BKoodakBold.ttf"
        self.popup.title_size=20
        self.popup.title_align="right"
        self.popup.open()
        Clock.schedule_interval(self.update_loading,0.5)
        self.i=0

    def show_popup_loading(self):
        layout=BoxLayout(padding=10,orientation="vertical")
        self.text_loading=self.instance.init_persian_text("در حال اتصال")
        self.popupLabel= Label(text="...."+self.text_loading,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.7))
        layout.add_widget(self.popupLabel)
        text_btn=self.instance.init_persian_text("انصراف")
        self.btn=Button(text=text_btn,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.3))
        self.btn.on_press=self.click_enseraf
        layout.add_widget(self.btn)
        self.popup = Popup(title=self.title,content=layout,size=(300,200),auto_dismiss = False,size_hint= (None, None))
        self.popup.title_font="Assets/Fonts/BKoodakBold.ttf"
        self.popup.title_size=20
        self.popup.title_align="right"
        self.popup.open()
        Clock.schedule_interval(self.update_loading,0.5)
        self.i=0

    def update_loading(self,dt):
        self.i+=1
        if(self.i==1):
            text="."+self.text_loading
        elif(self.i==2):
            text=".."+self.text_loading
        elif(self.i==3):
            text="..."+self.text_loading
        elif(self.i==4):
            text="...."+self.text_loading
            self.i=0
        self.popupLabel.text=text

    def click_enseraf(self):
        self.close()


    def close(self):
        try:
            self.popup.dismiss()
        except:
            print("pop up dont run")


