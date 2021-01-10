from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from hue_link import HueLink

class PhoneRequest(BaseModel):
    power_source: Optional[int] = None
    battery_percent: int


hue_link = HueLink('192.168.1.2')
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/iot/api/phone")
async def battery(item: PhoneRequest):
    charge_status = item.dict()
    try:
        if(charge_status['power_source'] != None):
            hue_link.bed_phone_indicator_on_plugin(charge_status['battery_percent'])
            #bed_phone_indicator_on_plugin(bridge, charge_status['battery_percent'], battery_palette)
        else:
            hue_link.bed_phone_indicator_on_unplug(charge_status['battery_percent'])
    except:
        print('Error')
        app.logger.info('Missing information - skipping')
        return 'error'
    return 'success'

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=80, debug=False)