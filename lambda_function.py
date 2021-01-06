
import uuid
import pymysql
import logging
import databasefile
import uuid
import json
from pyfcm import FCMNotification
import requests
import connection
import pytz
from datetime import datetime,timedelta
import stripe
Accesskey="Qbq5MV8XLWWB5+hOgYLZbXxqIJt47Ub3y96RHXE9"
BucketName="uplad-documents"
AcessId="AKIA2W4VA3GE5OVQ5TWQ"

import boto3
import base64
import razorpay 
s3=boto3.client("s3",aws_access_key_id=AcessId,aws_secret_access_key=Accesskey)







logger = logging.getLogger()
logger.setLevel(logging.INFO)

class d(dict):
    def __str__(self):
        return json.dumps(self)
    def __repr__(self):
        return json.dumps(self)





def amountpermonth(months,pa,interest,processFee,gst):
    months=int(months)
    pa=int(pa)
    interest=interest * 0.01
    
    profit= pa * interest * months
    processFee=processFee* pa * 0.01
    gst=gst*processFee*0.01
    
    sa=pa+profit+processFee+gst
    amountpermonth=int(sa/months)
    a='{:,d}'.format(amountpermonth)
    
    return a




def emibreakdown(pa,interest,processFee,gst):
    pa=pa
    interest=interest
    processFee=processFee
    gst=gst
    amonths = amountpermonth(3,pa,interest,processFee,gst)
    bmonths = amountpermonth(6,pa,interest,processFee,gst)
    cmonths = amountpermonth(9,pa,interest,processFee,gst)
    dmonths=amountpermonth(12,pa,interest,processFee,gst)
    emonths=amountpermonth(15,pa,interest,processFee,gst)
    fmonths=amountpermonth(18,pa,interest,processFee,gst)
    gmonths=amountpermonth(21,pa,interest,processFee,gst)
    hmonths=amountpermonth(24,pa,interest,processFee,gst)
    imonths=amountpermonth(27,pa,interest,processFee,gst)
    jmonths=amountpermonth(30,pa,interest,processFee,gst)
    kmonths=amountpermonth(33,pa,interest,processFee,gst)
    lmonths=amountpermonth(36,pa,interest,processFee,gst)
    result1=[]
    result1.append({"months":3,"emi":amonths})
    result1.append({"months":6,"emi":bmonths})
    result1.append({"months":9,"emi":cmonths})
    result1.append({"months":12,"emi":dmonths})
    result={}
    result['result']=result1
    
    
    return result

def amountbreakup(months,pa,interest,processFee,gst):
    months=int(months)
    pa=int(pa)
    interest=interest * 0.01
    
    profit= pa * interest * months
    processFee=processFee* pa * 0.01
    gst=gst*processFee*0.01
    
    sa=pa+profit+processFee+gst
    sa1=int(sa)
    amountpermonth=int(sa/months)
    a='{:,d}'.format(amountpermonth)
    
    result={}
    result['emitotal']='{:,d}'.format(sa1)
    result['emipermonth']=a
    result['processFee']=int(processFee)
    result['gst']=int(gst)
    return result   









def CurrentDatetime():
    ist = pytz.timezone('Asia/Kolkata')
    ist_time = datetime.now(tz=ist)
    ist_f_time = str(ist_time.strftime("%Y-%m-%d %H:%M:%S"))

    return ist_f_time        



def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data


def CreateHashKey(FirstKey,SecoundKey):
    Hashkey = uuid.uuid1()

    return Hashkey


def DecodeInputdata(data):
    data = json.loads(data.decode("utf-8"))                 
    return data







