from pathlib import Path

import requests

def main():
    # Manifest URL (should usually end in *.json)
    manifest_url = "https://gallica.bnf.fr/iiif/ark:/12148/btv1b100840691/manifest.json"

    response = requests.get(manifest_url)

    if response.status_code == 200:
        manifest = response.json()
        print("Manifest retrieved successfully.")
    else:
        print(f"Failed to get manifest. Status code: {response.status_code}\nResponse: {response.text}")
        return
    
    # Create a directory to store images
    label = manifest.get("label", "")
    images_dir = Path(label.replace(" ", "-") + "_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    canvases = manifest.get("sequences", [{}])[0].get("canvases", [])
    for canvas in canvases:
        # Get the last segment of the @id URL as the image/page identifier
        canvas_id = canvas.get("@id", "").split("/")[-1]
        image_url = canvas.get("images", [{}])[0].get("resource", {}).get("@id", "")
        if not image_url:
            print(f"No image URL found for canvas {canvas_id}. Skipping.")
            continue
        image_path = images_dir / f"{canvas_id}.jpg"
        if image_path.exists():
            print(f"Image for canvas {canvas_id} already exists at {image_path}. Skipping download.")
            continue
        # Download the image
        try:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(image_path, "wb") as image_file:
                    image_file.write(image_response.content)
                print(f"Downloaded image for canvas {canvas_id} to {image_path}.")
            else:
                print(f"Failed to download image for canvas {canvas_id}. Status code: {image_response.status_code}")
        except Exception as e:
            print(f"Error downloading image for canvas {canvas_id}: {e}")



if __name__ == "__main__":
    main()
