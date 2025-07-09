import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { updateDashboardStats, decreaseDashboardStats, ActivityTypes } from '../../utils/dashboard'
import { getLanguageOptions } from '../../config/languages'
import { 
  CalendarIcon, 
  ArrowDownTrayIcon, 
  BookOpenIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'
import api from '../../config/api'

const LessonPlanner = () => {
  const { t } = useTranslation()
  const [formData, setFormData] = useState({
    topic: '',
    subject: 'science',
    gradeLevel: '3',
    language: 'en'
  })
  const [loading, setLoading] = useState(false)
  const [lessonPlan, setLessonPlan] = useState('')
  const [error, setError] = useState('')
  const [pastPlans, setPastPlans] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_lesson_plans')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastPlans, setShowPastPlans] = useState(true)

  const subjects = [
    { value: 'science', label: 'Science / विज्ञान' },
    { value: 'math', label: 'Mathematics / गणित' },
    { value: 'language', label: 'Language Arts / भाषा' },
    { value: 'social', label: 'Social Studies / सामाजिक अध्ययन' }
  ]

  const languages = getLanguageOptions()

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const generatePlan = async (e) => {
    e.preventDefault()
    if (!formData.topic.trim()) return

    setLoading(true)
    setError('')

    try {
      const response = await api.post('/lessons/generate', {
        topic: formData.topic.trim(),
        subject: formData.subject,
        grade_level: formData.gradeLevel,
        language: formData.language
      })

      if (response.data && response.data.lesson_plan) {
        const plan = response.data.lesson_plan
        setLessonPlan(plan)
        
        // Save to past plans
        const newPlan = {
          id: Date.now(),
          topic: formData.topic,
          subject: formData.subject,
          gradeLevel: formData.gradeLevel,
          language: formData.language,
          content: plan,
          timestamp: new Date().toISOString()
        }
        
        const updatedPastPlans = [newPlan, ...pastPlans].slice(0, 10) // Keep only last 10
        setPastPlans(updatedPastPlans)
        localStorage.setItem('sahayak_past_lesson_plans', JSON.stringify(updatedPastPlans))
        
        // Notify dashboard to refresh stats
        window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
        
        // Auto-expand past plans to show the new item
        setShowPastPlans(true)
        
        // Update dashboard stats
        const description = `Created lesson plan for "${formData.topic}" (${formData.subject}) in ${formData.language.toUpperCase()} for Grade ${formData.gradeLevel}`
        updateDashboardStats(ActivityTypes.LESSON_PLANNED, description)
        
      } else {
        setError('No lesson plan received from server')
      }
    } catch (error) {
      console.error('Error generating lesson plan:', error)
      setError('Failed to generate lesson plan. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const deletePastPlan = (id) => {
    const itemToDelete = pastPlans.find(item => item.id === id)
    const updatedPastPlans = pastPlans.filter(item => item.id !== id)
    setPastPlans(updatedPastPlans)
    localStorage.setItem('sahayak_past_lesson_plans', JSON.stringify(updatedPastPlans))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    if (itemToDelete) {
      decreaseDashboardStats(ActivityTypes.LESSON_PLANNED, `Deleted lesson plan: ${itemToDelete.topic}`)
    }
  }

  const loadPastPlan = (plan) => {
    setLessonPlan(plan.content)
    setFormData({
      topic: plan.topic,
      subject: plan.subject,
      gradeLevel: plan.gradeLevel,
      language: plan.language
    })
  }

  const downloadPlan = () => {
    if (lessonPlan) {
      const element = document.createElement('a')
      const file = new Blob([lessonPlan], { type: 'text/plain' })
      element.href = URL.createObjectURL(file)
      element.download = `lesson_plan_${formData.topic}_${formData.language}_grade${formData.gradeLevel}.txt`
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-200 mb-2">
          {t('modules.planner.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('modules.planner.description')}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Input Form */}
        <div className="xl:col-span-2">
                  <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
              <CalendarIcon className="w-6 h-6 mr-2 text-blue-400" />
              Plan Details
            </h2>

            <form onSubmit={generatePlan} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Topic / Theme
                </label>
                <input
                  type="text"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  placeholder="e.g., Plants, Water Cycle, Numbers, Festivals"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Subject
                </label>
                <select
                  name="subject"
                  value={formData.subject}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {subjects.map(sub => (
                    <option key={sub.value} value={sub.value}>
                      {sub.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Grade Level
                </label>
                <select
                  name="gradeLevel"
                  value={formData.gradeLevel}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  <option value="1">Grade 1</option>
                  <option value="2">Grade 2</option>
                  <option value="3">Grade 3</option>
                  <option value="4">Grade 4</option>
                  <option value="5">Grade 5</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Language
                </label>
                <select
                  name="language"
                  value={formData.language}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {languages.map(lang => (
                    <option key={lang.value} value={lang.value}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                disabled={loading || !formData.topic}
                className="btn-primary w-full"
              >
                {loading ? 'Generating Plan...' : 'Generate Lesson Plan'}
              </button>
            </form>
          </div>

          {/* Generated Lesson Plan */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300 mt-6">
            <h2 className="text-xl font-semibold text-slate-200 mb-6">
              Generated Lesson Plan
            </h2>

            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
                <span className="ml-2 text-slate-300">Creating lesson plan...</span>
              </div>
            )}

            {lessonPlan && !loading && (
              <div>
                <div className="bg-slate-700 p-4 rounded-lg mb-4 max-h-96 overflow-y-auto border border-slate-600">
                  <pre className="whitespace-pre-wrap text-sm text-slate-200 font-serif leading-relaxed">
                    {lessonPlan}
                  </pre>
                </div>

                <div className="flex space-x-3">
                  <button
                    onClick={downloadPlan}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
                    Download Plan
                  </button>
                </div>
              </div>
            )}

            {!lessonPlan && !loading && !error && (
              <div className="text-center text-slate-400 h-40 flex items-center justify-center">
                <div>
                  <BookOpenIcon className="w-16 h-16 mx-auto text-slate-500 mb-4" />
                  <p>Enter a topic to generate a lesson plan</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Past Lesson Plans Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Plans
              </h2>
              <button
                onClick={() => setShowPastPlans(!showPastPlans)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastPlans ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastPlans && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastPlans.length > 0 ? (
                  pastPlans.map((plan) => (
                    <div
                      key={plan.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastPlan(plan)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            {plan.topic}
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            {plan.subject} • Grade {plan.gradeLevel} • {plan.language.toUpperCase()}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(plan.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastPlan(plan.id)
                          }}
                          className="p-1 rounded-md hover:bg-red-900 text-red-400 hover:text-red-300 transition-colors duration-200"
                        >
                          <TrashIcon className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8">
                    <p className="text-slate-400 text-sm">No past plans</p>
                    <p className="text-xs text-slate-500 mt-1">Generate plans to see them here</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default LessonPlanner 