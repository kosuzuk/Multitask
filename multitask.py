import pygame
import sys
import random
import math
import datetime

black     = (0, 0, 0)
darkgrey  = (130, 130, 130)
grey      = (200, 200, 200)
lightgrey = (230, 230, 230)
white     = (255, 255, 255)
red       = (255, 0, 0)
green     = (0, 220, 0)
blue      = (0, 0, 255)
yellow    = (255, 240, 0)
purple    = (255, 0, 255)
cyan      = (0, 255, 255)
darkblue  = (0, 55, 75)
orange    = (255, 150, 0)
coolblue  = (20, 115, 140)
pink      = (255, 180, 255)
brown     = (50, 20, 0)
tan       = (220, 220, 130)

#Utility funcs
def drawText(s, x, y, text, size, color = black, font = None):
    font = pygame.font.Font(font, int(size)) #regular font
    text = font.render(text, True, color) #smooth edges- True
    pos = text.get_rect()
    pos.centerx = x #make x, y the center of text
    pos.centery = y
    s.blit(text, pos)

def drawShape(s, shape, pts, color, w = 0, h = 0, r = 0, 
              outline = 0, outlineColor = black): #pts for points
    if shape == "polygon":
        pts = tuple([(int(i[0]), int(i[1])) for i in pts])
    else:
        pts = tuple([int(i) for i in pts])
    w, h, r, outline = int(w), int(h), int(r), int(outline)
    if shape == "rect":
        if outline != 0:
            pygame.draw.rect(s, outlineColor, (pts[0] - outline, pts[1] - outline, 
                             w + outline * 2, h + outline * 2))
        pygame.draw.rect(s, color, (pts[0], pts[1], w, h))
    elif shape == "polygon": #no outline available for polygon
        pygame.draw.polygon(s, color, pts)
    elif shape == "circle":
        if outline != 0:
            pygame.draw.circle(s, outlineColor, pts, r + outline)
        pygame.draw.circle(s, color, pts, r)

#classes
class var(object):
    version            = None
    subjectName        = None
    experimenterName   = None
    playing            = False
    timeLeft           = None
    msElapsed          = 0
    #duration of window pop-up for checking if default cfg, blank subjectname, and overwrite log are ok
    popUpDuration      = 0
    score              = 0
    log                = None
    surface            = None
    quadLst            = None
    backgroundTimerLst = None
    stroop             = None
    letters            = None
    target             = None
    numbers            = None
    colorNames         = ["red", "green", "blue", "yellow"]

class Cfg(object):
    obj      = None #file object
    text     = "" #original text in cfgObj
    fileName = ""

class Log(object):
    timeOutPeriod   = 10000
    msElapsed       = 0
    text            = "" #text in log
    fileName        = ""
    spacing         = [13, 37, 20] #number of characters in each col of log
    timeLeftText    = ""
    actionTextLst   = []
    timedOutTextLst = []

    def getValues(self):
        if var.playing == False:
            var.log = Log()
            #create the column titles
            colTitlesLst = ["Time Left", "Action", "Module Timed Out", "Score\n\n"]
            colTitlesStr = ""
            for i in xrange(len(colTitlesLst)):
                colTitlesStr += colTitlesLst[i]
                if i != 3:
                    colTitlesStr += " " * (Log.spacing[i] - len(colTitlesLst[i]))
            #also add cfg file at top
            Log.text += Cfg.text + "\n" * 10 + colTitlesStr
            Log.timeLeftText = str(var.timeLeft / 1000)
        else:
            Log.timeLeftText = str((var.timeLeft - var.msElapsed) / 1000 + 1)

    def update(self):
        if Log.actionTextLst == [] and Log.timedOutTextLst == []:
            if Log.timeLeftText != "":
                Log.text += Log.timeLeftText + "\n"
        else:
            if Log.timeLeftText == "":
                Log.text += " " * Log.spacing[0]
            else:
                Log.text += Log.timeLeftText + " " * (Log.spacing[0] - len(Log.timeLeftText))
        timeLeftText = ""
        first = True
        valuePresent = (False, False) #bools for action and timedOut cols
        while Log.actionTextLst != [] or Log.timedOutTextLst != []:
            if not first: timeLeftText = " " * Log.spacing[0]
            first = False
            if Log.actionTextLst == []:
                scoreText = Log.timedOutTextLst[0][1]
                valuePresent = (False, True)
            elif Log.timedOutTextLst == []:
                scoreText = Log.actionTextLst[0][1]
                if len(Log.actionTextLst[0][0]) < 20: scoreText = ""
                valuePresent = (True, False)
            elif Log.actionTextLst[0][2] < Log.timedOutTextLst[0][2]: #compare msElapsed
                scoreText = Log.actionTextLst[0][1]
                if len(Log.actionTextLst[0][0]) < 20: scoreText = ""
                valuePresent = (True, False)
            elif Log.actionTextLst[0][2] > Log.timedOutTextLst[0][2]: #compare msElapsed
                scoreText = Log.timedOutTextLst[0][1]
                valuePresent = (False, True)
            else:
                scoreText = Log.timedOutTextLst[0][1]
                valuePresent = (True, True)
            if valuePresent[0]:
                actionText = Log.actionTextLst[0][0] + " " * (Log.spacing[1] - len(Log.actionTextLst[0][0]))
                timedOutText = " " * Log.spacing[2]
                Log.actionTextLst.remove(Log.actionTextLst[0])
            if valuePresent[1]:
                actionText = " " * Log.spacing[1]
                timedOutText = Log.timedOutTextLst[0][0] + " " * (Log.spacing[2] - len(Log.timedOutTextLst[0][0]))
                Log.timedOutTextLst.remove(Log.timedOutTextLst[0])
            Log.text += timeLeftText + actionText + timedOutText + str(scoreText) + "\n"
        Log.timeLeftText = ""

