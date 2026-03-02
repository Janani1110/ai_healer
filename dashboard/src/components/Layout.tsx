import { Outlet, Link, useLocation } from 'react-router-dom'
import { Activity, GitBranch, AlertCircle, Wrench, Zap } from 'lucide-react'

export default function Layout() {
  const location = useLocation()
  
  const isActive = (path: string) => location.pathname === path
  
  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#0a0a0f' }}>
      <nav style={{
        width: '280px',
        background: 'linear-gradient(180deg, #1a0b2e 0%, #160b28 100%)',
        padding: '2rem 1.5rem',
        borderRight: '2px solid #7c3aed40',
        boxShadow: '4px 0 24px rgba(124, 58, 237, 0.15)'
      }}>
        <div style={{
          marginBottom: '3rem',
          padding: '1rem',
          background: 'linear-gradient(135deg, #7c3aed 0%, #ec4899 100%)',
          borderRadius: '1rem',
          textAlign: 'center',
          boxShadow: '0 8px 32px rgba(236, 72, 153, 0.3)'
        }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>⚡</div>
          <h1 style={{ 
            fontSize: '1.5rem', 
            fontWeight: 'bold',
            background: 'linear-gradient(135deg, #fff 0%, #e0e7ff 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text'
          }}>
            AI Healer
          </h1>
          <p style={{ fontSize: '0.75rem', color: '#e0e7ff', marginTop: '0.25rem' }}>
            Self-Healing CI/CD
          </p>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <NavLink to="/" icon={<Activity size={20} />} active={isActive('/')} color="#ec4899">
            Dashboard
          </NavLink>
          <NavLink to="/pipelines" icon={<GitBranch size={20} />} active={isActive('/pipelines')} color="#06b6d4">
            Pipelines
          </NavLink>
          <NavLink to="/failures" icon={<AlertCircle size={20} />} active={isActive('/failures')} color="#f97316">
            Failures
          </NavLink>
          <NavLink to="/fixes" icon={<Wrench size={20} />} active={isActive('/fixes')} color="#84cc16">
            Fixes
          </NavLink>
        </div>
        
        <div style={{
          marginTop: '3rem',
          padding: '1rem',
          background: '#7c3aed20',
          borderRadius: '0.75rem',
          border: '1px solid #7c3aed40'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <Zap size={16} color="#fbbf24" />
            <span style={{ fontSize: '0.875rem', fontWeight: '600', color: '#e0e7ff' }}>
              AI Status
            </span>
          </div>
          <div style={{ fontSize: '0.75rem', color: '#a78bfa' }}>
            Groq AI Active
          </div>
          <div style={{ 
            marginTop: '0.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <div style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              background: '#84cc16',
              boxShadow: '0 0 12px #84cc16',
              animation: 'pulse 2s infinite'
            }} />
            <span style={{ fontSize: '0.75rem', color: '#84cc16' }}>Online</span>
          </div>
        </div>
      </nav>
      
      <main style={{ 
        flex: 1, 
        padding: '2.5rem', 
        overflow: 'auto',
        background: 'linear-gradient(180deg, #0a0a0f 0%, #1a0b2e 100%)'
      }}>
        <Outlet />
      </main>
    </div>
  )
}

function NavLink({ to, icon, children, active, color }: any) {
  return (
    <Link
      to={to}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        padding: '1rem 1.25rem',
        borderRadius: '0.75rem',
        textDecoration: 'none',
        color: active ? color : '#94a3b8',
        background: active ? `${color}20` : 'transparent',
        border: active ? `1px solid ${color}40` : '1px solid transparent',
        fontWeight: active ? '600' : '500',
        transition: 'all 0.2s',
        position: 'relative',
        overflow: 'hidden'
      }}
      onMouseEnter={(e) => {
        if (!active) {
          e.currentTarget.style.background = `${color}10`
          e.currentTarget.style.color = color
        }
      }}
      onMouseLeave={(e) => {
        if (!active) {
          e.currentTarget.style.background = 'transparent'
          e.currentTarget.style.color = '#94a3b8'
        }
      }}
    >
      {active && (
        <div style={{
          position: 'absolute',
          left: 0,
          top: 0,
          bottom: 0,
          width: '4px',
          background: color,
          boxShadow: `0 0 12px ${color}`
        }} />
      )}
      {icon}
      <span>{children}</span>
    </Link>
  )
}
