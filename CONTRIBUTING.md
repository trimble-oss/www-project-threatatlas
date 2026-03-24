# Contributing to OWASP ThreatAtlas

Thank you for your interest in contributing to OWASP ThreatAtlas! We welcome contributions from the community in many forms.

## How to Contribute

- **Fix bugs and implement new features**
- **Improve the documentation**
- **Expand the knowledge base** with new threat models
- **Report a bug** ([create an issue](https://github.com/trimble-oss/www-project-threatatlas/issues))
- **Suggest a new feature** ([create an issue](https://github.com/trimble-oss/www-project-threatatlas/issues))
- **Join the conversation** on the [OWASP Slack](http://owasp.org/slack/invite) in the `#project-threatatlas` channel

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your change
4. **Make your changes** and commit them
5. **Push** your changes to your fork
6. **Open a Pull Request** against the `main` branch

For detailed setup instructions, see the [Development Guide](threatatlas-app/docs/development.md).

### Trimble Employees

Please also review the [Trimble OSS contribution guidelines](https://trimble-oss.github.io/contribute) including the [contributor guidelines](https://trimble-oss.github.io/contribute/guidelines/).

## Development Setup

### Prerequisites

- **Docker** v24+ and **Docker Compose** v2+ (for containerized development)
- **Node.js** v18+ with **pnpm** (for frontend development)
- **Python** 3.11+ with **pdm** (for backend development)

### Quick Start

```bash
# Clone your fork
git clone https://github.com/<your-username>/www-project-threatatlas
cd www-project-threatatlas/threatatlas-app

# Copy environment file
cp .env.example .env

# Start all services with Docker
docker compose up -d
```

For manual (non-Docker) setup, see the [Development Guide](threatatlas-app/docs/development.md).

## Pull Request Process

1. Ensure your code follows the project's existing style
2. Update documentation if your changes affect it
3. Add tests for new functionality where applicable
4. Make sure all existing tests pass
5. Use **rebase** instead of merge to keep a clean commit history
6. Fill out the pull request template completely

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [trimble-oss-contrib-admins-ug@trimble.com](mailto:trimble-oss-contrib-admins-ug@trimble.com).

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE.md).
