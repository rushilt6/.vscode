import discord
import wolframalpha
import pyrebase
import urllib.request
import re
import asyncio
import random

client = discord.Client()

questionQueryList = []

playQueryList = []

fireBaseQueryList = []

goalQuery = []

todoQuery = []

addsongQuery = []

addStudyQuery =[]

addsiteQuery = []

timerQuery = []

songqueue = []

lastSongTracker = []

lazyWords =  ['unmotivated', 'lazy', 'bored','sluggish', 'idle', 'slow', 'disinterested', 'fatigued', 'tired', 'sick', 'dull', 'apathetic', 'sick of', 'boring', 'lame', 'tired of', 'fed up', 'annoyed', 'careless', 'distracted', 'distraught', 'lost', 'worn', 'worn out', 
'worned out','worn down', 'blah', 'bleh', 'low energy', 'energyless', 'lackadaisical', 'sleep', 'out of it', 'passive', 'indifferent', 'stupid', 'lifeless','mundane', 'stale', 'monotonous', 'flat', 'uninterested', 'dry', 'lackluster', 'numb', 'bland', 'dim', 'stagnant',"stress", 'gas', 'dead', 'poop', 'exhausted']

uptempoPlaylist = ["Drip too hard", "All the way up","Yes indeed", "Bop", "Whats next", "temperature sean paul", "pump it black eyed peas", "thunderstruck acdc", "back in black", "immigrant song", "sicko mode", "flexicution", "til I collapse","trophies drake", "uptown vibes", "DNA Kendrick Lamar", "Attack on titan op 1", "gotta have it", "GOMD", "back to back", "6 god", "Champions kanye", "tyler herro", "Both drake" , "No Stylist", "Bonfire Childish Gambino"]

wolframBan = []

motivationalQuotes = ['"All our dreams can come true, if we have the courage to pursue them". – Walt Disney', "“The secret of getting ahead is getting started.” – Mark Twain", "“I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life and that is why I succeed.” – Michael Jordan", "“Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve.” – Mary Kay Ash", "“It’s hard to beat a person who never gives up.” – Babe Ruth", "“If people are doubting how far you can go, go so far that you can’t hear them anymore.” – Michele Ruiz", "“We need to accept that we won’t always make the right decisions, that we’ll screw up royally sometimes – understanding that failure is not the opposite of success, it’s part of success.” – Arianna Huffington", "“Fairy tales are more than true: not because they tell us that dragons exist, but because they tell us that dragons can be beaten.”― Neil Gaiman", "“When one door of happiness closes, another opens; but often we look so long at the closed door that we do not see the one which has been opened for us.” ― Helen Keller", "“Smart people learn from everything and everyone, average people from their experiences, stupid people already have all the answers.” – Socrates", "“Happiness is not something ready made. It comes from your own actions.” ― Dalai Lama XIV", "“Remember…the Force will be with you, always.” – Obi Wan Kenobi", "“Strike me down, and I will become more powerful than you could possibly imagine.”- Obi Wan Kenobi", "“Master Yoda says I should be mindful of the future… But not at the expense of the moment.” – Qui Gon Jinn", "“Do. Or do not. There is no try.”- Yoda","“Your focus determines your reality.” – Qui Gon Jinn", "“When we hit our lowest point, we are open to the greatest change.”- Aang", "In the darkest of times, hope is something you give yourself.” – Zuko", "“There is nothing wrong with letting the people who love you help you.” – Iroh", "“Nothing can suppress a human’s curiosity.” – Eren Jaeger","“If you win you live. If you lose you die. If you don’t fight, you can’t win.” – Eren Jaeger","“Even in moments of the deepest despair… I guess we can still find hope, huh?” – Hange Zoe","“When people are faced with a situation they don’t understand, it’s easy for fear to take hold.” – Armin Arlert","“Never give up without even trying. Do what you can, no matter how small the effect it may have!” – Onoki","“A person grows up when he’s able to overcome hardships. Protection is important, but there are some things that a person must learn on his own.” – Jiraiya,", '“If you don’t like your destiny, don’t accept it. Instead have the courage to change it the way you want it to be.” – Naruto Uzumaki']

convoDone = []

commandList = ['-w','-t', '-p','-s','-m','-h','-g','-eg','-es','-el','-ew','-todo','-l','-r']

firebaseQuestionDict = {}

stressDict = {}

questionsaskedfirebaseDict = {}

questionSpamDict = {}

firebaseConfig = {
  
    'apiKey': "AIzaSyCocU0WdysNG5GpQRg-hlC1Q52hHsYIuMw",
    'authDomain': "studybuddy-d124e.firebaseapp.com",
    'databaseURL': "https://studybuddy-d124e-default-rtdb.firebaseio.com/",
    'projectId': "studybuddy-d124e",
    'storageBucket': "studybuddy-d124e.appspot.com",
    'messagingSenderId': "994334797923",
    'appId': "1:994334797923:web:7ad29fc2524965c2c94856",
    'measurementId': "G-25JGL254J3"
}

