from os.path import isfile

def write_stats(data):

	# takes the list() and writes it

	# show ranking

	with open("statistics.txt", "w+") as f:
		for s in data:
			name = s[0]
			name = name.replace(" ","|")
			line =  name + " " + str(s[1]) + "\n"
			f.write(line)

def sort(arr):

	for i in range(len(arr)-1, 0, -1):
		for x in range(i):
			if int(arr[x][1]) < int(arr[x+1][1]):
				temp = arr[x+1]
				arr[x+1] = arr[x]
				arr[x] = temp
	return arr


def process_stats(stat):

	"""Returns names and scores correctly with spaces"""

	data = []

	data.append(stat) # new score

	if isfile("statistics.txt"): # if there is, read from it and if not, skip and make the file
		with open("statistics.txt", "r") as f:
			raw_data = f.readlines()
			for i in raw_data:
				i = i.replace("\n", "")
				score = i.split(" ")
				score = score[0].replace("|", " "), score[1]
				data.append(score)

	data = sort(data)

	if len(data) > 10: data.pop()

	#print data

	return data

#stat = ("BENIS", 1)
#dat = process_stats(stat)
#write_stats(dat)


# it takes list of 10 or so positions and manages it
# separate names with | <- save 

# 1. if isfile:
# 1. a)
#      read rankings
# 1. b) compare rankings to new score
# 1. c) update if needed
# 1. d) save rankings
# 2. else:
# 2. a) create file
# 2. b) settle new score
# 2. c) save rankings

# after setting the new record, show records
