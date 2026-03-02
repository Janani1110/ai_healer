import { useQuery } from '@tanstack/react-query'
import { fetchStats, fetchPipelines, fetchFailures, fetchFixes } from '../api/client'
import { Activity, AlertCircle, CheckCircle, TrendingUp, Sparkles, Clock, Zap, Target } from 'lucide-react'

export default function Dashboard() {
  const { data: stats, isLoading: statsLoading } = useQuery({ queryKey: ['stats'], queryFn: fetchStats })
  const { data: pipelines, isLoading: pipelinesLoading } = useQuery({ queryKey: ['pipelines'], queryFn: fetchPipelines })
  const { data: failures, isLoading: failuresLoading } = useQuery({ queryKey: ['failures'], queryFn: fetchFailures })
  const { data: fixes, isLoading: fixesLoading } = useQuery({ queryKey: ['fixes'], queryFn: fetchFixes })
  
  const isLoading = statsLoading || pipelinesLoading || failuresLoading || fixesLoading
  
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
          width: '56px',
          height: '56px',
          border: '5px solid #7c3aed40',
          borderTop: '5px solid #ec4899',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
        <p style={{ color: '#a78bfa', fontSize: '1.1rem' }}>Loading dashboard...</p>
      </div>
    )
  }
  
  return (
    <div>
      <div style={{ marginBottom: '3rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.75rem' }}>
          <div style={{
            padding: '0.75rem',
            background: 'linear-gradient(135deg, #ec4899 0%, #7c3aed 100%)',
            borderRadius: '1rem',
            boxShadow: '0 8px 24px rgba(236, 72, 153, 0.3)'
          }}>
            <Zap size={32} color="#fff" />
          </div>
          <div>
            <h1 style={{ fontSize: '2.75rem', fontWeight: 'bold', color: '#e0e7ff', marginBottom: '0.25rem' }}>
              Dashboard
            </h1>
            <p style={{ color: '#a78bfa', fontSize: '1rem' }}>
              AI-Powered Self-Healing CI/CD System
            </p>
          </div>
        </div>
      </div>
      
      {/* Recent Fixes Section - Highlighted at Top */}
      {fixes && fixes.length > 0 && (
        <div style={{ marginBottom: '2.5rem' }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.75rem',
            marginBottom: '1.5rem'
          }}>
            <Sparkles size={24} color="#84cc16" />
            <h2 style={{ fontSize: '1.75rem', fontWeight: 'bold', color: '#e0e7ff' }}>
              Recent Fixes
            </h2>
            <div style={{
              padding: '0.25rem 0.75rem',
              background: '#84cc1620',
              border: '1px solid #84cc1640',
              borderRadius: '9999px',
              fontSize: '0.875rem',
              color: '#84cc16',
              fontWeight: '600'
            }}>
              {fixes.length} total
            </div>
          </div>
          <div style={{ 
            display: 'grid', 
            gap: '1.25rem',
            gridTemplateColumns: 'repeat(auto-fill, minmax(380px, 1fr))'
          }}>
            {fixes.slice(0, 6).map((fix: any, idx: number) => (
              <div
                key={idx}
                style={{
                  background: 'linear-gradient(135deg, #064e3b 0%, #065f46 100%)',
                  padding: '1.75rem',
                  borderRadius: '1rem',
                  border: '1px solid #84cc1640',
                  boxShadow: '0 8px 32px rgba(132, 204, 22, 0.15)',
                  transition: 'all 0.3s',
                  cursor: 'pointer',
                  position: 'relative',
                  overflow: 'hidden'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-6px)'
                  e.currentTarget.style.boxShadow = '0 16px 48px rgba(132, 204, 22, 0.25)'
                  e.currentTarget.style.borderColor = '#84cc1680'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)'
                  e.currentTarget.style.boxShadow = '0 8px 32px rgba(132, 204, 22, 0.15)'
                  e.currentTarget.style.borderColor = '#84cc1640'
                }}
              >
                <div style={{
                  position: 'absolute',
                  top: '-30%',
                  right: '-15%',
                  width: '150px',
                  height: '150px',
                  background: 'radial-gradient(circle, #84cc1630 0%, transparent 70%)',
                  pointerEvents: 'none'
                }} />
                
                <div style={{ display: 'flex', alignItems: 'start', gap: '1rem', position: 'relative' }}>
                  <div style={{
                    background: '#84cc1630',
                    padding: '0.75rem',
                    borderRadius: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    border: '1px solid #84cc1640'
                  }}>
                    <CheckCircle size={24} color="#84cc16" />
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ 
                      fontWeight: '700', 
                      marginBottom: '0.5rem',
                      color: '#d9f99d',
                      fontSize: '1rem'
                    }}>
                      {fix.fix_description || fix.fix_type?.replace(/_/g, ' ') || 'Fix applied successfully'}
                    </div>
                    <div style={{ 
                      color: '#a3e635', 
                      fontSize: '0.85rem',
                      marginBottom: '0.75rem',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.5rem'
                    }}>
                      <Target size={12} />
                      {fix.error_category || 'Syntax error'}
                    </div>
                    <div style={{ 
                      display: 'flex', 
                      alignItems: 'center', 
                      gap: '0.5rem',
                      color: '#86efac',
                      fontSize: '0.75rem'
                    }}>
                      <Clock size={12} />
                      <span>{new Date(fix.created_at).toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Stats Cards */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '1.5rem',
        marginBottom: '2.5rem'
      }}>
        <StatCard
          title="Total Pipelines"
          value={stats?.total_pipelines || 0}
          icon={<Activity size={28} />}
          color="#06b6d4"
          bgGradient="linear-gradient(135deg, #164e63 0%, #155e75 100%)"
        />
        <StatCard
          title="Total Failures"
          value={stats?.total_failures || 0}
          icon={<AlertCircle size={28} />}
          color="#f97316"
          bgGradient="linear-gradient(135deg, #7c2d12 0%, #9a3412 100%)"
        />
        <StatCard
          title="Successful Fixes"
          value={stats?.successful_fixes || 0}
          icon={<CheckCircle size={28} />}
          color="#84cc16"
          bgGradient="linear-gradient(135deg, #365314 0%, #3f6212 100%)"
        />
        <StatCard
          title="Success Rate"
          value={`${stats?.success_rate || 0}%`}
          icon={<TrendingUp size={28} />}
          color="#ec4899"
          bgGradient="linear-gradient(135deg, #831843 0%, #9f1239 100%)"
        />
      </div>
      
      {/* Recent Activity */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(450px, 1fr))',
        gap: '1.5rem'
      }}>
        <RecentActivity title="Recent Pipelines" items={pipelines?.slice(0, 5) || []} type="pipeline" color="#06b6d4" />
        <RecentActivity title="Recent Failures" items={failures?.slice(0, 5) || []} type="failure" color="#f97316" />
      </div>
    </div>
  )
}

