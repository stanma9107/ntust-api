from selenium.webdriver.common.by import By
from copy import deepcopy

def parseCourseList(coursesList):
    courses = coursesList
    parsedCourses = deepcopy(coursesList)
    ownCoursesDetail = {}
    for day in courses:
        courseInDay = courses[day]
        lastCourse = ""
        for courseNum in courseInDay:
            course = courseInDay[courseNum]
            if lastCourse == course["name"]:
                specificCourse = [course for course in ownCoursesDetail[course["name"]] if course["day"] == day]
                specificCourse[0]["time"]["end"] = course["time"]["end"]
                specificCourse[0]["courseNum"].append(courseNum)
                del parsedCourses[day][courseNum]
                continue
            lastCourse = course["name"]
            if course["name"] not in ownCoursesDetail:
                ownCoursesDetail[course["name"]] = []
            ownCoursesDetail[course["name"]].append({
                "day": day,
                "courseNum": [courseNum],
                "time": {
                    "start": course["time"]["start"],
                    "end": course["time"]["end"],
                },
                "code": course["code"],
                "room": course["room"],
                "teacher": course["teacher"],
                "score": course["score"],
                "required": course["required"]
            })

    return ownCoursesDetail

def getCourseList(driver):
    courses = []
    ownCourses = {}

    # Get Course Page
    driver.get("https://courseselection.ntust.edu.tw/ChooseList/D01/D01")

    # Get Courses Detail
    courses_detail_table = driver.find_elements(By.CSS_SELECTOR, "table")[2]
    for rowId, course in enumerate(courses_detail_table.find_elements(By.TAG_NAME, "tr")):
        if rowId > 0:
            course_detail = course.find_elements(By.TAG_NAME, "td")
            courses.append({
                "code": course_detail[0].text,
                "name": course_detail[1].text,
                "score": course_detail[2].text,
                "required": course_detail[3].text,
                "teacher": course_detail[4].text,
                "comment": course_detail[5].text
            })

    # Get Course Schedule
    courses_table = driver.find_elements(By.CSS_SELECTOR, "table")[3]
    for rowId, course_row in enumerate(courses_table.find_elements(By.TAG_NAME, "tr")):
        if rowId > 0:
            time = ""
            for itemId, course_item in enumerate(course_row.find_elements(By.TAG_NAME, "td")):
                if itemId == 1:
                    time = course_item.text.replace("\n", "").replace(" ", "")
                    startTime = time.split("～")[0]
                    endTime = time.split("～")[1]
                else:
                    if itemId > 0 and course_item.text != "":
                        course = course_item.text
                        courseName = course.split("\n")[0].strip()
                        courseRoom = ""
                        if len(course.split("\n")) > 1:
                            courseRoom = course.split("\n")[1].strip()
                        course = [course for course in courses if course["name"] == courseName][0]
                        if itemId not in ownCourses:
                            ownCourses[itemId] = {}
                        ownCourses[itemId][rowId] = {
                            "name": courseName,
                            "room": courseRoom,
                            "time": {
                                "start": startTime,
                                "end": endTime
                            },
                            "code": course["code"],
                            "score": course["score"],
                            "required": course["required"],
                            "teacher": course["teacher"]
                        }
    ownCourses = parseCourseList(ownCourses)
    print(ownCourses)