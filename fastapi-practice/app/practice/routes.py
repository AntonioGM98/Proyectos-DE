from typing import List, Union
from fastapi import APIRouter, Header, HTTPException, requests
import json
from pydantic import BaseModel, Field

router = APIRouter()

#app = FastAPI()

@router.get("/")
async def health():
    return {"status": "OK"}

with open('/home/antoniogm/fastapi-practice/sources/markets.json') as f:
    data_markets = json.load(f)
    
@router.get('/markets/')
async def get_markets(idioma: str = Header(..., description='Codigo de idioma (ES, IT, FR)'), api_key: str = Header(...)):
    idioma = idioma.upper()
    languages = ['ES', 'IT', 'FR']

    if api_key != 'APIKEYPRUEBA':
        raise HTTPException(status_code=401, detail='Invalid API KEY')

    if idioma not in languages:
        raise HTTPException(status_code=400, detail='Codigo de idioma invalido')
    
    if idioma in data_markets:
        return data_markets[idioma]
    else:
        raise HTTPException(status_code=404, detail='No hay mercados para el idioma especificado')

class CabinClass(BaseModel):
    rbd: str
    type: str

class Cabin(BaseModel):
    cabinClass: CabinClass
    carrier: str

class Flight(BaseModel):
    flightNumber: int
    cabin: Cabin

class Segment(BaseModel):
    id: str
    departureDate: str
    arrivalDate: str
    utcDepartureDate: str
    utcArrivalDate: str
    departureCity: str
    arrivalCity: str
    time: str
    marketingFlight: Flight
    operatingFlight: Flight
    haul:str

class Passenger(BaseModel):
    id: str
    name: str
    surname: str
    birthDate: str
    passengerType: str

class Slice(BaseModel):
    id: str
    segmentIds: List[int]

class Context(BaseModel):
    locator: str
    issueCurrency: str
    issueCountry: str
    passengers: Union[List[Passenger], None] = None
    segments: Union[List[Segment], None] = None
    slices: Union[List[Slice], None] = None
    bookingDate: str

class Pass(BaseModel):
    id: str
    subtypes: List[str]

class requestSegment(BaseModel):
    id: int
    passengers: List[str]

class Item(BaseModel):
    type: str
    passengers: Union[List[Pass], None] = None
    segments: Union[List[requestSegment], None] = None

class Request(BaseModel):
    realm: str
    clientId: str
    items: List[Item]

class fullRequest(BaseModel):
    context: Context = Field(..., title='context')
    request: Request = Field(..., title='request')


@router.post('/parse/')
async def parse_json(request_data: fullRequest, status_code=204):
    print("JSON recibido: ", request_data)

    request_data_dict = request_data.model_dump()

    with open('request_salida.json','w') as f:
        json.dump(request_data_dict, f, indent=4)

    return {'message':'OK'}


with open('sources/airports.json', 'r') as f_airport:
    airports_data = json.load(f_airport)

with open('sources/bundles.json', 'r') as f_bundles:
    bundles_data = json.load(f_bundles)


def filtered_bundles(origin: str, dest: str):
    filtered_bundles = []

    for bundle in bundles_data:
        if bundle['origin_ida'] == airports_data.get(origin) and bundle['destination_ida'] == airports_data.get(dest):
            filtered_bundles.append(bundle)

    return filtered_bundles

def get_airport_code(city):
    return airports_data.get(city, "")

@router.post('/process_bundles')
async def process_bundles():
    bundles_from_madrid = []
    bundles_from_bilbao = []

    with open('request_salida.json','r') as f:
        request_data = json.load(f)

    context = request_data.get('context')
    segments = context.get('segments')

    for segment in segments:
        
        if(segment.get('departureCity') == 'Madrid'):
            origin =  segment.get('departureCity')
        if(segment.get('arrivalCity') == 'Bilbao'):
            destination = segment.get('arrivalCity')

        for bundle in bundles_data:
            if (bundle.get('origin_ida') == airports_data.get(origin) and not(bundle in bundles_from_madrid)):
                bundles_from_madrid.append(bundle)
            
            if (bundle.get('destination_ida') == airports_data.get(destination) and not(bundle in bundles_from_bilbao)):
                bundles_from_bilbao.append(bundle)
            
    return {'bundles_from_madrid': bundles_from_madrid,
            'bundles_from_bilbao': bundles_from_bilbao}


def get_priority(list_passenger, passenger_request):
    
    for passenger in list_passenger:
        if passenger not in passenger_request:
            return False
    
    return True

def get_flexibility(subtypes, product):
    for type in subtypes:
        if product in type:
            return True
        
    return False


def get_valid_bundles(file_path: str):

    bundles_valid = []
    request_data = []

    with open(file_path,'r') as f:
        request_data = json.load(f)
    
    context = request_data.get('context')
    request = request_data.get('request')

    segments = context.get('segments')
    slices = context.get('slices')
    passengers_context = context.get('passengers')
    list_passenger = []
    items = request.get('items')
    passengers_request = items[0].get('segments')[0].get('passengers')

    origin = ''
    destination = ''
    subtypes = []

    for item in items[1].get('passengers'):
        subtypes.append(item.get('subtypes'))

    for passenger in passengers_context:
        list_passenger.append(passenger.get('id'))

    for segment in segments:
        if(slices[0].get('segmentIds')[0] == int(segment.get('id'))):
            origin = segment.get('departureCity')
            destination = segment.get('arrivalCity')

    for bundle in bundles_data:
        if bundle['origin_ida'] == airports_data.get(origin) and bundle['destination_ida'] == airports_data.get(destination):
            #if filter_bundle(bundle, context.get('passengers')):
            if get_priority(list_passenger, passengers_request) and get_flexibility(subtypes, bundle.get('product_1')):
                bundles_valid.append(bundle)    
            

    return bundles_valid

@router.post('/valid_bundles')
async def valid_bundles():
    valid_bundles = get_valid_bundles('request_salida.json')

    return {'bundles validos': valid_bundles}