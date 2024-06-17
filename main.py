import aiohttp
import os
import asyncio

# Function to download a cat image
async def download_cat_image(session, image_url, filename):
    try:
        async with session.get(image_url) as response:
            response.raise_for_status()
            image_data = await response.read()
            with open(filename, "wb") as f:
                f.write(image_data)
            print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Function to download cat images concurrently
async def download_cat_images(num_images):
    # Create a directory to save the images
    os.makedirs("cat_images", exist_ok=True)
    
    # API endpoint for fetching random cat images
    api_url = "https://api.thecatapi.com/v1/images/search"
    
    # Number of tasks to run concurrently
    num_concurrent = 10
    
    # Create a session for making asynchronous requests
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_images):
            try:
                # Fetch a random cat image from the Cat API
                async with session.get(api_url) as response:
                    response.raise_for_status()
                    image_url = (await response.json())[0]['url']
                    
                    # Filename to save the image
                    filename = f"cat_images/cat_{i+1}.jpg"
                    
                    # Create a task to download the image
                    task = asyncio.create_task(download_cat_image(session, image_url, filename))
                    tasks.append(task)
            except Exception as e:
                print(f"Error downloading image {i+1}: {e}")
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)

# Number of images to download
num_images = 1000

# Run the asynchronous download
asyncio.run(download_cat_images(num_images))