class Surface(object):
    w     = None
    h     = None
    color = None

    def draw(self, s):
        pygame.Surface.fill(s, Surface.color)

class Quad(object):
    margin = None 
    w      = None 
    h      = None 
    color  = lightgrey

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getValues(self):
        var.quadLst = []
        for i in xrange(4):
            Quad.margin = Surface.w / 60
            Quad.w      = Surface.w / 2 - Quad.margin * 1.25
            Quad.h      = Surface.h / 2 - Quad.margin * 1.25
            new = Quad(Quad.margin + (not 0 < i < 3) * (Quad.w + Quad.margin / 2), 
                       Quad.margin + (i > 1) * (Quad.h + Quad.margin / 2))
            var.quadLst.append(new)

    def draw(self, s):
        for q in var.quadLst:
            drawShape(s, "rect", (q.x, q.y), q.color, 
                      q.w, q.h)

class BackgroundTimer(object):
    timeOutPeriod = 300
    msElapsed     = 0 #since last updated image
    color         = white

    def __init__(self, ptsLst, speed):
        self.ptsLst = ptsLst
        self.speed  = speed

    def getValues(self):
        if var.playing == False:
            var.backgroundTimerLst = []
            classes = [Stroop, Letters, Numbers]
            for i in xrange(3):
                x = Quad.margin + Quad.w / 2 + (not i == 1) * (Quad.w + Quad.margin / 2)
                y = Quad.margin + Quad.h / 2 + (i > 1) * (Quad.h + Quad.margin / 2)
                r = Quad.h / 2
                ptsLst = [[x, y], [x, y - r], [x + 1, y - r]]
                speed = ((Quad.w * 2 + Quad.h * 2) / (float(classes[i].timeOutPeriod))) * BackgroundTimer.timeOutPeriod
                var.backgroundTimerLst.append(BackgroundTimer(ptsLst, speed))
        else:
            for t in var.backgroundTimerLst: #t for timer
                lastIndex = len(t.ptsLst) - 1 #last index of points list
                dLst = [(1, 0), (0, 1), (-1, 0), (0, -1)]
                d = dLst[(len(t.ptsLst) - 3) % 4] #d for direction
                newPos = [t.ptsLst[lastIndex][0] + d[0] * t.speed, 
                          t.ptsLst[lastIndex][1] + d[1] * t.speed]
                newXorY = newPos[0] * abs(d[0]) + newPos[1] * abs(d[1])
                edge = ((t.ptsLst[0][0] + (Quad.w / 2 * d[0])) * abs(d[0]) + 
                        (t.ptsLst[0][1] + (Quad.h / 2 * d[1])) * abs(d[1]))
                t.ptsLst[lastIndex] = newPos
                if ((newXorY > edge and (dLst.index(d) < 2)) or 
                    (newXorY < edge and (dLst.index(d) >= 2))):
                    remainder = newXorY - edge
                    if dLst.index(d) >= 2: remainder *= -1
                    t.ptsLst[lastIndex][0] -= d[0] * remainder
                    t.ptsLst[lastIndex][1] -= d[1] * remainder
                    d = dLst[(dLst.index(d) + 1) % 4]
                    newPos = [t.ptsLst[lastIndex][0] + d[0] * remainder, 
                              t.ptsLst[lastIndex][1] + d[1] * remainder]
                    t.ptsLst.append(newPos)

    def draw(self, s):
        for i in var.backgroundTimerLst:
            drawShape(s, "polygon", i.ptsLst, i.color)

