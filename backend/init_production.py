#!/usr/bin/env python3
"""
Production initialization script for Suna backend.
This script sets up default feature flags and configurations for production deployment.
Run this script inside the Docker container or with the proper Python environment.
"""

import asyncio
import logging
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flags.flags import enable_flag
    from services.redis import get_client
except ImportError as e:
    print(f"❌ Failed to import modules: {e}")
    print("Make sure to run this script inside the Docker container or with proper dependencies installed")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_production_flags():
    """Initialize production feature flags"""
    try:
        # Enable core features by default
        await enable_flag('custom_agents', 'Enable custom agents functionality')
        await enable_flag('agent_workflows', 'Enable agent workflows')
        await enable_flag('mcp_integrations', 'Enable MCP integrations')
        
        logger.info("✅ Production feature flags initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize production flags: {e}")
        return False

async def verify_redis_connection():
    """Verify Redis connection is working"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            redis_client = await get_client()
            await redis_client.ping()
            logger.info("✅ Redis connection verified")
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"⚠️  Redis connection attempt {attempt + 1} failed, retrying in {retry_delay}s...")
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"❌ Redis connection failed after {max_retries} attempts: {e}")
                return False
    
    return False

async def main():
    """Main initialization function"""
    logger.info("🚀 Starting Suna production initialization...")
    
    # Verify Redis connection
    if not await verify_redis_connection():
        logger.error("❌ Production initialization failed - Redis not available")
        return False
    
    # Initialize feature flags
    if not await init_production_flags():
        logger.error("❌ Production initialization failed - Feature flags setup failed")
        return False
    
    logger.info("✅ Suna production initialization completed successfully!")
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)