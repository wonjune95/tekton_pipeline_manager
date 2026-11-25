import pickle

import yaml
from fastapi import APIRouter, UploadFile
from rest_framework.response import Response
from rest_framework.views import APIView

router = APIRouter()


@router.post("/models/upload")
async def upload(file: UploadFile):
    # 업로드한 파일을 pickle 로 읽는다
    # ruleid: mois-5-05-insecure-deserialization-py
    model = pickle.load(file.file)
    return {"name": getattr(model, "name", "")}


class PipelineView(APIView):
    def post(self, request):
        # DRF: 요청 본문(data)의 값을 YAML 로 읽으며 임의 객체를 허용
        # ruleid: mois-5-05-insecure-deserialization-py
        pipeline = yaml.load(request.data["pipeline"], Loader=yaml.Loader)
        return Response({"steps": len(pipeline)})

    def get(self, request):
        # ruleid: mois-5-05-insecure-deserialization-py
        state = pickle.loads(bytes.fromhex(self.request.query_params["state"]))
        return Response({"state": str(state)})
