#################################################
# Author: Chinelo Agazie
# Date: 9th of April 2024
# Description:
#################################################
from dotenv import load_dotenv
import os
import base64
from requests import post
import json

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

    def get_token(self, url: str = "https://accounts.spotify.com/") -> str:
        """

        :param url:
        :return:
        """

        result = post(f"{url}api/token",
                      headers={"Authorization": "Basic " + self.auth, "Content-Type": "application/x-www-form"
                                                                                      "-urlencoded"},
                      data={"grant_type": "client_credentials"})
        json_result = json.loads(result.content)
        access_token = json_result["access_token"]
        print(f"access_token: {access_token}")
        return access_token


if __name__ == "__main__":
    client = SpotifyCalls.create_conn_str()
    spotify_token = client.get_token()
