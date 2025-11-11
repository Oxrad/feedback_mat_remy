import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import '../style/Dashboard.scss'

function Dashboard() {
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Récupérer les statistiques depuis l'API
    fetch('http://localhost:8000/api/dashboard-stats')
      .then(res => res.json())
      .then(stats => {
        console.log('Statistiques reçues:', stats)
        setData(stats)
        setLoading(false)
      })
      .catch(error => {
        console.error('Erreur:', error)
        setLoading(false)
      })
  }, [])

  return (
    <main className='dashboard'>
      <button className='secondary' onClick={() => navigate('/')}>
        REVENIR SUR LA PAGE D'ACCUEIL
      </button>
      <h1>Tableau de bord</h1>
      <p>Cette page regroupe des statistiques moyennes sur l'ensemble des réponses données</p>

      {loading ? (
        <p id='loading'>Chargement des statistiques...</p>
      ) : data ? (
        <div className='stats-container'>
          <div className='stat-card'>
            <p className='stat-value'>{data.total_feedbacks}</p>
            <h2>Réponses</h2>
          </div>
          {data.average_grades && data.average_grades.map((item) => (
            <div className='stat-card' key={item.question_id}>
              <p className='stat-value'>{item.average_grade} / {item.maximum_grade}</p>
              <h2>{item.title}</h2>
            </div>
          ))}
        </div>
      ) : (
        <p>Erreur lors du chargement des statistiques</p>
      )}
    </main>
  )
}

export default Dashboard