class Stroop(object):
    timeOutPeriod = None #ms between each timeout
    successScore  = None
    failureScore  = None
    timeOutScore  = None
    msElapsed     = 0 #since newest instance of question
    buttonLst     = []
    numCorrect    = 0
    numIncorrect  = 0
    numTimedOut   = 0

    def getValues(self): #values for the question
        temp = random.choice(var.colorNames)
        #new instance of stroop
        if var.playing == False:
            Stroop.question.x    = Quad.w * 1.35
            Stroop.question.y    = Quad.margin * 0.75 + Quad.h / 2
            Stroop.question.size = Surface.w / 9
            var.stroop = Stroop()
            #inputs to Stroop.question.__init__ are text, answer, color
            var.stroop.question  = Stroop.question(temp, temp, eval(temp))

            #values for the four buttons
            b = Stroop.button
            b.w            = Quad.w / 3.2
            b.h            = Quad.h / 6
            b.outline      = b.w / 40
            b.outlineColor = black
            b.margin       = (Quad.h - b.h * 4) / 5 #take away height of buttons, then divide by 5
            for i in xrange(4):
                x = Surface.w - Quad.margin - b.margin - b.w
                y = (Quad.margin + b.margin + 
                    (b.h + b.margin) * i)
                newB = b(x, y, eval(var.colorNames[i]))
                var.stroop.buttonLst.append(newB)
        else:
            #new values, same stroop instance
            q = var.stroop.question
            while (temp == q.answer):
                temp = random.choice(var.colorNames)
            q.answer = temp
            q.color = eval(temp)

        q = var.stroop.question
        while (temp == q.answer):
            temp = random.choice(var.colorNames)
        q.text = temp
        x = Quad.margin + Quad.w / 2 + (Quad.w + Quad.margin / 2)
        y = Quad.margin + Quad.h / 2
        r = Quad.h / 2
        var.backgroundTimerLst[0].pstLst = [[x, y], [x, y - r], [x + 1, y - r]]

    def draw(self, s):
        #draw question
        q = var.stroop.question
        drawText(s, q.x, q.y, q.text, q.size, q.color)

        #draw buttons
        for b in var.stroop.buttonLst:
            drawShape(s, "rect", (b.x, b.y), b.color, #radius set to 0
                      b.w, b.h, 0, b.outline, b.outlineColor)

    def action(self, p):
        result = ""
        for b in var.stroop.buttonLst:
            if (p[1] > b.y and p[1] < b.y + b.h):
                if eval(var.stroop.question.answer) == b.color:
                    var.score += Stroop.successScore
                    Stroop.numCorrect += 1
                    result = "Stroop correct"
                else:
                    var.score += Stroop.failureScore
                    Stroop.numIncorrect += 1
                    result = "Stroop incorrect"
                Stroop().getValues()
                Stroop.msElapsed = var.msElapsed
        return result

    class question(object):
        x    = None
        y    = None
        size = None

        def __init__(self, text, answer, color):
            self.text   = text
            self.answer = answer
            self.color  = color

    class button(object):
        w            = None 
        h            = None 
        outline      = None 
        outlineColor = None 
        margin       = None 

        def __init__(self, x, y, color):
            self.x     = x
            self.y     = y
            self.color = color

class Letters(object):
    timeOutPeriod   = None
    successScore    = None
    failureScore    = None
    showStringScore = None
    timeOutScore    = None
    stringLength    = None
    stringDuration  = None
    string          = None
    stringStart     = 0
    msElapsed       = 0
    buttonLst       = []
    numCorrect      = 0
    numIncorrect    = 0
    numTimedOut     = 0

    def getValues(self):
        #first call
        if var.playing == False:
            Letters.stringDuration = Letters.timeOutPeriod / 3
            #one string for the entire game
            var.letters = Letters()
            temp = ""
            for i in xrange(Letters.stringLength):
                newChar = chr(random.randrange(97, 122))
                while newChar in temp: newChar = chr(random.randrange(97, 122))
                temp += newChar
            Letters.string = temp

            #instance of char question
            newChar = chr(random.randrange(97, 122))
            Letters.question              = Letters.question(newChar, newChar in temp)
            Letters.question.x            = Quad.margin * 0.75 + Quad.w / 2
            #between screen edge and show string button
            Letters.question.y            = (Quad.margin + Quad.h * 0.48) / 2 + Quad.margin
            Letters.question.radius       = Quad.w / 20 + Quad.h / 15
            Letters.question.circleColor  = white
            Letters.question.outline      = 2
            Letters.question.outlineColor = black
            Letters.question.textX        = Letters.question.x
            Letters.question.textY        = Letters.question.y
            Letters.question.textSize     = Letters.question.radius * 2
            Letters.question.textColor    = black

            #values for show string button
            b = Letters.button
            b.w            = Quad.w / 3
            b.h            = Quad.h / 7
            b.margin       = (Quad.w - 2 * b.w) / 5 #take away width of two boolean buttons,
            b.color        = grey                   #then divide the rest by 5
            b.outline      = b.w / 50
            b.outlineColor = black
            b.string       = ""
            b.textSize     = Quad.w / 13 + Quad.h / 30
            b.textColor    = black
            text = temp
            x = Quad.margin + Quad.w * 0.05
            y = Quad.margin + Quad.h * 0.48
            bLst = var.letters.buttonLst
            bLst.append(Letters.button(text, x, y))
            bLst[0].w            = Quad.w - (x - Quad.margin) * 2
            bLst[0].textX        = x + bLst[0].w / 2
            bLst[0].color        = white
            bLst[0].textColor    = black
            bLst[0].outlineColor = black

            #initialize values for boolean buttons
            for i in xrange(2):
                text = str(i == 0)
                x = Quad.margin + Letters.button.margin * 2 + \
                    (Letters.button.w + Letters.button.margin) * i
                y = Quad.h * 0.75
                bLst.append(Letters.button(text, x, y))
            return

        #new char question each time interval
        q = var.letters.question
        oldChar = q.char
        newChar = chr(random.randrange(97, 122))
        while newChar == oldChar: newChar = chr(random.randrange(97, 122))
        q.char = newChar
        q.answer = newChar in Letters.button.string
        x = Quad.margin + Quad.w / 2
        y = Quad.margin + Quad.h / 2
        r = Quad.h / 2
        var.backgroundTimerLst[1].pstLst = [[x, y], [x, y - r], [x + 1, y - r]]

    def draw(self, s):
        #draw char
        q = var.letters.question
        drawShape(s, "circle", (q.x, q.y), q.circleColor, 0, 0, q.radius, q.outline, q.outlineColor)
        drawText(s, q.textX, q.textY, q.char, q.textSize, q.textColor)

        #draw show string and boolean buttons
        for b in var.letters.buttonLst:
            drawShape(s, "rect", (b.x, b.y), b.color, 
                      b.w, b.h, 0, b.outline, b.outlineColor)
            drawText(s, b.textX, b.textY, b.text, 
                     b.textSize, b.textColor)

    def action(self, p):
        result = ""
        #show string button
        bLst = var.letters.buttonLst
        if ((p[0] > bLst[0].x) and 
            (p[0] < bLst[0].x + bLst[0].w) and 
            (p[1] > bLst[0].y) and 
            (p[1] < bLst[0].y + bLst[0].h)):
            var.letters.stringStart = var.msElapsed
            bLst[0].color = white
            bLst[0].text = Letters.string
            bLst[0].textColor = black
            var.score += Letters.showStringScore
            result = "Letters show string"
            return result

        #boolean button
        for i in xrange(1, 3):
            if (p[0] > bLst[i].x and 
                p[0] < bLst[i].x + bLst[i].w and 
                p[1] > bLst[i].y and 
                p[1] < bLst[i].y + bLst[i].h):
                if var.letters.question.answer == (i == 1):
                    var.score += Letters.successScore
                    Letters.numCorrect += 1
                    result = "Letters correct"
                else:
                    var.score += Letters.failureScore
                    Letters.numIncorrect += 1
                    result = "Letters incorrect"
                var.letters.getValues()
                Letters.msElapsed = var.msElapsed
        return result

    def displayed(self):
        #check whether string should be shown
        l = var.letters
        if ((var.msElapsed - l.stringStart)
            > l.stringDuration):
            l.buttonLst[0].color = grey
            l.buttonLst[0].text = "show string (" + str(Letters.showStringScore) + ")"
            l.buttonLst[0].textColor = red

    class question(object):
        x            = None
        y            = None
        radius       = None 
        circleColor  = None 
        outline      = None 
        outlineColor = None 
        textX        = None 
        textY        = None 
        textSize     = None 
        textColor    = None 

        def __init__(self, char, answer):
            self.char   = char
            self.answer = answer

    class button(object):
        w            = None
        h            = None
        margin       = None
        color        = None
        outline      = None
        outlineColor = None
        string       = None
        textSize     = None
        textColor    = None

        def __init__(self, text, x, y):
            self.x     = x
            self.y     = y
            self.text  = text
            self.textX = x + Letters.button.w / 2
            self.textY = y + Letters.button.h / 2

