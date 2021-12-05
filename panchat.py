#!/usr/bin/env python3
# pan - 11/21/21

'''
#############################################
def getspeechfromfile(thefile)
# get speech from recorded audio in a .WAV file
import speech_recognition as sr
import sys

# filename = thefile
# filename = "whatsthetemperaturerightnowinankenyiowa.wav"
filename = "WakingUp_083121.wav"
outfile = "x.txt"
sys.stdout = open(outfile, 'w')
# initialize the recognizer
r = sr.Recognizer()
# open the file
with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source,duration=130)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)
'''


'''
    wave_file_path = "WakingUp_083121.wav"
    outfile = "x.txt"
    print(splitbigaudio(wave_file_path), file=open(outfile, 'a'))

    def savespeechtofile():
        """Saving Voice to a file"""
        # On linux make sure that 'espeak' and 'ffmpeg' are installed
        engine.save_to_file(speech, 'x.mp3')
        engine.runAndWait()
        return ()
    return()
'''


'''
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   engine.say('The quick brown fox jumped over the stoopid lazy fat stinkin schwinehoonda.')
engine.runAndWait()
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
#print(rate)                        #printing current voice rate
engine.setProperty('rate', rate)     # setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print(volume)                          #printing current volume level
engine.setProperty('volume',volume)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

engine.say("Hello mister Nye!")
engine.say('My current speaking rate is ' + str(rate))
engine.say('My voice volume is ' + str(volume))

engine.runAndWait()
engine.stop()
'''


#############################################
def listenonmicrophone():
    # Record from microphone
    import pyaudio
    import speech_recognition as sr
    #
    r = sr.Recognizer()
    audiotext = ""
    #
    while not audiotext:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1.2)
            print('\t\tI\'m listening...')
            audio = r.listen(source, timeout=0)
            try:
                audiotext = (r.recognize_google(audio))
            except Exception as e:
                pass
            #    print("No audio detected :  " + str(e))
            #
            # with open("recorded.wav", "wb") as f:
            #    f.write(audio.get_wav_data())
    return audiotext


#############################################
def splitbigaudio():
    import speech_recognition as sr
    import os
    from pydub import AudioSegment
    from pydub.silence import split_on_silence

    # create a speech recognition object
    r = sr.Recognizer()

    # a function that splits the audio file into chunks
    # and applies speech recognition
    def get_large_audio_transcription(path):
        """
        Splitting the large audio file into chunks
        and apply speech recognition on each of these chunks
        """
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)
        # split audio sound where silence is xxxx miliseconds or more and get chunks
        chunks = split_on_silence(sound,
                                  # experiment with this value for your target audio file
                                  min_silence_len=1000,
                                  # adjust this per requirement
                                  silence_thresh=sound.dBFS - 14,
                                  # keep the silence for 1 second, adjustable as well
                                  keep_silence=2000,
                                  )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        txt = ''
        # process each chunk
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    txt = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    txt = f"{txt.capitalize()}. "
                    # print(chunk_filename, ":", txt)
                    txt += txt
        # return the text for all chunks detected
        return txt
    return


#############################################
def printvoices():
    import pyttsx3
    # import gtts
    # import tts-watson_developer_cloud
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #
    for voice in voices:
        print("Voice:")
        print("ID: %s" % voice.id)
        print("Name: %s" % voice.name)
        print("Age: %s" % voice.age)
        print("Gender: %s" % voice.gender)
        print("Languages Known: %s" % voice.languages)


#############################################
def say(wordsfromopenai):
    import pyttsx3
    #
    engine = pyttsx3.init()  # object creation
    rate = 150
    volume = 1
    #
    engine.setProperty('rate', rate)  # setting up new voice rate
    engine.setProperty('volume', volume)  # setting up volume level  between 0 and 1
    voices = engine.getProperty('voices')  # getting details of current voice
    engine.setProperty('voice', voices[0].id)  # changing index, changes voices. 1 for female
    #
    engine.say(wordsfromopenai)
    #
    engine.runAndWait()
    engine.stop()
    #
    return


#############################################
def callopenai(you):
    #
    import openai
    import os
    #
    # lets use host environment to manage openai keys.
    # Set the environment keys here for convenience while testing.  Set them
    # in the env shell for security
    #
    from dotenv import load_dotenv
    load_dotenv()
    #
    # move .env.example to .env to use with dotenv
    openaikey = os.environ['OPENAPIKEY']
    openaiorg = os.environ['OPENAPIORG']
    #
    openai.api_key = openaikey
    openai.organization = openaiorg
    # You'll need your own openai.com API keys.  I rotate mine often.
    #
    # https://beta.openai.com/docs/api-reference/completions/create#completions/create-engine_id
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=you,
        temperature=.1,
        # prompt and response token length cannot exceed 2048
        max_tokens=2000,
        top_p=.9,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    return response.choices[0].text


#############################################
def prettyprint(who, openaiwords):
    #
    import textwrap
    #
    print(":", who, ":")
    wrapper = textwrap.TextWrapper(width=40, initial_indent='     ', subsequent_indent='     ')
    word_list = wrapper.wrap(text=openaiwords)
    # Print each line.
    for element in word_list:
        print(f'{element}')
    return


# main() #####################################
while True:
    humantext = listenonmicrophone()
    if humantext:
        prettyprint("You", humantext)
        openairesponse = callopenai(humantext)
        prettyprint("AI", openairesponse)
        say(openairesponse)

