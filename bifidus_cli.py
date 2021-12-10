#!/usr/bin/env python
# coding: utf-8

import requests
import csv
import sys
import argparse

parser = argparse.ArgumentParser(
    prog="Bifidus, improve your transit",
    epilog="Mobility open data, proudly crafted by the OpenStreetMap community - An open source tool by Jungle Bus",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="Check quality of OpenStreetMap transport data",
)
parser.add_argument(
    "--useful-links",
    "-u",
    metavar="FILE",
    type=argparse.FileType("r"),
    help="a csv file with useful links",
)

parser.add_argument(
    "--route-masters",
    "-l",
    metavar="FILE",
    type=argparse.FileType("r"),
    help="a csv file with OSM route_master relations",
)

parser.add_argument(
    "--routes",
    "-r",
    metavar="FILE",
    type=argparse.FileType("r"),
    help="a csv file with OSM route relations",
)

parser.add_argument(
    "--name",
    "-n",
    default="My Awesome OpenStreetMap transport project",
    help="the name of your project",
)

args = parser.parse_args()

tt = csv.DictReader(args.route_masters)
osm_lines = list(tt)

tt = csv.DictReader(args.routes)
osm_routes = list(tt)

conf = None
if args.useful_links:
    conf = csv.DictReader(args.useful_links)

project_name = args.name


osmose_url = "http://osmose.openstreetmap.fr/fr/api/0.3/issues?osm_type=relation&osm_id={}&full=true"
josm_url = "http://localhost:8111/load_object?relation_members=true&objects="

# Guess format of osm id
sample_osm_id = osm_lines[0]["line_id"]

try:
    tmp = int(sample_osm_id)  # 10512380
    osm_relations = [line["line_id"] for line in osm_lines] + [
        line["route_id"] for line in osm_routes
    ]
except:
    try:
        tmp = int(sample_osm_id.split("r")[-1])  # r10512380
        osm_relations = [line["line_id"].split("r")[-1] for line in osm_lines] + [
            line["route_id"].split("r")[-1] for line in osm_routes
        ]
    except:
        try:
            tmp = int(sample_osm_id.split("/")[-1])  # relation/10512380
            osm_relations = [line["line_id"].split("/")[-1] for line in osm_lines] + [
                line["route_id"].split("/")[-1] for line in osm_routes
            ]
        except:
            try:
                tmp = int(sample_osm_id.split(":")[-1])  # relation:10512380
                osm_relations = [
                    line["line_id"].split(":")[-1] for line in osm_lines
                ] + [line["route_id"].split(":")[-1] for line in osm_routes]
            except:
                print(
                    "Error: Could not guess format of osm_id: need an line_id/route_id column with valid osm_id (for instance r10512380)"
                )
                sys.exit()


seems_ok = []
to_check = []
errors = {}

for a_relation in osm_relations:
    osmose_ = osmose_url.format(a_relation)
    osmose_call = requests.get(
        osmose_,
        headers={
            "Origin": "https://jungle-bus.github.io/bifidus/",
            "From": "contact@junglebus.io",
        },
    )
    osmose_results = osmose_call.json()["issues"]
    if not osmose_results:
        seems_ok.append(a_relation)
        continue

    for error in osmose_results:
        error_type = "{}_{}".format(error["item"], error["class"])
        if error_type not in errors:
            output_error = {
                "title": error["title"],
                "subtitle": error["subtitle"],
                "objects": [],
            }
            errors[error_type] = output_error
        errors[error_type]["objects"].append(a_relation)
        to_check.append(a_relation)

seems_ok_objects = ["r{}".format(relation) for relation in seems_ok]
josm_ok = "{}{}".format(josm_url, ",".join(seems_ok_objects))

to_check_objects = ["r{}".format(relation) for relation in to_check]
josm_to_check = "{}{}".format(josm_url, ",".join(to_check_objects))

print("# Analyse qualité pour {}".format(project_name))

if conf:
    for link in conf:
        print("- [{}]({})".format(link["display"], link["url"]))

print("")
print("")
print("## Erreurs")
print("- {} objets".format(len(osm_relations)))
print(
    "- {} objets en erreur : [Charger dans JOSM]({})".format(
        len(to_check_objects), josm_to_check
    )
)
print(
    "- {} objets a priori ok : [Charger dans JOSM]({})".format(
        len(seems_ok_objects), josm_ok
    )
)
print("")

print("## Liste des erreurs")

for error in errors.values():
    title = error["title"]["auto"]
    subtitle = ""
    if error["subtitle"]:
        subtitle = error["subtitle"]["auto"]
    if len(error["objects"]) > 4:
        object_list = [
            "- [{}]({}r{})\n".format(
                error["objects"][0], josm_url, error["objects"][0]
            ),
            "- [{}]({}r{})\n".format(
                error["objects"][1], josm_url, error["objects"][1]
            ),
            "- et {} autres erreurs de ce type\n".format(len(error["objects"]) - 2),
        ]
    else:
        object_list = [
            "- [{}]({}r{})\n".format(elem, josm_url, elem) for elem in error["objects"]
        ]

    print(
        """
#### {}

{}

Objet(s):

{}
    """.format(
            title, subtitle, "".join(object_list)
        )
    )
