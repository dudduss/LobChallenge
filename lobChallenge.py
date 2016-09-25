import lob 
from urllib.request import urlopen
import json

lob.api_key = 'test_b3ace3a1b52dca321f5c1b8a60bb3016fc8'


# Checks whether the input is valid before sending to Google Civic API and Lob
def checkValidInput():
	validInput = False
	global message
	global from_state
	global from_zipcode

	while (validInput == False):
		if (len(message.split()) > 200):
			print("Sorry, your message is too long. Please shorten it to under 200 words.")
			message = input("And what would you like to send to your senator? ")
			continue
		if (len(from_state) != 2):
			print("Sorry, please enter your state in abbreviated form with 2 characters.")
			from_state = input("What state are you from (abbreviated)? ")
			continue
		if (len(from_zipcode) != 5):
			print("Sorry, please enter a valid zipcode with at least 5 characters.")
			from_zipcode = input("What is your zipcode? ")
			continue
		validInput = True

	return

# Gets the first senator based on user's location
def getSenator():
	try:
		url = "https://www.googleapis.com/civicinfo/v2/representatives?address=" + from_city + "&includeOffices=true&roles=legislatorUpperBody&key=AIzaSyAU55DtK8jxhiBZKCG95Lag7La72sbQBYw"
		response = urlopen(url).read().decode('utf8')
		jsonData = json.loads(response)
	except:
		print("Sorry, the address information you have given us is invalid. Please try again.")

	#Parsing JSON
	senator = jsonData['officials'][0]

	to_name = senator['name']
	to_address1 = senator['address'][0]['line1']

	if 'line2' in senator['address'][0]:
		to_address2 = senator['address'][0]['line2']
	else:
		to_address2 = ""

	to_state = senator['address'][0]['state']
	to_city = senator['address'][0]['city'].title()
	to_zipcode = senator['address'][0]['zip']


	return (to_name, to_address1, to_address2, to_state, to_city, to_zipcode)

# Sends letter to selected senator via Lob
def sendLetter(senatorInfo):
	try:
		letter_request = lob.Letter.create(
		  description = 'Letter to Senator',
		  to_address = {
		      'name': senatorInfo[0],
		      'address_line1': senatorInfo[1],
		      'address_line2': senatorInfo[2],
		      'address_city': senatorInfo[4],
		      'address_state': senatorInfo[3],
		      'address_zip': senatorInfo[5],
		      'address_country': 'US'
		  },
		  from_address = {
		      'name': from_name,
		      'address_line1': from_address1,
		      'address_line2': from_address2,
		      'address_city': from_city,
		      'address_state': from_state,
		      'address_zip': from_zipcode,
		      'address_country': 'US'
		  },
		  file = '<html style="padding-top: 3in; margin: .5in;">' + message + '</html>',
		  data = {
		  },
		  color = True
		)

		letterUrl = letter_request['url']
		print("\nThanks a lot! We have sent your message as a letter to " + senatorInfo[0] + ". You can access the letter at the URL below: \n \n" + letterUrl + "\n \n")
	except Exception as e:
		print(e)
		print("Sorry we were unable to send a letter at this time. Please try again later.")


#Collecting Inputs 
from_name = input("What's your name? ")
from_address1 = input("What's the first line of your address? ")
from_address2 = input("What's the second line of your address? ")
from_city = input("What city are you from? ")
from_state = input("What state are you from (abbreviated)? ")
from_zipcode = input("What is your zipcode? ")
message = input("And what would you like to send to your senator? ")

# from_name = "Sampath"
# from_address1 = "3211 Lady Fern Loop"
# from_address2 = ""
# from_city = "Olympia"
# from_state = "WA"
# from_zipcode = "98502"
# message = "ANYTHING"

checkValidInput()
senatorInfo = getSenator()
# print(senatorInfo)
sendLetter(senatorInfo)






