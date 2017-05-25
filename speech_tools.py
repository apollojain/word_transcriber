import speech_recognition as sr
import os
import process_helpers as ph

final_string = ''
filename = 'result.docx'

def active_listen():
 
    r = sr.Recognizer()
    with sr.Microphone() as src:
     	audio = r.listen(src)
    msg = ''
    try:
        msg = r.recognize_google(audio) 
	print (msg.lower())
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google STT; {0}".format(e))
    except:
        print("Unknown exception occurred!")
    finally:
        return msg.lower()

def active_speech(text):
    os.system('say ' + text)

def instructions():
    active_speech('Instructions are simple. For each new piece of text you want, speak into the microphone.')
    active_speech('To make a header, say header.')
    active_speech('To start a new paragraph, say paragraph. It will be indented automatically.')
    active_speech('To just add more text, say text')
    active_speech('If you would like to see a preview, say preview.')
    active_speech('Otherwise, if you would like to end the document, say end.')
    active_speech('Your current document will appear in an asynchronous preview that will be converted to microsoft word format later.')

def take_input():
    global final_string
    global filename
    print filename
    active_speech('Say a command.')
    result = active_listen()
    if result == 'hdr':
        active_speech('What size header would you like? Small, medium, or large?')
        size = active_listen()
        if size in ['small', 'medium', 'large']:
            active_speech('Say what you would like in the header')
            header = active_listen()
            active_speech('Is that correct?')
            response = active_listen()
            if response == 'yes':
                final_string += '||' + size + '||' + header.capitalize()
            else: 
                active_speech('We are sorry. Try that again.')
        else:
            active_speech('We are sorry. We do not recognize this font size.')
    elif result == 'paragraph':
        final_string += '||pr||\n\t'
    elif result == 'text':
        active_speech('Speak a sentence')
        sentence = active_listen()
        active_speech('Is that correct?')
        response = active_listen()
        if response == 'yes':
            final_string += ' ' + sentence.capitalize() + '.'
        else: 
            active_speech('We are sorry. Try that sentence again.')
    elif result == 'image':
        active_speech('Say the keyword that you would like to be searched.')
        keyword = active_listen()
        ph.find_flickr_photo(keyword)
        active_speech('An image of this keyword has been added to the document.')
    elif result == 'preview':
        active_speech('OK. Opening preview.')
        ph.preview(final_string, filename)
    elif result == 'end':
        active_speech('Thank you for using the word document transcriber.')
        ph.process_string_to_doc(final_string, filename)
        active_speech('The document has been saved to ' + filename)
        return
    else: 
        active_speech('We are sorry. We did not recognize this command. Please try again.')
    take_input()

def ping_pong():
    global filename
    active_speech('Welcome to the speech to word document transcriber.')
    active_speech('Would you like to hear instructions?')
    result = active_listen()
    if result == 'yes':
        instructions()
    active_speech('Would you like to begin?')
    result = active_listen()
    if result == 'yes':
        active_speech('What would you like to call the document?')
        result = active_listen()
        filename = '_'.join(result.split(' ')) + '.docx'

        active_speech('The document you picked is' + filename + '. ok. lets begin.')
        take_input()
    else: 
        active_speech('alright. goodbye.')

if __name__ == '__main__':
    ping_pong()