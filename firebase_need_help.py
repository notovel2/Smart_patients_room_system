from firebase import firebase
from datetime import datetime
from datetime import timedelta
def init():
    print("Connecting to firebase")
    firebaseRef = firebase.FirebaseApplication('https://winnerfirebase.firebaseio.com/')
    return firebaseRef
def getData():
    firebaseRef = init()
    print("Getting data")
    result = firebaseRef.get('/need_help', None)
    print(result)
    return result
def putData(name,value):
    firebaseRef = init()
    print("Putting data")
    result = firebaseRef.put('/need_help',name,value)
    #print(result)
def postData(command,room):
    firebaseRef = init()
    print("Posting data")
    time_now = str(datetime.now()+timedelta(days=1))
    data = {'time': time_now,
            'command': command}
    #result = firebaseRef.post("/need_help",room,{'time':time_now},{'command':command},{'room':room})
    result = firebaseRef.post("/LOG/"+room,data)