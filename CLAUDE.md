# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (Next.js)
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check formatting
```

### Backend (Python/FastAPI)
```bash
cd backend
python -m uvicorn api:app --reload  # Start development server
python -m pytest                   # Run tests
python -m pytest tests/specific_test.py  # Run specific test
```

### Full Stack Development
```bash
python setup.py  # Run setup wizard for initial configuration
python start.py  # Start/stop all containers
```

## Architecture Overview

Suna is a multi-tenant AI agent platform with four main components:

### Backend Architecture
- **FastAPI-based REST API** with modular design
- **AgentPress Framework**: Custom tool system for agent capabilities
- **Supabase Database**: PostgreSQL with Row-Level Security for multi-tenancy
- **Daytona SDK**: Containerized sandbox environments for secure agent execution
- **MCP Integration**: Model Context Protocol for extensible tool ecosystem

Key backend modules:
- `agent/` - Agent runtime, configuration, and execution
- `agentpress/` - Tool framework and thread management
- `sandbox/` - Isolated execution environments
- `mcp_service/` - Model Context Protocol integrations
- `triggers/` - Event-driven automation system
- `services/` - External service integrations (Redis, LLM, billing)

### Frontend Architecture
- **Next.js 15 App Router** with React 18 and TypeScript
- **React Query** for server state management and caching
- **Supabase Auth** for authentication and user management
- **shadcn/ui + Radix UI** for accessible component system
- **Tailwind CSS 4.0** for styling
- **Real-time streaming** via EventSource for agent responses

Key frontend areas:
- `app/(dashboard)/` - Main application interface
- `components/thread/` - Chat and conversation components
- `components/agents/` - Agent management and configuration
- `hooks/react-query/` - Data fetching and state management
- `lib/` - API clients and utility functions

## Key Development Patterns

### Agent Development
- Agents are configured in the `agents` table with versioning support
- Tools are implemented in `backend/agent/tools/` using the AgentPress framework
- MCP servers can be added via the MCP service for extended functionality
- Sandbox environments provide secure, isolated execution for agent operations

### Frontend Patterns
- Use React Query for all server state management
- Implement real-time features using EventSource for streaming
- Follow the established component structure in `components/`
- Use TypeScript strictly throughout the codebase
- Prefer Server Components where possible, use Client Components for interactivity

### Database Patterns
- All tables use Row-Level Security (RLS) for tenant isolation
- Use `account_id` for multi-tenant data access
- Prefer structured JSONB for flexible data storage
- Use Supabase real-time subscriptions for live updates

### Security Considerations
- All agent execution happens in isolated Daytona containers
- Credentials are encrypted and managed through the secure credential system
- API endpoints are protected with JWT authentication
- Database access is restricted through RLS policies

## Tool System

The AgentPress framework provides a modular tool system:
- **Base tools**: Browser automation, file operations, shell commands
- **Data providers**: LinkedIn, Twitter, Amazon, and other API integrations
- **MCP tools**: Extensible tool ecosystem via Model Context Protocol
- **Custom tools**: Can be added by implementing the base Tool class

Tools are automatically registered and their schemas are exposed to agents for selection and execution.

## Testing

### Backend Testing
- Use pytest for all backend tests
- Test files should follow the pattern `test_*.py`
- Use async test fixtures for database operations
- Mock external services in tests

### Frontend Testing
- Component tests should be co-located with components
- Use React Testing Library for component testing
- Test API integration using MSW (Mock Service Worker)

## Deployment

The application is containerized and can be deployed using:
- Docker Compose for local development
- Individual container deployment for production
- Supabase for database and authentication
- Redis for caching and session management

## Important Notes

- The project uses uv for Python dependency management
- Frontend uses npm with Node.js 18+
- All async operations should use proper error handling
- File uploads go through the sandbox system for security
- Agent conversations are streamed in real-time via EventSource