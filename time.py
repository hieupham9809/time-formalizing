#!/usr/bin/env python
from datetime import *
from calendar import monthrange
import functools
import re

#Constants list:
date_time_pattern = {
# 
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
	"day":
	[
		"ngày (\\d\\d?)"
	],

	"month":
	[
		"tháng (\\d\\d?)"
	],
	"year":
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
	"hour":
	[
		"(\\d\\d?) giờ",
		"(\\d\\d?)[hg]"
	]
	
	
}
atomic = {
	"head": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"],
	"navigate": ["next", "previous"],
	"next": ["tới", "sau", "kế", "tiếp"],
	"previous": ["trước", "vừa", "qua"],
	"week": ["tuần", ""],
	"monday": ["thứ hai", "thứ 2"],
	"tuesday": ["thứ ba", "thứ 3"],
	"wednesday": ["thứ tư", "thứ 4"],
	"thursday": ["thứ năm", "thứ 5"],
	"friday": ["thứ sáu", "thứ 6"],
	"saturday": ["thứ bảy", "thứ 7"],
	"sunday": ["chủ nhật", "cn"]
}
advance_time = {
	"end_of_next_month": ["cuối tháng tới", "cuối tháng sau", "cuối tháng kế tiếp","cuối tháng tiếp"],
	"end_of_next_year": ["cuối năm tới", "cuối năm sau", "cuối năm kế tiếp", "cuối năm tiếp"],
	"end_of_next_week": ["cuối tuần tới", "cuối tuần sau", "cuối tuần kế tiếp", "cuối tuần tiếp"],
	"monday_of_next_week": ["cuối tuần tới", "cuối tuần sau", "cuối tuần kế tiếp", "cuối tuần tiếp"],
	
	"end_of_previous_month":["cuối tháng trước", "cuối tháng vừa", "cuối tháng qua"],
	"end_of_previous_year":["cuối năm trước", "cuối năm vừa", "cuối năm ngoái", "cuối năm qua"],
	"end_of_previous_week":["cuối tuần trước", "cuối tuần vừa", "cuối tuần qua"],
	"end_of_month_number" : ["cuối tháng (\\d\\d?)", "cuối tháng (một|giêng|hai|ba|tư|bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai|chạp)"],
	"end_of_year_number": ["cuối năm (\\d\\d\\d\\d)"],
	"end_of_week": ["cuối tuần"],
	"end_of_month": ["cuối tháng"],
	"end_of_year": ["cuối năm"],

	"begin_of_next_month": ["đầu tháng tới", "đầu tháng sau", "đầu tháng kế tiếp","đầu tháng tiếp"],
	"begin_of_next_year": ["đầu năm tới", "đầu năm sau", "đầu năm kế tiếp", "đầu năm tiếp"],
	"begin_of_next_week": ["đầu tuần tới", "đầu tuần sau", "đầu tuần kế tiếp", "đầu tuần tiếp"],
	"begin_of_previous_month": ["đầu tháng trước", "đầu tháng vừa", "đầu tháng qua"],
	"begin_of_previous_year": ["đầu năm trước", "đầu năm vừa", "đầu năm ngoái", "đầu năm qua"],
	"begin_of_previous_week": ["đầu tuần trước", "đầu tuần vừa", "đầu tuần qua"],
	"begin_of_month_number" : ["đầu tháng (\\d\\d?)", "đầu tháng (một|giêng|hai|ba|tư|bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai|chạp)"],
	"begin_of_year_number": ["đầu năm (\\d\\d\\d\\d)"],
	"begin_of_week": ["đầu tuần"],
	"begin_of_month": ["đầu tháng"],
	"begin_of_year": ["đầu năm"],

	"middle_of_next_month": ["giữa tháng tới", "giữa tháng sau", "giữa tháng kế tiếp","giữa tháng tiếp"],
	"middle_of_next_year": ["giữa năm tới", "giữa năm sau", "giữa năm kế tiếp", "giữa năm tiếp"],
	"middle_of_next_week": ["giữa tuần tới", "giữa tuần sau", "giữa tuần kế tiếp", "giữa tuần tiếp"],
	"middle_of_previous_month": ["giữa tháng trước", "giữa tháng vừa", "giữa tháng qua"],
	"middle_of_previous_year": ["giữa năm trước", "giữa năm vừa", "giữa năm ngoái", "giữa năm qua"],
	"middle_of_previous_week": ["giữa tuần trước", "giữa tuần vừa", "giữa tuần qua"],
	"middle_of_month_number" : ["giữa tháng (\\d\\d?)", "giữa tháng (một|giêng|hai|ba|tư|bốn|năm|sáu|bảy|tám|chín|mười|mười một|mười hai|chạp)"],
	"middle_of_year_number": ["giữa năm (\\d\\d\\d\\d)"],
	"middle_of_week": ["giữa tuần"],
	"middle_of_month": ["giữa tháng"],
	"middle_of_year": ["giữa năm"],

	"next_day": ["ngày mai", "sáng mai", "trưa mai", "tối mai", "chiều mai", "ngày sau", "hôm sau", "bữa sau", "1 ngày nữa"],
	"previous_day": ["hôm qua", "hôm trước", "hôm vừa", "ngày qua"],
	"double_next_day": ["ngày mốt"],
	"triple_next_day": ["ngày kia"],
	
	"number_next_day": ["(\\d\\d?) ngày nữa", "(\\d\\d?) ngày tới", "(\\d\\d?) ngày sắp tới", "(\\d\\d?) ngày sau"],
	"number_previous_day":["(\\d\\d?) ngày trước"]

}
month_mapping = {
	"1":"1", "một":"1","giêng":"1",
	"2":"2", "hai":"2",
	"3":"3", "ba":"3",
	"4":"4", "bốn":"4", "tư":"4",
	"5":"5", "năm":"5",
	"6":"6", "sáu":"6",
	"7":"7", "bảy":"7",
	"8":"8", "tám":"8",
	"9":"9", "chín":"9",
	"10":"10", "mười":"10",
	"11":"11", "mười một":"11",
	"12":"12", "mười hai":"12", "chạp":"12"
}

