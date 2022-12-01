from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes

from array import array
import os
from PIL import Image
import sys
import time


def get_word():
    IMAGES_DIR = 'static/image'

    key = '******'
    endpoint = '***********'
    # region = 'Japan East'

    computervision_client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(key)
    )

    # 画像のイメージテスト用
    # url = "https://github.com/Azure-Samples/cognitive-services-python-sdk-samples/raw/master/samples/vision/images/make_things_happen.jpg"

    # どうも画像の大きさがあるっぽい。50×50じゃないとエラーでる。
    url = "https://shinnosukeikeda.blob.core.windows.net/artists/make_things_happen.jpeg"
    raw = True
    numberOfCharsInOperationId = 36

    # SDKをコールする
    rawHttpResponse = computervision_client.read(url, language="en", raw=True)

    # Get ID from returned headers
    operationLocation = rawHttpResponse.headers["Operation-Location"]
    idLocation = len(operationLocation) - numberOfCharsInOperationId
    operationId = operationLocation[idLocation:]
    # print(operationId)

    # ステータス（準備）がランニングじゃなくなるまでリクエスト投げ続ける
    while True:
        result = computervision_client.get_read_result(operationId)

        if result.status not in OperationStatusCodes.running:
            break
        time.sleep(1)

    # 最終的に返す配列
    result_text_list = []
    print(result)

    # もしもresultのステータスが成功だったら 抽出文字リストに文字を追加して返す
    if result.status == OperationStatusCodes.succeeded:
        for line in result.analyze_result.read_results[0].lines:
            result_text_list.append(line.text)
            print(line.text)
            print(line.bounding_box)

    print(result_text_list)

    return result_text_list
