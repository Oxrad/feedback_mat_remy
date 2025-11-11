import React from 'react'
import '../style/Header.scss'

function Header() {
  return (
    <header>
        <div className='header-content'>
            <img src="/logo.png" alt="FeelBack Logo" className="logo" />
            <h2>FeelBack</h2>
            <h3>Le questionnaire de satisfaction</h3>
        </div>
    </header>
  )
}

export default Header
