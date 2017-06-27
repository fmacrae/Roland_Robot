#! /usr/bin/python
from notification import Notifier
Notification_Settings_File = 'Notification_Settings.csv'
notifier = Notifier()
notifier.load_config(Notification_Settings_File)
notifier.tweet('Found a Poop!', 'Poop', 'poop.png', 'High')
notifier.email('Found a Poop!', 'Poop', 'poop.png', 'High')
