import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Graph RAG MVP - Stepwise Labs',
  description: 'Intelligent question answering with knowledge graphs',
  keywords: ['Graph RAG', 'Knowledge Graph', 'AI', 'Machine Learning'],
  authors: [{ name: 'Stepwise Labs' }],
}

export const viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
      </head>
      <body className="antialiased">
        {children}
      </body>
    </html>
  )
} 