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
		" (\\d\\d?)[/-](\\d\\d?)"
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
		self.others = {
			"day": [],
			"month": [],
			"year": [],
			"hour": [],
			"minute": [],
			"second": []
		}
	def extractAllValue(self):
		# print("{0}/{1}/{2} {3}:{4}:{5}".format(self.day, self.month, self.year, self.hour, self.minute, self.second))
		print(self.others)
		return "{0}/{1}/{2} {3}:{4}:{5}".format(self.day, self.month, self.year, self.hour, self.minute, self.second)
	def convertToUnix(self):
		dt = datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second)
		return int(dt.replace(tzinfo=timezone.utc).timestamp())
	def validAndSetDay(self, dayString):
		if self.day != 0:
			self.others["day"].append(dayString)
			# print("\"{}\" archived".format(dayString))
			return
		dayInt = int(dayString)
		if 1 <= dayInt <= 31:
			self.day = dayInt
		else:
			print(">>>>>>>>>>>ERR: invalid day!")
	def validAndSetMonth(self, monthString):
		if self.month != 0:
			self.others["month"].append(monthString)
			# print("\"{}\" archived".format(monthString))
			return
		monthInt = int(monthString)
		if 1 <= monthInt <= 12:
			self.month = monthInt
		else:
			print(">>>>>>>>>>>ERR: invalid month")
	def validAndSetYear(self, yearString):
		if self.year != 0:
			self.others["year"].append(yearString)
			# print("\"{}\" archived".format(yearString))
			return
		yearInt = int(yearString)
		if MINYEAR <= yearInt <= MAXYEAR:
			self.year = yearInt
		else:
			print(">>>>>>>>>>>ERR: invalid year")
	def validAndSetHour(self, hourString):
		if self.hour != 0:
			self.others["hour"].append(hourString)
			# print("\"{}\" archived".format(hourString))
			return
		hourInt = int(hourString)
		if 0 <= hourInt < 24:
			self.hour = hourInt
		else:
			print(">>>>>>>>>>>ERR: invalid hour")
	def validAndSetMinute(self, minuteString):
		if self.minute != 0:
			self.others["minute"].append(minuteString)
			# print("\"{}\" archived".format(minuteString))
			return
		minuteInt = int(minuteString)
		if 0 <= minuteInt < 60:
			self.minute = minuteInt
		else:
			print(">>>>>>>>>>>ERR: invalid minute")
	def validAndSetSecond(self, secondString):
		if self.second != 0:
			self.others["second"].append(secondString)
			# print("\"{}\" archived".format(secondString))
			return
		secondInt = int(secondString)
		if 0 <= secondInt < 60:
			self.second = secondInt
		else:
			print(">>>>>>>>>>>ERR: invalid second")

