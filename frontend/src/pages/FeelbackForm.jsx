import React, { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import '../style/FeelbackForm.scss'

function FeelbackForm() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const orderId = searchParams.get('order_id')

  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    // Récupérer les questions depuis l'API
    fetch('http://localhost:8000/api/questions')
      .then(res => res.json())
      .then(data => {
        setQuestions(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Erreur:', error)
        setLoading(false)
      })
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!orderId) {
      alert('Aucune commande associée')
      return
    }

    setSubmitting(true)

    const formData = new FormData(e.target)
    const grades = []

    // Construire le tableau de grades
    for (let [key, value] of formData.entries()) {
      const questionId = parseInt(key.split('-')[1], 10)
      grades.push({ 
        question_id: questionId, 
        grade: parseInt(value, 10) 
      })
    }
    
    console.log("Données à envoyer :", { grades })

    try {
      const response = await fetch(`http://localhost:8000/api/orders/${orderId}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ grades })
      })

      if (!response.ok) {
        throw new Error('Erreur lors de l\'envoi du feedback')
      }

      const result = await response.json()
      console.log('Réponse serveur:', result)
      
      alert('Merci pour votre feedback ! ✅')
      navigate('/dashboard')
      
    } catch (error) {
      console.error('Erreur:', error)
      alert('Erreur lors de l\'envoi du feedback')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className='feelback-form'>
      <button className='secondary' onClick={() => navigate('/')}>
        REVENIR SUR LA PAGE D'ACCUEIL
      </button>
      <h1>Donner votre avis</h1>
      
      {loading ? (
        <p>Chargement des questions...</p>
      ) : (
        <form onSubmit={handleSubmit}>
          {questions.length > 0 ? (
            questions.map((question) => (
              <div key={question.id} className="question-block">
                <label htmlFor={`question-${question.id}`}>{question.title}</label>
                <div className="radio-group">
                  {[...Array(question.maximum_grade)].map((_, i) => {
                    const value = i + 1;
                    return (
                      <label key={value}>
                        <input
                          type="radio"
                          name={`question-${question.id}`}
                          required
                          value={value}
                        />
                        {value}
                      </label>
                    );
                  })}
                </div>
              </div>
            ))
          ) : (
            <p>Aucune question disponible.</p>
          )}
          
          <button 
            type="submit" 
            className='primary'
            disabled={submitting}
          >
            {submitting ? 'ENVOI EN COURS...' : 'ENVOYER'}
          </button>
        </form>
      )}
    </main>
  )
}

export default FeelbackForm