def lambda_handler(event, context):
    
    logger.info(event)
    logger.info(context)
    if event['path'] == "/agentlogin":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            email=i['email']
            password=i['password']
            
           
            column="email,password,agentId,name"
            WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)

                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['agentId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    asjj['agentId']=data['result'][0]['agentId']
                    WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("agentmaster",column,WhereCondition)

               
                hpp=d(asjj)
                hpp["status"]=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:

                return {'statusCode':201,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}
    elif event['path'] == "/agentdashboard":
        print("www")
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                completed=[]
                WhereCondition=" and u.status='"+str(1)+"' and u.userId=um.userId"
                WhereCondition1=" and u.status='"+str(0)+"' and u.userId=um.userId"
                WhereCondition2=" and u.status='"+str(2)+"'and u.userId=um.userId"
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,u.amount,u.months,u.status,um.name,um.phone"

                datac=databasefile.SelectQuery("useremiadd as u,usermaster as um",column,WhereCondition,"","","")
                datap=databasefile.SelectQuery("useremiadd as u,usermaster as um",column,WhereCondition1,"","","")
                datar=databasefile.SelectQuery("useremiadd as u,usermaster as um",column,WhereCondition2,"","","")
                for i in datac['result']:
                    completed.append(i)
                pending=[]
                for i in datap['result']:
                    pending.append(i)
                rejected=[]
                for i in datar['result']:
                    rejected.append(i)

                result={}
                result['completed']=completed
                result['pending']=pending
                result['rejected']=rejected

                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

    elif event['path'] == "/userpayemi":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            
            userId=i['userId']
            order_amount=i['amount']
            

           
            
           
            column="name,email"
            WhereCondition= " and userId='"+str(userId)+"' and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                order_receipt = 'order_rcptid_11'


                order_amount1=order_amount
                order_currency = 'INR'

                client = razorpay.Client(auth=("rzp_live_9c3OoVSfu1c23s", "0q9HXWoHFtCkKkrQkw5hlKbM"))
                clientId=client.order.create({"amount":order_amount1, "currency":order_currency, "receipt":order_receipt, "payment_capture":'0'})
                print(clientId,"ssj")
                uo=client.order.payments(clientId['id'])
                t={ }
                
                clientId['offer_id']="0"
                
                t['result']=clientId
                t['payment']=uo['items']

                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
        
    elif event['path'] == "/userdashboard":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            
            userId=i['userId']
            

           
            
           
            column="name,email"
            WhereCondition= " and userId='"+str(userId)+"' and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                completed=[]
                WhereCondition=" and u.userId=um.userId and um.userId='"+str(userId)+"'"
               
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,u.amount,u.months,u.status,um.name,um.phone"

                datac=databasefile.SelectQuery("useremiadd as u,usermaster as um",column,WhereCondition,"","","")
                
                for i in datac['result']:
                    completed.append(i)
                pending=[]
               

                result1={}
                result1['completed']=completed
               
               
                
                column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,accountNo,bankaccountNo,ifsccode'
                WhereCondition=" and userId='"+str(userId)+"'"
                data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")

               


                result=data['result'][0]
                result['loan']=completed
                j="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharback"+str(data['result'][0]['userId'])+str(".png")
                k="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharfront"+str(data['result'][0]['userId'])+str(".png")
                l="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"panCard"+str(data['result'][0]['userId'])+str(".png")
                result['aadaadharback']=j
                result['aadaadharfront']=k
                result['panCard']=l


                
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/emibreakdownpage":
        
            
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            amount=i['amount']
            column="interestrate,processFee,gst"
            d1=databasefile.SelectQuery("interestsettingMaster",column,"","","","")
            interest=int(d1['result'][0]['interestrate'])
            gst=int(d1['result'][0]['gst'])
            processFee=int(d1['result'][0]['processFee'])
            hhh=emibreakdown(amount,interest,processFee,gst)
            print(hhh,"")
           
            # u="ww"
            # result={'result':hhh['result']}
            # print(result,"qwws")
            # r=d(result)
            # t={}
            tq=[]
            for i in hhh['result']:
                j=d(i)
                tq.append(j)
            t={}


            t['result']=tq
            t['amount']=amount
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
                    
           
    if event['path'] == "/userlogin":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            phone=i['phone']
            password=i['password']
            
           
            column="email,password,userId,name"
            WhereCondition= "  and phone = '" + str(phone)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)

                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['userId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    asjj['userId']=data['result'][0]['userId']
                    WhereCondition= "  and phone = '" + str(phone)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("usermaster",column,WhereCondition)

               
                hpp=d(asjj)
                hpp['status']=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':201,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}
            
    
    
    elif event['path'] == "/agentregistration":
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            name=i['name']
            email=i['email']
            password=i['password']
            phone=i['phone']
            aadharcardNo=i['aadharcardNo']
            pancardNo=i['pancardNo']
            address=i['address']
            bankaccountNo=i['bankaccountNo']
            ifsccode=i['ifsccode']
            agentId=CreateHashKey(name,aadharcardNo)
            flag="i"
            WhereCondition = " and phone = '" + str(phone)+"' or email='"+str(email)+"'or aadharcardNo='"+str(aadharcardNo)+"'"
            count = databasefile.SelectCountQuery("agentmaster",WhereCondition,"")
            if int(count) > 0:
                t={}
                t['result'] ="Agent Already  exist "
                hpp=d(t)
                return {'statusCode':201,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
                
            else:
                aadharfront=i['aadharfront']
                aadharback=i['aadharback']
                panCard=i['panCard']
                panCardid1=pancardNo
                s3.put_object(Bucket=BucketName,Body='', Key='agent/')
                panCardid='agent/'+str(panCardid1)
                pp='agent/'+str(panCardid)+"/"
                s3.put_object(Bucket=BucketName,Body='', Key=pp)
                if flag =="i":
                    print("11111111111111111111111")
                    s=CurrentDatetime()
                    aadharbackId1="aadharback"+str(agentId)
                    aadharfrontId1="aadharfront"+str(agentId)
                    panCardId1="panCard"+str(agentId)
                    aadharback1=aadharback[aadharback.find(",")+1:]
                    aadharfront1=aadharfront[aadharfront.find(",")+1:]
                    panCard1=panCard[panCard.find(",")+1:]
                    dec1=base64.b64decode(aadharback1+"===")
                    dec2=base64.b64decode(aadharfront1+"===")
                    dec3=base64.b64decode(panCard1+"===")

                    a=aadharback.split("data:")
                    a1=a[1].split("/")
                    print(a1,"w")
                    a2=a1[1].split(";")
                    print(a2,"a2")
                    aadharbackextension=a2[0]
                    a3=aadharfront.split("data:")
                    a4=a3[1].split("/")
                    a5=a4[1].split(";")
                    print(a5,"a5")
                    aadharfrontextension=a5[0]
                    a6=panCard.split("data:")
                    a7=a6[1].split("/")
                    a8=a7[1].split(";")
                    print(a8,"a8")

                    pancardextension=a8[0]
                    aadharbackId000=aadharbackId1+"."+str(aadharbackextension)
                    aadharfrontId000=aadharfrontId1+"."+str(aadharfrontextension)
                    panCardId000=panCardId1+"."+str(pancardextension)
                   
                    aadharbackfileName=panCardid+"/"+str(aadharbackId000)
                    aadharfrontfileName= panCardid+"/"+str(aadharfrontId000)
                    panCardfileName= panCardid+"/"+str(panCardId000)
                    ip1=s3.put_object(Bucket=BucketName,Key=aadharbackfileName,Body=dec1)
                    ip2=s3.put_object(Bucket=BucketName,Key=aadharfrontfileName,Body=dec2)
                    ip3=s3.put_object(Bucket=BucketName,Key=panCardfileName,Body=dec3)
                    
                    column = "agentId,name,address,phone,password,email,pancardNo,aadharcardNo,registime,bankaccountNo,ifsccode"                
                    values = " '" + str(agentId)  + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(password)  + "','" + str(email)+ "','" + str(pancardNo) + "','" + str(aadharcardNo) + "','" + str(s) + "','" + str(bankaccountNo) + "','" + str(ifsccode) + "' "
                    data = databasefile.InsertQuery("agentmaster",column,values)       
                    if data != "0":

                        column = 'agentId,name,address,phone,email,pancardNo,aadharcardNo,registime,bankaccountNo,ifsccode'
                        data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
                        hhh=[]
                        for i in data['result']:
                            k=d(i)
                            print(k)
                            hhh.append(k)

                        
                        print(hhh,"swwww")


                        u="ww"
                        result={'result':hhh}
                        print(result,"qwws")
                        r=d(result)
                        t={}
                        t['result']=r['result']
                        hpp=d(t)
                        print({'statusCode':200,'body':hpp})
                        return {'statusCode':200,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        },'body':json.dumps(hpp)}
    elif event['path'] == "/emidetails":
        
            
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            amount=i['amount']
            months=int(i['months'])
            column="interestrate,processFee,gst"
            d1=databasefile.SelectQuery("interestsettingMaster",column,"","","","")
            interest=int(d1['result'][0]['interestrate'])
            gst=int(d1['result'][0]['gst'])
            processFee=int(d1['result'][0]['processFee'])
            hhh=amountbreakup(months,amount,interest,processFee,gst)
            interestrate=str(interest)+" "+ "%"
            hhh.update({'interestrate':interestrate})
            hhh.update({"amount":amount})
            hhh.update({"months":months})
            u="ww"
            result={'result':hhh}
            print(result,"qwws")
            r=d(result)
            t={}
            t['result']=r['result']
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
                    
           
                        
                        

                        
                  
    elif event['path'] == "/loantransfered":
            
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            accountNo=i['accountNo']
            amountTransfered=i['amountTransfered']
            totalAmount=i['totalAmount']
            amountleft=totalAmount-amountTransfered
            agentId=i['agentId']
           
            
            flag="i"
           
                
            
            if flag =="i":
                
                print("11111111111111111111111")
                s=CurrentDatetime()
                
                
                
                column = "accountNo,amountTransfered,totalAmountleft,agentId,transferDate"                
                values = " '" + str(accountNo)  + "','" + str(amountTransfered) + "','" + str(amountleft)+"','" + str(agentId) + "','" + str(transferDate)+ "'"
                data = databasefile.InsertQuery("loanAmountTransfer",column,values) 
                WhereCondition="and accountNo='"+str(accountNo)+"'"      
                
                if data != "0":

                    column = 'accountNo,amountTransfered,totalAmountleft,agentId,transferDate'
                    data = databasefile.SelectQuery("loanAmountTransfer",column,WhereCondition,"","","")
                    hhh=[]
                    for i in data['result']:
                        k=d(i)
                        print(k)
                        hhh.append(k)

                    
                    print(hhh,"swwww")


                    u="ww"
                    result={'result':hhh}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}

    elif event['path'] == "/emidetailsubmit":
        
            
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':

                t=type(event['body'])
                print(event['body'],"www")
                print(t,"w####")
                i=json.loads(event['body'])
                print(i,"sssq")
                print(type(i),"wwsw")
                amount=i['amount']
                months=int(i['months'])
                userId=i['userId']
                column="interestrate,processFee,gst"
                d1=databasefile.SelectQuery("interestsettingMaster",column,"","","","")
                interest=int(d1['result'][0]['interestrate'])
                gst=int(d1['result'][0]['gst'])
                processFee=int(d1['result'][0]['processFee'])
                hhh=amountbreakup(months,amount,interest,processFee,gst)
                interestrate=str(interest)+" "+ "%"
                hhh.update({'interestrate':interestrate})
                emitotal=hhh['emitotal']
                interestrate=hhh['interestrate']
                emipermonth=hhh['emipermonth']
                processFee=hhh['processFee']
                gst=hhh['gst']
                s=CurrentDatetime()
                column="userId,emitotal,interestrate,emipermonth,processFee,gst,loantime,amount,months"
                values= " '" + str(userId)  + "','" + str(emitotal) + "','" + str(interestrate) + "','" + str(emipermonth) + "','" + str(processFee)  + "','" + str(gst)+ "','" + str(s)+ "','" + str(amount)+ "','" + str(months)+ "' "
                data=databasefile.InsertQuery("useremiadd",column,values) 
                WhereCondition=" and userId='"+str(userId)+"'and loantime='"+(s)+"'"
                data=databasefile.SelectQuery("useremiadd",column,WhereCondition,"","","")
                hhh=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    hhh.append(i)
                

                u="ww"
                result={'result':hhh}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}

            else:
                return {'statusCode':301,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

                    
           
                    
                    

                        
                   
    elif event['path'] == "/userregistrationverify":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            
            phone=i['phone']
            aadharcardNo=i['aadharcardNo']
            agentId=i['agentId']

          

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and agentId='"+str(agentId)+"'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            if data['status']!='false':

           

                

                flag="i"
                
                WhereCondition = " and phone = '" + str(phone)+"' or aadharcardNo='"+str(aadharcardNo)+"'"
                count = databasefile.SelectCountQuery("usermaster",WhereCondition,"")
                if int(count) > 0:
                    t={}
                    t['result'] ="User Already  exist "
                    hpp=d(t)
                    return {'statusCode':201,'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                          },'body':json.dumps(hpp)}
                    
                else:
                    if flag =="i":
                        print("11111111111111111111111")
                        s=CurrentDatetime()
                        
                        
                        t={}
                        t['result']="New user,you can add this user as new"
                        hpp=d(t)
                        print({'statusCode':200,'body':hpp})
                        return {'statusCode':200,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                      },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="agents token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}

        else:
            
            column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,loanAmount,loanType,years,accountNo'
            data = databasefile.SelectQuery("usermaster",column,"","","","")
            hhh=[]
            for i in data['result']:
                k=d(i)
                print(k)
                hhh.append(k)

            
            print(hhh,"swwww")


            u="ww"
            result={'result':hhh}
            print(result,"qwws")
            r=d(result)
            t={}
            t['result']=r['result']
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
    elif event['path'] == "/agentuserdetails":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            agentId=i['agentId']
            userId=i['userId']
            

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                
                WhereCondition2=" and u.userId=um.userId and um.agentId=am.agentId and am.agentId='"+str(agentId)+"' and um.userId='"+str(userId)+"'"
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,u.amount,u.months,u.status,um.name,um.phone,am.name as agentName"

               
                datar=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition2,"","","")
                column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,bankaccountNo,ifsccode'
                WhereCondition=" and userId='"+str(userId)+"'"
                data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")

                
                rejected=[]
                for i in datar['result']:
                    rejected.append(i)


                result=data['result'][0]
                result['loan']=rejected
                j="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharback"+str(data['result'][0]['userId'])+str(".png")
                k="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharfront"+str(data['result'][0]['userId'])+str(".png")
                l="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"panCard"+str(data['result'][0]['userId'])+str(".png")
                result['aadaadharback']=j
                result['aadaadharfront']=k
                result['panCard']=l


                
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

    elif event['path'] == "/adminuserdetails":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            
            userId=i['userId']
            

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                
                WhereCondition2=" and u.userId=um.userId and um.agentId=am.agentId  and um.userId='"+str(userId)+"'"
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,u.amount,u.months,u.status,um.name,um.phone,am.name as agentName"

               
                datar=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition2,"","","")
                column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,accountNo'
                WhereCondition=" and userId='"+str(userId)+"'"
                data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")

                
                rejected=[]
                for i in datar['result']:
                    rejected.append(i)


                result=data['result'][0]
                result['loan']=rejected
                j="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharback"+str(data['result'][0]['userId'])+str(".png")
                k="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"aadaadharfront"+str(data['result'][0]['userId'])+str(".png")
                l="https://uplad-documents.s3.ap-south-1.amazonaws.com"+"/"+str(data['result'][0]['pancardNo'])+"/"+"panCard"+str(data['result'][0]['userId'])+str(".png")
                result['aadaadharback']=j
                result['aadaadharfront']=k
                result['panCard']=l


                
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/agentverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            
            agentId=i['agentId']
                

               
                
               
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
           
           
            
                column="status='" +str(1)+ "'"
                whereCondition= "  and agentId = '" + str(userId)+ "' "
                output=databasefile.UpdateQuery("agentmaster",column,whereCondition)
                           
                if output!='0':
                    t={ }
                    t['result']='verified Successfully'
                    hpp=d(t)
                                    
                    return {'statusCode':200,'body':json.dumps(hpp),'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                }}
            else:
                return {'statusCode':301,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

    
    elif event['path'] == "/approveemi":
    
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                userId=i['userId']
                loanTime=i['loanTime']

                print(userId)
                
                column="status='" +str(1)+ "'"
                whereCondition= "  and userId = '" + str(userId)+ "' and loanTime='"+str(loanTime)+"'"
                output=databasefile.UpdateQuery("useremiadd",column,whereCondition)
                           
                if output!='0':
                    t={ }
                    t['result']='verified Successfully'
                    hpp=d(t)


                u="ww"
                result={'result':hhh}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}

            else:
                return {'statusCode':301,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}

    elif event['path'] == "/rejectemi":
        
            
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                userId=i['userId']
                loanTime=i['loanTime']

                print(userId)
                
                column="status='" +str(2)+ "'"
                whereCondition= "  and userId = '" + str(userId)+ "' and loanTime='"+str(loanTime)+"'"
                output=databasefile.UpdateQuery("useremiadd",column,whereCondition)
                           
                if output!='0':
                    t={ }
                    t['result']='verified Successfully'
                    hpp=d(t)


                u="ww"
                result={'result':hhh}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}

            else:
                return {'statusCode':301,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
                    
           
                    
           


        
    elif event['path'] == "/adminlogin":
        print("www")
        if event['httpMethod'] == "POST":
            
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            email=i['email']
            password=i['password']
            
           
            column="email,adminId"
            WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)

                    stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

                    a=stripe.Token.create(
                      pii={"id_number": i['adminId']},
                    )

                    asjj={}
                    asjj['token']=a['id'] +str(a['id'][::-1])+str(a['id'][::-6])+str(a['id'][::-1])+str(a['id'][::-5])+str(a['id'][::-2])+str(a['id'][::-3])+str(a['id'][::-4])
                    print(asjj)
                    asjj['adminId']=i['adminId']
                    WhereCondition= "  and email = '" + str(email)+ "' and password='"+password+"'"
                    column="token ='"+ str(asjj['token'])+"'"
                    data = databasefile.UpdateQuery("adminmaster",column,WhereCondition)

               
                hpp=d(asjj)
                hpp['status']=1
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
            else:
                return {'statusCode':201,'headers': {
                            'Access-Control-Allow-Headers': 'Content-Type',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                        },'body':json.dumps({'result':'Wrong password and email ,Please Enter Correct Credentails','status':0})}

    elif event['path'] == "/addamountadhoc":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            adminId=i['adminId']
            amount=i['amount']
            start=i['start']
            end-i['end']
            diff=i['diff']

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and adminId='"+str(adminId)+"'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            if data['status']!='false':

           

               

                flag="i"
                
                WhereCondition = " and amount='"+str(amount)+"'"
                count = databasefile.SelectCountQuery("amountsetting",WhereCondition,"")
                if int(count) > 0:
                    t={}
                    t['result'] =" Already  exist for same amount"
                    hpp=d(t)
                    return {'statusCode':201,'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                          },'body':json.dumps(hpp)}
                    
                else:
                    if flag =="i":
                        print("11111111111111111111111")
                        s=CurrentDatetime()
                        
                        column = "amount,start,end,diff"                
                        values = " '" + str(amount) + "','" + str(start)   + "','" + str(end) + "','" + str(diff) + "'"
                        data = databasefile.InsertQuery("amountsetting",column,values)  
                        WhereCondition=""     
                        if data != "0":
                            column = "amount,start,end,diff"   

                            
                            data = databasefile.SelectQuery("amountsetting",column,WhereCondition,"","","")
                            hhh=[]
                            for i in data['result']:
                                k=d(i)
                                print(k)
                                hhh.append(k)

                            
                            print(hhh,"swwww")


                            u="ww"
                            result={'result':hhh[0]}
                            print(result,"qwws")
                            r=d(result)
                            t={}
                            t['result']=r['result']
                            hpp=d(t)
                            print({'statusCode':200,'body':hpp})
                            return {'statusCode':200,'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                          },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="admins token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
    elif event['path'] == "/updateamountadhoc":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            adminId=i['adminId']
            amount=i['amount']
            start=i['start']
            end-i['end']
            diff=i['diff']
            Id=i['id']

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and adminId='"+str(adminId)+"'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            if data['status']!='false':

           

               

               
                        
                column = "amount='"+str(amount)+"',start=='"+str(start)+"',end=='"+str(end)+"',diff='"+str(diff)+"'" 
                WhereCondition=" and id='"+str(Id)+"'"               
               
                data = databasefile.UpdateQuery("amountsetting",column,WhereCondition)  
                WhereCondition=""     
                if data != "0":
                    column = "amount,start,end,diff"   

                    
                    


                    u="ww"
                    result={'result':'Updated Successfully'}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                  },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="admins token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)} 

    elif event['path'] == "/selectamountadhoc":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            adminId=i['adminId']
            
            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and adminId='"+str(adminId)+"'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            if data['status']!='false':
                WhereCondition=""     
                if data != "0":
                    column = "id,amount,start,end,diff"   

                    
                    data = databasefile.SelectQuery("amountsetting",column,WhereCondition,"","","")
                    hhh=[]
                    for i in data['result']:
                        k=d(i)
                        print(k)
                        hhh.append(k)

                    
                    print(hhh,"swwww")


                    u="ww"
                    result={'result':hhh[0]}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                  },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="admins token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}   
    elif event['path'] == "/admindashboard":
        print("www")
        if event['httpMethod'] == "POST":
            
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")

                u="ww"
                result={'result':h}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']={"completed":8,"pending":2,"rejected":3,"agent":14}
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    
    elif event['path'] == "/emiTenuredropdown":
        print("www")
        if event['httpMethod'] == "POST":
            
           
            h=[]
            column="months"
            d1=databasefile.SelectQuery("emiTenuredropdown",column,WhereCondition,"","","")
            for i in d1:
                ii=d(i)
                h.append(ii['months'])
                
            print(h,"swwww")
            u="ww"
            result={'months':h}
            print(result,"qwws")
            
            t={}
            t['result']=result
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
    elif event['path'] == "/addemiTenuredropdown":
        
            
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            months=i['months']
           
            
            flag="i"
           
            
            if flag =="i":
                
                print("11111111111111111111111")
                s=CurrentDatetime()
                
                
                
                column = "months"                
                values = " '" + str(months)  
                data = databasefile.InsertQuery("emiTenuredropdown",column,values) 
                WhereCondition=""      
                
                if data != "0":

                    column = 'months'
                    data = databasefile.SelectQuery("emiTenuredropdown",column,WhereCondition,"","","")
                    hhh=[]
                    for i in data['result']:
                        k=d(i)
                        print(k)
                        hhh.append(k)

                    
                    print(hhh,"swwww")


                    u="ww"
                    result={'result':hhh}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
                    
           
    elif event['path'] == "/interestsetting":
        print("www")
        #5
        if event['httpMethod'] == "POST":
           
            data={}
            data['status']='true'
            print(data)
            if data['status'] !='false':
                h=[]
                column="interestrate,processFee,gst"
                d1=databasefile.SelectQuery("interestsettingMaster",column,"","","","")
                for i in d1['result']:
                    ii=d(i)
                    h.append(ii)
                print(h,"swwww")
                u="ww"
                result={'result':h}
                print(result,"qwws")
                
                t={}
                t['result']=h[0]
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/updateinterestsetting":
        print("www")
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            column,values="",""
            if 'interestrate' in i:
                interestrate=i['interestrate']
                column=column+"interestrate='" +str(interestrate)+ "'"
            if 'processFee' in i:
                processFee=i['processFee']
                if column !="":  
                    column=column+",processFee='" +str(processFee)+ "'"
                else:
                    column="processFee='" +str(processFee)+ "'"


            if 'gst' in i:
                gst=i['gst']
                if column !="":
                    column=column+",gst='" +str(gst)+ "'"
                else:
                    column="gst='" +str(gst)+ "'"

        
            
            
            whereCondition= "  and id = '" + str(1)+ "' "
            output=databasefile.UpdateQuery("interestsettingMaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='interestrate updated Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}

    elif event['path'] == "/allagents":
        
        if event['httpMethod'] == "POST":
            
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

           
            
           
            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                column = 'id,agentId,name,address,phone,email,pancardNo,aadharcardNo,registime'
                data = databasefile.SelectQuery("agentmaster",column,"","","","")
                hhh=[]
                for i in data['result']:
                    agentId=i['agentId']
                    WhereCondition=" and agentId='"+str(agentId)+"'"
                    co=databasefile.SelectTotalCountQuery("usermaster",WhereCondition,"")
                    useradded=int(co)
                    if useradded > 0:
                        i['useradded']=useradded
                    else:
                        i['useradded']=0
                    k=d(i)
                    print(k)
                    hhh.append(k)
 
            
               
                result={'result':hhh}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
            else:
                        return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/allusers":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                completed=[]
                WhereCondition=" and u.status='"+str(1)+"' and u.userId=um.userId and um.agentId=am.agentId"
                WhereCondition1=" and u.status='"+str(0)+"' and u.userId=um.userId and um.agentId=am.agentId"
                WhereCondition2=" and u.status='"+str(2)+"'and u.userId=um.userId and um.agentId=am.agentId"
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,u.amount,um.bankaccountNo,um.ifsccode,u.months,u.status,um.name,um.phone,am.name as agentName"

                datac=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition,"","","")
                datap=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition1,"","","")
                datar=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition2,"","","")
                for i in datac['result']:
                    completed.append(i)
                pending=[]
                for i in datap['result']:
                    pending.append(i)
                rejected=[]
                for i in datar['result']:
                    rejected.append(i)

                result={}
                result['completed']=completed
                result['pending']=pending
                result['rejected']=rejected

                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
            
    elif event['path'] == "/amountoption":
        print("www")
        
        if event['httpMethod'] == "POST":
           
            h=[]
            column="amount"
            d1=databasefile.SelectQuery("amountoption",column,WhereCondition,"","","")
            for i in d1:
                ii=d(i)
                h.append(ii['amount'])
                
            print(h,"swwww")
            u="ww"
            result={'amount':h}
            print(result,"qwws")
            
            t={}
            t['result']=result
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}

    
    elif event['path'] == "/addamountoption":
        
            
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            amount=i['amount']
           
            
            flag="i"
           
                
            
            if flag =="i":
                
                print("11111111111111111111111")
                s=CurrentDatetime()
                
                
                
                column = "amount"                
                values = " '" + str(amount)  
                data = databasefile.InsertQuery("amountoption",column,values) 
                WhereCondition=""      
                
                if data != "0":

                    column = 'amount'
                    data = databasefile.SelectQuery("amount",column,WhereCondition,"","","")
                    hhh=[]
                    for i in data['result']:
                        k=d(i)
                        print(k)
                        hhh.append(k)

                    
                    print(hhh,"swwww")


                    u="ww"
                    result={'result':hhh}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
    elif event['path'] == "/uploaddocument":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            userId=i['userId']
            agentId=i['agentId']
            aadharfront=i['aadharfront']
            aadharback=i['aadharback']
            panCard=i['panCard']
            panCardid=i['panCardId']
            pp=str(panCardid)+"/"
            s3.put_object(Bucket=BucketName,Body='', Key=pp)
            

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and agentId='"+str(agentId)+"'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            if data['status']!='false':
                print("ss")


                aadharbackId1="aadharback"+str(userId)
                aadharfrontId1="aadharfront"+str(userId)
                panCardId1="panCard"+str(userId)
                aadharback1=aadharback[aadharback.find(",")+1:]
                aadharfront1=aadharfront[aadharfront.find(",")+1:]
                panCard1=panCard[panCard.find(",")+1:]
                dec1=base64.b64decode(aadharback1+"===")
                dec2=base64.b64decode(aadharfront1+"===")
                dec3=base64.b64decode(panCard1+"===")

                a=aadharback.split("data:")
                a1=a[1].split("/")
                print(a1,"w")
                a2=a1[1].split(";")
                print(a2,"a2")
                aadharbackextension=a2[0]
                a3=aadharfront.split("data:")
                a4=a3[1].split("/")
                a5=a4[1].split(";")
                print(a5,"a5")
                aadharfrontextension=a5[0]
                a6=panCard.split("data:")
                a7=a6[1].split("/")
                a8=a7[1].split(";")
                print(a8,"a8")

                pancardextension=a8[0]
                aadharbackId000=aadharbackId1+"."+str(aadharbackextension)
                aadharfrontId000=aadharfrontId1+"."+str(aadharfrontextension)
                panCardId000=panCardId1+"."+str(pancardextension)
                # path_test1="aadharback"
                # path_test2="aadharfront"
                # path_test3="panCard"
                aadharbackfileName=panCardid+"/"+str(aadharbackId000)
                aadharfrontfileName= panCardid+"/"+str(aadharfrontId000)
                panCardfileName= panCardid+"/"+str(panCardId000)
                ip1=s3.put_object(Bucket=BucketName,Key=aadharbackfileName,Body=dec1)
                ip2=s3.put_object(Bucket=BucketName,Key=aadharfrontfileName,Body=dec2)
                ip3=s3.put_object(Bucket=BucketName,Key=panCardfileName,Body=dec3)








                # u="ww"
                # result={'result':hhh[0]}
                # print(result,"qwws")
                # r=d(result)
                t={}
                t['result']="upload Successfully"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="agents token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
    elif event['path'] == "/updateamountoption":
        print("www")
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            amount=i['amount']
           

        
            
            column="amount='" +str(amount)+ "'"
            whereCondition= "  and id = '" + str(1)+ "' "
            output=databasefile.UpdateQuery("amountoption",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='amountoption updated Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
                        
           
                        

                        
                   

           

    elif event['path'] == "/viewloantransfered":
        
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            accountNo=i['accountNo']
            
           
            
            flag="i"
           
                
            
            if flag =="i":
                print("11111111111111111111111")
                s=CurrentDatetime()
                WhereCondition="lat.accountNo='"+str(accountNo)+"'and lat.accountNo=um.accountNo"
                
               

                column = 'ltd.accountNo,ltd.amountTransfered,ltd.totalAmountleft,ltd.agentId,ltd.transferDate,um.regisTime,um.year,um.loanType,um.loanAmount'
                data = databasefile.SelectQuery("loanAmountTransfer as ltd,userMaster as um",column,WhereCondition,"","","")
                hhh=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    hhh.append(k)

                    
                    print(hhh,"swwww")


                    u="ww"
                    result={'result':hhh}
                    print(result,"qwws")
                    r=d(result)
                    t={}
                    t['result']=r['result']
                    hpp=d(t)
                    print({'statusCode':200,'body':hpp})
                    return {'statusCode':200,'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },'body':json.dumps(hpp)}
                    
                        

                    
              

    elif event['path'] == "/verfiedloanaccounts":
        print("www")
        if event['httpMethod'] == "GET":
            WhereCondition="loanverfication<>'0'"
            column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,loanAmount,loanType,years,accountNo'
            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
            hhh=[]
            for i in data['result']:
                k=d(i)
                print(k)
                hhh.append(k)

            
            print(hhh,"swwww")


            u="ww"
            result={'result':hhh}
            print(result,"qwws")
            r=d(result)
            t={}
            t['result']=r['result']
            hpp=d(t)
            print({'statusCode':200,'body':hpp})
            return {'statusCode':200,'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },'body':json.dumps(hpp)}
                                        
                        
            

    
    
    elif event['path'] == "/emailverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['agentId']

            print(userId)
            
            column="emailverfication='" +str(1)+ "'"
            whereCondition= "  and agentId = '" + str(userId)+ "' "
            output=databasefile.UpdateQuery("agentmaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='verified Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'body':json.dumps(hpp)}
    elif event['path'] == "/userregistration1":
        
           
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])

            t=type(event['body'])
            print(event['body'],"www")
            print(t,"w####")
            i=json.loads(event['body'])
            print(i,"sssq")
            print(type(i),"wwsw")
            name=i['name']
            email=i['email']
            password=i['password']
            phone=i['phone']
            aadharcardNo=i['aadharcardNo']
            pancardNo=i['pancardNo']
            address=i['address']
            agentId=i['agentId']
            bankaccountNo=i['bankaccountNo']
            ifsccode=i['ifsccode']

            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "' and agentId='"+str(agentId)+"'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            if data['status']!='false':

           

                userId=CreateHashKey(name,aadharcardNo)
                accountNo=CreateHashKey(aadharcardNo,pancardNo)

                flag="i"
                
                WhereCondition = " and phone = '" + str(phone)+"'"
                count = databasefile.SelectCountQuery("usermaster",WhereCondition,"")
                if int(count) > 0:
                    t={}
                    t['result'] ="user Already  exist "
                    hpp=d(t)
                    return {'statusCode':201,'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                          },'body':json.dumps(hpp)}
                    
                else:
                    aadharfront=i['aadharfront']
                    aadharback=i['aadharback']
                    panCard=i['panCard']
                    panCardid=pancardNo
                    pp=str(panCardid)+"/"
                    s3.put_object(Bucket=BucketName,Body='', Key=pp)
                    if flag =="i":
                        print("11111111111111111111111")
                        s=CurrentDatetime()
                        aadharbackId1="aadharback"+str(userId)
                        aadharfrontId1="aadharfront"+str(userId)
                        panCardId1="panCard"+str(userId)
                        aadharback1=aadharback[aadharback.find(",")+1:]
                        aadharfront1=aadharfront[aadharfront.find(",")+1:]
                        panCard1=panCard[panCard.find(",")+1:]
                        dec1=base64.b64decode(aadharback1+"===")
                        dec2=base64.b64decode(aadharfront1+"===")
                        dec3=base64.b64decode(panCard1+"===")

                        a=aadharback.split("data:")
                        a1=a[1].split("/")
                        print(a1,"w")
                        a2=a1[1].split(";")
                        print(a2,"a2")
                        aadharbackextension=a2[0]
                        a3=aadharfront.split("data:")
                        a4=a3[1].split("/")
                        a5=a4[1].split(";")
                        print(a5,"a5")
                        aadharfrontextension=a5[0]
                        a6=panCard.split("data:")
                        a7=a6[1].split("/")
                        a8=a7[1].split(";")
                        print(a8,"a8")

                        pancardextension=a8[0]
                        aadharbackId000=aadharbackId1+"."+str(aadharbackextension)
                        aadharfrontId000=aadharfrontId1+"."+str(aadharfrontextension)
                        panCardId000=panCardId1+"."+str(pancardextension)
                       
                        aadharbackfileName=panCardid+"/"+str(aadharbackId000)
                        aadharfrontfileName= panCardid+"/"+str(aadharfrontId000)
                        panCardfileName= panCardid+"/"+str(panCardId000)
                        ip1=s3.put_object(Bucket=BucketName,Key=aadharbackfileName,Body=dec1)
                        ip2=s3.put_object(Bucket=BucketName,Key=aadharfrontfileName,Body=dec2)
                        ip3=s3.put_object(Bucket=BucketName,Key=panCardfileName,Body=dec3)
                        
                        column = "userId,agentId,name,address,phone,password,email,pancardNo,aadharcardNo,registime,accountNo,bankaccountNo,ifsccode"                
                        values = " '" + str(userId) + "','" + str(agentId)   + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(password)  + "','" + str(email)+ "','" + str(pancardNo) + "','" + str(aadharcardNo) + "','" + str(s)+ "','" + str(accountNo)+ "','" + str(bankaccountNo)+ "','" + str(ifsccode)   + "' "
                        data = databasefile.InsertQuery("usermaster",column,values)  
                        WhereCondition="and accountNo='"+str(accountNo)+"'"     
                        if data != "0":

                            column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,bankaccountNo,ifsccode'
                            data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
                            hhh=[]
                            for i in data['result']:
                                k=d(i)
                                print(k)
                                hhh.append(k)

                            
                            print(hhh,"swwww")


                            u="ww"
                            result={'result':hhh[0]}
                            print(result,"qwws")
                            r=d(result)
                            t={}
                            t['result']=r['result']
                            hpp=d(t)
                            print({'statusCode':200,'body':hpp})
                            return {'statusCode':200,'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': '*',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                          },'body':json.dumps(hpp)}
            else:
                t={}

                t['result']="agents token is Wrong"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':301,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
              },'body':json.dumps(hpp)}
    elif event['path'] == "/agentuser":
   
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            agentId=i['agentId']
            

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("agentmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")
                column = 'agentId,name,userId,address,phone,email,pancardNo,aadharcardNo,registime,bankaccountNo,ifsccode'
                WhereCondition=" and agentId='"+str(agentId)+"'"
                data = databasefile.SelectQuery("usermaster",column,WhereCondition,"","","")
                hhh=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    hhh.append(k)

                
                print(hhh,"swwww")


                u="ww"
                result={'result':hhh}
                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r['result']
                hpp=d(t)




                
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/agentusers":
        
        if event['httpMethod'] == "POST":
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            agentId=i['agentId']
            

           
            
           
            column="name,email"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                h=[]
                for i in data['result']:
                    k=d(i)
                    print(k)
                    h.append(k)

                print(h,"swwww")



                u="ww"
                completed=[]
                WhereCondition=" and u.status='"+str(1)+"' and u.userId=um.userId and um.agentId=am.agentId and am.agentId='"+str(agentId)+"'"
                WhereCondition1=" and u.status='"+str(0)+"' and u.userId=um.userId and um.agentId=am.agentId and am.agentId='"+str(agentId)+"'"
                WhereCondition2=" and u.status='"+str(2)+"'and u.userId=um.userId and um.agentId=am.agentId and am.agentId='"+str(agentId)+"'"
                column="u.userId,u.emitotal,u.interestrate,u.emipermonth,u.processFee,u.gst,u.loantime,um.bankaccountNo,um.ifsccode,u.amount,u.months,u.status,um.name,um.phone,am.name as agentName"

                datac=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition,"","","")
                datap=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition1,"","","")
                datar=databasefile.SelectQuery("useremiadd as u,usermaster as um,agentmaster as am",column,WhereCondition2,"","","")
                for i in datac['result']:
                    completed.append(i)
                pending=[]
                for i in datap['result']:
                    pending.append(i)
                rejected=[]
                for i in datar['result']:
                    rejected.append(i)

                result={}
                result['completed']=completed
                result['pending']=pending
                result['rejected']=rejected

                print(result,"qwws")
                r=d(result)
                t={}
                t['result']=r
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    elif event['path'] == "/deleteuser":
        print("www")
        if event['httpMethod'] == "POST":
            
            p=event['headers']['Authorization']
            pdn=p.split(" ")
            print(pdn[1])
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['userId']

           
            
           
            column="name"
            WhereCondition= "  and token = '" + str(pdn[1])+ "'"
            data = databasefile.SelectQuery("adminmaster",column,WhereCondition,"","","")
            print(data)
            if data['status'] !='false':
                column="status='" +str(1)+ "'"
                whereCondition= "  and userId = '" + str(userId)+ "' "
                output=databasefile.UpdateQuery("usermaster",column,whereCondition)
 
            
               
               
                t={}
                t['result']="User Deleted successfully"
                hpp=d(t)
                print({'statusCode':200,'body':hpp})
                return {'statusCode':200,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps(hpp)}
            else:
                return {'statusCode':301,'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },'body':json.dumps({'result':'token got expired Please login again ,Either  Please enter Correct token'})}
    
    elif event['path'] == "/loanverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            accountNo=i['accountNo']
            agentId=i['agentId']


            print(userId)
            print(agentId)
            
            column="loanverfication='" +str(1)+ "'"
            whereCondition= "  and agentId = '" + str(agentId)+ "'  and accountNo='"+str(accountNo)+"'"
            output=databasefile.UpdateQuery("usermaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='verified Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'body':json.dumps(hpp)}
    elif event['path'] == "/mobileverfication":
        print("www")
        if event['httpMethod'] == "POST":
            t=type(event['body'])
            print(event['body'])
            print(t)
            i=json.loads(event['body'])
            print(i)
            print(type(i))
            userId=i['agentId']

            print(userId)
            
            column= "mobileverfication='" +str(1)+ "'"
            whereCondition = "  and agentId = '" + str(userId)+ "' "
            output=databasefile.UpdateQuery("agentmaster",column,whereCondition)
                       
            if output!='0':
                t={ }
                t['result']='verified Successfully'
                hpp=d(t)
                                    
                return {'statusCode':200,'body':json.dumps(hpp)}




    else:
        print("qwqw")
        