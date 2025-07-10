# Suna Production Deployment Guide

## Overview
This guide covers deploying Suna to production with:
- **Backend**: Render.com (Docker)
- **Frontend**: Vercel
- **Database**: Supabase (existing)
- **Redis**: External Redis service

## Backend Deployment (Render.com)

### 1. Prerequisites
- Render.com account
- External Redis service (Redis Cloud, Railway, etc.)
- Supabase project (already configured)

### 2. Deploy to Render

#### Option A: Using render.yaml (Recommended)
1. Connect your GitHub repository to Render
2. The `render.yaml` file will automatically configure the service
3. Add environment variables in Render dashboard

#### Option B: Manual Setup
1. Create new **Web Service** in Render
2. Connect your GitHub repository
3. Set build settings:
   - **Environment**: Docker
   - **Dockerfile Path**: `./backend/Dockerfile`
   - **Docker Context**: `./backend`

### 3. Environment Variables
Set these in your Render dashboard:

```bash
# Required
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
REDIS_URL=redis://your-redis-url:6379
FERNET_KEY=your-fernet-key
DAYTONA_URL=https://api.daytona.io
DAYTONA_API_KEY=your-daytona-api-key

# Optional
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
WORKERS=2
THREADS=2
```

### 4. Redis Setup
You'll need an external Redis service since Render doesn't include Redis:

**Option 1: Redis Cloud (Free tier available)**
```bash
# Sign up at https://redis.com/redis-enterprise-cloud/
# Get connection URL and set as REDIS_URL
REDIS_URL=redis://default:password@redis-server:port
```

**Option 2: Railway Redis**
```bash
# Deploy Redis on Railway
# Get connection URL and set as REDIS_URL
```

### 5. Health Check
Render will automatically use the health check endpoint: `/api/health`

## Frontend Deployment (Vercel)

### 1. Deploy to Vercel
1. Connect your GitHub repository to Vercel
2. Set **Root Directory**: `frontend`
3. Vercel will auto-detect Next.js

### 2. Environment Variables
Set these in Vercel dashboard:

```bash
# Required
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com

# Optional
NEXT_PUBLIC_ENVIRONMENT=production
EDGE_CONFIG=https://edge-config.vercel.com/your-config?token=your-token
```

### 3. Build Settings
Vercel should auto-detect these, but verify:
- **Framework Preset**: Next.js
- **Build Command**: `npm run build`
- **Output Directory**: `.next`

## Feature Flags Configuration

The backend automatically initializes these feature flags on startup:
- `custom_agents`: true (enabled by default)
- `agent_workflows`: true
- `mcp_integrations`: true

If Redis is unavailable, the system falls back to default values defined in the code.

## Monitoring & Health Checks

### Backend Health
- Health endpoint: `https://your-backend.onrender.com/api/health`
- Render provides automatic health monitoring

### Frontend Health
- Vercel provides automatic monitoring
- Check deployment logs in Vercel dashboard

## Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   - Verify `REDIS_URL` is correct
   - Check Redis service is running
   - Verify network connectivity

2. **Supabase Permissions**
   - Ensure service role key has correct permissions
   - Check RLS policies are configured

3. **Daytona Issues**
   - Verify API key is valid
   - Check if you have sufficient credits

4. **Build Failures**
   - Check Dockerfile syntax
   - Verify all dependencies are listed in pyproject.toml

### Logs
- **Render**: Check logs in service dashboard
- **Vercel**: Check function logs in dashboard
- **Supabase**: Check logs in dashboard

## Post-Deployment

1. **Test the application** thoroughly
2. **Monitor resource usage** in Render/Vercel
3. **Set up monitoring** (optional)
4. **Configure custom domain** (optional)

## Development vs Production

The system automatically detects the environment and:
- Enables production optimizations
- Sets appropriate log levels
- Configures resource limits
- Initializes feature flags

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Review service logs
3. Verify all environment variables are set correctly