firee = pyrebase.initialize_app(firebaseConfig)

db = firee.database()

def searchtoURL(search):
    try:
        
        search_keyword= search.replace(' ','+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword + '+audio')
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        return("https://www.youtube.com/watch?v=" + video_ids[0])
        

    except:
        return 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'

def askWolfram(question):
    

    app_id = 'V59E4X-QQ437AXW5E'
    
    
    client = wolframalpha.Client(app_id)
    
    
    res = client.query(question)
    
    
    try:
        answer = next(res.results).text
    
    except:
        answer = "I'm not sure"
    
    
    return answer


try:
    for keysN in db.child('data').get().val().keys():
        convoDone.append(keysN)
except:
    db.child('data').set({'Bot Parents': 'Kunal Amladi, Advait Borkar, Shahil'})
firebaseQuestionDict = db.child('data').get().val()

def getStudious(writer): #returns string
    studiousRating = int(db.child("data").child(writer).child("2").get().val())
    return studiousRating

def getReward(writer): #returns string
    rewardWebsite = str(db.child("data").child(writer).child("1").get().val())
    return rewardWebsite
    
def getTimerLength(studiousRating):#returns int of timer length in seconds
    timerLength = 0
    if studiousRating <= 8:
        timerLength = 5  #360*studiousRating
        return timerLength
    elif studiousRating == 9:
        timerLength = 10         #3600
        return timerLength
    elif studiousRating == 10:
       timerLength = 15     #3600*24
       return timerLength

def getSong(writer):
    song = db.child("data").child(writer).child("0")
    return song

def timeReporter(seconds): #returns string
    if seconds < 60:
        return str(seconds) + " seconds"
    else:
        minutes = seconds / 60
        return str(minutes) + " minutes"

def startStatus(writer, timeLength):
    message = writer +', a timer for ' + timeReporter(timeLength) + ' has been set for you!'
    return message

def endStatus(writer):
    message = writer + ', your timer is up! ' + 'Here is your reward website: ' + getReward(writer)
    return message


print(convoDone)
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)) 
    
@client.event
async def on_message(message):

    writer = str(message.author)[:str(message.author).index('#')]
    
    if message.author == client.user or message.content.startswith('***'):

        return
