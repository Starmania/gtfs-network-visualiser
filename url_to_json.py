from google.transit import gtfs_realtime_pb2 as gtfs
import requests
import json
import yaml
import time
from os.path import abspath, dirname , join

here = dirname(abspath(__file__))

config = yaml.load(open(f"services.yml").read(), Loader=yaml.CLoader)

########################## URL TO FEED
def urltofeed_content(url: str)->gtfs.FeedMessage:
    """A function that returns an feed from an api url
    Args:
        url (str): the api url

    Returns:
        gtfs.FeedMessage: a feed in protobuff.
    """
    feed = gtfs.FeedMessage()
    response = requests.get(url,headers={
    #    "If-Modifier-Since": 
    })
    feed.ParseFromString(response.content)
    return feed


########################## FEEDBUS TO JSON
def feedposition_to_dict(feed: gtfs.FeedMessage, whitelist: list = None, blacklist: list = None):
    def check(entity: gtfs.FeedEntity):
        if not (whitelist is None or entity.id in whitelist):
            return False
        if  blacklist is None or entity.id not in blacklist:
            return True
        return False


    big_dict = {}
    for entity in feed.entity:
        if check(entity.id):
            if entity.HasField('vehicle'):
                entity_tojson = { f"entityid{entity.id}":{
                "id": entity.id ,
                "vehicle" : {
                    "trip":{
                    "trip_id": entity.vehicle.trip.trip_id ,
                    "route_id": entity.vehicle.trip.route_id ,
                    "direction_id": entity.vehicle.trip.direction_id ,
                    "schedule_relationship": entity.vehicle.trip.schedule_relationship
                    },
                    "vehicle": {
                    "id": entity.vehicle.vehicle.id ,
                    "label": entity.vehicle.vehicle.label
                    },
                    "position": {
                    "latitude": entity.vehicle.position.latitude ,
                    "longitude": entity.vehicle.position.longitude ,
                    "bearing": entity.vehicle.position.bearing ,
                    "speed": entity.vehicle.position.speed
                    },
                    "stop_id": entity.vehicle.stop_id ,
                    "current_status": entity.vehicle.current_status ,
                    "timestamp": entity.vehicle.timestamp
                }
                } 
                }
                big_dict.update(entity_tojson)
    return big_dict


def refresh_json_position(url: str, output_name:str, whitelist: list = None, blacklist: list = None):
    """A function that use urltofeed_content() to create an json file with an api url

    Args:
        output_name (str): name for the output json
        whitelist (list): whitelist bus track
        blacklist (list): blacklist bus track
    """

    feed = urltofeed_content(url)
    big_dict = feedposition_to_dict(feed,whitelist,blacklist)


    with open(join(here, output_name), "w") as outfile: 
        json.dump(big_dict, outfile, indent=4,sort_keys=True)


########################## FEEDTRIP_UPDATE TO JSON
def feedtrip_update_to_dict(feed: gtfs.FeedMessage, whitelist: list = None, blacklist: list = None):
    def check(entity: str):
        if not (whitelist is None or entity.id in whitelist):
            return False
        if  blacklist is None or entity.id not in blacklist:
            return True
        return False


    big_dict = {}
    for entity in feed.entity:
        if check(entity.id):
            if entity.HasField('trip_update'):
                

                entity_tojson = { f"entityid{entity.id}":{
                "id": entity.id,
                "trip_update":{
                    "trip_id": entity.trip_update.trip.trip_id,
                    "route_id": entity.trip_update.trip.route_id,
                    "direction_id": entity.trip_update.trip.direction_id,
                    "schedule_relationship": entity.trip_update.trip.schedule_relationship 
                },
                }
                }

                big_dict.update(entity_tojson)
                
                for i in entity.trip_update.stop_time_update:
                    to_add = {
                    f"stop_time_update{i.stop_sequence}":{
                        "stop_sequence":i.stop_sequence ,
                        "stop_id":i.stop_id ,
                        "arrival":{
                            "time":i.arrival.time,
                            "uncertainty":i.arrival.uncertainty
                        },
                        "depature":{
                            "time":i.departure.time,
                            "uncertainty":i.departure.uncertainty
                        }
                    }
                    }
                    big_dict[f'entityid{entity.id}'].update(to_add)
                

    return big_dict

def refresh_json_trip(url: str, output_name:str, whitelist: list=None, blacklist: list=None):
    """A function that use urltofeed_content() to create an json file with an api url
    Args:
        output_name (str): name for the output json
        whitelist (list): whitelist bus track
        blacklist (list): blacklist bus track
    """

    feed = urltofeed_content(url)
    big_dict = feedtrip_update_to_dict(feed,whitelist,blacklist)



    with open(join(here, output_name), "w") as outfile:
        json.dump(big_dict, outfile, indent=4,sort_keys=True)



#MAIN#

if __name__ == '__main__':
    start = time.perf_counter()
    refresh_json_trip(config["tango"]["trip-updates"],'trip_updates.json')
    refresh_json_position(config["tango"]["bus-position"],'bus-position.json')
    end = time.perf_counter()
    print(end - start)