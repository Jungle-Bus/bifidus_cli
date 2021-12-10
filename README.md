# Bifidus, improve your transit

![Bifidus logo](https://github.com/Jungle-Bus/resources/raw/master/logo/Logo_Jungle_Bus-Bifidus.png)

This is a quality assurance script for transport data in OpenStreetMap.

## Usage

`poetry install` 

Grab some osm data and make list as csv 

`poetry run python bifidus_cli.py -l sample_data/lines.csv -r sample_data/routes.csv -u sample_data/config.csv -n SampleProject > qa.md`

## Credits

This project is developed by the [Jungle Bus](https://junglebus.io/) team.

It uses [Osmose](https://osmose.openstreetmap.fr/) issues about public transport as a data source.

If you value this work, show your support by donating to the [OSM French local chapter](https://openstreetmap.fr).