#    if(message.content.startswith('-t')and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery and writer not in timerQuery):
#       print(writer + " wrote t")
#        timerQuery.append(writer)
#        if (writer in timerQuery):
#            
#            studiousRating = getStudious(writer)
#            timerLength = getTimerLength(studiousRating)
#            await message.channel.send(startStatus(writer, timerLength))
#            await asyncio.sleep(timerLength)
#            await message.channel.send(endStatus(writer))
    if(message.content.startswith('-h')):
        await message.channel.send("-eg to edit your goal")
        await message.channel.send("-el to edit your productivity on a scale of 1-10")
        await message.channel.send("-es to edit your favorite song")
        await message.channel.send("-ew to edit your favorite website")
        await message.channel.send("-g to check the goal that you set")
        await message.channel.send("-l to check your to do list ")
        await message.channel.send("-m if you are feeling sad to receive motivation")
        await message.channel.send("-p to play a song from youtube/add a song to a playlist")
        await message.channel.send("-w to ask a question to wolframalpha")
        await message.channel.send("-s to skip a song")
        await message.channel.send("-t to start your timer based on how hard working you are") 
        await message.channel.send("-todo to add to your to do list")
        await message.channel.send("-r to clear your to do list")
    if(message.author == client.user  and 'youtube' in str(message.content) and 'Music' not in str(message.content)):
        lastSongTracker.append(message)
        print(lastSongTracker)
    elif message.author == client.user or message.content.startswith('**'):
        
        return
     
    for words in lazyWords:
        if(words in str(message.content).lower()):            

            if(writer not in stressDict.keys()):
                print('100')
                stressDict[writer] = 0
                break

            elif(stressDict[writer]>4):
                print('010')
                print(stressDict[writer])
                await message.channel.send('@'+writer+ ' Feeling Lazy? Here is an uptempo song to wake you up!')
                await message.channel.send('@'+writer+' Uptempo Music: '+ searchtoURL(uptempoPlaylist[random.randint(0,len(uptempoPlaylist)-1)]))
                stressDict.pop(writer)

                break
            else:
                print('001')
                stressDict[writer] += 1
    print('Stress')
    print(stressDict)
    if(message.content.startswith('-eg')and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        goalQuery.append(writer)
        await message.channel.send('@'+writer+' What would you like to update your goal for this session to?')
        return
        
        
    
    elif(writer not in playQueryList and writer not in questionQueryList and writer in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        print((db.child('data').child(writer).get().val()))
        db.child('data').child(writer).child('3').set(str(message.content))
        goalQuery.remove(writer)
        return
        print('Hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

    if(message.content.startswith('-ew')and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        addsiteQuery.append(writer)
        await message.channel.send('@'+writer+' What would you like to update your favorite website to?')
        return
        
        
    
    elif(writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer  in addsiteQuery and writer not in addStudyQuery):
        print((db.child('data').child(writer).get().val()))
        db.child('data').child(writer).child('1').set('https://'+str(message.content))
        addsiteQuery.remove(writer)
        return
        print('Hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')


    if(message.content.startswith('-es')and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        addsongQuery.append(writer)
        await message.channel.send('@'+writer+' What would you like to update your favorite song to?')
        return
        
        
    
    elif(writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer  in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        print((db.child('data').child(writer).get().val()))
        db.child('data').child(writer).child('0').set(searchtoURL(str(message.content)))
        addsongQuery.remove(writer)
        return
        print('Hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

    
    if(message.content.startswith('-el')and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        addStudyQuery.append(writer)
        await message.channel.send('@'+writer+' What would you like to update your study level to? (scale of 1-10)')
        return
        
        
    
    elif(writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and (writer in convoDone) and writer not in addsongQuery and writer not in addsiteQuery and writer  in addStudyQuery):
        print((db.child('data').child(writer).get().val()))
        db.child('data').child(writer).child('2').set(str(message.content))
        addStudyQuery.remove(writer)
        return
        print('Hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')

    
        
        
    if(message.content.startswith('-todo')and writer not in todoQuery and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        todoQuery.append(writer)
        await message.channel.send('@'+writer +' What do you want to add to your to do list?')
    elif (writer in todoQuery and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        db.child('data').child(writer).child('4').push(str(message.content))
        todoQuery.remove(writer)
        return

    if(message.content.startswith('-r')and writer not in todoQuery and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        db.child('data').child(writer).child('4').set(None)
        await message.channel.send(' ToDo List Cleared!')
   

    if(message.content.startswith("-l") and writer not in todoQuery and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        try :
            lister = list(db.child('data').child(writer).child('4').get().val().values())
        except:
            lister = []
        await message.channel.send('ToDo List: ')
        counter = 1
        while(not len(lister) == 0):


            stre = (lister.pop(0))

            await message.channel.send(str(counter)+ ': ' + stre)
            counter +=1
        
        
        
    

    


    if(message.content.startswith('-g')and writer not in todoQuery and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        await message.channel.send('@'+writer+' Your goal for this session was to ' + db.child('data').child(writer).child(3).get().val())
        return
    if(message.content.startswith('-m')and writer not in todoQuery and writer not in playQueryList and writer not in questionQueryList and (writer in convoDone)and writer not in playQueryList and writer not in goalQuery and writer not in questionQueryList and (writer in convoDone)and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        await message.channel.send('@'+writer+' Feeling stressed?')
        val = random.randint(0,1)
        if(val == 0):
            await message.channel.send("Here's your favorite song!")
            await message.channel.send('Music: '+ db.child('data').child(writer).child(0).get().val())
            await message.channel.send(motivationalQuotes[random.randint(0,len(motivationalQuotes)-1)])
        else:
            await message.channel.send("Here's your favorite website!")
            await message.channel.send('Favorite Website: '+ db.child('data').child(writer).child(1).get().val())
            await message.channel.send(motivationalQuotes[random.randint(0,len(motivationalQuotes)-1)])
        return



    if(message.content.startswith('-s') and writer not in todoQuery and (writer in convoDone)and writer not in playQueryList and writer not in questionQueryList and writer not in goalQuery and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        if(not len(lastSongTracker) == 0 and not len(songqueue) == 0):

            await lastSongTracker.pop(0).delete()
            songqueue.pop(0)
        else:
            await message.channel.send('@'+writer+' Nothing in queue!')
            
        if( not len(songqueue) == 0):
            await message.channel.send(searchtoURL(str(songqueue[0])))

        return

        

    print(goalQuery)
    print('^goal')
    if(message.content.startswith('-p') and writer not in playQueryList and writer not in todoQuery and writer not in questionQueryList and (writer in convoDone) and writer not in goalQuery and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery):
        await message.channel.send('@'+writer+' Enter Song Name: ')
        playQueryList.append(writer)
        return

    elif(writer in playQueryList and writer not in questionQueryList and writer not in todoQuery and writer not in addsongQuery and writer not in addsiteQuery and writer not in addStudyQuery and (writer in convoDone) and writer not in goalQuery ):

        if(len(songqueue) == 0):
            await message.channel.send(searchtoURL(str(message.content)))
            songqueue.append(message.content)
            
        else:
            await message.channel.send('@'+writer+' Added to the queue!')
            songqueue.append(message.content)
         
     
        playQueryList.remove(writer)
        return
    if(writer in fireBaseQueryList and (writer not in firebaseQuestionDict.keys())and writer not in convoDone ):
        #print(str(message.content) + ' is my favorite song')
        firebaseQuestionDict[writer] = [searchtoURL(str(message.content))]

    if(writer in fireBaseQueryList and questionsaskedfirebaseDict[writer] == 2 and writer not in  convoDone):
        #print(str(message.content) + ' is my favorite websites')
        
        firebaseQuestionDict[writer].append('https://'+str(message.content))

        #print(firebaseQuestionDict)

    if(writer in fireBaseQueryList and questionsaskedfirebaseDict[writer] == 3 and (writer not in convoDone)):
        #print(str(message.content) + ' is productivity num')
        try:
            firebaseQuestionDict[writer].append(int(message.content))
        except:
            firebaseQuestionDict[writer].append(1)



        #print(firebaseQuestionDict)

    if(writer in fireBaseQueryList and questionsaskedfirebaseDict[writer] == 4 and (writer not in convoDone)):
        #print(str(message.content) + ' is goal of the week')
        
        firebaseQuestionDict[writer].append(str(message.content))
        convoDone.append(writer)
        db.child('data').set(firebaseQuestionDict)


        #print(firebaseQuestionDict)

    elif(writer in fireBaseQueryList and len(firebaseQuestionDict[writer]) ==3 and writer not in convoDone):
        questionsaskedfirebaseDict[writer] += 1
        await message.channel.send('@'+writer+" What is your goal for today's study session?")

    elif(writer in fireBaseQueryList and len(firebaseQuestionDict[writer]) ==2 and writer not in convoDone):
        questionsaskedfirebaseDict[writer] += 1
        await message.channel.send('@'+writer+' On a scale of 1-10, how studious would you consider yourself?')

    elif(writer in fireBaseQueryList and len(firebaseQuestionDict[writer]) ==1 and writer not in convoDone):
        questionsaskedfirebaseDict[writer] += 1
        await message.channel.send('@'+writer+' What is your favorite website? (Example: netflix.com)')
        

    if(db.child('data').child(writer).get().val() == None and (writer not in firebaseQuestionDict.keys()) and writer not in convoDone and str(message.content) in commandList):
        questionsaskedfirebaseDict[writer] = 1
        fireBaseQueryList.append(writer)
        await message.channel.send('@'+writer+' What is your favorite song?')
        

    
    #print (message.content)


    if (message.content.startswith('-w')and writer not in todoQuery and (writer not in questionQueryList) and (writer not in wolframBan)and (writer in convoDone)and writer not in playQueryList and writer not in goalQuery and (writer in convoDone) and writer not in goalQuery ):
        await message.channel.send('@'+writer+' What is your question for WolframAlpha?')
        
        questionQueryList.append(writer)
        print(questionQueryList)
        return

    elif(message.content.startswith('-w')and writer not in todoQuery and writer  in questionQueryList and (writer not in wolframBan)and (writer in convoDone)and writer not in playQueryList and writer not in goalQuery and (writer in convoDone) and writer not in goalQuery ):
        print(questionSpamDict.keys())
        if(writer not in questionSpamDict.keys() ):
            print('100')
            await message.channel.send('@'+writer+' Please ask a question before using -w command')
            questionSpamDict[writer] = 1
        elif(questionSpamDict[writer]<5):
            print('010')
            questionSpamDict[writer]+=1
            await message.channel.send('@'+writer+' This is getting annoying.')

        elif(questionSpamDict[writer]==5):
            print('001')
            await message.channel.send('@'+writer+' Now you have to say sorry or you can no longer use Wolfram')
            if(writer not in wolframBan):
                wolframBan.append(writer)
        return

    elif(writer in  questionQueryList and (writer not in wolframBan)and (writer in convoDone)and writer not in todoQuery and writer not in playQueryList and writer not in goalQuery and (writer in convoDone) and writer not in goalQuery ):
        question = str(message.content)
        questionQueryList.remove(writer)
        if(writer in questionSpamDict.keys()):
            questionSpamDict.pop(writer)
        await message.channel.send(askWolfram(question))

        return

    if(str(message.content).lower()  == 'sorry'  and writer in wolframBan and (writer in convoDone) and writer not in todoQuery and writer not in goalQuery and (writer in convoDone) and writer not in goalQuery ):
        await message.channel.send('@'+writer+'It is alright welcome back!')
        wolframBan.remove(writer)
        if(writer in questionSpamDict.keys()):
            questionSpamDict.pop(writer)
        questionQueryList.remove(writer)
        return


client.run('ODMxNjIyMjc3ODg3NTU3Njcy.YHX6mQ.DFlD2DNKGsTkNLrHxvdFvFgey48')