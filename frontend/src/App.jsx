
import { useEffect, useState } from 'react'
import {
  ShieldCheck, Activity, AlertTriangle, Truck,
  Users, Video, RefreshCw, Clock, ArrowUpRight,
  CheckCircle2, Zap, Route, PauseCircle
} from 'lucide-react'
import './App.css'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

function App() {
  const [summary, setSummary] = useState(null)
  const [records, setRecords] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadDashboard = async () => {
    try {
      setError('')
      const [summaryResponse, recordsResponse] = await Promise.all([
        fetch(`${API}/dashboard/summary`),
        fetch(`${API}/dashboard/interventions`)
      ])

      if (!summaryResponse.ok || !recordsResponse.ok) {
        throw new Error('Backend API request failed')
      }

      const summaryData = await summaryResponse.json()
      const recordsData = await recordsResponse.json()

      setSummary(summaryData)
      setRecords(recordsData.records || [])
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const latestRecord = records.length
    ? records[records.length - 1]
    : null

  const bestIntervention = latestRecord?.best_scenario

  const riskCounts = summary?.risk_distribution_in_records || {}

  const formatName = (name = '') =>
    name.replaceAll('_', ' ').replace(/\b\w/g, c => c.toUpperCase())

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><ShieldCheck size={25} /></div>
          <div>
            <h2>SafeSphere</h2>
            <span>INDUSTRIAL INTELLIGENCE</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <div className="nav-item active"><Activity size={18} /> Overview</div>
        <div className="nav-item"><Video size={18} /> Video Monitoring</div>
        <div className="nav-item"><AlertTriangle size={18} /> Risk Analysis</div>
        <div className="nav-item"><Zap size={18} /> Interventions</div>

        <div className="sidebar-bottom">
          <div className="system-status">
            <span className="status-dot"></span>
            <div>
              <strong>Backend Connected</strong>
              <small>API services responding</small>
            </div>
          </div>
          <p>SAFESPHERE PROTOTYPE · v1.0</p>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">WORKSPACE / OVERVIEW</span>
            <h1>Safety Intelligence</h1>
            <p>Predictive monitoring and counterfactual safety analysis</p>
          </div>
          <button className="refresh-btn" onClick={loadDashboard}>
            <RefreshCw size={16} /> Refresh Data
          </button>
        </header>

        {error && <div className="error-banner">{error}</div>}

        {loading ? (
          <div className="loading">Loading SafeSphere analytics...</div>
        ) : (
          <>
            <section className="welcome-strip">
              <div>
                <span className="eyebrow">INDUSTRIAL SAFETY SYSTEM</span>
                <h2>Predict risks. Compare interventions. Improve safety.</h2>
                <p>Analysis based on the processed warehouse video and saved intervention results.</p>
              </div>
              <div className="welcome-icon"><ShieldCheck size={48} /></div>
            </section>

            <section className="stats-grid">
              <StatCard
                icon={<Activity />}
                label="Intervention Observations"
                value={summary?.intervention_triggered_observations ?? 0}
                note="Saved HIGH / MEDIUM observations"
                color="blue"
              />
              <StatCard
                icon={<AlertTriangle />}
                label="HIGH Risk Records"
                value={riskCounts.HIGH ?? 0}
                note="Within intervention records"
                color="red"
              />
              <StatCard
                icon={<Users />}
                label="MEDIUM Risk Records"
                value={riskCounts.MEDIUM ?? 0}
                note="Within intervention records"
                color="orange"
              />
              <StatCard
                icon={<Truck />}
                label="Scenarios Compared"
                value={records.length * 4}
                note="4 scenarios per observation"
                color="purple"
              />
            </section>

            <section className="content-grid">
              <div className="panel video-panel">
                <div className="panel-heading">
                  <div>
                    <h3><Video size={18} /> Warehouse Risk Analysis</h3>
                    <p>Processed video · Detection and tracking overlay</p>
                  </div>
                  <span className="tag">PROCESSED VIDEO</span>
                </div>
                <video
                  className="risk-video"
                  controls
                  preload="metadata"
                  src={`${API}/dashboard/video`}
                />
                <div className="video-caption">
                  <span><span className="legend green"></span> Detected workers</span>
                  <span><span className="legend orange"></span> Other tracked objects</span>
                </div>
              </div>

              <div className="panel intervention-panel">
                <div className="panel-heading">
                  <div>
                    <h3><Zap size={18} /> Counterfactual Engine</h3>
                    <p>Latest saved comparison</p>
                  </div>
                  <span className="tag purple-tag">CSIE</span>
                </div>

                {latestRecord ? (
                  <>
                    <div className="record-info">
                      <span>Frame {latestRecord.frame}</span>
                      <span>Worker #{latestRecord.worker_id} · Forklift #{latestRecord.forklift_id}</span>
                    </div>
                    <div className="scenario-list">
                      {latestRecord.scenarios.map((scenario, index) => (
                        <div className="scenario" key={index}>
                          <div className="scenario-name">
                            {scenario.intervention === 'baseline' && <Activity size={16} />}
                            {scenario.intervention === 'reduce_forklift_speed' && <Truck size={16} />}
                            {scenario.intervention === 'worker_pause' && <PauseCircle size={16} />}
                            {scenario.intervention === 'alternate_forklift_route' && <Route size={16} />}
                            {formatName(scenario.intervention)}
                          </div>
                          <div className="scenario-result">
                            <strong>{scenario.predicted_closest_distance} px</strong>
                            <span className={`risk-pill ${scenario.predicted_risk.toLowerCase()}`}>
                              {scenario.predicted_risk}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                    <div className="best-result">
                      <CheckCircle2 size={19} />
                      <div>
                        <strong>Best predicted scenario</strong>
                        <p>{formatName(bestIntervention?.intervention || 'Not available')}</p>
                        <small>Closest distance: {bestIntervention?.predicted_closest_distance ?? '—'} px</small>
                      </div>
                    </div>
                  </>
                ) : (
                  <p>No intervention records available.</p>
                )}
              </div>
            </section>

            <section className="panel records-panel">
              <div className="panel-heading">
                <div>
                  <h3><Clock size={18} /> Intervention History</h3>
                  <p>Saved observations from warehouse video analysis</p>
                </div>
                <span className="tag">{records.length} RECORDS</span>
              </div>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      <th>FRAME</th>
                      <th>WORKER ID</th>
                      <th>FORKLIFT ID</th>
                      <th>ORIGINAL RISK</th>
                      <th>BEST SCENARIO</th>
                      <th>PREDICTED DISTANCE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {records.slice(-10).reverse().map((record, index) => (
                      <tr key={`${record.frame}-${index}`}>
                        <td>#{record.frame}</td>
                        <td>Worker {record.worker_id}</td>
                        <td>Forklift {record.forklift_id}</td>
                        <td>
                          <span className={`risk-pill ${record.original_risk.toLowerCase()}`}>
                            {record.original_risk}
                          </span>
                        </td>
                        <td>{formatName(record.best_scenario?.intervention)}</td>
                        <td>{record.best_scenario?.predicted_closest_distance} px</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>

            <footer>
              <span>SafeSphere · Predictive and Counterfactual Industrial Safety Intelligence</span>
              <span><span className="status-dot"></span> Connected to local backend</span>
            </footer>
          </>
        )}
      </main>
    </div>
  )
}

function StatCard({ icon, label, value, note, color }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${color}`}>{icon}</div>
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-note">{note}</div>
    </div>
  )
}

export default App
