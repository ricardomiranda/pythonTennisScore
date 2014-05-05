#!/usr/bin/python

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# (c) Ricardo Cristovao Miranda, 2014, mail@ricardomiranda.com

"""
The program should take two arguments on the command line:
 respectively the name of an input file and the name of an output
 file.
Each line of the input file is a description of a tennis match
 between two players named 'A' and 'B', and comprises a sequence
 of 'A's and 'B's which indicates the winner of each point in the
 match in the order that they are played.
For each line in the input, the program should write a line to
 the output in the format:
  [completed set scores] [score in current set] [score in current game]
"""

import sys, getopt

class tennisScores(object):
    playerA = 0
    playerB = 1

    serving = playerA

    score        =[(0, 0)]
    currentScore = (0, 0)
    games        = [0, 0]

    def __init__(self):
        self.clearScores()

    def clearScores(self):
        serving = self.playerA

        self.score = [(0, 0)]
        self.currentScore = [0, 0]
        self.games = [0, 0]

    def newTennisGame(self, scoresString):
        """
        Entry point for this class
        """
        self.calcScores(scoresString) if scoresString else self.noGame()

        return self.printResults()

    def switchService(self):
        self.serving = self.otherPlayer(self.serving)

    def otherPlayer(self, player):
        return (player + 1) % 2

    def calcScores(self, scoresString):
        xs = list(scoresString)
        [self.addPoint(x) for x in xs]

    def addPoint(self, x):
        if x == 'A':
            player = self.playerA
            otherPlayer = self.playerB
        else:
            player = self.playerB
            otherPlayer = self.playerA

        self.games[player] = self.calcPoints(self.games[player], self.games[otherPlayer])
        if self.games[player] == 0:
            self.currentScore[player] = self.addGame(self.currentScore[player])
        if (self.currentScore[player] >= 6 and abs(self.currentScore[player] - self.currentScore[otherPlayer]) >= 2):
            self.addSet()


    def calcPoints(self, points, pointsOpponent):
    #I could use a dictionary here...
        if points == 0:
            return 15
        elif points == 15:
            return 30
        elif points == 30:
            return 40
        elif points == 40:
            if pointsOpponent < 40:
                return 0
            elif pointsOpponent == 40:
                return 'A'
            elif pointsOpponent == 'A':
                self.setAdvantageNull()
                return 40
        elif points == 'A':
            return 0

    def setAdvantageNull(self):
        self.games = [40, 40]

    def addGame(self, games):
        self.newGame()
        self.switchService()
        return games + 1

    def addSet(self):
        del self.score[-1]
        self.score.append(tuple(self.currentScore))
        self.score.append((0, 0))
        self.newGame()
        self.newSet()

    def newGame(self):
        self.games = [0, 0]

    def newSet(self):
        self.currentScore = [0, 0]

    def noGame(self):
        self.printResults()

    def printResults(self):
        player = self.serving
        otherPlayer = self.otherPlayer(self.serving)
        string = ''

        for sc in self.score:
            if sc != (0, 0):
                string = string + str(sc[player]) + "-" + str(sc[otherPlayer]) + ' '

#        if self.currentScore != [0, 0]:
        string = string + str(self.currentScore[player]) + "-" + str(self.currentScore[otherPlayer]) + ' '

        if self.games != [0, 0]:
            string = string + str(self.games[player]) + "-" + str(self.games[otherPlayer])

        return string.rstrip()

    def getScore(self):
        return self.score

    def getCurrentScore(self):
        return self.currentScore

    def getGames(self):
        return self.games

#-------------------------------------------------------------------------------

def main(argv):
    #From http://www.tutorialspoint.com/python/python_command_line_arguments.htm
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'python mainTennisGame.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python mainTennisGame.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print "Game ON"
    lines = openInputFile(inputfile)
    of = openOutputFile(outputfile)

    for line in lines:
        score = tennisScores().newTennisGame(line)
        print score
        printOutputFile(of, score)

    closeOutputFile(of)

    print "Game OFF"

def openInputFile(inputfile):
    #From Lazik in http://stackoverflow.com/questions/3277503/python-read-file-line-by-line-into-array
    lines = [line.rstrip('\r\n') for line in open(inputfile)]
    return lines

