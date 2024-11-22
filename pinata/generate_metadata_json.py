import json
import os

class MetadataJSONGenerator:
    def __init__(self, json_path, gateway_url):
        self.json_path = json_path
        self.gateway_url = gateway_url

    def add_image_attribute(self):
        # Load the JSON from the file
        with open(self.json_path, "r") as file:
            data = json.load(file)

        # Insert the "image" attribute after "description"
        if "description" in data:
            updated_data = {}
            for key, value in data.items():
                updated_data[key] = value
                if key == "description":
                    updated_data["image"] = self.gateway_url
            data = updated_data
        else:
            # If "description" is not found, append at the end
            data["image"] = self.gateway_url

        # Save the updated JSON back to the file
        with open(self.json_path, "w") as file:
            json.dump(data, file, indent=4)

        return data