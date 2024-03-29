# -*- coding: utf-8 -*-

import collections
import sys

# Start 1st block
ID, FORENAME, MIDDLENAME, SURNAME, DEPARTMENT = range(5)
# End 1st block

User = collections.namedtuple("User",
            "username forename middlename surname id")
# End 2d block

def main():
    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} file1 [file2 [... fileN]]".format(
              sys.argv[0]))
        sys.exit()

    usernames = set()
    users = {}
    for filename in sys.argv[1:]:
        with open(filename, encoding="utf8") as file:
            for line in file:
                line = line.rstrip()
                if line:
                    user = process_line(line, usernames)
                    users[(user.surname.lower(), user.forename.lower(),
                            user.id)] = user
    print_users(users)


def process_line(line, usernames):
    fields = line.split(":")
    username = generate_username(fields, usernames)
    user = User(username, fields[FORENAME], fields[MIDDLENAME],
                fields[SURNAME], fields[ID])
    return user


def generate_username(fields, usernames):
    username = ((fields[FORENAME][0] + fields[MIDDLENAME][:1] +
                 fields[SURNAME]).replace("-", "").replace("'", ""))
    username = original_name = username[:8].lower()
    count = 1
    while username in usernames:
        username = "{0}{1}".format(original_name, count)
        count += 1
    usernames.add(username)
    return username


def by_surname_forename(user):
    return user.surname.lower(), user.forename.lower(), user.id


def print_users(users):
    namewidth = 17
    usernamewidth = 9
    distance_between_columns = " " * 5

    column_headers = "{0:<{nw}} {1:^6} {2:{uw}}".format("Name", "ID",
            "Username", nw=namewidth, uw=usernamewidth)
    hyphens_under_each_heading = "{0:-<{nw}} {0:-<6} {0:-<{uw}}".format("",
            nw=namewidth, uw=usernamewidth)
    header = (column_headers + distance_between_columns + column_headers + "\n" +
              hyphens_under_each_heading + distance_between_columns + hyphens_under_each_heading)

    lines = []
    for key in sorted(users):
        user = users[key]
        initial = ""
        if user.middlename:
            initial = " " + user.middlename[0]
        name = "{0.surname}, {0.forename}{1}".format(user, initial)
        lines.append("{0:.<{nw}.{nw}} ({1.id:4}) "
                     "{1.username:{uw}}".format(name, user,
                     nw=namewidth, uw=usernamewidth))

    lines_per_page = 64
    lino = 0
    for left_part, right_part in zip(lines[::2], lines[1::2]):
        if lino == 0:
            print(header)
        print(left_part + distance_between_columns + right_part)
        lino += 1
        if lino == lines_per_page:
            print("\f")
            lino = 0

main()