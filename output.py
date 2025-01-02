import input

sessionsList = []
sessions = input.AudioUtilities.GetAllSessions()
for sess in sessions:
    if sess.Process:
        sessionsList.append(sess.Process.name())
        print(sess.Process.name())