function StatCard({ title, value, icon, color, bgGradient }: any) {
  return (
    <div style={{
      background: bgGradient,
      padding: '2rem',
      borderRadius: '1rem',
      border: `1px solid ${color}40`,
      boxShadow: `0 8px 32px ${color}20`,
      transition: 'all 0.3s',
      cursor: 'pointer',
      position: 'relative',
      overflow: 'hidden'
    }}
    onMouseEnter={(e) => {
      e.currentTarget.style.transform = 'translateY(-6px) scale(1.02)'
      e.currentTarget.style.boxShadow = `0 16px 48px ${color}40`
    }}
    onMouseLeave={(e) => {
      e.currentTarget.style.transform = 'translateY(0) scale(1)'
      e.currentTarget.style.boxShadow = `0 8px 32px ${color}20`
    }}>
      <div style={{
        position: 'absolute',
        top: '-50%',
        right: '-20%',
        width: '200px',
        height: '200px',
        background: `radial-gradient(circle, ${color}30 0%, transparent 70%)`,
        pointerEvents: 'none'
      }} />
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', position: 'relative' }}>
        <div>
          <p style={{ color: '#cbd5e1', fontSize: '0.875rem', marginBottom: '0.75rem', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {title}
          </p>
          <p style={{ fontSize: '2.75rem', fontWeight: 'bold', color, textShadow: `0 0 24px ${color}40` }}>
            {value}
          </p>
        </div>
        <div style={{ 
          color, 
          background: `${color}30`,
          padding: '1rem',
          borderRadius: '0.75rem',
          border: `1px solid ${color}40`,
          boxShadow: `0 0 24px ${color}30`
        }}>
          {icon}
        </div>
      </div>
    </div>
  )
}

function RecentActivity({ title, items, type, color }: any) {
  const getStatusColor = (item: any) => {
    if (type === 'pipeline') {
      return item.status === 'completed' ? '#84cc16' : item.status === 'failed' ? '#f87171' : '#fbbf24'
    }
    return '#f97316'
  }
  
  return (
    <div style={{
      background: 'linear-gradient(135deg, #1e293b 0%, #1a1f35 100%)',
      padding: '2rem',
      borderRadius: '1rem',
      border: `1px solid ${color}40`,
      boxShadow: `0 8px 32px ${color}15`
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <div style={{
          width: '4px',
          height: '24px',
          background: color,
          borderRadius: '2px',
          boxShadow: `0 0 12px ${color}`
        }} />
        <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#e0e7ff' }}>
          {title}
        </h2>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {items.length === 0 ? (
          <div style={{ 
            color: '#64748b', 
            textAlign: 'center', 
            padding: '3rem',
            background: '#0f172a',
            borderRadius: '0.75rem',
            border: '1px solid #334155'
          }}>
            <AlertCircle size={32} style={{ margin: '0 auto 0.75rem', opacity: 0.5 }} />
            <p style={{ fontSize: '0.95rem' }}>No data available</p>
          </div>
        ) : (
          items.map((item: any, idx: number) => (
            <div
              key={idx}
              style={{
                padding: '1.25rem',
                background: '#0f172a',
                borderRadius: '0.75rem',
                fontSize: '0.875rem',
                border: '1px solid #1e293b',
                transition: 'all 0.2s',
                cursor: 'pointer'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#1e293b'
                e.currentTarget.style.borderColor = `${color}40`
                e.currentTarget.style.transform = 'translateX(4px)'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = '#0f172a'
                e.currentTarget.style.borderColor = '#1e293b'
                e.currentTarget.style.transform = 'translateX(0)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                <div style={{
                  width: '10px',
                  height: '10px',
                  borderRadius: '50%',
                  background: getStatusColor(item),
                  boxShadow: `0 0 12px ${getStatusColor(item)}`,
                  flexShrink: 0
                }} />
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: '600', marginBottom: '0.375rem', color: '#e2e8f0', fontSize: '0.95rem' }}>
                    {item.repository || item.error_message?.substring(0, 50) || 'Unknown'}
                  </div>
                  <div style={{ color: '#94a3b8', fontSize: '0.8rem' }}>
                    {item.branch || item.error_category || 'N/A'}
                  </div>
                </div>
                {item.created_at && (
                  <div style={{ 
                    color: '#64748b', 
                    fontSize: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.375rem',
                    flexShrink: 0
                  }}>
                    <Clock size={12} />
                    {new Date(item.created_at).toLocaleDateString()}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
