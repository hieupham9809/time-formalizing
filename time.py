#!/usr/bin/env python
from datetime import *
import re

#Constants list:
date_time_pattern = {
# full day, month, year
	"day_month_year":
	[
		"ngày (\\d\\d?) tháng (\\d\\d?) năm (\\d\\d\\d?\\d?)",
		"ngày (\\d\\d?)[/-](\\d\\d?)[/-](\\d\\d\\d?\\d?)",
		"(\\d\\d?)[/-](\\d\\d?)[/-](\\d\\d\\d?\\d?)"
	],
# month, year
	"month_year":
	[
		"tháng (\\d\\d?) năm (\\d\\d\\d?\\d?)",
		"tháng (\\d\\d?)[/-](\\d\\d\\d?\\d?)",
		"(\\d\\d?)[/-](\\d\\d\\d\\d)"
	],
	
# day, month
	"day_month":
	[
		"ngày (\\d\\d?) tháng (\\d\\d?)",
		"ngày (\\d\\d?)[/-](\\d\\d?)",
		"ngày (\\d\\d?)",
		"(\\d\\d?)[/-](\\d\\d?)"
	],
	
# single day | month | year
	"day_single":
	[
		"ngày (\\d\\d?)"
	],

	"month_single":
	[
		"tháng (\\d\\d?)"
	],
	"year_single":
	[
		"năm (\\d\\d\\d?\\d?)"
	],

#full hour, minute, second
	"hour_minute_second":
	[
		"(\\d\\d?) giờ (\\d\\d?) phút (\\d\\d?) giây",
		"(\\d\\d?)[hg:](\\d\\d?)[mp:](\\d\\d?)[s]?"
	],

#hour, minute
	"hour_minute":
	[
		"(\\d\\d?) giờ (\\d\\d?) phút",
		"(\\d\\d?)[hg:](\\d\\d?)[mp]?"
	],	

	#single hour 
	"hour_single":
	[
		"(\\d\\d?) giờ",
		"(\\d\\d?)[hg]"
	]
	
	
}



separator_list = [
	"từ ({0}) đến ({1})",
	"({0}) đến ({1})",
	"({0}) cho tới ({1})"
]
class ActivityDateTime:
	def __init__(self, day=0, month=0, year=0, hour=0, minute=0, second=0):
		self.day = day
		self.month = month
		self.year = year
		self.hour = hour
		self.minute = minute
		self.second = second
	def printRawValue(self):
		print("{0}/{1}/{2} {3}:{4}:{5}".format(self.day, self.month, self.year, self.hour, self.minute, self.second))
	def validAndSetDay(self, dayString):
		dayInt = int(dayString)
		if 1 <= dayInt <= 31:
			self.day = dayInt
		else:
			print(">>>>>>>>>>>ERR: invalid day!")
	def validAndSetMonth(self, monthString):
		monthInt = int(monthString)
		if 1 <= monthInt <= 12:
			self.month = monthInt
		else:
			print(">>>>>>>>>>>ERR: invalid month")
	def validAndSetYear(self, yearString):
		yearInt = int(yearString)
		if MINYEAR <= yearInt <= MAXYEAR:
			self.year = yearInt
		else:
			print(">>>>>>>>>>>ERR: invalid year")
	def validAndSetHour(self, hourString):
		hourInt = int(hourString)
		if 0 <= hourInt < 24:
			self.hour = hourInt
		else:
			print(">>>>>>>>>>>ERR: invalid hour")
	def validAndSetMinute(self, minuteString):
		minuteInt = int(minuteString)
		if 0 <= minuteInt < 60:
			self.minute = minuteInt
		else:
			print(">>>>>>>>>>>ERR: invalid minute")
	def validAndSetSecond(self, secondString):
		secondInt = int(secondString)
		if 0 <= secondInt < 60:
			self.second = secondInt
		else:
			print(">>>>>>>>>>>ERR: invalid second")

