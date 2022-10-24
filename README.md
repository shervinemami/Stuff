Stuff
=====

Random files that some people might be interested in.

<br>
*measure_typing_rate.py:*
A script to measure instant keyboard typing rate (WPM & CPS). Simply run the script without any args, then type words or characters into it.
I use this for measuring the latency of speech recognition typing rates. There are many online WPM tools but they usually require 60 seconds of typing, whereas this tool will print the speed between each character or word, hence is handy for doing small tests.


<br>
*run_kaldi.sh:*
Calling the "run_kaldi.sh" script starts or stops Kaldi AG.
eg: `/Core/SpeechRec/Kaldi_Dragonfly/run_kaldi.sh &`


<br>
*process_retained.py:*
I save a lot of my speech recognition recordings from Kaldi-active-grammar / Dragonfly into a "retain.tsv" file. I normally run the "process_retained.py" script using this command, to remove my noise utterances every few months:
```
(cd /Core/SpeechRec/Kaldi_Dragonfly/ ; python3 ./process_retained.py ; cp retained/retain.tsv retained/retain.tsv.old ; mv retained/processed.tsv retained/retain.tsv)
```


<br>
"crucial.bashrc" is the most important parts of my Linux .bashrc script, since it allows me to find commands instantly and to know if a command gave a hidden error or not. Just copy-paste the content into your .bashrc file (tested on Ubuntu, Linux Mint, Debian and Arch) if you want the same feature. The screenshot of my KDE desktop shows an example in the top-right window where you can see it highlights my commands in green unless if it had an error in which case it highlights the next command as red.

![Screenshot of my KDE Desktop showing the shell prompt highlighting in green & red in the top-right window](https://raw.githubusercontent.com/shervinemami/Stuff/master/Screenshot_KDE_Desktop.png)
