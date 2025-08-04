FROM scottyhardy/docker-wine:latest

# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip curl build-essential

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . .

RUN pip3 freeze > requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Build the executable using PyInstaller
CMD ["wine", "pyinstaller", "--onefile", "--windowed", "main.py", "--distpath", "/app/dist/windows"]
