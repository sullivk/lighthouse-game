from PIL import Image

# Open the PNG image
image = Image.open("BG2/ground/ground_unscaled.png")

# Define the new dimensions
new_width = 800  # Set to your desired width
new_height = 135 # Set to your desired height

# Resize the image
resized_image = image.resize((new_width, new_height))

# Save the resized image to a new file
resized_image.save("ground.png")

# Optional: Show the resized image
resized_image.show()