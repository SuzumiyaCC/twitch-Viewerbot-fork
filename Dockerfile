# Build frontend assets
FROM node:18 AS frontend-build
WORKDIR /app/frontend
# Install dependencies
COPY frontend/package*.json ./
RUN npm ci
# Copy source and build
COPY frontend/ .
RUN npm run build

# Final image
FROM python:3.11-slim
WORKDIR /app
# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend
# Copy built frontend static files
COPY --from=frontend-build /app/frontend/out ./backend/static

WORKDIR /app/backend
EXPOSE 3001
CMD ["python", "app.py"]
