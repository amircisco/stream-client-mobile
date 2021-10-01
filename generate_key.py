import random


class GenerateKey():

    def __init__(self):
        self.data={}
        self.arr_adad=['0','1','2','3','4','5','6','7','8','9']
        self.arr_horof_k=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','w','x','y','z']
        self.arr_horof_b=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','W','X','Y','Z']
        self.arr_char=['!','@','#','$','%','^','&','*','+']
    def get_random(self):
        list_random=list()
        index1=random.randrange(0,len(self.arr_adad)-1)
        list_random.append(self.arr_adad[index1])
        index2=random.randrange(0,len(self.arr_adad)-1)
        list_random.append(self.arr_adad[index2])

        index1=random.randrange(0,len(self.arr_horof_k)-1)
        list_random.append(self.arr_horof_k[index1])
        index2=random.randrange(0,len(self.arr_horof_k)-1)
        list_random.append(self.arr_horof_k[index2])

        index1=random.randrange(0,len(self.arr_horof_b)-1)
        list_random.append(self.arr_horof_b[index1])
        index2=random.randrange(0,len(self.arr_horof_b)-1)
        list_random.append(self.arr_horof_b[index2])

        index1=random.randrange(0,len(self.arr_char)-1)
        list_random.append(self.arr_char[index1])
        index2=random.randrange(0,len(self.arr_char)-1)
        list_random.append(self.arr_char[index2])

        list_adad=[0,1,2,3,4,5,6,7]
        list_tartip=list()
        while len(list_adad)>0:
            index=random.randrange(0,8)
            if index in list_adad and not index in list_tartip:
                list_tartip.append(index)
                list_adad.remove(index)

        str_data=""
        for item in list_tartip:
            value=list_random[item]
            str_data+=str(value)

        return str_data

    def get_key(self):
        key=""
        for i in range(0,8):
            key+=self.get_random()

        return key

    def start(self,count):
        for i in range(0,count):
            self.data[i]=self.get_key()

        with open('database.db','w') as file:
            file.write(str(self.data))
            file.close()


    def read_database(self):
        with open('database.db','r') as file:
            data=file.read()
            file.close()
            self.arr=eval(data)

    def get_uniq_key(self,key):
        self.read_database()
        return self.arr.get(key)

if __name__=="__main__":
    gen=GenerateKey()
    #gen.start(100001)
    arr=gen.read_database()