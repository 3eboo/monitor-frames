### approach used: 

To solve the [data engineering challenge challenge](https://github.com/DoodleScheduling/hiring-challenges/tree/master/data-engineer) I used [Faust](https://github.com/robinhood/faust) library to make use of 
its high performance and scalability for streaming applications. To be explicit I ve made use of faust applications, agents and tables. Where faust table data structure is a distributed in-memory dict used for prsistant storage. We 
can replay changelog upon network failure and node restarts, allowing us to rebuild the state of the table as it was before the fault.


### faust requirements:
python 3.6 or later
kafka


## running and setup the application:

Idealy you can use Makefile to do the following steps, but I didn't have time to fully test it so here are the steps:

1- clone and cd to the project repo

2- create and activate python 3 virtual env

    python3 -m venv .venv

	cd .venv/bin/ && source activate

3- Install dependencies:

``pip install -r requirements.txt``

4- Run kafka instance using the image in docker-compose.yml

``docker-compose run ``

5- After making sure that kafka is up and running on port 9092, run our faust application using the following: 

`faust -A event_stream worker -l info`

6- Now you can send stream of events in file using: 

`python3 main.py path_to_file number_of_events(optional)` 

like:

`python3 main.py stream.jsonl 5` will test sending the first 5 objects in stream.jsonl file

