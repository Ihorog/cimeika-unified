'use client'
import { useEffect, useState, useRef } from 'react'

const API = 'https://api.cimeika.com.ua'

const PHASES: Record<string, string> = {
  'Нема': '#2A2E40', 'До': '#3A3F5A', 'оСі': '#4A6FD4',
  'Є': '#C8A84B', 'оЧЄВиднЄ': '#8A4BD4', 'Було': '#4CAF78',
  'Буде': '#D44A4A', '∞': '#C8A84B',
}

interface Narrative {
  number: number
  title: string
  subtitle: string
  emoji: string
  phase: string
  dualism_axis: string
  fig_ref: string
  tags: string[]
}

interface GraphData {
  nodes: { node_key: string; label: string; depth: number; emoji: string; color: string }[]
  edges: { source_key: string; target_key: string; weight: number }[]
}

export default function KazkarPage() {
  const [narratives, setNarratives] = useState<Narrative[]>([])
  const [graph, setGraph] = useState<GraphData | null>(null)
  const [active, setActive] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    Promise.all([
      fetch(`${API}/legenda/narratives`).then(r => r.json()),
      fetch(`${API}/legenda/graph`).then(r => r.json()),
    ]).then(([n, g]) => {
      if (n.ok) setNarratives(n.data)
      if (g.ok) setGraph(g.data)
      setLoading(false)
    })
  }, [])

  // Canvas граф
  useEffect(() => {
    if (!graph || !canvasRef.current) return
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')!
    const W = canvas.width = canvas.offsetWidth
    const H = canvas.height = 340

    const nodes = graph.nodes
    const edges = graph.edges
    const N = nodes.length

    // Позиції — концентричні кола за depth
    const positions: Record<string, {x: number; y: number}> = {}
    const cx = W / 2, cy = H / 2

    const depthNodes: Record<number, typeof nodes> = {}
    nodes.forEach(n => {
      if (!depthNodes[n.depth]) depthNodes[n.depth] = []
      depthNodes[n.depth].push(n)
    })

    Object.entries(depthNodes).forEach(([depth, ns]) => {
      const r = Number(depth) === 1 ? 0 : Number(depth) * 72
      ns.forEach((n, i) => {
        const angle = (i / ns.length) * Math.PI * 2 - Math.PI / 2
        positions[n.node_key] = {
          x: cx + Math.cos(angle) * r,
          y: cy + Math.sin(angle) * r,
        }
      })
    })

    // Малюємо
    ctx.clearRect(0, 0, W, H)

    // Edges
    edges.forEach(e => {
      const s = positions[e.source_key]
      const t = positions[e.target_key]
      if (!s || !t) return
      ctx.beginPath()
      ctx.moveTo(s.x, s.y)
      ctx.lineTo(t.x, t.y)
      ctx.strokeStyle = `rgba(200,168,75,${e.weight * 0.3})`
      ctx.lineWidth = e.weight * 1.5
      ctx.stroke()
    })

    // Nodes
    nodes.forEach(n => {
      const p = positions[n.node_key]
      if (!p) return
      const r = n.depth === 1 ? 18 : n.depth === 2 ? 14 : n.depth === 3 ? 11 : 9
      ctx.beginPath()
      ctx.arc(p.x, p.y, r, 0, Math.PI * 2)
      ctx.fillStyle = n.color || '#2A2E40'
      ctx.fill()
      ctx.strokeStyle = '#C8A84B'
      ctx.lineWidth = n.depth <= 2 ? 2 : 1
      ctx.stroke()
      ctx.fillStyle = '#DDE0EA'
      ctx.font = `${r + 2}px serif`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(n.emoji || '●', p.x, p.y)
    })

  }, [graph])

  if (loading) return (
    <div style={{minHeight:'100dvh',display:'flex',alignItems:'center',justifyContent:'center',background:'#080910',color:'#C8A84B',fontFamily:'Cormorant Garamond,serif',fontSize:22}}>
      Казкар завантажується...
    </div>
  )

  const activeNarrative = narratives.find(n => n.number === active)

  return (
    <main style={{minHeight:'100dvh',background:'#080910',color:'#DDE0EA',fontFamily:'Onest,sans-serif'}}>
      {/* Header */}
      <header style={{padding:'32px 24px 0',textAlign:'center',borderBottom:'1px solid #1F2333',paddingBottom:24}}>
        <div style={{fontSize:13,color:'#5A6077',letterSpacing:4,textTransform:'uppercase',marginBottom:8}}>Cimeika</div>
        <h1 style={{fontFamily:'Cormorant Garamond,serif',fontSize:36,color:'#C8A84B',margin:0}}>📖 Казкар</h1>
        <p style={{color:'#5A6077',fontSize:14,marginTop:8}}>Легенда Сі · 15 наративів · Семантичний граф</p>
      </header>

      {/* Граф */}
      <section style={{padding:'24px 16px',borderBottom:'1px solid #1F2333'}}>
        <div style={{fontSize:11,color:'#5A6077',letterSpacing:3,textTransform:'uppercase',marginBottom:12}}>Семантичний граф</div>
        <canvas ref={canvasRef} style={{width:'100%',height:340,background:'#0F1018',borderRadius:12,border:'1px solid #1F2333',display:'block'}} />
      </section>

      {/* Фази */}
      <section style={{padding:'16px',display:'flex',gap:8,flexWrap:'wrap',borderBottom:'1px solid #1F2333'}}>
        {Object.entries(PHASES).map(([phase, color]) => (
          <div key={phase} style={{
            padding:'4px 12px',borderRadius:20,fontSize:12,
            background: color + '33', border: `1px solid ${color}55`, color:'#DDE0EA'
          }}>{phase}</div>
        ))}
      </section>

      {/* Наративи */}
      <section style={{padding:'16px'}}>
        <div style={{fontSize:11,color:'#5A6077',letterSpacing:3,textTransform:'uppercase',marginBottom:16}}>
          15 канонічних наративів
        </div>
        <div style={{display:'grid',gap:8}}>
          {narratives.map(n => (
            <button key={n.number} onClick={() => setActive(active === n.number ? null : n.number)}
              style={{
                background: active === n.number ? '#161922' : '#0F1018',
                border: `1px solid ${active === n.number ? (PHASES[n.phase]||'#C8A84B') : '#1F2333'}`,
                borderRadius:10,padding:'12px 16px',cursor:'pointer',
                textAlign:'left',color:'#DDE0EA',width:'100%',transition:'all .2s'
              }}>
              <div style={{display:'flex',alignItems:'center',gap:12}}>
                <span style={{fontSize:22}}>{n.emoji}</span>
                <div style={{flex:1}}>
                  <div style={{display:'flex',alignItems:'center',gap:8}}>
                    <span style={{color:'#5A6077',fontSize:12}}>{n.number}.</span>
                    <span style={{fontFamily:'Cormorant Garamond,serif',fontSize:17,color:'#DDE0EA'}}>{n.title}</span>
                    <span style={{
                      marginLeft:'auto',fontSize:10,padding:'2px 8px',borderRadius:10,
                      background:(PHASES[n.phase]||'#2A2E40')+'44',
                      color:'#DDE0EA',border:`1px solid ${PHASES[n.phase]||'#2A2E40'}66`
                    }}>{n.phase}</span>
                  </div>
                  <div style={{color:'#5A6077',fontSize:12,marginTop:2}}>{n.dualism_axis}</div>
                </div>
              </div>
              {active === n.number && (
                <div style={{marginTop:12,paddingTop:12,borderTop:'1px solid #1F2333'}}>
                  {n.subtitle && <div style={{color:'#C8A84B',fontSize:13,marginBottom:8}}>{n.subtitle}</div>}
                  <div style={{display:'flex',gap:6,flexWrap:'wrap'}}>
                    {(n.tags||[]).map(t => (
                      <span key={t} style={{fontSize:11,padding:'2px 8px',background:'#1F2333',borderRadius:10,color:'#5A6077'}}>{t}</span>
                    ))}
                  </div>
                  <div style={{marginTop:8,color:'#8A6F2E',fontSize:12}}>{n.fig_ref}</div>
                </div>
              )}
            </button>
          ))}
        </div>
      </section>
    </main>
  )
}
