import { useQuery } from '@tanstack/react-query'
import { fetchFailures } from '../api/client'
import { formatDistanceToNow } from 'date-fns'
import { AlertTriangle, TrendingUp, Zap, Clock } from 'lucide-react'

export default function Failures() {
  const { data: failures, isLoading } = useQuery({ 
    queryKey: ['failures'], 
    queryFn: fetchFailures 
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
          borderTop: '4px solid #f97316',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <p style={{ color: '#a78bfa' }}>Loading failures...</p>
      </div>
    )
  }
  
  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
          <AlertTriangle size={32} color="#f97316" />
          <h1 style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#e0e7ff' }}>
            Failure Analyses
          </h1>
        </div>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem', marginLeft: '3rem' }}>
          AI-powered error analysis and root cause detection
        </p>
      </div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {failures?.map((failure: any, idx: number) => (
          <div
            key={failure.id}
            style={{
              background: 'linear-gradient(135deg, #1e293b 0%, #1a1f35 100%)',
              padding: '2rem',
              borderRadius: '1rem',
              border: '1px solid #f9731640',
              boxShadow: '0 8px 32px rgba(249, 115, 22, 0.1)',
              transition: 'all 0.3s',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-4px)'
              e.currentTarget.style.boxShadow = '0 12px 48px rgba(249, 115, 22, 0.2)'
              e.currentTarget.style.borderColor = '#f9731680'
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)'
              e.currentTarget.style.boxShadow = '0 8px 32px rgba(249, 115, 22, 0.1)'
              e.currentTarget.style.borderColor = '#f9731640'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
                <CategoryBadge category={failure.error_category} />
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.5rem 1rem',
                  background: '#7c3aed20',
                  border: '1px solid #7c3aed40',
                  borderRadius: '0.5rem'
                }}>
                  <TrendingUp size={14} color="#a78bfa" />
                  <span style={{ fontSize: '0.875rem', color: '#a78bfa', fontWeight: '600' }}>
                    {failure.confidence_score}% confidence
                  </span>
                </div>
              </div>
              <div style={{ 
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                fontSize: '0.875rem', 
                color: '#94a3b8' 
              }}>
                <Clock size={14} />
                {formatDistanceToNow(new Date(failure.analyzed_at), { addSuffix: true })}
              </div>
            </div>
            
            <div style={{ 
              marginBottom: '1.5rem',
              padding: '1.25rem',
              background: '#0f172a',
              borderRadius: '0.75rem',
              border: '1px solid #f8717140'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                <Zap size={16} color="#f87171" />
                <strong style={{ color: '#f87171', fontSize: '0.95rem' }}>Error Message</strong>
              </div>
              <p style={{ color: '#e0e7ff', lineHeight: '1.6', fontSize: '0.9rem' }}>
                {failure.error_message}
              </p>
            </div>
            
            {failure.root_cause && (
              <div style={{
                padding: '1.25rem',
                background: 'linear-gradient(135deg, #06b6d420 0%, #7c3aed20 100%)',
                borderRadius: '0.75rem',
                border: '1px solid #06b6d440'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
                  <Zap size={16} color="#06b6d4" />
                  <strong style={{ color: '#06b6d4', fontSize: '0.95rem' }}>Root Cause Analysis</strong>
                </div>
                <p style={{ color: '#cbd5e1', lineHeight: '1.6', fontSize: '0.9rem' }}>
                  {failure.root_cause}
                </p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function CategoryBadge({ category }: { category: string }) {
  const configs: any = {
    dependency_conflict: { color: '#f59e0b', bg: '#f59e0b20', border: '#f59e0b40', icon: '📦' },
    test_failure: { color: '#ef4444', bg: '#ef444420', border: '#ef444440', icon: '🧪' },
    syntax_error: { color: '#ec4899', bg: '#ec489920', border: '#ec489940', icon: '⚠️' },
    configuration_error: { color: '#8b5cf6', bg: '#8b5cf620', border: '#8b5cf640', icon: '⚙️' },
    environment_issue: { color: '#06b6d4', bg: '#06b6d420', border: '#06b6d440', icon: '🌍' },
    timeout: { color: '#f97316', bg: '#f9731620', border: '#f9731640', icon: '⏱️' },
    resource_limit: { color: '#84cc16', bg: '#84cc1620', border: '#84cc1640', icon: '💾' },
    unknown: { color: '#6b7280', bg: '#6b728020', border: '#6b728040', icon: '❓' }
  }
  
  const config = configs[category] || configs.unknown
  
  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '0.5rem',
      padding: '0.5rem 1rem',
      borderRadius: '0.75rem',
      fontSize: '0.875rem',
      fontWeight: '600',
      background: config.bg,
      color: config.color,
      border: `1px solid ${config.border}`,
      boxShadow: `0 0 16px ${config.color}20`
    }}>
      <span>{config.icon}</span>
      {category.replace(/_/g, ' ')}
    </span>
  )
}
