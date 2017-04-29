from homemonitoring.server.hms import HMS

class Recipients(object):
    url = "api/base/notification"
    cache = []
    
    def __get__(self, obj, objtype):
        response = HMS().request(self.url).get()
        #print response
        return response

    def __set__(self, obj, val):
        assert isinstance(val, str), "Should be a string"
        data = {'add': val}
        response = HMS().request(self.url).post(data)
        #print response
        self.cache.append(val)
        return response

    def __delete__(self, obj):
        for x in self.cache:
            data = {'delete': x}
            response = HMS().request(self.url).post(data)
            #print response
        del self.cache[:]
        
class Phone(Recipients):
    url = "{0}/{1}".format(Recipients.url, "phone")
    
class Email(Recipients):
    url = "{0}/{1}".format(Recipients.url, "email")

class Sms(Recipients):
    url = "{0}/{1}".format(Recipients.url, "sms")

       
class RecipientsHandler(object):
    phone = Phone()
    email = Email()
    sms = Sms()



    


