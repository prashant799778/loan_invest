
import razorpay 
order_receipt = 'order_rcptid_11'


order_amount="100"
order_currency = 'INR'

client = razorpay.Client(auth=("rzp_live_9c3OoVSfu1c23s", "0q9HXWoHFtCkKkrQkw5hlKbM"))
clientId=client.order.create({"amount":order_amount, "currency":order_currency, "receipt":order_receipt, "payment_capture":'0'})

o=client.order.fetch(clientId['id'])
print(o,"sss")
u=client.order.payments("order_FksC1Fb5IfzM3o")
print(u,"sws")
