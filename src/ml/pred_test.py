import requests
import base64
import numpy as np
from onnx import numpy_helper
# from google.protobuf.json_format import MessageToJson
from src.proto import onnx_ml_pb2, predict_pb2

json_request_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
pb_request_headers = {
    'Content-Type': 'application/octet-stream',
    'Accept': 'application/octet-stream'
}


ENDPOINT = 'http://localhost:8001/v1/models/resnet101/versions/1:predict'
ONNX_SERVER_ADDRESS: str = "localhost:50051"
ONNX_INPUT_NAME: str = "input"
ONNX_OUTPUT_NAME: str = "output"


# JSON形式のリクエスト
img = ImageClassifier.open_image("../data/sample/bobby.jpg")
preprocessed_img = ImageClassifier.preprocess(img)
# input_array = np.random.rand(1, 3, 224, 224).astype(np.float32)
tensor_proto = numpy_helper.from_array(preprocessed_img)  # ONNXのutility関数でTensorProtoを作成

json_str = MessageToJson(tensor_proto, use_integers_for_enums=True)  # TensorProtoをJSON形式に変換
data = json.loads(json_str)

inputs = {}
inputs['input'] = data       # 保存時に指定した入力層の名前
output_filters = ['output']  # 保存時に指定した出力層の名前

payload = {}  # リクエストで送るペイロードの作成、 inputs と outputFilter のフィールドをそれぞれ埋める
payload["inputs"] = inputs
payload["outputFilter"] = output_filters

res = requests.post(ENDPOINT, headers=json_request_headers, data=json.dumps(payload))
raw_data = json.loads(res.text)['outputs']['output']['rawData']  # 生データを取得
outputs = np.frombuffer(base64.b64decode(raw_data), dtype=np.float32)  # 生データはbase64でencodeされたバイナリ列なので適切にdecode
print(outputs.shape)  # (1, 1000)

# バイナリ形式のリクエスト
input_array = np.random.rand(1, 3, 224, 224).astype(np.float32)
onnx_tensor_proto = numpy_helper.from_array(input_array)  # ONNXのutility関数でTensorProtoを作成
tensor_proto = onnx_ml_pb2.TensorProto()  # ビルド時に作成されたスクリプトからTensorProtoを作成、次で中身をコピー
tensor_proto.ParseFromString(onnx_tensor_proto.SerializeToString())  # 回りくどいが、実は生データで初期化する方がちょっと遅い

predict_request = predict_pb2.PredictRequest()  # リクエスト用のprotocol buffer
predict_request.inputs['input'].CopyFrom(tensor_proto)  # 保存時に指定した入力層の名前のフィールドへTensorProtoをコピー
predict_request.output_filter.append('output')  # 保存時に指定した出力層の名前をoutput_filterに登録

payload = predict_request.SerializeToString()  # リクエストとして送るためにstring型へdump

res = requests.post(ENDPOINT, headers=pb_request_headers, data=payload)
actual_result = predict_pb2.PredictResponse()  # リクエストのレスポンス用のprotocol buffer
actual_result.ParseFromString(res.content)
outputs = np.frombuffer(actual_result.outputs['output'].raw_data, dtype=np.float32)  # バイナリ列が入ってるのでdecode
print(outputs.shape)  # (1, 1000)


# if __name__ == "__main__":

#     img = ImageClassifier.open_image("../data/sample/bobby.jpg")
#     preprocessed_img = ImageClassifier.preprocess(img)

#     input_tensor = onnx_ml_pb2.TensorProto()
#     input_tensor.dims.extend(preprocessed_img.shape)
#     input_tensor.data_type = 1
#     input_tensor.raw_data = preprocessed_img.tobytes()

#     request_message = predict_pb2.PredictRequest()
#     request_message.inputs[ONNX_INPUT_NAME].data_type = input_tensor.data_type
#     request_message.inputs[ONNX_INPUT_NAME].dims.extend(preprocessed_img.shape)
#     request_message.inputs[ONNX_INPUT_NAME].raw_data = input_tensor.raw_data

#     response = self.st



    

#     sess = onnxruntime.InferenceSession(onnx_filename)
#     outputs = sess.run(['output'], {'input': preprocessed_img})[0]
#     print(outputs)
#     labels = ImageClassifier.load_labels(conf.LABEL_PATH)
#     res = ImageClassifier.postprocess(outputs, labels)
#     print(res)

#             logger.info(f"registering cache: {data.data}")
#             image = Image.open(os.path.join("data/", f"{data.data}.jpg"))
#             preprocessed = self.preprocess_transformer.transform(image)

#             input_tensor = onnx_ml_pb2.TensorProto()
#             input_tensor.dims.extend(preprocessed.shape)
#             input_tensor.data_type = 1
#             input_tensor.raw_data = preprocessed.tobytes()

#             request_message = predict_pb2.PredictRequest()
#             request_message.inputs[self.onnx_input_name].data_type = input_tensor.data_type
#             request_message.inputs[self.onnx_input_name].dims.extend(preprocessed.shape)
#             request_message.inputs[self.onnx_input_name].raw_data = input_tensor.raw_data

#             response = self.stub.Predict(request_message)
#             output = np.frombuffer(response.outputs[self.onnx_output_name].raw_data, dtype=np.float32)

#             softmax = self.softmax_transformer.transform(output).tolist()
