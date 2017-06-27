import tweepy
import csv
from gmailAPI import SendMessage


class Notifier():
	
	
	
	def __init__(self):
		#Need to get these from a config file
		self.consumer_key ='xxx'
		self.consumer_secret ='xxxx'
		self.access_token = 'xxxx'
		self.access_token_secret = 'xxxx'
		self.gmail_user = 'Roland.Hooverbot@gmail.com'
		self.owner_email = 'finlay.macrae@gmail.com'

		
	def load_config(self, config_file_name):
		with open(config_file_name, 'rb') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				if row['Setting'] == 'consumer_key':
					self.consumer_key = row['Value']
				elif row['Setting'] == 'consumer_secret':
					self.consumer_secret = row['Value']
				elif row['Setting'] == 'access_token':
					self.access_token = row['Value']
				elif row['Setting'] == 'access_token_secret':
					self.access_token_secret = row['Value']
				elif row['Setting'] == 'gmail_user':
					self.gmail_user = row['Value']
				elif row['Setting'] == 'owner_email':
					self.owner_email = row['Value']
				print(row['Setting'], row['Value'])
		#Authenticate
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_token, self.access_token_secret)
		self.api = tweepy.API(auth)



	def tweet(self, notification_message, object_type, picture_location_and_name, priority):
		#post the picture to an online location
		#construct the message and check it's small enough
		self.api.update_with_media(picture_location_and_name, status=notification_message)
		print 'sent tweet'

	def email(self, notification_message, object_type, picture_location_and_name, priority):
		to = self.owner_email
		sender = self.gmail_user
		subject = "Found " + object_type
		msgHtml = "Hi<br/>" + notification_message
		msgPlain = "Hi\n" + notification_message
		SendMessage(sender, to, subject, msgHtml, msgPlain, picture_location_and_name)

