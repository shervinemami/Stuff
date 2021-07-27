# Performs various post-processing operations of the "retain.tsv" file and associated wav files.
#   * Deletes single misrecognition lines from the TSV file.
#   * Deletes ranges of lines between "begin_misrecognition_mode" until "misrecognition" from the TSV file.
#   * Deletes NoiseRule lines from the TSV file.
#   * Deletes the most recent actual recognition, everytime it sees a "misrecognition" tag in a NoiseRule. Allows user to tag a misrecognition even if there's noise utterances in between the misrecognition and the tag.
#   * Deletes all wav files from filesystem that aren't listed in the processed TSV file.
# By Shervin Emami (shervin.emami@gmail.com), 2020.

import time
import os

inFilename = "retained/retain.tsv"
outFilename = "retained/processed.tsv"

# Convert filename such as "retained/retain_2020-05-05_18-05-36_665975.wav" into a timestamp
def getSecondsSince2000(filename):
    index = 16    # Position of the year string within the filename string
    year = int(filename[index:index+4])
    index += 5
    month = int(filename[index:index+2])
    index += 3
    day = int(filename[index:index+2])
    index += 3
    hours = int(filename[index:index+2])
    index += 3
    minutes = int(filename[index:index+2])
    index += 3
    seconds = int(filename[index:index+2])
    index += 3
    days_since_2000 = (year-2000) * 365 + month * 30 + day   # Each month is roughly 30 days right :-)
    seconds_since_2000 = days_since_2000 * (24*60*60) + hours * (60*60) + minutes * (60) + seconds
    return seconds_since_2000

def removeBadFilesFromTSV():
    print("Deleting files that are misrecognitions ...")
    total = 0
    num_recognitions = 0
    list_of_filenames = []
    with open(inFilename, "r") as f:
        data = f.readlines()

        outputList = []
        removeNextLines = False
        for line in data:

            words = line.split('\t')
            print(words)
            filename = words[0]
            duration = words[1]
            ruleType = words[3]
            phrase = words[4]
            tag = words[6]

            # Convert filename such as "retained/retain_2020-05-05_18-05-36_665975.wav" into a timestamp
            seconds_timestamp = getSecondsSince2000(filename)

            # Ignore the grammars we don't want, including Dragon dictation in Shervin's custom dual microphone mode
            removeThisLine = False
            if (ruleType == "IgnoredRule" or ruleType == "NoiseRule"):
                removeThisLine = True
            # Ignore lines with "misrecognition" tag
            if (tag == "misrecognition"):
                removeThisLine = True

            # Remove lines marked as bad, and everything between "begin_misrecognition_mode" until "misrecognition".
            if (removeNextLines or removeThisLine):
                print("    Deleting ", words)
                try:
                    os.remove(filename)
                except:
                    pass
            else:
                # Process the line
                duration_f = float(duration)
                total = total + duration_f
                num_recognitions = num_recognitions + 1

                # Remember the line in the output file, so we can write it into the TSV file later
                outputList.append(line)

                # Remember the filename
                list_of_filenames.append(filename)

            # If we have a misrecognition tag on a NoiseRule, then delete the most recent proper line, not just the noise line. Instead of searching backwards for the most recent
            # non-NoiseRule line, we can simply delete the latest outputList entry
            if (tag == "misrecognition" and ruleType == "NoiseRule"):
                outputList.pop()

            # Check if we should change modes
            if (tag == "begin_misrecognition_mode"):
                # Delete all the next lines
                removeNextLines = True
                removeNextLines_timestamp = seconds_timestamp
                removeNextLines_filename = filename
            if (tag == "misrecognition"):
                # Stop deleting the next lines
                removeNextLines = False
            if removeNextLines:
                # Put a timeout on misrecognition ranges
                if seconds_timestamp > removeNextLines_timestamp + 60:
                    print("WARNING: begin_misrecognition_mode of", removeNextLines_filename, "has been running for", (seconds_timestamp - removeNextLines_timestamp), "seconds! Assuming the closing misrecognition tag was missing and thus accepting recognitions from here on.")
                    # Stop deleting the next lines
                    removeNextLines = False

        # Store the actual output file
        with open(outFilename, "w") as wf:
            for line in outputList:
                wf.write(line)

    return num_recognitions, total, list_of_filenames


def removeFilesInFolderThatArentInTSV(list_of_filenames):
    import glob
    #print(list_of_filenames)
    print("Deleting files in 'retained' folder that aren't in the TSV file of", len(list_of_filenames), "names ...")
    for filename in glob.glob("retained/retain_*.wav"):
        if filename not in list_of_filenames:
            print("    Deleting unused file", filename)
            try:
                os.remove(filename)
            except:
                pass




num_recognitions, total, list_of_filenames = removeBadFilesFromTSV()
print()
removeFilesInFolderThatArentInTSV(list_of_filenames)
time_str = time.strftime('%H hours, %M mins, %S seconds', time.gmtime(total))
print()
print(int(total), "seconds across", num_recognitions, "utterances means", time_str)
print("Stored processed output file as '" + outFilename + "'")
print()
