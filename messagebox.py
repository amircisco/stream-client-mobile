from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MessageBox():
    def __init__(self,title,msg,instance):
        self.title=title
        self.msg=msg
        self.instance=instance
    def show_message_box(self):
        layout=BoxLayout(padding=10,orientation="vertical")
        self.text=self.instance.init_persian_text(self.msg)
        self.popupLabel= Label(text=self.text,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.7))
        layout.add_widget(self.popupLabel)
        text_btn=self.instance.init_persian_text("بستن")
        self.btn=Button(text=text_btn,font_size=20,font_name="Assets/Fonts/BKoodakBold.ttf",size_hint=(1,.3))
        self.btn.on_press=self.click_enseraf
        layout.add_widget(self.btn)
        self.title=self.instance.init_persian_text(self.title)
        self.popup = Popup(title=self.title,content=layout,size_hint=(.7,.3),auto_dismiss = False)
        self.popup.title_font="Assets/Fonts/BKoodakBold.ttf"
        self.popup.title_size=20
        self.popup.title_align="right"
        self.popup.open()
    def click_enseraf(self):
        self.close()

    def close(self):
        try:
            self.popup.dismiss()
        except:
            print("pop up dont run")


