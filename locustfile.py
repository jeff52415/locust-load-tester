import logging
from locust import HttpUser, task, between, events
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    logger.info("Load test is starting")
    if environment.host is None:
        logger.error("Missing host configuration")
        environment.runner.quit()

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logger.info("Load test is stopping")

class EmbeddingUser(HttpUser):
    # Use constant pacing for more consistent load
    wait_time = between(3, 5)
    
    def on_start(self):
        """Called when a User starts running"""
        logger.info("User started")
        # Test the info endpoint first
        try:
            with self.client.get("/info", catch_response=True) as response:
                if response.status_code == 200:
                    logger.info("Successfully connected to embedding service")
                else:
                    logger.error(f"Failed to connect to embedding service: {response.status_code}")
        except Exception as e:
            logger.error(f"Failed to connect to embedding service: {str(e)}")
    
    @task(1)
    def get_embeddings(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payload = {
            "input": [
                "What is Deep Learning?",
                "What is BGE M3?"
            ]
        }

        try:
            with self.client.post(
                "/v1/embeddings",
                json=payload,
                headers=headers,
                catch_response=True,
                name="embedding_request",
                timeout=30  # Add timeout
            ) as response:
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'data' in data and len(data['data']) == 2:
                            response.success()
                            logger.debug("Successfully got embeddings")
                        else:
                            error_msg = "Invalid response format"
                            logger.error(error_msg)
                            response.failure(error_msg)
                    except json.JSONDecodeError as e:
                        error_msg = f"Invalid JSON response: {str(e)}"
                        logger.error(error_msg)
                        response.failure(error_msg)
                else:
                    error_msg = f"Request failed with status code: {response.status_code}"
                    logger.error(f"{error_msg}, Response: {response.text}")
                    response.failure(error_msg)
        except Exception as e:
            error_msg = f"Request exception: {str(e)}"
            logger.error(error_msg)
            if not response.closed:
                response.failure(error_msg)