for day in atomic["head"]:
	for week in atomic["week"]:
		if week != "":
			for navigate in atomic["navigate"]:
				advance_time["{0}_of_{1}_week".format(day, navigate)] = ["{0} tuần {1}".format(dayValue, navigateValue) for dayValue in atomic[day] for navigateValue in atomic[navigate]]
				# for dayValue in atomic[day]:
				# 	for navigateValue in atomic[navigate]:

		else:
			for navigate in atomic["navigate"]:
				advance_time["{0}_of_{1}_week".format(day, navigate)] += ["{0} {1}".format(dayValue, navigateValue) for dayValue in atomic[day] for navigateValue in atomic[navigate]]
			advance_time["{0}_of_week".format(day)] = ["{}".format(dayValue) for dayValue in atomic[day]]

advance_time_range = {
	"month":{
		"begin": [10, 1, 5],
		"middle": [20, 11, 15],
		"end": {
			"1": [31, 21, 26],"một": [31, 21, 26],"giêng": [31, 21, 26],
			"2": [monthrange(int(datetime.today().year),2)[1], 21, 24],"hai": [monthrange(int(datetime.today().year),2)[1], 21, 24],
			"3": [31, 21, 26],"ba": [31, 21, 26],
			"4": [30, 21, 25],"bốn": [30, 21, 25],"tư": [30, 21, 25],
			"5": [31, 21, 26],"năm": [31, 21, 26],
			"6": [30, 21, 25],"sáu": [30, 21, 25],
			"7": [31, 21, 26],"bảy": [31, 21, 26],
			"8": [31, 21, 26],"tám": [31, 21, 26],
			"9": [30, 21, 25],"chín": [30, 21, 25],
			"10": [31, 21, 26],"mười": [31, 21, 26],
			"11": [30, 21, 25],"mười một": [30, 21, 25],
			"12": [31, 21, 26],"mười hai": [31, 21, 26],"chạp": [31, 21, 26]
		}
	},
	"year": {
		"begin": [4, 1, 2],
		"middle": [8, 5, 6],
		"end": [12, 9, 10]
	},
	# begin with the first day of week
	"week": {
		"begin": [1, 0, 0],
		"middle": [4, 2, 3],
		"end": [-1, 5, -1],
		"monday": [0, 0, 0],
		"tuesday": [1, 1, 1],
		"wednesday": [2, 2, 2],
		"thursday": [3, 3, 3],
		"friday": [4, 4, 4],
		"saturday": [5, 5, 5],
		"sunday": [-1, -1, -1]
	}
}

