import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../style/Home.scss'

function Home() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)

  const handleCreateOrder = async () => {
    setLoading(true)
    try {
      const response = await fetch('http://localhost:8000/api/orders/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      if (!response.ok) {
        throw new Error('Erreur lors de la création de la commande')
      }
      
      const order = await response.json()
      console.log('Commande créée:', order)
      
      // Rediriger vers le formulaire avec l'ID de la commande
      navigate(`/feelback-form?order_id=${order.id}`)
      
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de la création de la commande')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className='home'>
      <button className='secondary' onClick={() => navigate('/dashboard')}>
        CONSULTER LE TABLEAU DE BORD
      </button>
      <h1>Bienvenue sur l'application FeelBack</h1>
      <p>Cette application vous permet d'évaluer la livraison de votre commande</p>
      <button 
        className='primary' 
        onClick={handleCreateOrder}
        disabled={loading}
      >
        {loading ? 'CRÉATION EN COURS...' : 'CRÉER UNE COMMANDE FICTIVE ET RÉPONDRE AU QUESTIONNAIRE DE SATISFACTION'}
      </button>
    </main>
  )
}

export default Home