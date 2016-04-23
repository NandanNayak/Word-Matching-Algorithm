#import all module
import string

#arguments
threshold=1
onlyOne=1           #Developers who are in either Play Store or iTunes Store
both=2              #Developers whoe are in both Stores
headingDict={
    1:"[App_Name,  Developer_Name,  Developer_ID,  App_ID]",
    2:"[App_Name,  Developer_Name(iTunes),  Developer_Name(PlayStore),  Developer_ID(iTunes),  App_ID(iTunes),  Developer_ID(PlayStore),  App_ID(PlayStore))]"
}


#define all functions
def getLinesList(lines):        #Gets the list of all the lines in the files
    lines=lines.split('\n')
    linesList=[]    
    for line in lines:
        line=line.split(',')
        linesList.append(line)
    return linesList

def convertListToDict(linesList):  #Converts the lists to Dictionaries
    tempDict={}
    for eachList in linesList:
        if len(eachList)==4 and eachList[2] != " ":
            tempDict[eachList[2]]=eachList
    return tempDict


def checkString(str1,str2):    #Finds the matching developers across the stores
    global threshold
    count=0
    for c in str1:
        if c in str2:
           count+=1
    #print count
    matchingPercent=float(count)/float(len(str1))
    if matchingPercent>=threshold:
        return True
    else:
        return False
            

def isDevMatching(iTunesString,playStoreString):      #Does pre-processing of developer strings and finds the matching developers across the stores
    len1=len(iTunesString)
    len2=len(playStoreString)
    iTunesString=iTunesString.lower()
    #print iTunesString
    iTunesString=iTunesString.translate(None,string.punctuation)    
    playStoreString=playStoreString.lower()
    playStoreString=playStoreString.translate(None,string.punctuation)
    #print "%s, %s"%(iTunesString, playStoreString)
    
    if len1<=len2:
        flag=checkString(iTunesString,playStoreString)
    else:
        flag=checkString(playStoreString,iTunesString)
    return flag


def printDevelopers(myDict,myString,typeOfDev):     #Prints the developer results into a .txt file
    keyList=[]
    keyList=myDict.keys()
    keyList.sort()
    
    outFile=open("Output2.txt","a")
    outFile.write("\n\n\n\n%s developers\n"%(myString))
    if typeOfDev==onlyOne:
        outFile.write(headingDict[onlyOne]+"\n")
    else:
        outFile.write(headingDict[both]+"\n")
        
    for key in keyList:
        outFile.write(str(myDict[key])+"\n")


#The main function
if __name__=='__main__':    
    iTunesFile=open('iTunes_apps.csv','r')
    lines = iTunesFile.read()
    iTunesLinesList=getLinesList(lines)    
    iTunesDict=convertListToDict(iTunesLinesList)
    
    playStoreFile=open('Play_Store_apps_Book2.csv','r')
    lines = playStoreFile.read()
    playStoreLinesList=getLinesList(lines)    
    playStoreDict=convertListToDict(playStoreLinesList)

    matchingDevelopers={}
    iTunesOnlyDevelopers={}
    playStoreOnlyDevelopers={}
    for key in playStoreDict:
        tempList=[]
        if key in iTunesDict:
            if isDevMatching(iTunesDict[key][0],playStoreDict[key][0]):                
                tempList.append(key)
                tempList.append(iTunesDict[key][0])
                tempList.append(playStoreDict[key][0])
                tempList.append(iTunesDict[key][1])
                tempList.append(iTunesDict[key][3])
                tempList.append(playStoreDict[key][1])
                tempList.append(playStoreDict[key][3])
                matchingDevelopers[key]=tempList
        else:            
            tempList.append(key)            
            tempList.append(playStoreDict[key][0])
            tempList.append(playStoreDict[key][1])
            tempList.append(playStoreDict[key][3])
            playStoreOnlyDevelopers[key]=tempList

    for key in iTunesDict:
        if key not in matchingDevelopers:
            tempList=[]
            tempList.append(key)
            tempList.append(iTunesDict[key][0])            
            tempList.append(iTunesDict[key][1])
            tempList.append(iTunesDict[key][3])            
            iTunesOnlyDevelopers[key]=tempList    

    outFile=open("Output.txt","w+")
    outFile.close()   

    printDevelopers(iTunesOnlyDevelopers,"iTunes Only",onlyOne)
    printDevelopers(playStoreOnlyDevelopers,"PlayStore Only",onlyOne)
    printDevelopers(matchingDevelopers,"iTunes and PlayStore",both)



#close all files
    iTunesFile.close()
    playStoreFile.close()
    outFile.close()