class ActivityDateTimeToUnixFactory:
	def test_processRawDatetimeInput(self, inputDict):
		for index, value in enumerate(inputDict):
			datetimeObjects = self.processRawDatetimeInput(inputDict[index]["rawDatetime"])
			output = ";".join([datetimeObject.extractAllValue() for datetimeObject in datetimeObjects])
			if output == inputDict[index]["expectedOutput"]:
				print("test case {0}: PASS".format(index))
				# print("utc: {}".format(datetimeObject.convertToUnix()))

			else:
				print("test case {0}: FAIL".format(index))
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))
	def processRawDatetimeInput(self, rawDatetime):
		rawValueSplitted = self.splitRawValues(rawDatetime)
		if len(rawValueSplitted) > 1:
			slot1 = self.processSingleDatetimeInput(rawValueSplitted[0])
			slot2 = self.processSingleDatetimeInput(rawValueSplitted[1])
			# print(slot1.extractAllValue())
			# print(slot2.extractAllValue())
			return [slot1, slot2]
			# activityDateTime = self.processSingleDatetimeInput(rawDatetime)
		elif len(rawValueSplitted) == 1:
			slot1 = self.processSingleDatetimeInput(rawValueSplitted[0])
			# print(slot1.extractAllValue())
			return [slot1]
			
			# unixFormat = self.convertToUnixFormat(activityDateTime)
			# return unixFormat
		else:
			print("ERROR: cannot extract any value")
	def splitRawValues(self, rawDatetime):
		date_time_pattern_joined = ""
		for separator in separator_list:
			# date_time_pattern = single_date_regex_list + single_time_regex_list
			pattern_list = [pattern for key in date_time_pattern for pattern in date_time_pattern[key]]

			for pattern in pattern_list:

				date_time_pattern_joined = "({0})".format(pattern)
				print(date_time_pattern_joined)
				full_pattern = separator.format(date_time_pattern_joined, date_time_pattern_joined)
				print(full_pattern)
				separator_search_result = re.findall(full_pattern, rawDatetime, re.IGNORECASE)
				print(separator_search_result)
				if len(separator_search_result) > 0:
					# print(separator_search_result[0][0])
					# print(separator_search_result[0][3])
					return [separator_search_result[0][0], separator_search_result[0][3]]
				print("({0})".format(date_time_pattern_joined))
				single_search_result = re.findall("({0})".format(date_time_pattern_joined), rawDatetime, re.IGNORECASE)
				print(single_search_result)
				if len(single_search_result) > 0:
					return [single_search_result[0][0]]
				
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

	def test_processSingleDatetimeInput(self, inputDict):
		for index, value in enumerate(inputDict):
			datetimeObject = self.processSingleDatetimeInput(inputDict[index]["rawDatetime"])
			output = datetimeObject.extractAllValue()
			if output == inputDict[index]["expectedOutput"]:
				print("test case {0}: PASS".format(index))
				print("utc: {}".format(datetimeObject.convertToUnix()))

			else:
				print("test case {0}: FAIL".format(index))
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))
	def processSingleDatetimeInput(self, datetime):
		activityDateTime = ActivityDateTime()
		

		phraseOneOutput = self.phraseOne(datetime, activityDateTime)
		print("phrase 1 output: {}".format(phraseOneOutput))
		
		phraseTwoOutput = self.phraseTwo(phraseOneOutput, activityDateTime)
		print("phrase 2 output: {}".format(phraseTwoOutput))

		phraseThreeOutput = self.phraseThree(phraseTwoOutput, activityDateTime)
		print("phrase 3 output: {}".format(phraseThreeOutput))
		# activityDateTime.extractAllValue()
		return activityDateTime
		

	def phraseOne(self, datetime, activityDateTime):
		# find all full pattern: day-month-year, hour-minute-second
		inputDatetime = datetime

		# for full day-month-year
		for pattern in date_time_pattern["day_month_year"]:
			date_full_pattern = "({0})".format(pattern)
			date_full_result = re.findall(date_full_pattern, inputDatetime, re.IGNORECASE)
			# print(date_full_result)
			if date_full_result:
				for result in date_full_result:
					inputDatetime = inputDatetime.replace(result[0], "")
					activityDateTime.validAndSetDay(result[1])
					activityDateTime.validAndSetMonth(result[2])
					activityDateTime.validAndSetYear(result[3])

				break

		# for full hour-minute-second
		
		for pattern in date_time_pattern["hour_minute_second"]:
			time_full_pattern = "({0})".format(pattern)
			time_full_result = re.findall(time_full_pattern, inputDatetime, re.IGNORECASE)
			# print(time_full_result)
			if time_full_result:
				for result in time_full_result:
					inputDatetime = inputDatetime.replace(result[0], "")
					activityDateTime.validAndSetHour(result[1])
					activityDateTime.validAndSetMinute(result[2])
					activityDateTime.validAndSetSecond(result[3])

				break

		return inputDatetime

	def phraseTwo(self, datetime, activityDateTime):
		inputDatetime = datetime

		# for month-year
		for pattern in date_time_pattern["month_year"]:
			month_year_pattern = "({0})".format(pattern)
			month_year_result = re.findall(month_year_pattern, inputDatetime, re.IGNORECASE)
			# print(date_full_result)
			if month_year_result:
				for result in month_year_result:
					inputDatetime = inputDatetime.replace(result[0], "")				
					activityDateTime.validAndSetMonth(result[1])
					activityDateTime.validAndSetYear(result[2])

				break

		# for day-month
		for pattern in date_time_pattern["day_month"]:
			day_month_pattern = "({0})".format(pattern)
			day_month_result = re.findall(day_month_pattern, inputDatetime, re.IGNORECASE)
			# print(date_full_result)
			if day_month_result:
				for result in day_month_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetDay(result[1])
					activityDateTime.validAndSetMonth(result[2])

				break

		# for full hour-minute
		
		for pattern in date_time_pattern["hour_minute"]:
			time_full_pattern = "({0})".format(pattern)
			time_full_result = re.findall(time_full_pattern, inputDatetime, re.IGNORECASE)
			# print(time_full_result)
			if time_full_result:
				for result in time_full_result:
					inputDatetime = inputDatetime.replace(result[0], "")
					activityDateTime.validAndSetHour(result[1])
					activityDateTime.validAndSetMinute(result[2])
				

				break

		return inputDatetime

	def phraseThree(self, datetime, activityDateTime):
		inputDatetime = datetime

		# for year
		for pattern in date_time_pattern["year_single"]:
			year_pattern = "({0})".format(pattern)
			year_result = re.findall(year_pattern, inputDatetime, re.IGNORECASE)
			# print(date_full_result)
			if year_result:
				for result in year_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetYear(result[1])

				break

		# for month
		for pattern in date_time_pattern["month_single"]:
			month_pattern = "({0})".format(pattern)
			month_result = re.findall(month_pattern, inputDatetime, re.IGNORECASE)
			
			if month_result:
				for result in month_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetMonth(result[1])

				break
		# for day
		for pattern in date_time_pattern["day_single"]:
			day_pattern = "({0})".format(pattern)
			day_result = re.findall(day_pattern, inputDatetime, re.IGNORECASE)
			
			if day_result:
				for result in day_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetDay(result[1])

				break
		# for hour
		
		for pattern in date_time_pattern["hour_single"]:
			hour_pattern = "({0})".format(pattern)
			hour_result = re.findall(hour_pattern, inputDatetime, re.IGNORECASE)
			# print(time_full_result)
			if hour_result:
				
				for result in hour_result:
					inputDatetime = inputDatetime.replace(result[0], "")
					activityDateTime.validAndSetHour(result[1])
				
				break

		return inputDatetime

factory = ActivityDateTimeToUnixFactory()

factory.test_splitRawValues(
		[
			{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019;16h ngày 25/12/2019"}
			# {"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019;16h ngày 25/12/2019"},
			# {"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"},
			# {"rawDatetime":"thời gian dự thi: vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"},
			# {"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"9g30 ngày 24/12/2019"}

		]
	)


# factory.test_processSingleDatetimeInput(
# 	[
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30 - 10g ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30-10g ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30-10g ngày 24 và 8h ngày 25/12/2019", "expectedOutput":"25/12/2019 9:30:0"}


# 	])

# factory.test_processRawDatetimeInput(
# 	[
# 			{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 16:0:0"},
# 			{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"}


# 	])