def openOutputFile(outputfile):
    of = open(outputfile, 'w')
    return of

def printOutputFile(outputfile, line):
    outputfile.write(line + '\n')

def closeOutputFile(outputfile):
    outputfile.close()

if __name__ == '__main__':
    """
    Program to comute tennis games scores
    usage: python mainTennisGame.py -i <inputfile> -o <outputfile>
    """
    main(sys.argv[1:])

#-------------------------------------------------------------------------------

def testEmptyScore():
    """
    Tests empty lines
    """
    ts = tennisScores()
    ts.newTennisGame("")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [0, 0]), \
             "Error with empty string."

def testScoreA():
    """
    Tests A
    """
    ts = tennisScores()
    ts.newTennisGame("A")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [15, 0]), \
             "Error with A string."

def testScoreAA():
    """
    Tests AA
    """
    ts = tennisScores()
    ts.newTennisGame("AA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [30, 0]), \
             "Error with AA string."

def testScoreAAA():
    """
    Tests AAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [40, 0]), \
             "Error with AAA string."

def testScoreBA():
    """
    Tests BA
    """
    ts = tennisScores()
    ts.newTennisGame("BA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [15, 15]), \
             "Error with BA string."

def testScoreAAAA():
    """
    Tests AAAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAAA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [1, 0] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAA string."

def testScoreAAAAA():
    """
    Tests AAAAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAAAA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [1, 0] and \
            ts.getGames() == [15, 0]), \
             "Error with AAAAA string."

def testScoreBBBBB():
    """
    Tests BBBBB
    """
    ts = tennisScores()
    ts.newTennisGame("BBBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 1] and \
            ts.getGames() == [0, 15]), \
             "Error with BBBBB string."

def testScoreBBBBBA():
    """
    Tests BBBBBA
    """
    ts = tennisScores()
    ts.newTennisGame("BBBBBA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 1] and \
            ts.getGames() == [15, 15]), \
             "Error with BBBBBA string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBBBBBA():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBBBBBA 1
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBBBBBA")
    assert (ts.getScore() == [(6, 3), (4, 6), (0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [15, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBBBBBA string."

def testScoreBBBAAA():
    """
    Tests BBBAAA
    """
    ts = tennisScores()
    ts.newTennisGame("BBBAAA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [40, 40]), \
             "Error with BBBAAA string."

def testScoreBBBAAAABBB():
    """
    Tests BBBAAAABBB
    """
    ts = tennisScores()
    ts.newTennisGame("BBBAAAABBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 1] and \
            ts.getGames() == [0, 0]), \
             "Error with BBBAAAABBB string."

def testScoreBBBAAAA():
    """
    Tests BBBAAAA
    """
    ts = tennisScores()
    ts.newTennisGame("BBBAAAA")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == ['A', 40]), \
             "Error with BBBAAAA string."

def testScoreBBBAAAABB():
    """
    Tests BBBAAAABB
    """
    ts = tennisScores()
    ts.newTennisGame("BBBAAAABB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [40, 'A']), \
             "Error with BBBAAAABB string."

def testScoreAAAABBBB():
    """
    Tests AAAABBBB
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [1, 1] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBB string."

def testScoreAAAABBBBAAAABBBB():
    """
    Tests AAAABBBBAAAABBBB
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [2, 2] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBBAAAABBBB string."

def testScoreAAAABBBBAAAABBBBAAAABBBB():
    """
    Tests AAAABBBBAAAABBBBAAAABBBB
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [3, 3] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBB string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [5, 5] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB")
    assert (ts.getScore() == [(0, 0)] and \
            ts.getCurrentScore() == [6, 6] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBB string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAA():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAA")
    assert (ts.getScore() == [(7, 5), (0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [0, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAA string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAAA():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAAA")
    assert (ts.getScore() == [(6, 3), (0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [15, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAAAAAAAAAAA string."

def testScoreAAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAAA():
    """
    Tests AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAAA
    """
    ts = tennisScores()
    ts.newTennisGame("AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAAA")
    assert (ts.getScore() == [(6, 4), (0, 0)] and \
            ts.getCurrentScore() == [0, 0] and \
            ts.getGames() == [15, 0]), \
             "Error with AAAABBBBAAAABBBBAAAABBBBAAAABBBBAAAAAAAAA string."


