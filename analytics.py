import os

DIFFICULTYMAP = {}
COMPANYWISEPROBLEMSETLIST = []
COMPANYWISEPROBLEMLISTLIST = []
SOLVEDPROBLEMSET = set()
SOLVEDPROBLEMLIST = []
HITCOUNTER = {}
SORTEDHITS = []

def readSolvedProblems(filename):
	f = open(filename)
	for line in f:
		probId = int(line)
		SOLVEDPROBLEMLIST.append(probId)
		SOLVEDPROBLEMSET.add(probId)
	f.close()
	SOLVEDPROBLEMLIST.sort()

def readAllCompanyData(filenames):
	for filepaths in filenames:
		companyName, problemList, problemSet = readData(filepaths)
		COMPANYWISEPROBLEMSETLIST.append(problemSet)
		COMPANYWISEPROBLEMLISTLIST.append(problemList)
	for key, value in HITCOUNTER.items():
		SORTEDHITS.append((value, key))
	SORTEDHITS.sort(key=lambda tup: tup[0], reverse=True )



def difficultyStringtoId(str):
	str = str.strip()
	if str=='Easy':
		return 0
	elif str == 'Medium':
		return 1
	else:
		return 2

def classifyProblemListByDifficulty(probIds):
	easy = []
	medium = []
	hard = []
	for probs in probIds:
		if DIFFICULTYMAP[probs]==1:
			medium.append(probs)
		elif DIFFICULTYMAP[probs]==2:
			hard.append(probs)
		else:
			easy.append(probs)
	return [easy, medium, hard]

def classifyProblemListBySolved(probIds):
	solved = []
	unsolved = []
	for probs in probIds:
		if probs in SOLVEDPROBLEMSET:
			solved.append(probs)
		else:
			unsolved.append(probs)
	return [solved, unsolved]

def getTopKUnsolved(k):
	counter = 0
	topKUnsolved = []
	for items in SORTEDHITS:
		if items[1] in SOLVEDPROBLEMSET:
			continue
		topKUnsolved.append(items[1])
		counter += 1
		if (counter==k):
			break
	topKUnsolved.sort()
	return topKUnsolved



def analytics():
	
	#most frequently occuring problems
	topkUnsolved =  getTopKUnsolved(40) #list(set.intersection(*COMPANYWISEPROBLEMSETLIST))
	[tEasy, tMedium, tHard] = classifyProblemListByDifficulty(topkUnsolved)
	print('\nMOST FREQUENTLY OCCURING UNSOLVED PROBLEMS')
	print('*************EASY*******************************')
	print([ (t, HITCOUNTER[t]) for t in tEasy])
	print('*************MEDIUM*****************************')
	print([ (t, HITCOUNTER[t]) for t in tMedium])
	print('*************HARD*******************************')
	print([ (t, HITCOUNTER[t]) for t in tHard])

	#next find the union of all problems 
	unionList = list(set.union(*COMPANYWISEPROBLEMSETLIST))
	unionList.sort()
	[uEasy, uMedium, uHard] = classifyProblemListByDifficulty(unionList)
	print('\nALL PROBLEMS (UNION OF ALL COMPANIES)')
	print('*************EASY*******************************')
	# print(uEasy)
	[ueSolved, ueUnsolved] = classifyProblemListBySolved(uEasy)
	print('Solved({}/{}) {}'.format(len(ueSolved), len(uEasy), ueSolved))
	print('Unsolved({}/{}) {}'.format(len(ueUnsolved), len(uEasy), ueUnsolved))
	print('*************MEDIUM*****************************')
	# print(uMedium)
	[umSolved, umUnsolved] = classifyProblemListBySolved(uMedium)
	print('Solved({}/{}) {}'.format(len(umSolved), len(uMedium), umSolved))
	print('Unsolved({}/{}) {}'.format(len(umUnsolved), len(uMedium), umUnsolved))
	print('*************HARD*******************************')
	# print(uHard)
	[uhSolved, uhUnsolved] = classifyProblemListBySolved(uHard)
	print('Solved({}/{}) {}'.format(len(uhSolved), len(uHard), uhSolved))
	print('Unsolved({}/{}) {}'.format(len(uhUnsolved), len(uHard), uhUnsolved))
	


def readData(filename):
	#try to obtain the filename 
	basename = os.path.basename(filename)
	#remove the .txt portion 
	dotIdx = basename.find('.')
	companyName = basename[0:dotIdx].upper()
	f = open(filename, 'r')
	problemList = []
	problemSet = set()
	for line in f:
		data = line.split(' ')
		problemID = int(data[0])
		difficultyString = data[-1]
		if problemID not in DIFFICULTYMAP:
			DIFFICULTYMAP[problemID] = difficultyStringtoId(difficultyString)
		HITCOUNTER[problemID] = HITCOUNTER.get(problemID,0) + 1
		problemList.append(problemID)
		problemSet.add(problemID)
	f.close()
	print('Finished processing company {}'.format(companyName))
	return [companyName, problemList, problemSet]

def getAllFiles(dir_path):
	files = []
	for f in os.listdir(dir_path):
		if os.path.isfile(os.path.join(dir_path,f)):
			if not f.startswith('.'):
				files.append(os.path.join(dir_path,f))
	return files

CURRENTPATH = os.getcwd()
DATADIRECTORYPATH = os.path.join(CURRENTPATH, 'data')
#remember you need to ignore any files that start with . or is a directory 
COMPANYFILES = getAllFiles(DATADIRECTORYPATH)
SOLVEDPROBLEMFILE = os.path.join(CURRENTPATH, 'solved.txt')

readAllCompanyData(COMPANYFILES)
readSolvedProblems(SOLVEDPROBLEMFILE)
analytics()