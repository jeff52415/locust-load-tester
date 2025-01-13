# Locust Load Tester for Text Embeddings

A load testing suite for text embedding APIs that follow OpenAI's v1/embeddings interface. Supports both cloud APIs (like HuggingFace Inference Endpoints) and local deployment using text-embeddings-inference.

![Locust Charts](assets/image_0.png)
![Locust Dashboard](assets/image_1.png)


## Quick Start

1. Clone and enter the repository:
```bash
git clone https://github.com/jeff52415/locust-load-tester
cd locust-load-tester
```

2. Configure your API (optional):
Create a `.env` file:
```env
# For cloud API (optional)
API_ENDPOINT=https://your-endpoint.cloud
API_TOKEN=your_api_token

# If not provided, defaults to local text-embeddings-inference with BAAI/bge-m3
```

> **Important**: Your API must expose a `/v1/embeddings` endpoint (e.g., if API_ENDPOINT=https://your-endpoint.cloud, then https://your-endpoint.cloud/v1/embeddings must be accessible)

3. Start the services:
```bash
docker-compose up
```

4. Access Locust at http://localhost:8089

## Configuration Options

### Default Setup (No Configuration)
If no API_ENDPOINT is provided, the system will:
- Start a local text-embeddings-inference server with BAAI/bge-m3 model
- Run load tests against this local server

### Custom API Testing
To test your own API:
1. Create `.env` with your API details:
   - API_ENDPOINT should be your base endpoint (e.g., https://your-endpoint.cloud)
   - Your API must implement the `/v1/embeddings` endpoint
   - API_TOKEN if authentication is required
2. The API must follow OpenAI's v1/embeddings interface
3. Authorization header will be added automatically if API_TOKEN is provided

## Monitoring

- Real-time metrics at http://localhost:8089
- Response times and request rates
- Error tracking and detailed logs

## Available Commands

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## License

MIT License