
import uuid
import pymysql
import logging
import databasefile
import uuid
import json
from pyfcm import FCMNotification

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class d(dict):
    def __str__(self):
        return json.dumps(self)
    def __repr__(self):
        return json.dumps(self)



def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data


def CreateHashKey(FirstKey,SecoundKey):
    # hash = hashlib.sha256()
    # hash.update(('%s%s' % (FirstKey,SecoundKey)).encode('utf-8'))
    Hashkey = uuid.uuid1()

    return Hashkey


def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data







def userNotification(DeviceToken,name):
    try:
        push_service = FCMNotification(api_key="AAAACCftdfM:APA91bG2v1DlrKLfDDNfso43UuaDXkzy2FZb-zgVY4rw1K3P3zSNn0dMbfpUfUDxfaGs_qu6kG0N2C6Rmw9c8v2BdhQQE3wR24BwZTHEjM50AU5xyFlNjQ_gF5gmUPD56R1GMQWszA-r ")
        registration_id = str(DeviceToken)
        message_title = "New Call Received"
        message = "Dear , You got new call from    from "+str(name)+"  "
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message)
        print(result,"jssjd")
        # config.data['to'] = str(DeviceToken)
        # config.data['subtitle'] = "Dear ,"+str(UserName)+" you got new message  from "+str(adminName)+" message "+str(comment)+" "

        # print(config.data)        
        # r=requests.post(config.URL, headers=config.headers, data=json.dumps(config.data))
        # response=json.loads(r.text) 
        if result:
            return result
        else:
            return commonfile.Errormessage()
    except Exception as e :
        print("Exception--->" + str(e))                                  
        return commonfile.Errormessage()




def lambda_handler(event, context):
    
    logger.info(event)
    logger.info(context)

    
    if event['path'] =="/userregistration":

        v1="1"
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            name=i['name']
            print(name)
            MobileToken=i['MobileToken']
            UserId=CreateHashKey(name,MobileToken)
            flag="i"
            WhereCondition = " and name = '" + str(name)+"'"
            count = databasefile.SelectCountQuery("userMaster",WhereCondition,"")
            if int(count) > 0:
                return {'statusCode':404}
            else:
                if flag =="i":
                    print("11111111111111111111111")
                    column = "name,MobileToken,userId"                
                    values = " '" + str(name)  + "','" + str(MobileToken)+ "','" + str(UserId)  + "' "
                    data = databasefile.InsertQuery("userMaster",column,values)       
                    if data != "0":

                        column = 'name,MobileToken,userId'
                        data = databasefile.SelectQuery("userMaster",column,WhereCondition,"","","")
                        print(data)
                        # dat={}
                        # dat["glasstypeId"]=int(data['result'][0]['glasstypeId'])
                        # dat["cof"]=int(data['result'][0]['cof'])
                        # print(dat)
                        
                        

                        return { 'statusCode': 200, 'body':event['body']}
                    else:
                        return "qq"
    elif event['path'] == "/mobileTokenupdate":
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['userId']
            print(userId)
            MobileToken=i['MobileToken']
            column="MobileToken='" + MobileToken+ "'"
            whereCondition= "  and userId = '" + str(userId)+ "' "
            output=databasefile.UpdateQuery("userMaster",column,whereCondition)
                       
            if output!='0':
                Data = {'statusCode':200,'body':'updated SuccessFully '}                   
                return Data
    else:
        if event['httpMethod'] == "POST":
            print("w")
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['userId']
            summary=i['summary']
            notificationId=i['notificationId']
            MobileToken=[]

            for i in userId:
                WhereCondition=" and userId='"+str(i)+"'"
                column = 'name,MobileToken'
                data = databasefile.SelectQuery1("userMaster",column,WhereCondition)
                mt=data['result']['MobileToken']
                name=data['result']['name']
                MobileToken.append(mt)
                for k in MobileToken:
                    column="notificationId,summary,MobileToken,userId"
                    values= "'" + str(notificationId)+ "','" + str(summary)  + "','" + str(k)  + "','" + str(i) + "'"
                    data66=databasefile.InsertQuery('userNotification',column,values)
                    whereCondition=" and notificationId ="+str(notificationId)+" "
                    d=databasefile.SelectQuery('userNotification',column,whereCondition)
                    print(d,"+++++++++")
                    result=d['result']
                    if k !=None:
                        a=userNotification(k,name)
            Data = {'statusCode':200,'body':' Notification send SuccessFully '}                   
            return Data


       
        