separator_list = [
# 1st priority

	"bắt đầu.*?({0}).*?kết thúc.*?({1})",
	"khởi đầu.*?({0}).*?kết thúc.*?({1})",
# 2nd priority
	"sáng.*?({0}).*?chiều.*?({1})",
	"sáng.*?({0}).*?trưa.*?({1})",
	"sáng.*?({0}).*?tối.*?({1})",
	"trưa.*?({0}).*?chiều.*?({1})",
	"trưa.*?({0}).*?tối.*?({1})",

	"từ.*?({0}).*?đến.*?({1})",
	"từ.*?({0}).*?tới.*?({1})",
# 3rd priority
	# "từ ("
	"({0}).*?đến.*?({1})",
	"({0}).*?cho tới.*?({1})",
	"từ.*?({0}).*?-.*?({1})",
# 4th priority
	"({0}).*?-.*?({1})"

]
class ActivityDateTime:
	def __init__(self, day=int(datetime.today().day), month=int(datetime.today().month), year=int(datetime.today().year), hour=0, minute=0, second=0):
		self.day = day
		self.month = month
		self.year = year
		self.hour = hour
		self.minute = minute
		self.second = second
		self.others = {
			"day": {"priority": 0, "values": []},
			"month": {"priority": 0, "values": []},
			"year": {"priority": 0, "values": []},
			"hour": {"priority": 0, "values": []},
			"minute": {"priority": 0, "values": []},
			"second": {"priority": 0, "values": []}
		}
	def __getitem__(self, key):
		return self.__getattribute__(key)
	def __setitem__(self, key, value):
		self.__setattr__(key, value)
	def extractAllValue(self):
		# print("{0}/{1}/{2} {3}:{4}:{5}".format(self.day, self.month, self.year, self.hour, self.minute, self.second))
		print(self.others)
		return "{0}/{1}/{2} {3}:{4}:{5}".format(self.day, self.month, self.year, self.hour, self.minute, self.second)
	def convertToUnix(self):
		dt = datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second)
		return int(dt.replace(tzinfo=timezone.utc).timestamp())
	
	def validAndSetDay(self, dayString, priority=2):
		if priority <= self.others["day"]["priority"]:
			self.others["day"]["values"].append(dayString)
			
			# print("\"{}\" archived".format(dayString))
			return
		dayInt = int(dayString)
		if 1 <= dayInt <= 31:
			self.day = dayInt
			self.others["day"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid day!")
	def validAndSetMonth(self, monthString, priority=2):
		if priority <= self.others["month"]["priority"]:
			self.others["month"]["values"].append(monthString)
			

			# print("\"{}\" archived".format(monthString))
			return
		monthInt = int(monthString)
		if 1 <= monthInt <= 12:
			self.month = monthInt
			self.others["month"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid month")
	def validAndSetYear(self, yearString, priority=2):
		if priority <= self.others["year"]["priority"]:
			self.others["year"]["values"].append(yearString)
			

			# print("\"{}\" archived".format(yearString))
			return
		yearInt = int(yearString)
		if MINYEAR <= yearInt <= MAXYEAR:
			self.year = yearInt
			self.others["year"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid year")
	def validAndSetHour(self, hourString, priority=2):
		if priority <= self.others["hour"]["priority"]:
			self.others["hour"]["values"].append(hourString)
			

			# print("\"{}\" archived".format(hourString))
			return
		hourInt = int(hourString)
		if 0 <= hourInt < 24:
			self.hour = hourInt
			self.others["hour"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid hour")
	def validAndSetMinute(self, minuteString, priority=2):
		if priority <= self.others["minute"]["priority"]:
			self.others["minute"]["values"].append(minuteString)
			

			# print("\"{}\" archived".format(minuteString))
			return
		minuteInt = int(minuteString)
		if 0 <= minuteInt < 60:
			self.minute = minuteInt
			self.others["minute"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid minute")
	def validAndSetSecond(self, secondString, priority=2):
		if priority <= self.others["second"]["priority"]:
			self.others["second"]["values"].append(secondString)
			

			# print("\"{}\" archived".format(secondString))
			return
		secondInt = int(secondString)
		if 0 <= secondInt < 60:
			self.second = secondInt
			self.others["second"]["priority"] = priority
		else:
			print(">>>>>>>>>>>ERR: invalid second")

class ActivityDateTimeToUnixFactory:
	def constraintTwoTimestamp(self, activityDateTime1, activityDateTime2):
		#constraint day, month, year
		for key in ["day", "month", "year"]:
			if activityDateTime1.others[key]["priority"] * activityDateTime2.others[key]["priority"] == 0:
				if activityDateTime1.others[key]["priority"] == 0:
					activityDateTime1[key] = activityDateTime2[key]
				else:
					activityDateTime2[key]= activityDateTime1[key]
	def test_processRawDatetimeInput(self, inputDict):
		passnum = 0
		failnum = 0
		for index, value in enumerate(inputDict):
			datetimeObjects = self.processRawDatetimeInput(inputDict[index]["rawDatetime"])
			output = ";".join([datetimeObject.extractAllValue() for datetimeObject in datetimeObjects])
			if output == inputDict[index]["expectedOutput"]:
				print("test case {0}: PASS".format(index))
				passnum += 1
				# print("utc: {}".format(datetimeObject.convertToUnix()))

			else:
				failnum += 1
				print("test case {0}: FAIL".format(index))
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))
		print("PASSED: {0}/{1}".format(passnum, passnum + failnum))
		
	def processRawDatetimeInput(self, rawDatetime):
		rawValueSplitted = self.splitRawValues(rawDatetime)
		print(rawValueSplitted)
		if len(rawValueSplitted) > 1:
			slot1 = self.processSingleDatetimeInput(rawValueSplitted[0], 0)
			slot2 = self.processSingleDatetimeInput(rawValueSplitted[1], 1)
			# print(slot1.extractAllValue())
			# print(slot2.extractAllValue())
			self.constraintTwoTimestamp(slot1, slot2)
			return [slot1, slot2]
			# activityDateTime = self.processSingleDatetimeInput(rawDatetime)
		elif len(rawValueSplitted) == 1:
			slot1 = self.processSingleDatetimeInput(rawValueSplitted[0], 2)
			# print(slot1.extractAllValue())
			return [slot1]
			
			# unixFormat = self.convertToUnixFormat(activityDateTime)
			# return unixFormat
		else:
			print("ERROR: cannot extract any value")
			return []

	def splitRawValues(self, rawDatetime):
		date_time_pattern_joined = "(({0}).*)+".format("|".join([pattern for key in date_time_pattern for pattern in date_time_pattern[key]] + [pattern for key in advance_time for pattern in advance_time[key]]))
		for separator in separator_list:
			# date_time_pattern = single_date_regex_list + single_time_regex_list

			# print(date_time_pattern_joined)
			full_pattern = separator.format(date_time_pattern_joined, date_time_pattern_joined)
			separator_search_result = re.findall(full_pattern, rawDatetime, re.IGNORECASE)
			# print(separator_search_result)
			if len(separator_search_result) > 0:
				# print(full_pattern)
				print(separator_search_result)

				secondIdx = functools.reduce(lambda x,y: x + y, list(map(lambda x: (" ".join(x[1])).count('(') , {**date_time_pattern, **advance_time}.items())))
				print(secondIdx)
				# print(separator_search_result[0][0])
				# print(separator_search_result[0][secondIdx + 3])
				return [separator_search_result[0][0], separator_search_result[0][secondIdx + 3]]
			# print("({0})".format(date_time_pattern_joined))
		single_search_result = re.findall("({0})".format(date_time_pattern_joined), rawDatetime, re.IGNORECASE)
		# print(single_search_result)
		if len(single_search_result) > 0:
			print("SINGLE DETECTED: {}".format(single_search_result))
			return [single_search_result[0][0]]
		else:
			# print("Trying advance pattern...")
			# advance_datetime_pattern_joined = "(({0}).*)+".format("|".join([pattern for key in advance_time for pattern in advance_time[key]]))
			# for separator in separator_list:
			# 	advance_datetime_full_pattern = separator.format(advance_datetime_pattern_joined, advance_datetime_pattern_joined)
			# 	advance_datetime_full_result = re.findall(advance_datetime_full_pattern, rawDatetime, re.IGNORECASE)
			# 	if len(advance_datetime_full_result) > 0:
			# 		secondIdx = functools.reduce(lambda x,y: x + y, list(map(lambda x: len(x[1]) if "number" in x[0].split("_") else 0, advance_time.items())))
			# 		# print("secondIdx: {}".format(secondIdx))
			# 		print(advance_datetime_full_result)
			# 		return [advance_datetime_full_result[0][0], advance_datetime_full_result[0][secondIdx + 3]]
			# advance_datetime_single_result = re.findall("({0})".format(advance_datetime_pattern_joined), rawDatetime, re.IGNORECASE)
			# if len(advance_datetime_single_result) > 0:
			# 	print(advance_datetime_single_result)
			# 	return [advance_datetime_single_result[0][0]]
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
		passnum = 0
		failnum = 0
		for index, value in enumerate(inputDict):
			output = ";".join(self.splitRawValues(inputDict[index]["rawDatetime"]))
			
			if output == inputDict[index]["expectedOutput"]:
				print("test case {0}: PASS".format(index))
				passnum += 1
			else:
				failnum += 1
				print("test case {0}: FAIL".format(index))	
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))		
		print("PASSED: {0}/{1}".format(passnum, passnum + failnum))
	def test_processSingleDatetimeInput(self, inputDict):
		passnum = 0
		failnum = 0
		for index, value in enumerate(inputDict):
			datetimeObject = self.processSingleDatetimeInput(inputDict[index]["rawDatetime"])
			output = datetimeObject.extractAllValue()
			if output == inputDict[index]["expectedOutput"]:
				passnum += 1
				print("test case {0}: PASS".format(index))
				print("utc: {}".format(datetimeObject.convertToUnix()))

			else:
				failnum += 1
				print("test case {0}: FAIL".format(index))
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))
		print("PASSED: {0}/{1}".format(passnum, passnum + failnum))

	def processSingleDatetimeInput(self, datetime, boundIdx):
		activityDateTime = ActivityDateTime()
		
		self.catchAdvancePattern(datetime, activityDateTime, boundIdx)

		phraseOneOutput = self.phraseOne(datetime, activityDateTime)
		print("phrase 1 output: {}".format(phraseOneOutput))
		
		phraseTwoOutput = self.phraseTwo(phraseOneOutput, activityDateTime)
		print("phrase 2 output: {}".format(phraseTwoOutput))

		phraseThreeOutput = self.phraseThree(phraseTwoOutput, activityDateTime)
		print("phrase 3 output: {}".format(phraseThreeOutput))
		# activityDateTime.extractAllValue()
		return activityDateTime
		
	def test_catchAdvancePattern(self, inputDict):
		passnum = 0
		failnum = 0
		for index, value in enumerate(inputDict):
			activityDateTime = ActivityDateTime()
		
			self.catchAdvancePattern(inputDict[index]["rawDatetime"], activityDateTime, inputDict[index]["boundIdx"])
			# datetimeObject = self.processSingleDatetimeInput(inputDict[index]["rawDatetime"])
			output = activityDateTime.extractAllValue()
			if output == inputDict[index]["expectedOutput"]:
				passnum += 1
				print("test case {0}: PASS".format(index))
				print("utc: {}".format(activityDateTime.convertToUnix()))

			else:
				failnum += 1
				print("test case {0}: FAIL".format(index))
				print("rawDatetime: {0}\n expectedOutput: {1}\n currentOutput: {2}".format(inputDict[index]["rawDatetime"],
					inputDict[index]["expectedOutput"], output))
		print("PASSED: {0}/{1}".format(passnum, passnum + failnum))
		

	def catchAdvancePattern(self, rawDatetime, activityDateTime, boundIdx):
		currentDatetime = datetime.today() 
		currentDay = int(currentDatetime.day)
		currentMonth = int(currentDatetime.month)
		currentYear = int(currentDatetime.year)
		for key, advancePatternList in advance_time.items():
			# TODO: find the pattern in advance pattern list
			# if find, handle key: keyNameList = key.split("_")
			for advancePattern in advancePatternList:
				advance_result = re.findall(advancePattern, rawDatetime, re.IGNORECASE)
				if advance_result:
					keyNameList = key.split("_")

					# if "month" exists in keyNameList:
					if "month" in keyNameList:
						if "next" in keyNameList:
							if currentMonth + 1 < 13: 
								activityDateTime.validAndSetMonth(currentMonth + 1, priority=1) 
							else: 
								activityDateTime.validAndSetMonth(1, priority=1)
							
						elif "previous" in keyNameList:
							if currentMonth - 1 > 0: 
								activityDateTime.validAndSetMonth(currentMonth - 1, priority=1) 
							else: 
								activityDateTime.validAndSetMonth(12, priority=1)
						elif "number" in keyNameList and advance_result[0] in month_mapping.keys():
							activityDateTime.validAndSetMonth(month_mapping[advance_result[0]], priority=1)	
						
						if keyNameList[0] == "end":
							activityDateTime.validAndSetDay(advance_time_range["month"][keyNameList[0]][str(activityDateTime.month)][boundIdx], priority=1)	
						else:
							activityDateTime.validAndSetDay(advance_time_range["month"][keyNameList[0]][boundIdx], priority=1)
					elif "year" in keyNameList:
						if "next" in keyNameList:
							activityDateTime.validAndSetYear(currentYear + 1, priority=1)
						elif "previous" in keyNameList:
							activityDateTime.validAndSetYear(currentYear - 1, priority=1)
						elif "number" in keyNameList:
							activityDateTime.validAndSetYear(advance_result[0], priority=1)


						activityDateTime.validAndSetMonth(advance_time_range["year"][keyNameList[0]][boundIdx], priority=1)

					elif "week" in keyNameList:
						week = int(datetime.today().isocalendar()[1]) - 1
						if "next" in keyNameList:
							week += 1
						elif "previous" in keyNameList:
							week -= 1

						dayOfWeek = 1
						newDate = datetime.strptime("{0}-W{1}-{2}".format(currentYear, week, dayOfWeek + advance_time_range["week"][keyNameList[0]][boundIdx]),"%Y-W%W-%w")
						activityDateTime.validAndSetDay(newDate.day, priority=1)
						if int(newDate.month) != currentMonth:
							activityDateTime.validAndSetMonth(newDate.month, priority=1)
						if int(newDate.year) != currentYear:
							activityDateTime.validAndSetYear(newDate.year, priority=1)
					elif "day" in keyNameList:
						numOfDays = 1
						newDate = currentDatetime
						if "double" in keyNameList:
							numOfDays = 2
						elif "triple" in keyNameList:
							numOfDays = 3
						elif "number" in keyNameList:
							numOfDays = int(advance_result[0])
						
						if "next" in keyNameList:
							newDate = newDate + timedelta(days=numOfDays)
						elif "previous" in keyNameList:
							newDate = newDate - timedelta(days=numOfDays)

						activityDateTime.validAndSetDay(newDate.day, priority=1)
						if int(newDate.month) != currentMonth:
							activityDateTime.validAndSetMonth(newDate.month, priority=1)
						if int(newDate.year) != currentYear:
							activityDateTime.validAndSetYear(newDate.currentYear, priority=1)


				# if "next" in keyNameList:
					# change month += 1

				# elif "previous" in keyNameList:
					# change month -= 1
				# else:
					# pass
				# # change day by lookup in advance_time_range["month"][keyNameList[0]]


			# if "year" in keyNameList:


			# if "week" in keyNameList:
				# if "next" in keyNameList:
						# get week by current datetime
						# increase week
						# convert to new datetime
						# set new day
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
		for pattern in date_time_pattern["year"]:
			year_pattern = "({0})".format(pattern)
			year_result = re.findall(year_pattern, inputDatetime, re.IGNORECASE)
			# print(date_full_result)
			if year_result:
				for result in year_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetYear(result[1])

				break

		# for month
		for pattern in date_time_pattern["month"]:
			month_pattern = "({0})".format(pattern)
			month_result = re.findall(month_pattern, inputDatetime, re.IGNORECASE)
			
			if month_result:
				for result in month_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetMonth(result[1])

				break
		# for day
		for pattern in date_time_pattern["day"]:
			day_pattern = "({0})".format(pattern)
			day_result = re.findall(day_pattern, inputDatetime, re.IGNORECASE)
			
			if day_result:
				for result in day_result:
					inputDatetime = inputDatetime.replace(result[0], "")	
					activityDateTime.validAndSetDay(result[1])

				break
		# for hour
		
		for pattern in date_time_pattern["hour"]:
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

