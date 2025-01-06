from pprint import pprint

import pandas as pd

from music_helper.spotify_helper import SpotifyCalls

href = []
href2 = []
ids = []
spotify = []
genre = []
total = []
name = []
popularity = []
types = []

columns = {}


def flatten_artist(data, append=None):
    if type(data) is dict:
        for key in data.keys():
            if type(data[key]) is str or type(data[key]) is int or data[key] is None:

                if key == 'name':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = name
                    name.append(data[key])
                elif key == 'id':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = ids
                    ids.append(data[key])
                elif key == 'popularity':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = popularity
                    popularity.append(data[key])
                elif key == 'total':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = total
                    total.append(data[key])
                elif key == 'type':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = types
                    types.append(data[key])
                elif key == 'href':
                    if append is None:
                        append = ""
                        columns[f"{key}"] = href2
                        href2.append(data[key])
                    else:
                        columns[f"{append}{key}"] = href
                        href.append(data[key])
                elif key == 'spotify':
                    if append is None:
                        append = ""
                    columns[f"{append}{key}"] = spotify
                    spotify.append(data[key])
            else:
                if type(data[key]) is list:
                    if sum([True for k in data[key] if type(k) is str]) == len(data[key]):
                        if key == "genres":
                            columns[f"{key}"] = genre
                            genre.append(data[key])
                    else:
                        flatten_artist(data[key], f"{key}_")

                else:
                    flatten_artist(data[key], f"{key}_")

    elif type(data) is list:
        for item in data:
            flatten_artist(item)
    else:
        print(f"we are not handling this type of {data} ")


def create_dataframe(api):
    flatten_artist(api)
    return pd.DataFrame(columns)


if __name__ == "__main__":
    client = SpotifyCalls.create_conn_str()
    result = client.artist_albums("fela", "artist")
    print(result)
    df = create_dataframe(result)
    print(df.iloc[0, 5])
    # # df_ordered = df.iloc[:, [6, 5, 3, 7, 8, 2, 4, 1, 0]]
    # # print(df_ordered)

    # df_left_aligned = df_ordered.style.set_properties(**{"text-align": "left"})
    # df_left_aligned = df_left_aligned.set_table_styles([dict(selector="th", props=[("text-align", "left")])])
    # print(df_left_aligned)
