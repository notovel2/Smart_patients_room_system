from firebase import firebase

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