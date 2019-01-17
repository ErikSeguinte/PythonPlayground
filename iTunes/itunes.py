import re, argparse
import sys
from matplotlib import pyplot
import plistlib
import numpy as np


def findDuplicates(filename):
    plist = plistlib.load(filename)
    tracks = plist['Tracks']
    trackNames = dict()

    for trackid, track in tracks.items():
        try:
            name = track['name']
            duration = track['duration']

            if name in trackNames:
                if duration // 1000 == trackNames[name][0] // 1000:
                    count = trackNames[name][1]
                    trackNames[name] = (duration, count + 1)
                else:
                    trackNames[name] = (duration, 1)

        except:
            pass

    dups = []
    for k, v in trackNames.items():
        if v[1] > 1:
            dups.append((v[1], k))

    if len(dups) > 0:
        print("Found %d duplicates. Track names saved to dup.txt" % len(dups))
    else:
        print("No duplicates found")

    with open("dups.txt", "w", encoding="utf8") as f:
        for val in dups:
            f.write("[%d] %s\n" % (val[0], val[1]))


def findCommonTracks(fileNames):
    trackNameSets = []
    for fileName in fileNames:
        trackNames = set()
        with open(fileName, "rb") as f:
            plist = plistlib.load(f)
            tracks = plist["Tracks"]

            for trackID, track in tracks.items():
                try:
                    trackNames.add(track['Name'])
                except:
                    pass
            trackNameSets.append(trackNames)
    commonTracks = set.intersection(*trackNameSets)

    if len(commonTracks) > 0:
        with open("common.txt", "w", encoding="UTF-8") as f:
            for val in commonTracks:
                s = "%s\n" % val
                f.write(s)
        print("%d common tracks found. "
              "Track names written to common.txt." % len(commonTracks))
    else:
        print("No common tracks!")

def plotStats(fileName):
    tracks = None
    with open(fileName, "rb") as f:
        plist = plistlib.load(f)
        tracks = plist['Tracks']

    ratings = []
    durations = []

    for trackID, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass


    if ratings == [] or durations ==[]:
        print("No valid data in %s" % fileName)
        return

    x = np.array(durations, np.int32)
    x = x/60000.0
    y = np.array(ratings, np.int32)

    pyplot.subplot(2, 1, 1)
    pyplot.plot(x,y, 'o')
    pyplot.axis([0,1.05*np.max(x), -1, 110])
    pyplot.xlabel('Track Duration')
    pyplot.ylabel('Track rating')

    pyplot.subplot(2, 1, 2)
    pyplot.hist(x, bins=20)
    pyplot.xlabel('Track duration')
    pyplot.ylabel('Count')

    pyplot.show()

def main():
    # create parser
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """

    parser = argparse.ArgumentParser(description=descStr)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--common', nargs='*', dest='plFiles', required=False)
    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFiles:
        findCommonTracks(args.plFiles)
    elif args.plFile:
        plotStats(args.plFile)
    elif args.plFileD:
        findDuplicates(args.plFileD)

    else:
        print ("These are not the tracks you are looking for")

# main method
if __name__ == '__main__':
    main()