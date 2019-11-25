# python-snippets

Snippets of Python sample code I've created during my Dev life.

## Getting Started

Each folder contains one or more different snippets, meant for a lot of different stuff.
Feel free to grab them and use them in your works.

### AWS Stuff

* [external-s3-json-configuration](./aws/external-s3-json-configuration) - Parse a configuration json directly from AWS S3 into a dictionary object.
* [query-athena](./aws/query-athena) - Query AWS Athena and download results as a list of dictionaries.
* [deploy-emr](./aws/deploy-emr) - Deploy EMR with refined configuration and bootstrap script, using Boto3.

### Data Bases

* [es-scrolling-query](./dbs/es-scrolling-query) - Scrolling query elasticsearch, with a page size of 1000 records (configurable).

### Files

* [read-write-csv](./files/read-write-csv) - Read/write csv files from/to list of dictionaries.
* [hotfolder](./files/hotfolder) - Process files as soon as they are saved within a folder.


### Prerequisites

* Python 3.6
* The required lib (if needed) inside each `requirements.txt` file

### Installing

You can download each file manually or clone the whole repo and start browsing the snippets in your machine.

## Contributing

You can feel free to open PRs to modify my code or to add new snippets, I'll analyse all of them. 

## Versioning

I currently use only Git to version.
I'll use mostly the `master` branch 'cause I only post functional snippets i've already used in real life projects.

## Authors

* **Flavio Teixeira** - *Initial work* - [ap3xx](https://github.com/ap3xx)

See also the list of [contributors](https://github.com/ap3xx/python-snippets/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
