"""
    Nicholas Walters
    2224339
    CITS1401 - Problem Solving and Programming
    University Of Western Australia
    Date Updated: 18/09/2017
    
"""


def getCandidates(f):
    candidatesList = []
    try:
        file = open(f, "r")
        # for each line/person in the file, put it in the List of candidates
        for person in file:
            candidatesList.append(person[0: len(person)-1])
        file.close()
        
    except IOError:
        # print an error, if the filename cannot be found in present working directory
        print("--ERROR-- Cannnot find the file specified: " + f)

    return(candidatesList)



def parseVote(s):

    # remove any spaces, and check if its a number (not a string or something else)
    if(s.strip().isnumeric()):
        return int(s.strip())

    # check if the value is empty. By removing any whitespace and checking for "" of length 0
    elif(len(s.strip()) == 0):
        return(0)
    else:
        return(-1)



def parsePaper(s, n):
    # split s into its components, and use as variable throughout
    ballotPaper = s.split(",")
    list1 = []
    list2 = []
    errorCode = ""

    # check if no.of votes is greater than n.of participants first
    if(len(ballotPaper) > n):
        errorCode = "too long"
        list1.append([])
        list1.append(errorCode)
        return(list1)

    #if all values in ballotPaper is 0, return blank array
    elif(all(parseVote(x) == 0 for x in ballotPaper)):
        errorCode = "blank"
        list1.append([])
        list1.append(errorCode)
        return(list1)
        
    
    for value in ballotPaper:
        if(parseVote(value) == -1):
            errorCode = "non-digits"
            list1.append([])
            list1.append(errorCode)
            return(list1)

    for validNum in ballotPaper:
        list1.append(parseVote(validNum))
        # all values in ballotPaper are valid, so we can put it in array. Need to put it through parseVote first, so zeros count.
    list2.append(list1)
    list2.append(errorCode) # there is no errorCode as it equals ""
    return(list2)





def getPapers(f, n):
    papers = []
    try:
        file = open(f, "r")
        for line in file:
            papers.append(parsePaper(line, n))
        file.close()

    except IOError:
            print("--ERROR-- Could not find the file specified: " + f)

    return(papers)
        



def normalisePaper(p, n): # sum(p) > 0
    y = sum(p)
    # assign values to each participants votes/score
    for index, item in enumerate(p, start=0):
        p[index] = p[index] / y
    if len(p) < n:
        for x in range(len(p),n):
            p.append(0)
    return p





def normalisePapers(ps, n):
    pf = []
    #collect every single paper provided and normalise it into one list
    for p in ps:
        normalised_p = normalisePaper(p, n)
        pf.append(normalised_p)
    return(pf)
        
            


def countVotes(cs, ps): 
    k = {}
    for i in range(len(cs)):
        count = 0
        for j, item in enumerate(ps, start=0):
            count = count + item[i]
        k[cs[i]] = count
    s = sorted([[value,key] for [key,value] in k.items()],reverse = True)
    return s



def printCount(c):
    for r in c:
        print(" " + str(format(r[0],'.2f')) + " " + str(r[1]))
        # add whitespace to each printed out line before results, and format numbered results correctly.


        
def main():
    candid = getCandidates(input("Candidate List File Name: "))
    n = len(candid)
    
    papers = getPapers(input("Papers List File Name: "), n)
    
    inf_count = 0
    papers2 = []
    for num in papers:
        # informal votes = no of error codes
        # formal votes are ""
        if (num[1] != ""):
            inf_count = inf_count + 1
        papers2.append(num[0])
        # formal votes = total votes - number of informal votes
    print('Nerdvanian election 2017\n\nThere were ' + str(inf_count) + ' informal votes\nThere were ' + str((len(papers)-inf_count)) + ' formal votes\n')
    papers = normalisePapers(papers2, n)
    printCount(countVotes(candid, papers))
main()

