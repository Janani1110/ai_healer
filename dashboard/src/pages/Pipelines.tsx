import { useQuery } from '@tanstack/react-query'
import { fetchPipelines } from '../api/client'
import { formatDistanceToNow } from 'date-fns'
import { GitBranch, Clock, CheckCircle2, XCircle, Loader2, PlayCircle } from 'lucide-react'

export default function Pipelines() {
  const { data: pipelines, isLoading } = useQuery({ 
    queryKey: ['pipelines'], 
    queryFn: fetchPipelines 
  })
  
  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '60vh',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        <div style={{
          width: '48px',
          height: '48px',
          border: '4px solid #7c3aed40',
          borderTop: '4px solid #06b6d4',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <p style={{ color: '#a78bfa' }}>Loading pipelines...</p>
      </div>
    )
  }
  
  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
          <GitBranch size={32} color="#06b6d4" />
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#e0e7ff' }}>
            Pipelines
          </h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem', marginLeft: '3rem' }}>
          Monitor all CI/CD pipeline executions
        </p>
      </div>
      
      <div style={{
        background: 'linear-gradient(135deg, #1e293b 0%, #1a1f35 100%)',
        borderRadius: '1rem',
        border: '1px solid #06b6d440',
        overflow: 'hidden',
        boxShadow: '0 8px 32px rgba(6, 182, 212, 0.1)'
      }}>
        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ 
                background: 'linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%)',
                borderBottom: '2px solid #06b6d440'
              }}>
                <th style={thStyle}>Repository</th>
                <th style={thStyle}>Branch</th>
                <th style={thStyle}>Commit</th>
                <th style={thStyle}>Status</th>
                <th style={thStyle}>Started</th>
              </tr>
            </thead>
            <tbody>
              {pipelines?.map((pipeline: any, idx: number) => (
                <tr 
                  key={pipeline.id} 
                  style={{ 
                    borderBottom: '1px solid #334155',
                    transition: 'all 0.2s',
                    cursor: 'pointer'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = '#06b6d410'
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'transparent'
                  }}
                >
                  <td style={tdStyle}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <div style={{
                        width: '8px',
                        height: '8px',
                        borderRadius: '50%',
                        background: '#06b6d4',
                        boxShadow: '0 0 8px #06b6d4'
                      }} />
                      <span style={{ fontWeight: '600', color: '#e0e7ff' }}>
                        {pipeline.repository}
                      </span>
                    </div>
                  </td>
                  <td style={tdStyle}>
                    <span style={{
                      padding: '0.375rem 0.75rem',
                      background: '#7c3aed20',
                      border: '1px solid #7c3aed40',
                      borderRadius: '0.5rem',
                      fontSize: '0.875rem',
                      color: '#a78bfa',
                      fontWeight: '500'
                    }}>
                      {pipeline.branch}
                    </span>
                  </td>
                  <td style={tdStyle}>
                    <code style={{ 
                      fontSize: '0.875rem',
                      background: '#0f172a',
                      padding: '0.375rem 0.75rem',
                      borderRadius: '0.375rem',
                      color: '#06b6d4',
                      border: '1px solid #06b6d420'
                    }}>
                      {pipeline.commit_sha.substring(0, 7)}
                    </code>
                  </td>
                  <td style={tdStyle}>
                    <StatusBadge status={pipeline.status} />
                  </td>
                  <td style={tdStyle}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#94a3b8' }}>
                      <Clock size={14} />
                      {formatDistanceToNow(new Date(pipeline.started_at), { addSuffix: true })}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

const thStyle = {
  padding: '1.25rem 1.5rem',
  textAlign: 'left' as const,
  fontSize: '0.875rem',
  fontWeight: '700',
  color: '#a78bfa',
  textTransform: 'uppercase' as const,
  letterSpacing: '0.05em'
}

const tdStyle = {
  padding: '1.25rem 1.5rem',
  fontSize: '0.875rem',
  color: '#cbd5e1'
}

function StatusBadge({ status }: { status: string }) {
  const configs: any = {
    success: { color: '#84cc16', icon: CheckCircle2, bg: '#84cc1620', border: '#84cc1640' },
    failure: { color: '#f87171', icon: XCircle, bg: '#f8717120', border: '#f8717140' },
    pending: { color: '#fbbf24', icon: Clock, bg: '#fbbf2420', border: '#fbbf2440' },
    running: { color: '#06b6d4', icon: Loader2, bg: '#06b6d420', border: '#06b6d440' }
  }
  
  const config = configs[status] || configs.pending
  const Icon = config.icon
  
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.5rem',
      padding: '0.5rem 1rem',
      borderRadius: '9999px',
      fontSize: '0.8rem',
      fontWeight: '600',
      background: config.bg,
      color: config.color,
      border: `1px solid ${config.border}`,
      boxShadow: `0 0 12px ${config.color}20`
    }}>
      <Icon size={14} />
      {status}
    </span>
  )
}
