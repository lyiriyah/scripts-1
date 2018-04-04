#!/bin/sh
# Copyright Whatever 2018 Tener
# Officially my first addition to this repo for FreeBSD :)

x=`cat <<EOF | rofi -dmenu -i -p "Chrome: "
GMail
Google Inbox
Google Drive
Google Calendar
Google Photos
Google Keep
GitHub
WakaTime
Reddit
Sheets: Places
EOF
`
# Sheets: Visa
# Sheets: iPad
# Sheets: VPN
# Sheets: Sleep

# when i get around to doing this in python:
# check for the presence of "://" in the input and launch that site instead
# of searching for it.
# also, add some aliases for different search engines?
case "$x" in
	"Sheets: Places")
		exec chrome "https://sheets.google.com"
		# need a good way to make these spreadsheet addresses not visible on github..
		break
		;;
	"GMail")
		exec chrome "https://gmail.com"
		break
		;;
	"WakaTime")
		exec chrome "https://wakatime.com"
		break
		;;
	"Google Drive")
		exec chrome "https://drive.google.com"
		break
		;;
	"Google Photos")
		exec chrome "https://photos.google.com"
		break
		;;
	"Google Inbox")
		exec chrome "https://inbox.google.com"
		break
		;;
	"Google Calendar")
		exec chrome "https://calendar.google.com"
		break
		;;
	"Reddit")
		exec chrome "https://reddit.com"
		break
		;;
	"Google Keep")
		exec chrome "https://keep.google.com"
		break
		;;
	"GitHub")
		exec chrome "https://github.com"
		break
		;;
	*)
		# just search (for now)
		[ -z "$x" ] || exec chrome "https://google.com/search?q=$x"
esac
