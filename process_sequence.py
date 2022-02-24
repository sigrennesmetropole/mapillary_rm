#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Process_sequence : extract metadata from IML files and upload to Mapillary
# Copyright (c) Adrien PAVIE 2020 - Under GPL 3 license
#

# Libraries imports
import argparse
import json
import datetime
import time
import sys
import re
from os import listdir, rename, mkdir
from os.path import isfile, isdir, join, exists
from PIL import Image
from mapillary_tools import authenticate
from mapillary_tools.commands.upload import Command as UploadCommand
from osgeo import ogr
from osgeo import osr

# Constants
PROVIDER="Geofit"
SECS_PER_WEEK=60*60*24*7
GPS_ERA_EPOCH=time.mktime(datetime.datetime(1980,1,6,0,0,0).timetuple())
COORDINATES_EPSG=3948

# Read command-line parameters
parser = argparse.ArgumentParser(description='Processing '+PROVIDER+' files for geolocating pictures and upload to Mapillary')
parser.add_argument('date', metavar='DATE', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help='pictures shooting date in YYYY-MM-DD format')
parser.add_argument('folder', metavar='PATH', type=str, help='path to access one sequence files (IML + JPG)')
parser.add_argument('username', metavar='MAPILLARY_USER', type=str, help='Mapillary user name')
parser.add_argument('--skip-preprocess', help='don\'t run preprocessing of pictures', action="store_true", dest='nopreprocess')
parser.add_argument('--skip-upload', help='don\'t run upload of pictures', action="store_true", dest='noupload')
args = parser.parse_args()


#
# Functions
#

# Function to convert GPS time of week into ISO date string
gpsWeek = int((time.mktime(args.date.timetuple()) - GPS_ERA_EPOCH) / SECS_PER_WEEK)
def getIsoString(gpsTime):
	epoch = GPS_ERA_EPOCH + gpsWeek * SECS_PER_WEEK + gpsTime
	gpsDate = datetime.datetime.fromtimestamp(epoch)
	return gpsDate.isoformat() + ".000000" if gpsDate.microsecond == 0 else gpsDate.isoformat()

# Function to get ISO date string from corrected time based on user input
def getFixedIsoString(gpsTime, zeroTime, startEpoch):
	gpsDate = datetime.datetime.fromtimestamp(startEpoch + gpsTime - zeroTime)
	return gpsDate.isoformat() + ".000000" if gpsDate.microsecond == 0 else gpsDate.isoformat()

# Function to transform ISO String into Mapillary date format
def getMapillaryDateString(isoDateString):
	return isoDateString.replace("-", "_").replace("T", "_").replace(":", "_").replace(".", "_")

# Function to convert x/y into lon/lat
InSR = osr.SpatialReference()
InSR.ImportFromEPSG(COORDINATES_EPSG)
OutSR = osr.SpatialReference()
OutSR.ImportFromEPSG(4326)
def projectCoordinates(x, y):
	thept = ogr.Geometry(ogr.wkbPoint)
	thept.AddPoint(float(x), float(y)) # use your coordinates here
	thept.AssignSpatialReference(InSR)    # tell the point what coordinates it's in
	thept.TransformTo(OutSR)              # project it to the out spatial reference
	return thept

# Function to print progress in check images validity
def printProgressValidity(current, total):
	sys.stdout.write('\rChecking picture validity '+str(current)+'/'+str(total)+' ('+str(int(float(current)/total*100))+'%)')
	sys.stdout.flush()

# Function to print progress in reading IML file
def printProgressIML(current, total):
	sys.stdout.write('\rReading IML file line '+str(current)+'/'+str(total)+' ('+str(int(float(current)/total*100))+'%)')
	sys.stdout.flush()

# Function to check image validity
def isImageValid(img):
	try:
		v = Image.open(img).verify()
		return True
	except:
		return False


#
# Start processing
#

# List files, separating IML and JPG
filesIml = [ f for f in listdir(args.folder) if isfile(join(args.folder, f)) and f.lower().endswith('.iml') ]
folderPictures = join(args.folder, "panoramas") if isdir(join(args.folder, "panoramas")) else args.folder
filesJpg = [ f for f in listdir(folderPictures) if isfile(join(folderPictures, f)) and f.lower().endswith('.jpg') ]

# Check validity
nbPics = len(filesJpg)
filesJpgInvalid = []
countPics = 0

for f in filesJpg:
	printProgressValidity(countPics, nbPics)
	if not isImageValid(join(folderPictures, f)):
		filesJpgInvalid.append(f)
	countPics += 1

print("")
filesJpg = [ f for f in filesJpg if f not in filesJpgInvalid ]

# Display errors if any
if len(filesIml) == 0:
	raise Exception("No IML file found")
if len(filesIml) > 1:
	raise Exception("Several IML files found, there should be only one")
if len(filesJpgInvalid) > 0:
	print("There are %d corrupted JPG files" % len(filesJpgInvalid))
