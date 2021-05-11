import landsatxplore.api
from landsatxplore.earthexplorer import EarthExplorer
import re

"""
previous:
download Landsat 8 data with landsatxplore[revise] package:
https://github.com/yannforget/landsatxplore

Now:
Because the author has not updated the latest api, it will not be able to access.
Based on this package, I updated the latest API interface, please refer to :
https://github.com/wendylay/landsatxplore/tree/master/landsatxplore

"""


def landsat8_search(dataset='LANDSAT_8_C1', bbox=(), start_date='',
                    end_date='', max_cloud_cover=20):
    # Initialize a new API instance and get an access key
    username = 'wendina_lai@163.com'
    password = '0802Laiwendian'
    api = landsatxplore.api.API(username, password)

    # Request
    # scences is a list, each item in this list is dict
    scenes = api.search(
        dataset=dataset,  # [LANDSAT_TM_C1|LANDSAT_ETM_C1|LANDSAT_8_C1]  TM: Landsat4 5  ETM: Landsat7
        bbox=bbox,  # (xmin, ymin, xmax, ymax) format
        start_date=start_date,  # YYYY-MM-DD
        end_date=end_date,  # YYYY-MM-DD, must have this
        max_cloud_cover=max_cloud_cover,  # int Max. cloud cover in percent (1-100).
        max_results=40000)  # can not exceed 50000
    api.logout()
    return scenes


def landsat8_download(scenes, output_dir='./data'):
    username = 'wendina_lai@163.com'
    password = '0802Laiwendian'
    ee = EarthExplorer(username, password)
    try:
        for idx in range(len(scenes)):
            ee.download(scene_id=scenes[idx]['entityId'], output_dir=output_dir)  # download with entityId
    except KeyError:
        ee.download(scene_id=scenes['entityId'], output_dir=output_dir)
    except:
        print('Please input a valid Landsat8 scene entityId')

    ee.logout()


def landsat8_download_entityId(entityId, output_dir='./data'):
    """
    entityId: list type
    """
    username = 'wendina_lai@163.com'
    password = '0802Laiwendian'
    ee = EarthExplorer(username, password)
    for idx in range(len(entityId)):
        ee.download(scene_id=entityId[idx], output_dir=output_dir)  # download with entityId
    ee.logout()


if __name__ == '__main__':
    # Example1 : search and download
    start_date = '2018-10-13'
    end_date = '2020-11-30'
    max_cloud_cover = 30
    bbox = (23.4, -79.21, 25.38, -76.87)  # (latmin, lonmin, latmax, lonmax)
    scenes = landsat8_search(start_date=start_date, end_date=end_date,
                             bbox=bbox, max_cloud_cover=max_cloud_cover)
    print('{} scenes found.'.format(len(scenes)))
    # landsat8_download(scenes)

    # Example2 :download with entityid
    # entityId = ['LC80100442020272LGN00']
    # landsat8_download_entityId(entityId=entityId, output_dir='./download_data')
