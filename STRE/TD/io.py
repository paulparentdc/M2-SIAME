#!/usr/bin/python
# coding: utf8

import argparse
import json
import os
import os.path
import sys
from scheduler import *


def parse_tasks():
    parser = argparse.ArgumentParser(description = "Parser for task systems described in json")
    parser.add_argument('files', type=str, nargs='+', help='tasks to schedule (in json)')
    parser.add_argument('--app', '-a', nargs='?', help="name of the application")

    args= parser.parse_args() 
    if args.files == []:
        parser.print_help()
        sys.stderr.write("\nERROR: at least one task file must be given!\n")
        sys.exit(1)

    app_name = args.app
    if not app_name:
        (app_name, _) = os.path.splitext(args.files[0])

    tasks = []
    path = args.files[0]

    for f in args.files:
        app = json.load(open(f))
        for t in app:
            tasks.append(Task(t["name"], t["idx"], t["period"], t["deadline"], t["wcet"]))

    return tasks


t = parse_tasks()
for ta in t:
    print(ta)
sched = Scheduler(t)
sched.creer_schedule()
sched.creer_jobs()
sched.construire()
sched.affiche()

