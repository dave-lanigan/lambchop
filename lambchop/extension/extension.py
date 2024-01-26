
import os
import sys

import requests
from lambchop.server import Server


TIMEOUT_MS = 1000 # Maximum time (in milliseconds) that a batch would be buffered.
MAX_BYTES = 262144 # Maximum size in bytes that the logs would be buffered in memory.
MAX_ITEMS = 10000 # Maximum number of events that would be buffered in memory.


class LambdaExtension(Server):
    def __init__(self, name, port=1956):
        super().__init__(port)
        self.name = name
        self.agent_id = None
        
        self.rt_api_address = os.environ['AWS_LAMBDA_RUNTIME_API']
        self.rt_api_url = f"http://{self.rt_api_address}/2020-01-01/extension"
        self.logs_api_base_url = f"http://{self.rt_api_address}/2020-08-15"
        self.headers = {}

        self.register()

    def register(self):
        """Register the extension with the Lambda runtime API
        
        Its required to register the extension with the Lambda runtime API before it can be used.
        """
        print("Registering Extension")
        URL = f"{self.rt_api_url}/register"
        headers = {
            "Lambda-Extension-Name": self.name,
            "Content-Type": "application/json"
        }
        body = {"events": ["INVOKE", "SHUTDOWN"]}
        try:
            r = requests.post(URL, headers=headers, json=body)

            if r.status_code != 200:
                print(
                    f"/register request to ExtensionsAPIClient failed. Status:  {r.status}, Response: {r.text}"
                )
                sys.exit(1)
            self.agent_id = r.headers.get("Lambda-Extension-Identifier")
            self.headers = {
                "Lambda-Extension-Identifier": self.agent_id,
                "Content-Type": "application/json"
            }
            return self.agent_id
        except Exception as e:
            raise Exception(f"Failed to register to extention") from e
    
    def get_event(self):
        """Get the next event from the Lambda runtime API
        
        The Lambda runtime API will send an event to the extension when there is a new invocation or the Lambda runtime is shutting down.
        """
        URL = f"{self.rt_api_url}/event/next"
        r = requests.get(URL, headers=self.headers)
        if r.status_code != 200:
            print(
                f"/register request to ExtensionsAPIClient failed. Status:  {r.status}, Response: {r.text}"
            )
            sys.exit(1)
        return r.json()
    
    def subscibe_to_logs(self):
        print(f"Subscribing to Logs API on {self.logs_api_base_url}")
        URL=f"{self.logs_api_base_url}/logs"
        body={
            "destination":{
                "protocol": "HTTP",
                "URI": f"http://sandbox:{RECEIVER_PORT}",
            },
            "types": ["platform", "function"],
            "buffering": {
                "timeoutMs": TIMEOUT_MS,
                "maxBytes": MAX_BYTES,
                "maxItems": MAX_ITEMS
            }
        }
        r = requests.put(URL, json=body, headers=self.headers)
        if r.status_code != 200:
            print(
                f"/register request to ExtensionsAPIClient failed. Status:  {r.status}, 
                Response: {r.text}"
            )
            sys.exit(1)
        print("Subscribed to Logs API")
        print(r.text)
    
    def run(self):
        print(f"Running Extension {self.name}")
        print(f"Starting TCP server in seperate thread...")

        print("Starting keep-alive logging loopback mechanism...")
        while True:
            r = self.get_event()
            while self.jobs > 0:
                print(f"{self.jobs} background tasks running.")
            self.serve()


def main():
    print(f"Starting Extensions")
    
    name = os.path.basename(__file__)
    extension = LambdaExtension(name=name)
    extension.run()


if __name__ == "__main__":
    main()