# factory.test_splitRawValues(
# 		[
# 			{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 - 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019-16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ khung giờ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ ngày 24/12/2019 khung giờ 9h30-10h30 đến 16h ngày 25/12/2019", "expectedOutput":"ngày 24/12/2019 khung giờ 9h30-10h30 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ thứ năm lúc 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"từ một ngày thứ năm lúc 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"}
# 			,{"rawDatetime":"thời gian dự thi: vào lúc 9h30-10h30 ngày 24/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019"}
# 			,{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"9g30 ngày 24/12/2019"}
# 			,{"rawDatetime":"thời gian: buổi sáng 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019, buổi ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"thời gian: buổi sáng thứ năm 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019, buổi ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"thời gian: buổi sáng từ 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019, buổi ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"thời gian: sáng từ 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019, buổi ;16h ngày 25/12/2019"}
# 			,{"rawDatetime":"thời gian: bắt đầu từ 9h30-10h30 ngày 24/12/2019 và sau đó kết thúc vào 16h ngày 25/12/2019", "expectedOutput":"9h30-10h30 ngày 24/12/2019 và sau đó ;16h ngày 25/12/2019"}

# 		]
# 	)


# factory.test_processSingleDatetimeInput(
# 	[
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30 - 10g ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30-10g ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"},
# 		{"rawDatetime":"thời gian dự thi: vào lúc 9g30-10g ngày 24 và 8h ngày 25/12/2019", "expectedOutput":"25/12/2019 9:30:0"}