class Target(object):
    timeOutPeriod        = None
    successScore         = None
    failureScore         = None
    msElapsed            = 0
    x                    = None
    y                    = None
    numCircles           = None
    offset               = None
    distance             = None
    outline              = None
    outlineColor         = None
    timeOutPeriod        = None
    color                = None
    buttonLst            = []
    totalCorrectScore    = 0
    totalIncorrectScore  = 0

    def getValues(self):
        if var.playing == False:
            Target.x             = Quad.margin + Quad.w / 2
            Target.y             = Quad.margin * 1.5 + Quad.h * 1.5
            Target.numCircles    = 6
            #difference in radius between successive circles
            Target.offset        = min(Surface.w, Surface.h) / 28
            #distance from center of target to outer rim of target
            Target.distance      = Target.offset * Target.numCircles
            Target.outline       = 1
            Target.outlineColor  = black
            Target.timeOutPeriod /= 10.0
            #initialize var.target and dot
            var.target = Target()
            direction = math.radians(random.randrange(0, 359))
            speed = min(Surface.w, Surface.h) / 28 / 6
            var.target.dot = Target.dot(Target.x, Target.y, direction, 0 - speed)
            Target.dot.radius = min(Surface.w, Surface.h) / 28 / 5 #5 times smaller than Target.offset
            Target.dot.speed  = speed

            #initionalize buttons
            for i in xrange(2):
                b = Target.button
                b.w            = Quad.w / 6
                b.h            = Quad.h / 14
                b.color        = grey
                b.outline      = 2
                b.outlineColor = black
                b.text         = "reset"
                b.textSize     = b.w / 3
                b.textColor    = black
                if i == 0:
                    x = Quad.margin * 2
                    y = Surface.h - Quad.margin * 2 - Target.button.h
                    var.target.buttonLst.append(Target.button(x, y))
                else:
                    x = Quad.margin + Quad.w - Quad.margin - Target.button.w
                    var.target.buttonLst.append(Target.button(x, y))

        #change position of dot
        d = var.target.dot
        if d.distance < (Target.distance + (Quad.h / 2 - Target.distance) / 2):
            d.distance += d.speed
            d.x = Target.x + d.distance * math.cos(d.direction)
            d.y = Target.y + d.distance * math.sin(d.direction)

        #change score
        if d.distance > Target.distance:
            var.score += Target.failureScore
            Target.totalIncorrectScore += Target.failureScore
        else:
            for i in xrange(Target.numCircles):
                if d.distance < Target.offset * (i + 1) + Target.offset / 3:
                    if i > var.target.dot.curRing:
                        var.target.dot.curRing = i
                        var.score += i * Target.successScore
                        Target.totalCorrectScore += i * Target.successScore
                    return

    def draw(self, s):
        #draw target
        t = Target
        for i in xrange(t.numCircles):
            #gradient
            color = tuple(t.color[j] + (255 - t.color[j]) / (Target.numCircles - 1) * i 
                          for j in xrange(3))
            drawShape(s, "circle", (t.x, t.y), color, 0, 0, #w and h are 0
                      t.numCircles * t.offset - t.offset * i, t.outline, t.outlineColor)

        #draw dot
        d = var.target.dot
        drawShape(s, "circle", (d.x, d.y), d.color, 0, 0, d.radius)

        #draw reset buttons
        for b in var.target.buttonLst:
            drawShape(s, "rect", (b.x, b.y), b.color, 
                      b.w, b.h, 0, b.outline, b.outlineColor)        
            drawText(s, b.textX, b.textY, b.text, b.textSize, black)

    def action(self, p):
        direction = math.radians(random.randrange(0, 359))
        var.target.dot = Target.dot(Target.x, Target.y, direction, 0 - Target.dot.speed)
        return "Target reset"

    class dot(object):
        radius = None
        speed  = None
        color = red
        def __init__(self, x, y, direction, distance):
            self.x         = x
            self.y         = y
            self.direction = direction
            self.distance  = distance #distance from center of target to center of dot
            self.curRing   = 0

    class button(object):
        w            = None
        h            = None
        color        = None
        outline      = None
        outlineColor = None
        text         = None
        textSize     = None
        textColor    = None

        def __init__(self, x, y):
            self.x     = x
            self.y     = y
            self.textX = x + Target.button.w / 2
            self.textY = y + Target.button.h / 2

