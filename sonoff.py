from pysonofflanr3 import SonoffSwitch
    
class Switch():
    def __init__(self, host, api_key, device_id):
        self.host = host
        self.api_key = api_key
        self.device_id = device_id
        
    async def print_state_callback(self, device):
        #print(device.basic_info)
        if device.basic_info is not None:
            if device.available:
                #print("ON" if device.is_on else "OFF")
                device.shutdown_event_loop()

    async def turn_on_callback(self, device):
        if device.basic_info is not None:
            if device.is_on:
                device.shutdown_event_loop()
            else:
                device.update_params({"switch": "on"})

    async def turn_off_callback(self, device):
        if device.basic_info is not None:
            if not device.is_on:
                device.shutdown_event_loop()
            else:
                device.update_params({"switch": "off"})

    def get_properties(self):
        # TODO: Handle the case of the switch being completely turned off
        s = SonoffSwitch(
            host=self.host,
            api_key=self.api_key,
            callback_after_update=self.print_state_callback
        )
        
        if s.is_on:
            return {'power': 'on'}
        else:
            return {'power': 'off'}
    
    def turn_on(self):
        s = SonoffSwitch(
            host=self.host,
            api_key=self.api_key,
            callback_after_update=self.turn_on_callback
        )
    
    def turn_off(self):
        s = SonoffSwitch(
            host=self.host,
            api_key=self.api_key,
            callback_after_update=self.turn_off_callback
        )
        