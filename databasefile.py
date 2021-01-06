
from connection import DBconnection


import json
import smtplib 

#success message for crud operation
def Successmessage(type):
    if type == "insert":
        output ="Record Inserted Successfully"
    elif type == "update":
        output ="Record Updated Successfully"
    elif type == "delete":
        output ="Record Deleted Successfully"

    return output

def InsertQuery(table,columns,values):
    try:
        
        query = " insert into " + table + " (" + columns + ") values(" + values + ");" 
        print(query)
        con = DBconnection()
        cursor = con.cursor()
        cursor.execute(query)            
        con.commit()        
        cursor.close()   

        message = Successmessage('insert')
        data = {"status":"true","message":message,"result":""}       
        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def InsertRtnId(table,columns,values):
    try:
        
        query = " insert into " + table + " (" + columns + ") values(" + values + ");" 
        print(query)
        con = DBconnection()
        cursor = con.cursor()
        cursor.execute(query)     
        Id = cursor.lastrowid
        con.commit()        
        cursor.close()
        message = Successmessage('insert')
        data = {"status":"true","message":message,"result":"","Id":Id}          
              
        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectQueryMaxId(table,columns):
    try:

        query = " select " + columns + " from " + table + " ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
        else:
            data = {"status":"true","message":"No Data Found","result":""}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectQuery1(table,columns,whereCondition):
    try:
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
                
        query = " select " + columns + " from " + table + " " + whereCondition  + "  ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        cursor.close()
      
        if data:
            data={"status":"true","result":data,"message":""}
            return data
        else:
            data = {"status":"False","message":"No Data Found","result":""}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0"   



def SelectQuery4(table,columns,whereCondition):
    try:
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
                
        query = " select " + columns + " from " + table + " " + whereCondition  + "  ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data={"status":"true","result":data,"message":""}
            return data
        else:
            data = {"status":"false","message":"No Data Found","result":""}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0"         

            


def SelectTimeQuery(columns):
    try:         
        query = " select " + columns +" ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
        else:
            data = {"status":"true","message":"No Data Found","result":""}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectQuery(table,columns,whereCondition,groupby,startlimit,endlimit):
    try:
        limitCondition= ""
        
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if startlimit != "" and endlimit != "":
            limitCondition = "limit "+startlimit+","+endlimit
            #whereCondition = " where 1=1 and " + whereCondition
        
        if groupby != "":
            groupby = " group by " + groupby
                
        query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby +" "+ limitCondition +" ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
        else:
            data = {"status":"false","message":"No Data Found","result":[]}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectQueryOrderbyAsc(table,columns,whereCondition,groupby,orderby,startlimit,endlimit):
    try:
        limitCondition= ""
        
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if startlimit != "" and endlimit != "":
            limitCondition = "limit "+startlimit+","+endlimit
            whereCondition = " where 1=1  and " + whereCondition
        
        if groupby != "":
            groupby = " group by " + groupby

        if orderby != "":
            orderby = " order by " + orderby            
                
        query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby +" "+ orderby + limitCondition +" ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
        else:
            data = {"status":"true","message":"No Data Found","result":""}

        return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectQueryOrderbyNew(table,columns,whereCondition,groupby,startlimit,endlimit,orderby):
    try:
        limitCondition= ""
        

        if orderby != "":
            orderby = " order by " + orderby + " DESC "  
        if groupby != "":
            groupby = " group by " + groupby

        print("startlimit"+str(startlimit))
        print("endlimit"+str(endlimit))

        #if startlimit == 0 and endlimit == 0:
        query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby +" "+ orderby + limitCondition +" ;"
        #else:
        #if whereCondition != "" and startlimit != "0":
            #whereCondition = " where 1=1 " + whereCondition
        #if startlimit != "" and endlimit != "":
            #limitCondition = "  limit "+startlimit+","+endlimit
            
        print(orderby)    
                    
            # query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby +" "+ orderby + limitCondition +" ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
            return data
        else:
            data ={"status":"true","message":"No data Found","result":""}
            return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 