class Numbers(object):
    timeOutPeriod    = None
    successScore     = None
    failureScore     = None
    timeOutScore     = None
    msElapsed        = 0
    rows             = 4
    columns          = 4
    numMaxNumbers    = 0
    maxNumber        = 0
    buttonLst        = []
    pressedButtonLst = []
    numCorrect       = 0
    numIncorrect     = 0
    numTimedOut      = 0

    def getValues(self):
        if var.playing == False:
            var.numbers = Numbers()
        Numbers.numMaxNumbers    = random.randint(1, 7)
        Numbers.maxNumber        = random.randint(4, 9)
        Numbers.pressedButtonLst = []
        Numbers.buttonLst        = []
        bLst = var.numbers.buttonLst
        for row in xrange(Numbers.rows): #fill list with numbers except maxNumber
            for col in xrange(Numbers.columns):
                b = Numbers.button
                b.radius       = min(Quad.w, Quad.h) / 10
                b.offset       = b.radius * 2 + b.radius / 4 #distance between the centers of two adjacent buttons
                b.startX       = (Quad.margin * 1.5 + Quad.w + 
                                 (Quad.w - (b.radius * 2 + b.offset * 3)) / 2 + b.radius)
                b.startY       = (Quad.margin * 1.5 + Quad.h + 
                                    (Quad.h - (b.radius * 2 + b.offset * 3)) / 2 + b.radius)
                b.outline      = 2
                b.outlineColor = black
                b.textColor    = black
                b.textSize     = b.radius * 2
                new = Numbers.button(random.randint(1, Numbers.maxNumber - 1))
                bLst.append(new)
        for i in xrange(Numbers.numMaxNumbers): #fill list with maxNumber
            randomIndex = random.randint(0, len(bLst) - 1)
            while bLst[randomIndex].number == Numbers.maxNumber:
                randomIndex = random.randint(0, len(bLst) - 1)
            bLst[randomIndex].number = Numbers.maxNumber
        x = Quad.margin + Quad.w / 2 + (Quad.w + Quad.margin / 2)
        y = Quad.margin + Quad.h / 2 + (Quad.h + Quad.margin / 2)
        r = Quad.h / 2
        var.backgroundTimerLst[2].pstLst = [[x, y], [x, y - r], [x + 1, y - r]]

    def draw(self, s):
        b = var.numbers.button
        for row in xrange(Numbers.rows):
            for col in xrange(Numbers.columns):
                drawShape(s, "circle", (b.startX + b.offset * col, b.startY + b.offset * row), 
                          var.numbers.buttonLst[row * 4 + col].color, 0, 0, b.radius, b.outline, b.outlineColor)
                drawText(s, b.startX + b.offset * col, b.startY + b.offset * row, 
                         str(var.numbers.buttonLst[row * 4 + col].number), b.textSize, b.textColor)

    def action(self, p):
        result = ""
        n = Numbers
        for row in xrange(n.rows):
            for col in xrange(n.columns):
                if math.sqrt((p[1] - (n.button.startY + n.button.offset * row)) ** 2 + 
                             (p[0] - (n.button.startX + n.button.offset * col)) ** 2) < n.button.radius:
                    if var.numbers.buttonLst[row * 4 + col].number == Numbers.maxNumber:
                        var.numbers.buttonLst[row * 4 + col].color = darkgrey
                        n.pressedButtonLst.append(var.numbers.buttonLst[row * 4 + col])
                        if len(n.pressedButtonLst) == n.numMaxNumbers:
                            n().getValues()
                            n.msElapsed = var.msElapsed
                            var.score += Numbers.successScore
                            Numbers.numCorrect += 1
                            result = "Numbers correct"
                    else:
                        var.score += Numbers.failureScore
                        Numbers.numIncorrect += 1
                        result = "Numbers incorrect"
        return result

    class button(object):
        radius       = None
        offset       = None
        startX       = None
        startY       = None
        outline      = None
        outlineColor = None
        textColor    = None
        textSize     = None

        def __init__(self, number):
            self.number = number
            self.color  = white

def getValue(l, firstIndex):
    valueString = l[firstIndex : len(l)]
    try:
        return eval(valueString)
    except:
        return valueString

