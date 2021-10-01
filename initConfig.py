import os
import codecs
class initConfig:

    def __init__(self):
        self.address='config.py'
        self.data=''


    def write_data(self,data):
        file=codecs.open(self.address,"w",encoding='utf8')
        file.write(data)
        file.close()

    def get_data(self):
        if os.path.isfile(self.address):
            file=codecs.open(self.address,"r",encoding='utf8')
            data=file.read()
            file.close()
            return  data

    def get_update_config(self,key):
        if os.path.isfile(self.address):
            try:
                file=codecs.open(self.address,"r",encoding='utf8')
                data=file.read()
                file.close()
                az=data.find(key+'=')
                ta=data.find('\n',az)
                tmp=data[az:ta]
                if tmp.find('"')> -1:
                    return tmp.split('"')[1]
                else:
                    return tmp.split('=')[1]
            except:
                print("error in read file beacause is look for write")

    def set_new_val_data(self,key,value):
        data=self.get_data()
        tmp=key+'='
        az=data.find(tmp)
        ta=data.find('\n',az)
        old=data[az:ta]
        if str(value).isalnum():
            new_data=key+'='+str(value)
        elif str(value).isalpha():
            new_data=key+'="'+value+'"'
        else:
            new_data=key+'="'+value+'"'
        data=data.replace(old,new_data)
        self.write_data(data)

if __name__=="__main__":
    config=initConfig()
    config.check_config_ex()