def SelectQueryOrderby(table,columns,whereCondition,groupby,startlimit,endlimit,orderby):
    try:
        limitCondition= ""
                     
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if startlimit != "" and endlimit != "":
            limitCondition = "  limit "+startlimit+","+endlimit
        if orderby != "":
            orderby = " order by " + orderby + " DESC "  
        if groupby != "":
            groupby = " group by " + groupby

        print(orderby)    
                
        query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby +" "+ orderby + limitCondition +" ;"

        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
      
        if data:
            data = {"status":"true","message":"","result":data}
            return data
        else:
            data ={"status":"true","message":"No data Found","result":""}
            return data

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 


def rtnJsonFormatData(table,columns,whereCondition,groupby):
    try:
        groupby = ""
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if groupby != "":
            groupby = " group by " + groupby
                
        query = " select " + columns + " from " + table + " " + whereCondition  + " " + groupby + ";"
        
        print(query)
        con = DBconnection()      
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        print(data)        
        if data:
            return data
        else:
            return "0"

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectTotalCountQuery(table,whereCondition,groupby):
    try:
        groupby = ""
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if groupby != "":
            groupby = " group by " + groupby
               
        query = " select count(*) as count from " + table + " " + whereCondition  + " " + groupby  + ";"
        print(query)
        con = DBconnection()
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()  
        print(data)
        cursor.close()   

        if data:
            data = json.loads(json.dumps(data))                                 
            return str(data[0]["count"])
        else:
            return "0"

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def SelectCountQuery(table,whereCondition,groupby):
    try:
        groupby = ""
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if groupby != "":
            groupby = " group by " + groupby
               
        query = " select count(1) as count from " + table + " " + whereCondition  + " " + groupby  + ";"
        print(query)
        con = DBconnection()
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()  
        cursor.close()   

        if data:
            data = json.loads(json.dumps(data))                                 
            return str(data[0]["count"])
        else:
            return "0"

    except Exception as e:
        print("Error--->" + str(e))            
        return "0" 

def rtnsum(table,column,whereCondition,groupbycolumns):
    try:     
        groupby = "" 
        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition
        if groupbycolumns != "":
            groupby = " group by " + groupbycolumns
              
        query = " select sum("+column+") as total from " + table + " " + whereCondition  + " " + groupby  + ";"
        print(query)
        con = DBconnection()
        cursor = con.cursor()
        cursor.execute(query)
        data = cursor.fetchall()  
        cursor.close()   

        if data:
            data = json.loads(json.dumps(data))                                 
            return str(data[0]["total"])
        else:
            return "0"

    except Exception as e:
        print("Error--->" + str(e))            
        return "0"

def UpdateQuery(table,columns,whereCondition):
    try:

        if whereCondition != "":
            whereCondition = " where 1=1  " + whereCondition  

        if columns != "":   
            query = " update " + table + " set " + columns  + " " + whereCondition  + ";"             
            print(query)
            con = DBconnection()
            cursor = con.cursor()         
            cursor.execute(query)
            con.commit()
            cursor.close()
              
            message = Successmessage('update')
            data = {"status":"true","message":message,"result":""}
            return data
        else:
            return "0"

    except Exception as e:
        print("Error--->" + str(e))            
        return "0"

def DeleteQuery(table,whereCondition):
    try:

        if whereCondition != "":
            whereCondition = " where 1=1 " + whereCondition        

            query = " delete from " + table + " " + whereCondition + ";" 
            print(query)
            con = DBconnection()
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()

            query = " alter table " + table + " " + " AUTO_INCREMENT = 0 " + ";" 
            print(query)
            con = DBconnection()
            cursor = con.cursor()
            cursor.execute(query)
            con.commit()
            cursor.close()            

            message = commonfile.Successmessage('delete')
            data = {"status":"true","message":message,"result":""}
            return data

        else :
            return "0"
                
    except Exception as e:
       print("Error--->" + str(e))            
       return "0"

def SendEmail(emailto,subject,message):
       
    message = Mail(
    from_email = 'abcd@gmail.com',
    to_emails = str(email),
    subject = "Account Verification",
    html_content = '<strong> Click on the Link Given:' +  + ' </strong> <br> .<br> Thanks, FandomLive Team')
    print(message)

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
       
        return "1" 
            
    except Exception as e:
        print("Error--->" + str(e))            
        return "0"