def enterText(s, text):
    if "config" in text: text = "config file"
    elif "subject" in text: text = "subject"
    elif "log" in text: text = "log file"
    text = "enter " + text + " name: "
    if "subject" in text: text.replace(": ", "(use underscore for space): ")
    s.fill(black)
    drawText(s, 400, 100, text, 40, white)
    p = pygame
    p.display.update()
    asking = True
    while asking:
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key < 0 or event.key > 127: pass #invalid key
                elif text[text.index(":") + 2: ] == "" and event.key == p.K_RETURN: pass #no enter when no chars
                elif text[len(text) - 2] == ":" and event.key == p.K_BACKSPACE: pass #no backspace when no chars
                elif event.key == p.K_RETURN:
                    asking = False
                    break
                elif event.key == p.K_ESCAPE:
                    p.quit()
                    sys.exit()
                else:
                    if event.key == p.K_BACKSPACE: text = text[ : len(text) - 1]
                    else: text += chr(event.key) #valid key
                    s.fill(black)
                    drawText(s, 400, 100, text, 40, white)
                    p.display.update()
            elif event.type == p.QUIT: #x out
                p.quit()
                sys.exit()
    if "config" in text: 
        Cfg.fileName = text[text.index(":") + 2 : ]
    elif "subject" in text: 
        var.subjectName = text[text.index(":") + 2 : ]
        lines = Cfg.text.splitlines()
        for l in lines: 
            if l.startswith("subjectname"):
                line = l
                break
        newL = l.replace("_", var.subjectName)
        Cfg.text = Cfg.text.replace(l, newL)
    elif "log" in text:
        Log.fileName = text[text.index(":") + 2 : ]

def ask(text):
    surfaceSize = (800, 200)
    surface = pygame.display.set_mode(surfaceSize)
    drawText(surface, surfaceSize[0] / 2, surfaceSize[1] / 2, text, 40, white)
    pygame.display.update()
    asking = True
    while asking:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                try:
                    if event.key == pygame.K_y:
                        asking = False
                    elif event.key == pygame.K_n:
                        enterText(surface, text)
                        asking = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                except:
                    pass
            elif event.type == pygame.QUIT: #x out
                pygame.quit()
                sys.exit()

def checkDefaultCfg():
    if Cfg.fileName == "default.cfg" or Cfg.fileName == "":
        text = "Ok to use default config file? (y/n)"
        ask(text)

def checkBlankSubjectName():
    #checks if black subject name field is ok
    if var.subjectName == "_":
        text = "Blank subject name ok? (y/n)"
        ask(text)

def checkOverwriteLog():
    try: #checks for file of same name and ask for permission to overwrite
        open(Log.fileName, "r")
        text = "Ok to overwrite log file with same name? (y/n)"
        ask(text)
    except: #no file with that name exists
        pass

def checkLine(l):
    try:
        eqIndex = l.index("=")
    except: #start/end module line
        valid = [i + j for i in ["begin{", "end{"] for j in ["stroop}", "letters}", "target}", "numbers}"]]
        return (l in valid, "\b")
    head = l[0 : eqIndex] #all other lines with values being assigned to variables
    tail = l[eqIndex + 1: len(l)]
    valid = ["version", "subjectname", "experimentername", "timeleft", 
             "surfacew", "surfaceh", "backgroundcolor", "timeoutperiod", 
             "successscore", "failurescore", "timeoutscore", "showstringscore", 
             "stringlength", "color"]
    if head not in valid:
        return (False, "variable")
    elif "=" in tail or "{" in tail or "}" in tail:
        return (False, "value")
    elif tail == "":
        return (False, "value")
    else:
        return (True, "")

def checkMissing():
    variables = [var.version, var.subjectName, var.experimenterName, 
                 var.timeLeft, Surface.w, Surface.h, Surface.color, 
                 Stroop.timeOutPeriod, Stroop.successScore, 
                 Stroop.failureScore, Stroop.timeOutScore, 
                 Letters.timeOutPeriod, Letters.successScore, 
                 Letters.failureScore, Letters.showStringScore, 
                 Letters.timeOutScore, Letters.stringLength, 
                 Target.timeOutPeriod, Target.successScore, 
                 Target.failureScore, Target.color, 
                 Numbers.timeOutPeriod, Numbers.successScore, 
                 Numbers.failureScore, Numbers.timeOutScore]
    variableNames = ["version", "subjectName", "experimenterName", 
                     "timeLeft", "surfaceW", "surfaceH", "backgroundColor", 
                     "stroop.timeOutPeriod", "stroop.successScore", 
                     "stroop.failureScore", "stroop.timeOutScore", 
                     "letters.timeOutPeriod", "letters.successScore", 
                     "letters.failureScore", "letters.showStringScore", 
                     "letters.timeOutScore", "Letters.stringLength", 
                     "target.timeOutPeriod", "target.successScore", 
                     "target.failureScore", "target.color", 
                     "target.timeOutPeriod", "target.successScore", 
                     "target.failureScore", "target.timeOutScore"]
    try:
        i = variables.index(None) #check if any variables are missing
        return variableNames[i]
    except:
        pass #nothing missing

def error(lineNumber, reason):
    if reason in ["variable", "value", "\b"]:
        print "error: invalid %s at line number %d" %(reason, lineNumber + 1)
    elif reason == "duplicate":
        print "error: duplicate variable at line number %d" %(reason, lineNumber + 1)
    else:
        print "error: missing %s" %(reason)
    Cfg.obj.close()
    return False

