from datetime import datetime
from numbers import Number
import json
import requests
from uuid import uuid4, UUID
from requests.api import post, get
from src.TrackZero_package.analytics_space_session import space_session
from src.TrackZero_package.entity import entity

class TrackZero:
    base_url = "https://api.trackzero.io"
    def __init__(self, api_key):
        self.api_key = api_key

    def json_serializer(self, obj):
        if isinstance(obj, (datetime)):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return obj.hex
        raise TypeError ("Type %s not serializable" % type(obj))

    def create_analytics_space(self, analytics_space_id: str) -> bool:
        """Creates a new Analytics Space Container

        Parameters:
        analytics_space_id (str): The id of the new Analytics Space.

        Returns:
        bool: represents if the operation was successful.
        """
        res = requests.post(self.base_url + "/analyticsSpaces", params={"analyticsSpaceId":analytics_space_id}, headers={"X-API-KEY": self.api_key})
        return res.status_code == 200

    def delete_analytics_space(self, analytics_space_id: str) -> bool:
        """Deletes Analytics Space Container

        Parameters:
        analytics_space_id (str): The id of the Analytics Space to delete.

        Returns:
        bool: represents if the operation was successful.

        Warning:
        This action is immediate and permanent.
        """
        res = requests.delete(self.base_url + "/analyticsSpaces", params={"analyticsSpaceId":analytics_space_id}, headers={"X-API-KEY": self.api_key})
        return res.status_code == 200

    def upsert_entity(self, entity: entity, analytics_space_id: str) -> bool:
        """Adds or Updates an entity

        Parameters:
        analytics_space_id (str): The id of the Analytics Space to store this entity in.

        Returns:
        bool: represents if the operation was successful.

        Warning:
        This action is immediate and permanent.
        """
        res = requests.post(self.base_url + "/tracking/entities", params={"analyticsSpaceId":analytics_space_id}, data=json.dumps(entity.__dict__, default=self.json_serializer), headers={"X-API-KEY": self.api_key, "content-type":"application/json"})
        return res.status_code == 200

    def delete_entity(self, analytics_space_id: str, entity_type:str, entity_id) -> bool:
        """Deletes an entity

        Parameters:
        analytics_space_id (str): The id of the Analytics Space to delete this entity from.

        Returns:
        bool: represents if the operation was successful.
        
        Warning:
        This action is immediate and permanent.
        """

        if not isinstance(entity_id, ( str, Number, UUID )):
            raise TypeError("Type %s is invalid for entity_id" % type(entity_id) )
        res = requests.post(self.base_url + "/tracking/entities", params={"analyticsSpaceId":analytics_space_id}, data=json.dumps({"type":entity_type, "id": entity_id}), headers={"X-API-KEY": self.api_key, "content-type":"application/json"})
        return res.status_code == 200


    def create_analytics_space_session(self, analytics_space_id: str, ttl_seconds: int) -> space_session:
        """Adds or Updates an entity

        Parameters:
        analytics_space_id (str): The id of the Analytics Space to store this entity in.
        ttl_seconds (int): The life time of the session in seconds. This value must be between 300 and 3600 seconds.
        Returns:
        track_zero_space_session: The session object, use the url string to redirect the user to the Analytics Page.

        """
        if not (300 <= ttl_seconds <= 3600):
            raise ValueError("ttl_seconds must be between 300 and 3600" )
        res = requests.get(self.base_url + "/analyticsSpaces/session",params={"analyticsSpaceId": analytics_space_id, "ttl": ttl_seconds}, headers={"X-API-KEY": self.api_key})
        loaded = json.loads(res.text)
        if res.status_code == 200:
            return space_session(True, loaded["url"], loaded["sessionKey"])
        return space_session(False, "", "")


        

            
