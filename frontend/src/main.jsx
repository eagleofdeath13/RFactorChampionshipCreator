import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'react-hot-toast'
import App from './App.jsx'
import './index.css'

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 5000,
            style: {
              background: '#1F1F1F',
              color: '#fff',
              border: '1px solid rgba(255,255,255,0.1)',
              borderLeft: '4px solid #E31E24',
              fontFamily: 'Rajdhani, sans-serif',
              fontWeight: 600,
            },
            success: {
              iconTheme: {
                primary: '#00FF41',
                secondary: '#0A0A0A',
              },
            },
            error: {
              iconTheme: {
                primary: '#FF0040',
                secondary: '#fff',
              },
            },
          }}
        />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
