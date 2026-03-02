import { useQuery } from '@tanstack/react-query'
import { fetchFixes } from '../api/client'
import { formatDistanceToNow } from 'date-fns'
import { CheckCircle, XCircle, Wrench, GitCommit, Sparkles } from 'lucide-react'

export default function Fixes() {
  const { data: fixes, isLoading } = useQuery({ 
    queryKey: ['fixes'], 
    queryFn: fetchFixes 
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
          borderTop: '4px solid #84cc16',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <p style={{ color: '#a78bfa' }}>Loading fixes...</p>
      </div>
    )
  }
  
  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
          <Wrench size={32} color="#84cc16" />
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#e0e7ff' }}>
            Applied Fixes
          </h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem', marginLeft: '3rem' }}>
          AI-generated fixes automatically applied to your codebase
        </p>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {fixes?.map((fix: any, idx: number) => (
          <div
            key={fix.id}
            style={{
              background: fix.success 
                ? 'linear-gradient(135deg, #064e3b 0%, #065f46 100%)'
                : 'linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%)',
              padding: '2rem',
              borderRadius: '1rem',
              border: fix.success ? '1px solid #84cc1640' : '1px solid #f8717140',
              boxShadow: fix.success 
                ? '0 8px 32px rgba(132, 204, 22, 0.15)'
                : '0 8px 32px rgba(248, 113, 113, 0.15)',
              transition: 'all 0.3s',
              cursor: 'pointer',
              position: 'relative',
              overflow: 'hidden'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)'
              e.currentTarget.style.boxShadow = fix.success
                ? '0 12px 48px rgba(132, 204, 22, 0.25)'
                : '0 12px 48px rgba(248, 113, 113, 0.25)'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = fix.success
                ? '0 8px 32px rgba(132, 204, 22, 0.15)'
                : '0 8px 32px rgba(248, 113, 113, 0.15)'
            }}
          >
            {fix.success && (
              <div style={{
                position: 'absolute',
                top: '-50%',
                right: '-10%',
                width: '200px',
                height: '200px',
                background: 'radial-gradient(circle, #84cc1630 0%, transparent 70%)',
                pointerEvents: 'none'
              }} />
            )}
            
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1.5rem', position: 'relative' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{
                  padding: '0.75rem',
                  background: fix.success ? '#84cc1630' : '#f8717130',
                  borderRadius: '0.75rem',
                  border: fix.success ? '1px solid #84cc1640' : '1px solid #f8717140'
                }}>
                  {fix.success ? (
                    <CheckCircle size={28} color="#84cc16" />
                  ) : (
                    <XCircle size={28} color="#f87171" />
                  )}
                </div>
                <div>
                  <div style={{ 
                    fontWeight: '700', 
                    fontSize: '1.25rem',
                    color: fix.success ? '#d9f99d' : '#fecaca',
                    marginBottom: '0.25rem'
                  }}>
                    {fix.fix_type.replace(/_/g, ' ').toUpperCase()}
                  </div>
                  <div style={{ 
                    fontSize: '0.9rem', 
                    color: fix.success ? '#a3e635' : '#fca5a5',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    <Sparkles size={14} />
                    {fix.description || 'AI-generated fix applied'}
                  </div>
                </div>
              </div>
              <StatusBadge status={fix.status} success={fix.success} />
            </div>
            
            {fix.commit_sha && (
              <div style={{ 
                marginTop: '1.5rem', 
                padding: '1rem', 
                background: '#0f172a80', 
                borderRadius: '0.75rem',
                fontSize: '0.875rem',
                border: '1px solid #ffffff10',
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem'
              }}>
                <GitCommit size={16} color={fix.success ? '#84cc16' : '#f87171'} />
                <strong style={{ color: '#94a3b8' }}>Commit:</strong> 
                <code style={{
                  background: '#0f172a',
                  padding: '0.375rem 0.75rem',
                  borderRadius: '0.375rem',
                  color: fix.success ? '#84cc16' : '#f87171',
                  fontWeight: '600'
                }}>
                  {fix.commit_sha.substring(0, 7)}
                </code>
              </div>
            )}
            
            {fix.applied_at && (
              <div style={{ 
                marginTop: '1rem', 
                fontSize: '0.875rem', 
                color: fix.success ? '#a3e635' : '#fca5a5',
                opacity: 0.8
              }}>
                Applied {formatDistanceToNow(new Date(fix.applied_at), { addSuffix: true })}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function StatusBadge({ status, success }: { status: string; success: boolean }) {
  const configs: any = {
    pending: { color: '#fbbf24', bg: '#fbbf2420', border: '#fbbf2440' },
    in_progress: { color: '#06b6d4', bg: '#06b6d420', border: '#06b6d440' },
    applied: { color: '#84cc16', bg: '#84cc1620', border: '#84cc1640' },
    verified: { color: '#10b981', bg: '#10b98120', border: '#10b98140' },
    failed: { color: '#f87171', bg: '#f8717120', border: '#f8717140' }
  }
  
  const config = configs[status] || configs.pending
  
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
      boxShadow: `0 0 16px ${config.color}30`,
      textTransform: 'uppercase',
      letterSpacing: '0.05em'
    }}>
      {status.replace(/_/g, ' ')}
    </span>
  )
}