# 	])

# factory.test_catchAdvancePattern(
# 	[
# 			{"rawDatetime":"thời gian vào cuối tháng này", "boundIdx": 0, "expectedOutput":"31/{0}/{1} 0:0:0".format(datetime.today().month, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng tới", "boundIdx": 0, "expectedOutput":"30/{0}/{1} 0:0:0".format(int(datetime.today().month) + 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng tới", "boundIdx": 1, "expectedOutput":"21/{0}/{1} 0:0:0".format(int(datetime.today().month) + 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng tới", "boundIdx": 2, "expectedOutput":"25/{0}/{1} 0:0:0".format(int(datetime.today().month) + 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng 2", "boundIdx": 0, "expectedOutput":"29/2/{0} 0:0:0".format(datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tháng tới", "boundIdx": 0, "expectedOutput":"10/{0}/{1} 0:0:0".format(int(datetime.today().month) + 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tháng tư", "boundIdx": 0, "expectedOutput":"10/4/{0} 0:0:0".format(datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào giữa tháng chạp", "boundIdx": 0, "expectedOutput":"20/12/{0} 0:0:0".format(datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tháng chạp", "boundIdx": 0, "expectedOutput":"10/12/{0} 0:0:0".format(datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng trước", "boundIdx": 0, "expectedOutput":"30/{0}/{1} 0:0:0".format(int(datetime.today().month) - 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tháng vừa qua", "boundIdx": 0, "expectedOutput":"30/{0}/{1} 0:0:0".format(int(datetime.today().month) - 1, datetime.today().year)}
# 			,{"rawDatetime":"thời gian diễn ra vào đầu năm nay", "boundIdx": 0, "expectedOutput":"{0}/4/{1} 0:0:0".format(int(datetime.today().day), datetime.today().year)}
# 			,{"rawDatetime":"thời gian diễn ra vào đầu năm ngoái", "boundIdx": 0, "expectedOutput":"{0}/4/{1} 0:0:0".format(int(datetime.today().day), int(datetime.today().year) - 1)}
# 			,{"rawDatetime":"thời gian diễn ra vào đầu năm tới", "boundIdx": 0, "expectedOutput":"{0}/4/{1} 0:0:0".format(int(datetime.today().day), int(datetime.today().year) + 1)}
# 			,{"rawDatetime":"thời gian diễn ra vào đầu năm tới", "boundIdx": 1, "expectedOutput":"{0}/1/{1} 0:0:0".format(int(datetime.today().day), int(datetime.today().year) + 1)}
# 			,{"rawDatetime":"thời gian diễn ra vào giữa năm tới", "boundIdx": 1, "expectedOutput":"{0}/5/{1} 0:0:0".format(int(datetime.today().day), int(datetime.today().year) + 1)}
# 			,{"rawDatetime":"thời gian vào đầu tuần sau", "boundIdx": 0, "expectedOutput":"19/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tuần sau", "boundIdx": 1, "expectedOutput":"18/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào cuối tuần sau", "boundIdx": 0, "expectedOutput":"24/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tuần này", "boundIdx": 0, "expectedOutput":"12/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào đầu tuần trước", "boundIdx": 0, "expectedOutput":"5/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian vào 5 ngày tới", "boundIdx": 0, "expectedOutput":"18/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào ngày mai", "boundIdx": 0, "expectedOutput":"14/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào thứ 5", "boundIdx": 0, "expectedOutput":"14/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào thứ 5 tuần sau", "boundIdx": 0, "expectedOutput":"21/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào thứ ba tuần trước", "boundIdx": 0, "expectedOutput":"5/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào chủ nhật tuần này", "boundIdx": 0, "expectedOutput":"17/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}
# 			,{"rawDatetime":"thời gian bắt đầu vào thứ 5 tuần kế nhé", "boundIdx": 0, "expectedOutput":"21/{0}/{1} 0:0:0".format(int(datetime.today().month), datetime.today().year)}

