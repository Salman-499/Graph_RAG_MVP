# Graph RAG MVP Frontend

A modern Next.js frontend for the Graph RAG MVP application, built with TypeScript and Tailwind CSS.

## Features

- **Query Interface**: Ask questions and get AI-powered answers using Graph RAG
- **Document Upload**: Upload documents to build the knowledge base
- **Real-time Results**: View answers, sources, and knowledge graph context
- **Responsive Design**: Works on desktop and mobile devices
- **Stepwise Labs Branding**: Consistent with company design philosophy

## Tech Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS 3.4.17**: Utility-first CSS framework
- **React 18**: Latest React features and hooks

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp env.example .env.local
```

3. Configure environment variables in `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

Start the development server:
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/                 # Next.js App Router
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Main page
│   └── globals.css     # Global styles
├── components/         # React components
│   ├── Footer.tsx      # Footer with branding
│   └── StepwiseLogo.tsx # Company logo
└── types/             # TypeScript types
    └── api.ts         # API interface definitions
```

## API Integration

The frontend integrates with the FastAPI backend through these endpoints:

- `POST /api/query/` - Process user queries
- `POST /api/documents/upload` - Upload documents
- `GET /health` - Health check

## Design System

### Colors
- **Primary**: Blue (#3b82f6) for main actions
- **Secondary**: Gray (#6b7280) for secondary elements
- **Success**: Green (#10b981) for positive states
- **Error**: Red (#ef4444) for error states

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Components
- **Cards**: White background with subtle shadows
- **Buttons**: Primary (blue) and secondary (gray) variants
- **Inputs**: Consistent styling with focus states

## Customization

### Adding New Components

1. Create component in `src/components/`
2. Import and use in pages
3. Follow existing naming conventions

### Styling

- Use Tailwind CSS utility classes
- Custom styles in `src/app/globals.css`
- Component-specific styles in component files

### Environment Variables

Add new environment variables to `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=Graph RAG MVP
```

## Troubleshooting

### Common Issues

1. **API Connection Errors**: Ensure backend is running on correct port
2. **TypeScript Errors**: Run `npm install` to ensure all types are installed
3. **Styling Issues**: Check Tailwind CSS configuration

### Development Tips

- Use browser dev tools to inspect API calls
- Check console for error messages
- Verify environment variables are loaded

## Deployment

### Vercel (Recommended)

1. Connect GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Other Platforms

The app can be deployed to any platform that supports Next.js:
- Netlify
- AWS Amplify
- DigitalOcean App Platform

## Contributing

1. Follow existing code style and conventions
2. Add TypeScript types for new features
3. Test changes thoroughly
4. Update documentation as needed

## License

This project is part of the Graph RAG MVP by Stepwise Labs. 