# Bifidus, improve your transit

![Bifidus logo](https://github.com/Jungle-Bus/resources/raw/master/logo/Logo_Jungle_Bus-Bifidus.png)

This is a quality assurance script for transport data in OpenStreetMap.

## Usage

Install with `poetry install` 

Grab some osm data and make lists of routes as csv 

`poetry run python bifidus_cli.py -l sample_data/lines.csv -r sample_data/routes.csv -u sample_data/config.csv -n SampleProject > qa.md`

Check an [example output result](https://github.com/Jungle-Bus/bifidus_cli/blob/main/sample_data/output.md).

### Inputs route data

Bifidus needs a list of route_master and route relations to check. You can get these list with the following tools:

* [Jungle Bus prism](https://github.com/Jungle-Bus/prism/)
	* install prism
	* download some osm data
	* extract in csv (`poetry run python prism/cli.py data.osm.pbf -csv`)
	* the lines.csv and routes.csv files can be used with Bifidus
* [OSM Transit Extractor](https://github.com/CanalTP/osm-transit-extractor)
	* install osm transit extractor
	* download some osm data
	* extract in csv (`osm_transit_extractor -i data.osm.pbf`)
	* the osm-transit-extractor_lines.csv and osm-transit-extractor_routes.csv files can be used with Bifidus
* with overpass
* etc

### Other params

You can specify the name of your project with the `-n` parameter. It will be used in the header of the result.

You can also add some useful links such as OpenStreetMap wiki page with the `-u` parameter. Check out the `config.csv` file in `sample_data` directory to see an example.

## Credits

This project is developed by the [Jungle Bus](https://junglebus.io/) team.

It uses [Osmose](https://osmose.openstreetmap.fr/) issues about public transport as a data source.

If you value this work, show your support by donating to the [OSM French local chapter](https://openstreetmap.fr).
