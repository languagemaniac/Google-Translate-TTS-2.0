Google-Translate-TTS
====================

I modified the original script quite a lot with the help of Chatgpt. Overall here are the changes:

1. Made it work with python 3
2. Changed the api link as I got 404 errors, I guess the api used in the original code doesn't exist anymore
3. Made it support UTF-8, so it's compatible with japanese and chinese and many other languages.
4. Has a welcome screen so instead of having to write a command with arguments you just have to answer 3 questions: Language, speed, and filename. 
5. Added a way for it to download multiple chunks of text simultaneously so it downloads faster, and added a progress bar too

For more background about the original script, check out this [blog post](http://www.hung-truong.com/blog/2013/04/26/hacking-googles-text-to-speech-api/).

Usage
=====
 
Execute "python GoogleTTS.py"

It will first ask you to choose a language by inputing a number. (If the language you want to select, is not on the list, open an issue and I'll add it)
Then it's goint to ask you at which speed do you want your document to be read. 

Here's what [a sentence](https://www.google.com/speech-api/v1/synthesize?text=%22This%20is%20an%20example%20sentence%20at%20a%20speed%20of%20zero%20point%20four%22&enc=mpeg&lang=en-us&speed=0.4&client=lr-language-tts&use_google_only_voices=1) in english sounds like at a speed value of 0.4

Here's what [a sentence](https://www.google.com/speech-api/v1/synthesize?text=%22This%20is%20an%20example%20sentence%20at%20a%20speed%20of%200.5%22&enc=mpeg&lang=en-us&speed=0.5&client=lr-language-tts&use_google_only_voices=1) in english sounds like at a speed of 0.5

Useful if you're learning a new language

Then it's going to ask you for the filename of your novel. I have only tried txt files. So just place your novel in the same folder and type its name. ex. mynovel.txt

Now it will display a progress bar, and it will download the audio for your novel and save it with the same file name base, as an mp3. In this case mynovel.mp3
 

Note
=====
The number of simultaneous downloads can be changed by altering the "max_workers" number in the code. Currently set to 20.