def readCfg():
    try:
        Cfg.fileName = sys.argv[1]
    except:
        Cfg.fileName = "default.cfg"
    checkDefaultCfg()
    Cfg.obj = open(Cfg.fileName, "r")
    Cfg.text = Cfg.obj.read().lower() #ignore cases
    date = str(datetime.datetime.now()).replace(" ", "_")[ : 16].replace(":", "-")
    Cfg.text = Cfg.text.replace("automaticdateandtime", date)
    lines = Cfg.text.splitlines()
    i = -1
    inModule = False
    module = None
    for l in lines:
        i += 1
        if ";" in l: l = l[0 : l.index(";")] #comment is ignored
        l = l.replace(" ", "") #spaces are ignored
        if l == "\n" or l == "": continue #blank line is ignored
        checkLineResult = checkLine(l)
        if checkLineResult[0] == False:
            return error(i, checkLineResult[1])
        try:
            try:
                firstIndex = l.index("=") + 1 #get the value after equal sign
                value = getValue(l, firstIndex)
            except:
                pass
            if not inModule: #not module info
                if l.startswith("end"):
                    return error(i, "\b")
                elif l.startswith("begin"):
                    firstIndex = l.index("{") + 1
                    oldModule = module
                    module = eval(l[firstIndex : l.index("}")].
                                  replace(l[firstIndex], l[firstIndex].upper(), 1))
                    if module == oldModule:
                        return error(i, "\b")
                    inModule = True
                elif l.startswith("version"):
                    if ((type(eval(value[0 : 4]) + eval(value[5]) + eval(value[6]) + 
                              eval(value[8]) + eval(value[9]) + eval(value[11]) + 
                              eval(value[12]) + eval(value[14]) + eval(value[15])) != int) or \
                       (value[4] != "-" or value[7] != "-" or value[13] != "-") or \
                       (value[10] != "_" or value[16] != "_" or 15 < len(value) - 1 - l[ : : -1].index("_") < 18)):
                        return error(i, "value")
                    if var.version != None:
                        return error(i, "duplicate")
                    var.version = value
                    Log.fileName = var.version + ".log"
                    checkOverwriteLog()
                elif l.startswith("subjectname"):
                    if var.subjectName != None:
                        return error(i, "duplicate")
                    var.subjectName = value
                    checkBlankSubjectName()
                elif l.startswith("experimentername"):
                    if var.experimenterName != None:
                        return error(i, "duplicate")
                    var.experimenterName = value
                elif l.startswith("timeleft"):
                    if type(value) != int:
                        return error(i, "value")
                    if var.timeLeft != None:
                        return error(i, "duplicate")
                    var.timeLeft = value * 1000
                elif l.startswith("surfacew"):
                    if type(value) != int:
                        return error(i, "value")
                    if Surface.w != None:
                        return error(i, "duplicate")
                    Surface.w = value
                elif l.startswith("surfaceh"):
                    if type(value) != int:
                        return error(i, "value")
                    if Surface.h != None:
                        return error(i, "duplicate")
                    Surface.h = value
                elif l.startswith("backgroundcolor"):
                    if type(value) != tuple or \
                       type(value[0] + value[1] + value[2]) != int:
                        return error(i, "value")
                    if Surface.color != None:
                        return error(i, "duplicate")
                    Surface.color = value
                else: return error(i, "variable")
            elif inModule: #module info
                if l.startswith("begin"):
                    return error(i, "\b")
                elif l.startswith("end"):
                    firstIndex = l.index("{") + 1
                    oldModule = module
                    module = eval(l[firstIndex : l.index("}")].
                                  replace(l[firstIndex], l[firstIndex].upper(), 1))
                    if module != oldModule:
                        return error(i, "\b")
                    module = None
                    inModule = False
                elif l.startswith("timeoutperiod"):
                    if type(value) != int:
                        return error(i, "value")
                    if module.timeOutPeriod != None:
                        return error(i, "duplicate")
                    module.timeOutPeriod = value * 1000
                elif l.startswith("successscore"):
                    if type(value) != int:
                        return error(i, "value")
                    if module.successScore != None:
                        return error(i, "duplicate")
                    module.successScore = value
                elif l.startswith("failurescore"):
                    if type(value) != int:
                        return error(i, "value")
                    if module.failureScore != None:
                        return error(i, "duplicate")
                    module.failureScore = value
                elif l.startswith("timeoutscore"):
                    if module == Target:
                        return error(i, "value")
                    if type(value) != int:
                        return error(i, "value")
                    if module.timeOutScore != None:
                        return error(i, "duplicate")
                    module.timeOutScore = value
                elif l.startswith("showstringscore"):
                    if module != Letters:
                        return error(i, "value")
                    if type(value) != int:
                        return error(i, "value")
                    if module.showStringScore != None:
                        return error(i, "duplicate")
                    module.showStringScore = value
                elif l.startswith("stringlength"):
                    if module != Letters:
                        return error(i, "value")
                    if type(value) != int:
                        return error(i, "value")
                    if module.stringLength != None:
                        return error(i, "duplicate")
                    module.stringLength = value
                elif l.startswith("color"):
                    if type(value) != tuple or \
                       type(value[0] + value[1] + value[2]) != int:
                        return error(i, "value")
                    if module.color != None:
                        return error(i, "duplicate")
                    module.color = value
                else:
                    return error(i, "variable")
        except:
            return error(i, "\b")
    if inModule: return error(i, "\b")
    checkMissingResult = checkMissing()
    if checkMissingResult != None: return error(0, checkMissingResult)
    Cfg.obj.close()
    return True

