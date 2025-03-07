# LexiMentis - AI-Powered Workers' Compensation Platform

![LexiMentis Logo](public/LexiMentis-Logo.svg)

LexiMentis transforms workers' compensation legal practice through an integrated AI platform leveraging the Model Context Protocol (MCP) to streamline document processing, case management, and legal analysis.

## Overview

LexiMentis provides a comprehensive solution for workers' compensation attorneys, combining:

- **Intelligent Document Analysis**: Automated processing of medical records and legal documents
- **Jurisdiction-Specific Knowledge**: Pre-trained on Kansas and Missouri workers' comp statutes and case law
- **Complete Case Management**: End-to-end workflow solutions from intake to resolution
- **AI-Powered Legal Assistant**: Interactive support for research, document generation, and strategy

This revolutionary MCP-powered architecture replaces the typical fragmented ecosystem of legal software with an integrated platform tailored to workers' compensation practice.

## Features

### Current MVP Features

- Interactive AI assistant for Kansas and Missouri workers' compensation questions
- Cost savings calculator to demonstrate ROI potential
- Basic demonstration of document analysis capabilities
- Informational website explaining platform functionality

### Under Development

- Full document processing with OCR and intelligent analysis
- Complete case management dashboard with task tracking
- Medical record summarization and analysis
- Settlement valuation assistance
- Client portal with automated status updates

## Technology Stack

- **Frontend**: React, TailwindCSS, Lucide Icons
- **Backend**: Node.js/Python serverless architecture
- **AI/ML**: MCP integration with various LLMs
- **Database**: Vector database for knowledge retrieval (DataStax)
- **Authentication**: JWT-based authentication system

## Getting Started

### Prerequisites

- Node.js v16 or higher
- npm or yarn

### Installation

```bash
# Clone the repository
git clone https://github.com/leximentis/leximentis-webapp.git

# Navigate to the project directory
cd leximentis-webapp

# Install dependencies
npm install

# Run the development server
npm run dev
```

### Configuration

Create a `.env` file in the root directory with the following variables:

```
REACT_APP_API_ENDPOINT=https://your-api-endpoint.com
REACT_APP_AUTH_DOMAIN=your-auth-domain
REACT_APP_AUTH_CLIENT_ID=your-client-id
```

## Development Roadmap

### Phase 1: MVP (Current)

- Basic website with informational content
- AI demo capabilities
- Cost savings calculator

### Phase 2: Core Platform (Q2-Q3 2025)

- Full document processing system
- Complete case management dashboard
- Medical record analysis
- Jurisdiction-specific knowledge base

### Phase 3: Expansion (Q4 2025-Q1 2026)

- Multi-state support
- Advanced analytics
- Client portal
- Additional practice areas

## MCP Integration

LexiMentis leverages the Model Context Protocol to create a network of specialized AI agents that together form a comprehensive practice environment:

```
[Client App] <-> [MCP Client] <-> [LexiMentis MCP Servers]
                                   ├── Document MCP
                                   ├── Medical Records MCP
                                   ├── Legal Research MCP
                                   ├── Form Generation MCP
                                   └── Case Management MCP
```

The MCP architecture provides several advantages:

- Specialized AI knowledge in different domains
- Secure, controlled access to firm information
- Standardized communication between components
- Enhanced privacy and data protection

## Contributing

We welcome contributions to LexiMentis! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Proprietary. © 2025 LexiMentis, LLC. All rights reserved.

## Contact

L.J. Cox - [lj.cox@leximentis.com](mailto:lj.cox@leximentis.com)  
Website: [https://leximentis.com](https://leximentis.com)

---

## About LexiMentis, LLC

Founded by L.J. Cox, a legal operations expert with 17+ years of experience, LexiMentis combines deep legal knowledge with cutting-edge AI technology to revolutionize workers' compensation practice. Our vision extends beyond workers' compensation to create the first true "law firm in a box" - a unified platform that replaces the fragmented legal tech ecosystem.

Starting with Kansas and Missouri workers' compensation as our beachhead market, we're building a scalable solution that will transform legal practice management across multiple practice areas and jurisdictions.
