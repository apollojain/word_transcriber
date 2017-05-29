import sys
import speech_tools as st
from threading import Timer

if sys.version_info < (3, 0):
    # Python 2
    import Tkinter as tk
else:
    # Python 3
    import tkinter as tk
root = tk.Tk()
root.title("WordDocTranscriber")
# computer_text = tk.Text(root)
# user_text = tk.Text(root)
# computer_text.insert(tk.INSERT, "This is the computer's response")
# user_text.insert(tk.END, "This is your response")


canvas = tk.Canvas(width = 700, height = 450, bg = 'yellow')
canvas.pack(expand = tk.YES, fill = tk.BOTH)
text1 = canvas.create_text(10, 100,fill="darkblue", anchor=tk.NW, font="Times 20 italic bold",
                        text="Word Document Speech to Text Transcriber", width=380)
text2 = canvas.create_text(10, 200,fill="darkblue", anchor=tk.NW, font="Times 20 italic bold",
                        text="Word Document Speech to Text Transcriber 3", width=380)
dictionary = {}
dictionary['root'] = root
dictionary['canvas'] = canvas
dictionary['text1'] = text1
dictionary['text2'] = text2
t = Timer(0.01, st.ping_pong, [dictionary])
print "what"
t.start()
# canvas.create_image(200, 10, image = 'recorder.gif', anchor = tk.fNW)
# tk.Button(root, text="Make me a Sandwich").pack()
tk.mainloop()
