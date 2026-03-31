from fastapi import APIRouter

from apps.magnetic.core.client.ElasticClient import ElasticClient


router = APIRouter()
magnetic_router = router

@router.post("/test")
def add_data_org_units() -> str:
    elastic = ElasticClient()
    return elastic.test()
