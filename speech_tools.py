import speech_recognition as sr
import os
import process_helpers as ph


final_string = ''
filename = 'result.docx'
label = False
extras = None
def modify_text(text, extras):
    old_text = str(extras['canvas'].itemcget(extras['text2'], 'text'))
    extras['canvas'].itemconfig(extras['text1'], text=old_text)
    extras['canvas'].itemconfig(extras['text2'], text=text)

def active_listen(extras=None):
    r = sr.Recognizer()
    with sr.Microphone() as src:
     	audio = r.listen(src)
    msg = ''
    try:
        msg = r.recognize_google(audio) 
    except sr.UnknownValueError:
        modify_text("Google Speech Recognition could not understand audio", extras)
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google STT; {0}".format(e))
    except:
        print("Unknown exception occurred!")
    finally:
        modify_text(msg.lower(), extras)
        return msg.lower()

def active_speech(text, extras=None):
    modify_text(text, extras)
    os.system('say ' + text)

def instructions(extras=None):
    active_speech('Instructions are simple. For each new piece of text you want, speak into the microphone.', extras)
    active_speech('To make a header, say header.', extras)
    active_speech('To start a new paragraph, say paragraph. It will be indented automatically.', extras)
    active_speech('To just add more text, say text', extras)
    active_speech('If you would like to see a preview, say preview.', extras)
    active_speech('Otherwise, if you would like to end the document, say end.', extras)
    active_speech('Your current document will appear in an asynchronous preview that will be converted to microsoft word format later.', extras)

def take_input(extras=None):
    global final_string
    global filename
    global label
    active_speech('Say a command.', extras)
    result = active_listen(extras)
    if result == 'header':
        active_speech('What size header would you like? Small, medium, or large?', extras)
        size = active_listen(extras)
        if size in ['small', 'medium', 'large']:
            active_speech('Say what you would like in the header', extras)
            header = active_listen(extras)
            active_speech('Is that correct?', extras)
            response = active_listen(extras)
            if response == 'yes':
                final_string += '||' + size + '||' + header.capitalize()
            else: 
                active_speech('We are sorry. Try that again.', extras)
        else:
            active_speech('We are sorry. We do not recognize this font size.', extras)
        label = False
    elif result == 'paragraph':
        final_string += '||pr||\n\t'
        label = True
    elif result == 'text':
        active_speech('Speak a sentence', extras)
        sentence = active_listen(extras)
        active_speech('Is that correct?', extras)
        response = active_listen(extras)
        if response == 'yes':
            final_string += ' ' + sentence.capitalize() + '.'
        else: 
            active_speech('We are sorry. Try that sentence again.', extras)
        label = False
    elif result == 'image':
        active_speech('Say the keyword that you would like to be searched.', extras)
        keyword = active_listen(extras)
        impath = ph.find_flickr_photo(keyword)
        final_string += '||img||' + impath
        active_speech('An image of this keyword has been added to the document.', extras)
        label = False
    elif result == 'preview':
        active_speech('OK. Opening preview.', extras)
        ph.preview(final_string, filename)
    elif result == 'end' or result == 'exit':
        active_speech('Thank you for using the word document transcriber.', extras)
        ph.process_string_to_doc(final_string, filename)
        active_speech('The document has been saved to ' + filename, extras)
        # extras['root'].destroy()
        return
    else: 
        active_speech('We are sorry. We did not recognize this command. Please try again.', extras)
    take_input(extras)

def ping_pong(extras=None):
    global filename
    active_speech('Welcome to the speech to word document transcriber.', extras)
    active_speech('Would you like to hear instructions?', extras)
    result = active_listen(extras)
    if result == 'yes':
        instructions(extras)
    active_speech('Would you like to begin?', extras)
    result = active_listen(extras)
    if result == 'yes':
        active_speech('What would you like to call the document?', extras)
        result = active_listen(extras)
        filename = '_'.join(result.split(' ')) + '.docx'

        active_speech('The document you picked is ' + filename + '. Is this correct?', extras)
        answer = active_listen(extras)
        while answer != 'yes':
            filename = '_'.join(result.split(' ')) + '.docx'
            active_speech('What would you like to call the document?', extras)
            result = active_listen(extras)
            filename = '_'.join(result.split(' ')) + '.docx'

            active_speech('The document you picked is ' + filename + '. Is this correct?', extras)
            answer = active_listen(extras)  
            
        take_input(extras)
    else: 
        active_speech('alright. goodbye.', extras)
        # extras['root'].destroy()

if __name__ == '__main__':
    ping_pong()