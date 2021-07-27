Stuff
=====

Random files that some people might be interested in.

<br>
Calling the "run_kaldi.sh" script starts or stops Kaldi AG.

eg: `/Core/SpeechRec/Kaldi_Dragonfly/run_kaldi.sh &`

Whereas I normally run the "process_retained.py" script using this command, to remove my noise utterances every few months:

```
(cd /Core/SpeechRec/Kaldi_Dragonfly/ ; python3 ./process_retained.py ; cp retained/retain.tsv retained/retain.tsv.old ; mv retained/processed.tsv retained/retain.tsv)
```


<br>
"crucial.bashrc" is the most important parts of my Linux .bashrc script, since it allows me to find commands instantly and to know if a command gave a hidden error or not. Just copy-paste the content into your .bashrc file (tested on Ubuntu, Linux Mint, Debian and Arch) if you want the same feature. The screenshot of my KDE desktop shows an example in the top-right window where you can see it highlights my commands in green unless if it had an error in which case it highlights the next command as red.

![Screenshot of my KDE Desktop showing the shell prompt highlighting in green & red in the top-right window](https://raw.githubusercontent.com/shervinemami/Stuff/master/Screenshot_KDE_Desktop.png)
