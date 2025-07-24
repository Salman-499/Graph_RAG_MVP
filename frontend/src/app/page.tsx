'use client';

import { useState } from 'react';
import { QueryResponse } from '@/types/api';
import Footer from '@/components/Footer';
import StepwiseLogo from '@/components/StepwiseLogo';

export default function Home() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [documentContent, setDocumentContent] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  const handleQuery = async () => {
    if (!query.trim()) return;

    setIsLoading(true);
    setResponse(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/query/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          max_results: 5,
          include_graph_context: true,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResponse(data);
    } catch (error) {
      console.error('Error processing query:', error);
      alert('Error processing query. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDocumentUpload = async () => {
    if (!documentContent.trim()) return;

    setIsUploading(true);
    setUploadStatus('');

    try {
      const response = await fetch(`${API_BASE_URL}/api/documents/upload`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: documentContent,
          metadata: {
            source: 'manual_upload',
            timestamp: new Date().toISOString(),
          },
          document_type: 'text',
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setUploadStatus(`Document uploaded successfully! ID: ${data.id}`);
      setDocumentContent('');
    } catch (error) {
      console.error('Error uploading document:', error);
      setUploadStatus('Error uploading document. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header with Stepwise Labs branding */}
      <header className="bg-gray-100 border-b border-gray-400">
        <div className="px-4 py-3">
          <div className="flex items-center space-x-4">
            <StepwiseLogo width={80} height={64} />
            
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Graph RAG MVP</h1>
              <p className="text-sm text-gray-600">Intelligent question answering with knowledge graphs</p>
            </div>
          </div>
        </div>
      </header>

      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Query and Upload */}
          <div className="space-y-6">
            {/* Query Section */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                Ask a Question
              </h2>
              <div className="space-y-4">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your question here..."
                  className="input-field resize-none"
                  rows={4}
                />
                <button
                  onClick={handleQuery}
                  disabled={isLoading || !query.trim()}
                  className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="loading-spinner mr-2"></div>
                      Processing...
                    </div>
                  ) : (
                    'Ask Question'
                  )}
                </button>
              </div>
            </div>

            {/* Document Upload Section */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                Upload Document
              </h2>
              <div className="space-y-4">
                <textarea
                  value={documentContent}
                  onChange={(e) => setDocumentContent(e.target.value)}
                  placeholder="Paste document content here..."
                  className="input-field resize-none"
                  rows={6}
                />
                <button
                  onClick={handleDocumentUpload}
                  disabled={isUploading || !documentContent.trim()}
                  className="btn-secondary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isUploading ? (
                    <div className="flex items-center justify-center">
                      <div className="loading-spinner mr-2"></div>
                      Uploading...
                    </div>
                  ) : (
                    'Upload Document'
                  )}
                </button>
                {uploadStatus && (
                  <div className={`text-sm p-3 rounded-lg ${
                    uploadStatus.includes('Error') 
                      ? 'bg-red-50 text-red-700 border border-red-200' 
                      : 'bg-green-50 text-green-700 border border-green-200'
                  }`}>
                    {uploadStatus}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            {/* Answer Section */}
            {response && (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <div className="w-2 h-2 bg-purple-500 rounded-full mr-3"></div>
                  Answer
                </h2>
                <div className="space-y-4">
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <p className="text-gray-900 leading-relaxed">{response.answer}</p>
                  </div>
                  <div className="flex items-center justify-between text-sm text-gray-600">
                    <span>Confidence: {(response.confidence_score * 100).toFixed(1)}%</span>
                    <span>Time: {response.processing_time.toFixed(2)}s</span>
                  </div>
                </div>
              </div>
            )}

            {/* Sources Section */}
            {response && response.sources.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <div className="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
                  Sources ({response.sources.length})
                </h2>
                <div className="space-y-3">
                  {response.sources.map((source, index) => (
                    <div key={index} className="bg-gray-50 p-3 rounded-lg">
                      <p className="text-sm text-gray-700 line-clamp-3">{source.content}</p>
                      {source.distance && (
                        <p className="text-xs text-gray-500 mt-1">
                          Similarity: {(1 - source.distance).toFixed(3)}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Graph Context Section */}
            {response && response.graph_context && (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                  <div className="w-2 h-2 bg-indigo-500 rounded-full mr-3"></div>
                  Knowledge Graph Context
                </h2>
                <div className="space-y-4">
                  {/* Entities */}
                  {response.graph_context.entities.length > 0 && (
                    <div>
                      <h3 className="font-medium text-gray-900 mb-2">Entities ({response.graph_context.entities.length})</h3>
                      <div className="flex flex-wrap gap-2">
                        {response.graph_context.entities.map((entity, index) => (
                          <span key={index} className="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                            {entity.name} ({entity.type})
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {/* Relationships */}
                  {response.graph_context.relationships.length > 0 && (
                    <div>
                      <h3 className="font-medium text-gray-900 mb-2">Relationships ({response.graph_context.relationships.length})</h3>
                      <div className="space-y-2">
                        {response.graph_context.relationships.map((rel, index) => (
                          <div key={index} className="bg-gray-50 p-2 rounded text-sm">
                            <span className="font-medium">{rel.source_id}</span>
                            <span className="text-gray-500 mx-2">→</span>
                            <span className="text-blue-600">{rel.relationship_type}</span>
                            <span className="text-gray-500 mx-2">→</span>
                            <span className="font-medium">{rel.target_id}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}