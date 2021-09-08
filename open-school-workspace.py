"""
School Workspace Startup Script

Author:
    Christian P. Byrne

From:
    Sep 21


"""

import time
import argparse
import os
import webbrowser


always = {
    "links": [
        "https://calendar.google.com/calendar/u/0/r/month"
    ]
}

courses = {
    ("fall", 2021): {
        243: {
            "files": [
                "/home/bymyself/s/243/syllabus/calendar.pdf"
            ],
            "links": [
                "https://teams.microsoft.com/_#/school/conversations/General?threadId=19:_s92xiCyj2cdHB6WlE1mqnU8uOHq0mq0nmEnOEKBO6g1@thread.tacv2&ctx=channel",
                "https://d2l.arizona.edu/d2l/home/1069119",
                "https://web.stanford.edu/class/cs103/tools/truth-table-tool/",
                "http://logictools.org/prop.html"
            ],
            "dirs": [
                "/home/bymyself/s/243/"
            ]
        },
        129: {
            "files": [
                "/home/bymyself/s/129/ch7/integration-table.pdf"
            ],
            "links": [
                "https://teams.microsoft.com/_#/school/conversations/General?threadId=19:AJJLFAkZWqzMvQZ1KrNtyJ24NFzlY6YF8GglnP3oLFQ1@thread.tacv2&ctx=channel",
                "https://app.groupme.com/chats",
                "https://d2l.arizona.edu/d2l/le/content/1065012/viewContent/11338667/View",
                "https://www.webassign.net/v4cgi/login.pl?courseKey=WA-production-1061695&eISBN=9781337827584",
                "https://online.vitalsource.com/#/books/9781118748558?context_token=9d16fab0-e8f2-0139-eb10-129461d28e9b",
                "https://d2l.arizona.edu/d2l/le/content/1048236/Home",
                "https://d2l.arizona.edu/d2l/le/content/1065012/Home",
                "https://www.wolframalpha.com/",
                "https://www.desmos.com/calculator",
                "https://www.symbolab.com/",
                "https://reference.wolfram.com/language/tutorial/KeyboardShortcutListing.html",
                "https://reference.wolfram.com/language/guide/MathematicalTypesetting.html",
                "https://www.wolframcloud.com/"
            ],
            "dirs": [
                "/home/bymyself/s/129/"
            ]
        },
        210: {
            "files": [],
            "links": [
                "https://piazza.com/class/ksi3px4i7oh5ed",
                "https://d2l.arizona.edu/d2l/le/content/1081255/Home",
                "https://arizona.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?embedded=1#folderID=%\22cf83f35f-aafd-4f02-80ff-ad8d0047c3f0%22",
                "https://www.w3schools.com/java/"
            ],
            "dirs": [
                "/home/bymyself/s/210/"
            ]
        },
        346: {
            "files": [],
            "links": [
                "https://app.groupme.com/chats",
                "https://lecturer-russ.appspot.com/courses/cs346/fall21/",
                "https://discord.com/channels/855585027689807893/855585028178968579",
                "https://d2l.arizona.edu/d2l/le/content/1048951/Home",
                "https://arizona.hosted.panopto.com/Panopto/Pages/Sessions/List.aspx?embedded=1#folderID=%\22ffadf22f-764c-4317-af6b-ad8b00fcd19c%22"
            ],
            "dirs": [
                "/home/bymyself/s/346/"
            ]
        }
    },
    ("summer", 2021): {
        110: "hi"
    }
}


def current_semester():
    """Get current semester based on UA academic calendar.


    """
    month = time.localtime().tm_mon
    year = time.localtime().tm_year
    day = time.localtime().tm_mday

    if month >= 8 and month <= 12:
        season = "fall"
    elif month == 5 and day < 15 or month > 5:
        season = "summer"
    else:
        season = "spring"

    return tuple([season, year])


def get_args():
    """Arg parser.


    """
    parser = argparse.ArgumentParser(
        description="Automate opening workspaces for different courses. Open links with default browser. Open files with default program. Open directories in a new terminal window.")

    course_list = []
    for semester in courses.values():
        for course in semester.keys():
            course_list.append(course)

    parser.add_argument("course", nargs="?", default=999, type=int,
                        choices=course_list, help=f"Courses in DB: {course_list}", metavar="###")
    # Open one item (or matches) by keyword search
    parser.add_argument("--apropos", "-a", nargs="*",
                        help="Only open files/links that match with keywords", metavar="KEYWORD")
    parser.add_argument("--exclude", "-x", nargs="*", help="Don't open files/links that includes keywords", metavar="KEYWORD")                        
    parser.add_argument("--web-only", "-w", nargs="?", default=False, type=bool,
                        const=True, help="Only open links; no files or dirs.")
    parser.add_argument("--semester", metavar=["SEASON", "YEAR"], nargs=2,
                        default=current_semester(), help="Season Year. E.g., 'Fall 21'. Default is automatically selected based on current time.")

    return vars(parser.parse_args())


def open_class(course, web_only=False):
    """Open the links, files, and directories for a given course.


    """
    if course["links"]:
        # Open first link in a new browser window.
        webbrowser.open(course["links"][0], 1)
        # Open rest of links in that window.
        for link in course["links"][1:]:
            webbrowser.open(link)

    if not web_only:
        for fi in course["files"]:
            os.system(f"xdg-open {fi}")
        for dir in course["dirs"]:
            os.system(f"nohup > /dev/null deepin-terminal -w {dir} & disown")


def apropos_filter(course, apropos, exclude, web_only=False):
    """Filter the links/files/dirs for a course based on a given
    keyword then call the open_class method using a filtered
    copy of the course dict.


    """
    if type(apropos) != list:
        apropos = [apropos]
    if type(exclude) != list:
        exclude = [exclude]

    # Create copy of course dict with only matches included.
    filtered_course = {}
    for category, links in course.items():
        if category not in filtered_course.keys():
            filtered_course[category] = []
        for link in links:
            if apropos[0] != None:
                for keyword in apropos:
                    if keyword in link:
                        filtered_course[category].append(link)
            elif exclude[0] != None:
                for keyword in exclude:
                    if keyword not in link:
                        filtered_course[category].append(link)

    # Pass filtered course to open_class method per usual.
    open_class(filtered_course, web_only=web_only)


def one_course(options):
    """Wrapper for opening items for a single course. Repeated when
    opening multiple courses' content


    """
    course = courses[options["semester"]][options["course"]]
    if not options["apropos"] and not options["exclude"]:
        open_class(course, web_only=options["web_only"])
    else:
        apropos_filter(course, options["apropos"], options["exclude"], options["web_only"])


def main():
    options = get_args()
    print(options)

    # Default value (no arg) = open all classes for this semester.
    if options["course"] == 999:
        # Change semester each iteration and pass options object.
        for course in courses[options["semester"]].keys():
            options["course"] = course
            one_course(options)
    else:
        one_course(options)


if __name__ == "__main__":
    main()
