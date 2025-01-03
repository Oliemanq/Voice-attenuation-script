import main

def testOutput():
    sessionsList = []
    sessions = main.AudioUtilities.GetAllSessions()
    for sess in sessions:
        if sess.Process:
            sessionsList.append(sess.Process.name())
            print(sess.Process.name())

