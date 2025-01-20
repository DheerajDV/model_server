import os

# Get current directory
current_dir = os.getcwd()
print(f"Current directory: {current_dir}")

# Create requirements.txt
requirements = """fastapi
uvicorn
gliner
requests
numpy
setfit
torch
transformers
sentence-transformers"""

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("requirements.txt created successfully") 