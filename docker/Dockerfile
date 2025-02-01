# Base image
FROM openjdk:17-jdk-slim

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Maven dependencies
COPY pom.xml .
COPY target/*.jar app.jar

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy Python collectors
COPY src/python/collectors/*.py /app/collectors/

# Expose port
EXPOSE 8080

# Run the application
CMD ["java", "-jar", "app.jar"]