if len(filesJpg) == 0:
	raise Exception("No JPG files found")

print("Found %d IML files" % len(filesIml))
print("Found %d JPG files" % len(filesJpg))


# Move corrupted JPEG in a subfolder
if len(filesJpgInvalid) > 0:
	corruptedFolder = join(folderPictures, "corrupted")
	if not exists(corruptedFolder):
		mkdir(corruptedFolder)
	for img in filesJpgInvalid:
		rename(join(folderPictures, img), join(corruptedFolder, img))
	print("Moved %d corrupted pictures to %s" % (len(filesJpgInvalid), corruptedFolder))

if not args.nopreprocess:
	# Parse IML file and store information in memory
	picturesMetadata = dict()
	currentMetadata = None
	skipCount = 0
	count = 0
	askedForDate = False
	fixStartDate = False
	fixedStartDate = None
	fixedStartDelta = None

	iml = open(join(args.folder, filesIml[0]), "r")
	nbLines = sum(1 for _ in iml)
	iml.seek(0)

	for line in iml:
		# Show progress
		count += 1
		printProgressIML(count, nbLines)

		# Read key/value for current line
		lineData = line.strip().split("=")
		key = lineData[0]
		value = lineData[1] if len(lineData) > 1 else None

		# If key is image
		if key == "Image":
			# Image entry separates every file metadata
			# So we store previous metadata in global object
			if currentMetadata is not None:
				picturesMetadata[currentMetadata["filename"]] = currentMetadata

			# Check image exist in folder
			image = re.sub('_\d{1,2}_', '_', value) # Change name format

			# If exists, create empty metadata to store next picture info
			if image in filesJpg:
				currentMetadata = dict()
				currentMetadata["filename"] = join(args.folder, image)
			# If not, create void metadata to skip processing
			else:
				currentMetadata = None
				skipCount += 1

		# Check other keys if current image exists in JPG files
		elif currentMetadata is not None:
			if key == "Time":
				currentMetadata["MAPCaptureTime"] = getMapillaryDateString(getIsoString(float(value)) if not fixStartDate else getFixedIsoString(float(value), fixedStartDelta, fixedStartDate))

				# Ask user for potential start date change if necessary
				if not askedForDate:
					askedForDate = True
					print("\nStart date read from IML : %s" % currentMetadata["MAPCaptureTime"])
					askChangeDate = None
					while askChangeDate != "y" and askChangeDate != "n":
						askChangeDate = input("Do you want to use your date instead (%s) ? (y/n) " % args.date.date())

					if askChangeDate == "y":
						fixStartDate = True
						hour = ""
						hourRgx = re.compile("\d{2}\:\d{2}")
						while not hourRgx.match(hour):
							hour = input("Set the capture start time (in HH:MM format) : ")

						fixedStartDate = (datetime.datetime.strptime(str(args.date.date()) + " " + hour, '%Y-%m-%d %H:%M') - datetime.datetime.fromtimestamp(0)).total_seconds()
						fixedStartDelta = float(value)


			elif key == "Xyz":
				coords = value.split(" ")
				ptx = projectCoordinates(coords[0], coords[1])
				# X/Y are inverted in IML file
				currentMetadata["MAPLatitude"] = ptx.GetX()
				currentMetadata["MAPLongitude"] = ptx.GetY()
				currentMetadata["MAPAltitude"] = float(coords[2])

			# HRP = heading/roll/pitch
			elif key == "Hrp":
				hrp = value.split(" ")
				currentMetadata["MAPCompassHeading"] = { "TrueHeading": float(hrp[0]), "MagneticHeading": float(hrp[0]) }
				#currentMetadata["r"] = hrp[1] # Not used by Mapillary script
				#currentMetadata["p"] = hrp[2] # Not used by Mapillary script

			# OPK = Omega/phi/kappa (alternative version of HRP)
			elif key == "Opk":
				opk = value.split(" ")
				# ~ currentMetadata["p"] = opk[0] # Pitch, not used by Mapillary script
				# ~ currentMetadata["r"] = opk[1] # Roll, not used by Mapillary script
				currentMetadata["MAPCompassHeading"] = { "TrueHeading": float(opk[2]), "MagneticHeading": float(opk[2]) }

	# Write metadata as JSON
	jsonpath = join(args.folder, "mapillary_image_description.json")
	descs = list(picturesMetadata.values())
	with open(jsonpath, "w") as jsonfile:
		jsonfile.write(json.dumps(descs, indent=2))

	# Print JSON processing results
	print("")
	if skipCount > 0:
		print("Skipped %d images listed in IML but not in path" % skipCount)
	print("Metadata written in %s" % jsonpath)
else:
	print("Pictures pre-processing is skipped")


# Call Mapillary commands for upload
if not args.noupload:
	# ~ user_items = authenticate.authenticate_user(args.username)
	UploadCommand().run({
		"--user_name": args.username,
		"import_path": args.folder,
		# ~ "--dry_run": True
	})
else:
	print("Pictures upload is skipped")
