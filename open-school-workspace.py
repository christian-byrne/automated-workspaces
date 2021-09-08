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
import json


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


def get_args(courses):
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


def one_course(options, courses):
    """Wrapper for opening items for a single course. Repeated when
    opening multiple courses' content


    """
    course = courses[options["semester"]][options["course"]]
    if not options["apropos"] and not options["exclude"]:
        open_class(course, web_only=options["web_only"])
    else:
        apropos_filter(course, options["apropos"], options["exclude"], options["web_only"])


def parse_workspaces():
    """Read json workspaces file and serialize to python dict.
    
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for fi in os.listdir(dir_path):
        if "workspaces" in fi and "json" in fi:
            with open(f"{dir_path}/{fi}") as json_file:
                data = json.load(json_file)
                return data
    

def convert_tuple_keys(dictionary):
    """Convert json string keys to python tuples for semesters and
    ints for course codes.
    
    """
    ret = {}
    for workspace, values in dictionary.items():
        new_name = tuple([workspace[:-4], int(workspace[-4:])])
        ret[new_name] = {}
        for k, v in values.items():
            ret[new_name][int(k)] = v
    return ret


def main():
    courses = convert_tuple_keys(parse_workspaces())

    options = get_args(courses)
    print(courses)

    # Default value (no arg) = open all classes for this semester.
    if options["course"] == 999:
        # Change semester each iteration and pass options object.
        for course in courses[options["semester"]].keys():
            options["course"] = course
            one_course(options, courses)
    else:
        one_course(options, courses)


if __name__ == "__main__":
    main()