def writeLog():
    fileObj = open(Log.fileName, "w")
    classes = ["Stroop", "Letters", "Target", "Numbers"]
    Log.text += "\n" * 10
    for c in classes:
        if c == "Target":
            Log.text += (c + ":\n" + "total scores gained: " + str(eval(c).totalCorrectScore) + 
                         "\n" + "total scores lost: " + str(eval(c).totalIncorrectScore) + "\n\n")
        else:
            Log.text += (c + ":\n" + "number correct: " + str(eval(c).numCorrect) + 
                         "\n" + "number incorrect: " + str(eval(c).numIncorrect) + "\n" + 
                         "number timed out: " + str(eval(c).numTimedOut) + "\n\n")
    Log.text += "\n" + "final score: " + str(var.score) + "\n\n"
    fileObj.write(Log.text)
    fileObj.close()

def checkTime():
    #reset log variables for this iteration
    Log.actionTextLst, Log.timedOutTextLst = [], []

    var.msElapsed = pygame.time.get_ticks() - var.popUpDuration
    #check time out for entire game
    if var.msElapsed > var.timeLeft:
        var.playing = False

    #check time out for specific modules
    classes = [var.backgroundTimerLst[0], var.stroop, var.letters, var.target, var.numbers, var.log]
    classNames = ["", "Stroop", "Letters", "Target", "Numbers"]
    for c in classes:
        if var.msElapsed - c.msElapsed > c.timeOutPeriod:
            c.getValues()
            c.msElapsed = var.msElapsed
            i = classes.index(c)
            if i in [0, 3, 5]: continue
            var.score += c.timeOutScore
            eval(classNames[i]).numTimedOut += 1
            Log.timedOutTextLst.append((classNames[i], var.score, var.msElapsed))

def getValuesAll():
    if var.playing == False:
        classes = [BackgroundTimer((), 0), Stroop(), Letters(), Target(), Numbers(), Log()]
        var.surface = Surface()
        Quad(0, 0).getValues()
        for c in classes:
            c.getValues()

def drawTimerAndScore(s):
    #rect at center for timer and score
    rectW = Surface.w / 7
    rectH = Surface.h / 15
    rectX = Surface.w / 2 - rectW / 2
    rectY = Surface.h / 2 - rectH / 2 - 2
    drawShape(s, "rect", (rectX, rectY), white, rectW, rectH, 0, 
              outline = Quad.margin / 2, outlineColor = Surface.color)
    textSize = (rectW + rectH * 2) / 9
    timerText = "Timer: " + str((var.timeLeft - var.msElapsed) / 1000 + 1)
    scoreText = "Score: " + str(var.score)
    drawText(s, rectX + rectW / 2, rectY + rectH * 0.35, timerText, textSize)
    drawText(s, rectX + rectW / 2, rectY + rectH * 0.7, scoreText, textSize)

def drawAll(s):
    var.surface.draw(s)
    var.quadLst[0].draw(s)
    var.backgroundTimerLst[0].draw(s)
    drawTimerAndScore(s)
    var.stroop.draw(s)
    var.letters.draw(s)
    var.target.draw(s)
    var.numbers.draw(s)
    pygame.display.update()

def actionAll(p): #p for mouse position
    text = "click" + str((int(p[0]), int(p[1])))
    result = ""
    if (p[0] > var.stroop.buttonLst[0].x and 
        p[0] < var.stroop.buttonLst[0].x + var.stroop.buttonLst[0].w and 
        p[1] > var.stroop.buttonLst[0].y and
        p[1] < var.stroop.buttonLst[3].y + var.stroop.buttonLst[0].h):
        result = var.stroop.action(p)
    elif (p[0] > 0 and p[0] < Surface.w / 2 and p[1] > 0 and p[1] < Surface.h / 2):
        result = var.letters.action(p)
    elif ((p[0] > Target.buttonLst[0].x and 
           p[0] < Target.buttonLst[0].x + Target.buttonLst[0].w) or
          (p[0] > Target.buttonLst[1].x and 
           p[0] < Target.buttonLst[1].x + Target.buttonLst[1].w) and
           p[1] > Target.buttonLst[0].y and
           p[1] < Target.buttonLst[0].y + Target.buttonLst[0].h):
        result = var.target.action(p)
    elif (p[0] > Surface.w / 2 and p[0] < Surface.w and 
          p[1] > Surface.h / 2 and p[1] < Surface.h): 
        result = var.numbers.action(p)
    text += " " + result
    Log.actionTextLst.append((text, var.score, var.msElapsed))

def main():
    pygame.init()
    if readCfg() == False:
        return
    var.popUpDuration = pygame.time.get_ticks()
    surfaceSize = (Surface.w, Surface.h)
    surface = pygame.display.set_mode(surfaceSize)
    getValuesAll()
    var.playing = True
    while var.playing:
        checkTime()
        drawAll(surface)
        Letters().displayed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if var.playing:
                    mousePos = pygame.mouse.get_pos()
                    actionAll(mousePos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    var.playing = False
            if event.type == pygame.QUIT:
                var.playing = False
        var.log.update()
    writeLog()
    pygame.quit()
    sys.exit()

main()