class ActivityDateTimeToUnixFactory:
	def processRawDatetimeInput(self, rawDatetime):
		rawValueSplitted = self.splitRawValues(rawDatetime)
		if len(rawValueSplitted) > 1:
			pass
			# activityDateTime = self.processSingleDatetimeInput(rawDatetime)
		elif len(rawValueSplitted) == 1:
			activityDateTime = self.processSingleDatetimeInput(rawValueSplitted[0])
			
			# unixFormat = self.convertToUnixFormat(activityDateTime)
			# return unixFormat
		else:
			print("ERROR: cannot extract any value")
	def splitRawValues(self, rawDatetime):
		date_time_pattern_joined = ""
		for separator in separator_list:
			# date_time_pattern = single_date_regex_list + single_time_regex_list
			date_time_pattern_joined = "(({0}).*)+".format("|".join([pattern for key in date_time_pattern for pattern in date_time_pattern[key]]))
			# print(date_time_pattern_joined)
			full_pattern = separator.format(date_time_pattern_joined, date_time_pattern_joined)
			# print(full_pattern)
			separator_search_result = re.findall(full_pattern, rawDatetime, re.IGNORECASE)
			# print(separator_search_result)
			if len(separator_search_result) > 0:
				# print(separator_search_result[0][0])
				# print(separator_search_result[0][3])
				return [separator_search_result[0][0], separator_search_result[0][3]]
			

		single_search_result = re.findall("({0})".format(date_time_pattern_joined), rawDatetime, re.IGNORECASE)
		# print(single_search_result[0][0])
		if len(single_search_result) > 0:
			return [single_search_result[0][0]]
		else:
			return []

			# if (search_result):
			# 	print(search_result)
			# 	# print(search_result.group(0))
			# 	print(search_result.group(1).split())
			# 	print(search_result.group(2).split())
			# 	return
			# else:
			# 	print("not found pattern")	
			# for date_pattern in single_date_regex_list:
				
			# 	for time_pattern in single_time_regex_list:
					
	def test_splitRawValues(self, inputDict):
		for index, value in enumerate(inputDict):
			if ";".join(self.splitRawValues(inputDict[index]["rawDatetime"])) == inputDict[index]["expectedOutput"]:
				print("test case {0}: PASS".format(index))
			else:
				print("test case {0}: FAIL".format(index))			


	def processSingleDatetimeInput(self, datetime):
		activityDateTime = ActivityDateTime()
		

		phraseOneOutput = self.phraseOne(datetime, activityDateTime)
		print(phraseOneOutput)
		
		phraseTwoOutput = self.phraseTwo(phraseOneOutput, activityDateTime)

		activityDateTime.printRawValue()
		return activityDateTime
		

	def phraseOne(self, datetime, activityDateTime):
		# find all full pattern: day-month-year, hour-minute-second
		inputDatetime = datetime

		# for full day-month-year
		for pattern in date_time_pattern["day_month_year"]:
			date_full_pattern = "({0})".format(pattern)
			date_full_result = re.findall(date_full_pattern, inputDatetime, re.IGNORECASE)
			print(date_full_result)
			if date_full_result:
				inputDatetime = inputDatetime.replace(date_full_result[0][0], "")
				activityDateTime.validAndSetDay(date_full_result[0][1])
				activityDateTime.validAndSetMonth(date_full_result[0][2])
				activityDateTime.validAndSetYear(date_full_result[0][3])

				break

		# for full hour-minute-second
		
		for pattern in date_time_pattern["hour_minute_second"]:
			time_full_pattern = "({0})".format(pattern)
			time_full_result = re.findall(time_full_pattern, inputDatetime, re.IGNORECASE)
			print(time_full_result)
			if time_full_result:
				inputDatetime = inputDatetime.replace(time_full_result[0][0], "")
				activityDateTime.validAndSetHour(time_full_result[0][1])
				activityDateTime.validAndSetMinute(time_full_result[0][2])
				activityDateTime.validAndSetSecond(time_full_result[0][3])

				break

		return inputDatetime

	def phraseTwo(self, datetime, activityDateTime):
		inputDatetime = datetime

		# for month-year
		for pattern in date_time_pattern["month_year"]:
			date_full_pattern = "({0})".format(pattern)
			date_full_result = re.findall(date_full_pattern, inputDatetime, re.IGNORECASE)
			print(date_full_result)
			if date_full_result:
				inputDatetime = inputDatetime.replace(date_full_result[0][0], "")				
				activityDateTime.validAndSetMonth(date_full_result[0][1])
				activityDateTime.validAndSetYear(date_full_result[0][2])

				break

		# for day-month
		for pattern in date_time_pattern["day_month"]:
			date_full_pattern = "({0})".format(pattern)
			date_full_result = re.findall(date_full_pattern, inputDatetime, re.IGNORECASE)
			print(date_full_result)
			if date_full_result:
				inputDatetime = inputDatetime.replace(date_full_result[0][0], "")	
				activityDateTime.validAndSetDay(date_full_result[0][1])
				activityDateTime.validAndSetMonth(date_full_result[0][2])

				break

		# for full hour-minute
		
		for pattern in date_time_pattern["hour_minute"]:
			time_full_pattern = "({0})".format(pattern)
			time_full_result = re.findall(time_full_pattern, inputDatetime, re.IGNORECASE)
			print(time_full_result)
			if time_full_result:
				inputDatetime = inputDatetime.replace(time_full_result[0][0], "")
				activityDateTime.validAndSetHour(time_full_result[0][1])
				activityDateTime.validAndSetMinute(time_full_result[0][2])
				

				break

		return inputDatetime



factory = ActivityDateTimeToUnixFactory()

# factory.test_splitRawValues(
# 		[
# 			{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019;16h ngày 25/12/2019"},
# 			{"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019;16h ngày 25/12/2019"},
# 			{"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"},
# 			{"rawDatetime":"thời gian dự thi: vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"},
# 			{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"9g30 ngày 24/12/2019"}

# 		]
# 	)

# factory.processSingleDatetimeInput("9h30-10h30 ngày 24/12/2019")
factory.processSingleDatetimeInput("9h30 - 10h30 ngày 24 tháng 12 năm 2019")