# 	]
# )

result = factory.processRawDatetimeInput("thời gian bắt đầu từ thứ 5 tuần kế nhé")
# result = factory.processRawDatetimeInput("thời gian bắt đầu từ thứ 5 đến thứ 6 tuần kế nhé")

time = [obj.extractAllValue() for obj in result]
print(time)

# factory.test_processRawDatetimeInput(
# 	[
# 			{"rawDatetime":"từ 9h30-10h30 ngày 24/12/2019 đến 16h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 16:0:0"}
# 			,{"rawDatetime":"thời gian dự thi: vào lúc 9g30 ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0"}
# 			,{"rawDatetime":"thời gian: buổi sáng 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 16:0:0"}
# 			,{"rawDatetime":"thời gian: sáng từ 9h30-10h30 ngày 24/12/2019, buổi chiều: 16h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 16:0:0"}
# 			,{"rawDatetime":"thời gian: bắt đầu từ 9h30-10h30 ngày 24/12/2019 và sau đó kết thúc vào 16h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 16:0:0"}
# 			,{"rawDatetime":"thời gian: 9h sáng 15/01", "expectedOutput":"15/1/2020 9:0:0"}
# 			,{"rawDatetime":"thời gian: từ sáng thứ 4 lúc 9h30-10h30 ngày 24/12/2019 đến trưa sau 12h ngày 25/12/2019", "expectedOutput":"24/12/2019 9:30:0;25/12/2019 12:0:0"}
# 			,{"rawDatetime":"cuối tháng 8 năm 2019", "expectedOutput":"26/8/2019 0:0:0"}
# 			,{"rawDatetime":"lúc 9h30-10h30", "expectedOutput":"14/5/2020 9:30:0;14/5/2020 10:30:0"}
# 			,{"rawDatetime":"lúc 9h30- 10h30", "expectedOutput":"14/5/2020 9:30:0;14/5/2020 10:30:0"}
# 			,{"rawDatetime":"lúc 9h30- 10h30 ngày 24/12/2019", "expectedOutput":"24/12/2019 9:30:0;24/12/2019 10:30:0"}
# 			,{"rawDatetime":"trong 2 ngày 24-25/12/2019", "expectedOutput":"24/12/2019 0:0:0;25/12/2019 0:0:0"}
# 			,{"rawDatetime":"từ ngày 24 đến 25/12/2019", "expectedOutput":"24/12/2019 0:0:0;25/12/2019 0:0:0"}
# 			,{"rawDatetime":"từ 10h ngày 24 đến 25/12/2019", "expectedOutput":"24/12/2019 10:0:0;25/12/2019 0:0:0"}
# 			,{"rawDatetime":"lúc 10h ngày 24 đến 25/12/2019", "expectedOutput":"24/12/2019 10:0:0;25/12/2019 0:0:0"}



# 	])


# TODO: pattern "cuối ... ", split by "-"
