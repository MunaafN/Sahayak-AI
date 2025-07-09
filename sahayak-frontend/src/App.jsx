import { useState, useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from './config/firebase'
import { useTranslation } from 'react-i18next'

// Components
import Sidebar from './components/layout/Sidebar'
import Header from './components/layout/Header'
import LoadingSpinner from './components/common/LoadingSpinner'

// Pages
import Home from './pages/Home'
import Login from './pages/auth/Login'
import Dashboard from './pages/Dashboard'
import ContentGenerator from './pages/modules/ContentGenerator'
import WorksheetGenerator from './pages/modules/WorksheetGenerator'
import KnowledgeBase from './pages/modules/KnowledgeBase'
import VisualAids from './pages/modules/VisualAids'
import ReadingAssessment from './pages/modules/ReadingAssessment'
import LessonPlanner from './pages/modules/LessonPlanner'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const { i18n } = useTranslation()

  useEffect(() => {
    // Simple Firebase authentication listener
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        
        {/* Protected routes */}
        {user ? (
          <Route path="/*" element={
            <div className="flex">
              {/* Sidebar */}
              <Sidebar />
              
              {/* Main Content */}
              <div className="flex-1 flex flex-col">
                <Header user={user} />
                
                <main className="flex-1 p-6 bg-gradient-to-br from-slate-900 to-slate-800">
                  <Routes>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/content" element={<ContentGenerator />} />
                    <Route path="/worksheets" element={<WorksheetGenerator />} />
                    <Route path="/knowledge" element={<KnowledgeBase />} />
                    <Route path="/visuals" element={<VisualAids />} />
                    <Route path="/assessment" element={<ReadingAssessment />} />
                    <Route path="/planner" element={<LessonPlanner />} />
                    <Route path="*" element={<Navigate to="/dashboard" replace />} />
                  </Routes>
                </main>
              </div>
            </div>
          } />
        ) : (
          <Route path="/*" element={<Navigate to="/login" replace />} />
        )}
      </Routes>
    </div>
  )
}

export default App
