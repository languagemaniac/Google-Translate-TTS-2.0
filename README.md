Google-Translate-TTS 2.0
====================

I modified the original script quite a lot with the help of Chatgpt. Overall here are the changes:

1. Made it work with python 3
2. Changed the api link as I got 404 errors, I guess the api used in the original code doesn't exist anymore
3. Made it support UTF-8, so it's compatible with japanese and chinese and many other languages.
4. Has a welcome screen so instead of having to write a command with arguments you just have to answer 3 questions: Language, speed, and filename. 
5. Added a way for it to download multiple chunks of text simultaneously so it downloads faster, and added a progress bar too
6. Made a Gui version for ease of use.

For more background about the original script, check out this [blog post](http://www.hung-truong.com/blog/2013/04/26/hacking-googles-text-to-speech-api/).

Usage
=====

First, make sure you have install all the necessary dependencies by running "pip install -r requirements.txt" if you're going to use the gui version.
 
Execute "python GoogleTTS.py" in the command line or "GoogleTTS-gui.py" by simply double clicking it.

This is what the gui looks like:

![novel](https://github.com/languagemaniac/Google-Translate-TTS-2.0/assets/43100450/5507441f-fc53-48d0-b092-99a2579ebd24)

Pretty simple.

If accessing from the command line, It will first ask you to choose a language by inputting a number.

Then it's going to ask you at which speed do you want your document to be read. 

Here's what [a sentence](https://www.google.com/speech-api/v1/synthesize?text=%22This%20is%20an%20example%20sentence%20at%20a%20speed%20of%20zero%20point%20four%22&enc=mpeg&lang=en-us&speed=0.4&client=lr-language-tts&use_google_only_voices=1) in english sounds like at a speed value of 0.4

Here's what [a sentence](https://www.google.com/speech-api/v1/synthesize?text=%22This%20is%20an%20example%20sentence%20at%20a%20speed%20of%200.5%22&enc=mpeg&lang=en-us&speed=0.5&client=lr-language-tts&use_google_only_voices=1) in english sounds like at a speed value of 0.5

Useful if you're learning a new language

Then it's going to ask you for the filename of your novel. So just place your novel in txt format and either select it from the gui, or place it in the same folder as the non-gui version, and type its name. eg. mynovel.txt

Now it will download the audio for your novel and save it with the same file name base, as an mp3. In this case mynovel.mp3
 

Note
=====
If the language you want to select, is not on the list, open an issue and I'll add it

The number of simultaneous downloads can be changed by altering the "max_workers" number in the code. Currently set to 20.
