class DataFilter():

    #用来从序列化的字典中的
    @classmethod
    def filter(self,dic,*args):
        data = []
        for elem in dic:
            temp = dict()
            for index in args:
                temp[index] = elem[index]
            data.append(temp)
        return data