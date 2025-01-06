#################################################
# Author: Chinelo Agazie
# Date: 9th of April 2024
# Description:
#################################################
from typing import Any

from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from spotify_music.artists_dataframe import create_dataframe

load_dotenv()


class SpotifyCalls:
    @classmethod
    def create_conn_str(cls):
        """

        """
        client_id = os.getenv("CLIENT_ID")
        secret_id = os.getenv("SECRET_ID")
        auth_str = f"{client_id}:{secret_id}"
        auth_byt = auth_str.encode("utf-8")
        print(auth_byt)
        auth_b64 = str(base64.b64encode(auth_byt), "utf-8")
        print(auth_b64)
        return cls(auth_b64)

    def __init__(self, auth: str):
        """

        :param auth:
        """
        self.auth = auth
        self.access_token = ""

    def get_token(self, url: str = "https://accounts.spotify.com/") -> str:
        """

        :param url:
        :return:
        """

        token_result = post(f"{url}api/token",
                            headers={"Authorization": "Basic " + self.auth, "Content-Type": "application/x-www-form"
                                                                                            "-urlencoded"},
                            data={"grant_type": "client_credentials"})
        json_result = json.loads(token_result.content)
        access_token = json_result["access_token"]
        return access_token

    def artist_search(self, artist_name: str, kind: str,
                      url: str = "https://api.spotify.com/v1/search",
                      limit: int = 1) -> Any | None:
        """

        :param artist_name:
        :param kind:
        :param url:
        :param limit:
        :return:
        """
        query = f"?q={artist_name}&type={kind}&limit={limit}"
        query_url = f"{url}{query}"
        self.access_token = self.get_token()
        headers = {"Authorization": f"Bearer {self.access_token}"}
        search_result = get(query_url, headers=headers)
        json_result = json.loads(search_result.content)["artists"]["items"]
        if len(json_result) == 0:
            print(f"No artist with this name {artist_name} exists.....")
            return None
        return json_result

    def artist_albums(self, artist_name: str, kind: str,
                      url: str = "https://api.spotify.com/v1/search",
                      limit: int = 1):
        """

        :param artist_name:
        :param kind:
        :param url:
        :param limit:
        :return:
        """
        artist_result = self.artist_search(artist_name, kind, url, limit)
        print(artist_result)
        df = create_dataframe(artist_result)
        artist_id = df.iloc(0, 5)

        query_url = "https://api.spotify.com /v1/artists/" + artist_id + "/albums"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        search_result = get(query_url, headers=headers)

        return artist_result


if __name__ == "__main__":
    client = SpotifyCalls.create_conn_str()
    spotify_token = client.get_token()
    result = client.artist_search("fela", "artist")
