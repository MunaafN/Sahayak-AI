import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { getLanguageOptions } from '../../config/languages'
import { 
  QuestionMarkCircleIcon, 
  MicrophoneIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'
import { updateDashboardStats, decreaseDashboardStats, ActivityTypes } from '../../utils/dashboard'
import api from '../../config/api'

const KnowledgeBase = () => {
  const { t } = useTranslation()
  const [question, setQuestion] = useState('')
  const [language, setLanguage] = useState('en')
  const [gradeLevel, setGradeLevel] = useState('3')
  const [length, setLength] = useState('medium')
  const [loading, setLoading] = useState(false)
  const [answer, setAnswer] = useState('')
  const [error, setError] = useState('')
  const [isRecording, setIsRecording] = useState(false)

  const [pastQuestions, setPastQuestions] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_questions')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastQuestions, setShowPastQuestions] = useState(true)

  const languages = getLanguageOptions()

  const gradeOptions = [
    { value: '1', label: 'Grade 1-2 (Very Simple)' },
    { value: '3', label: 'Grade 3-4 (Simple)' },
    { value: '5', label: 'Grade 5+ (Detailed)' }
  ]

  const lengthOptions = [
    { value: 'short', label: 'Short (100-150 words)' },
    { value: 'medium', label: 'Medium (200-300 words)' },
    { value: 'long', label: 'Long (400-500 words)' }
  ]

  const commonQuestions = [
    'Why is the sky blue?',
    'Where does rain come from?',
    'Why do plants need sunlight?',
    'How do birds fly?',
    'Why do we need to eat food?',
    'What makes the moon shine?',
    'Why do seasons change?',
    'How do fish breathe underwater?'
  ]

  const askQuestion = async (e) => {
    e.preventDefault()
    if (!question.trim()) return

    setLoading(true)
    setError('')
    setAnswer('')

    try {
      const response = await api.post('/knowledge/ask', {
        question: question.trim(),
        language,
        gradeLevel: gradeLevel,
        length: length
      })
      
      if (response.data && response.data.answer) {
        const answerText = response.data.answer
        setAnswer(answerText)
        
        // Save to past questions
        const newQuestion = {
          id: Date.now(),
          question: question.trim(),
          answer: answerText,
          language,
          gradeLevel,
          length,
          timestamp: new Date().toISOString()
        }
        
        const updatedPastQuestions = [newQuestion, ...pastQuestions].slice(0, 10) // Keep only last 10
        setPastQuestions(updatedPastQuestions)
        localStorage.setItem('sahayak_past_questions', JSON.stringify(updatedPastQuestions))
        
        // Notify dashboard to refresh stats
        window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
        
        // Auto-expand past questions to show the new item
        setShowPastQuestions(true)
        
        // Update dashboard stats
        const description = `Asked "${question.trim()}" in ${language.toUpperCase()} for Grade ${gradeLevel} (${length} answer)`
        updateDashboardStats(ActivityTypes.QUESTION_ANSWERED, description)
      } else {
        setError('No answer received from server')
      }
    } catch (error) {
      console.error('Error getting answer:', error)
      setError('Failed to get answer. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const deletePastQuestion = (id) => {
    const itemToDelete = pastQuestions.find(item => item.id === id)
    const updatedPastQuestions = pastQuestions.filter(item => item.id !== id)
    setPastQuestions(updatedPastQuestions)
    localStorage.setItem('sahayak_past_questions', JSON.stringify(updatedPastQuestions))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    if (itemToDelete) {
      decreaseDashboardStats(ActivityTypes.QUESTION_ANSWERED, `Deleted question: ${itemToDelete.question}`)
    }
  }

  const loadPastQuestion = (questionData) => {
    setQuestion(questionData.question)
    setAnswer(questionData.answer)
    setLanguage(questionData.language)
    setGradeLevel(questionData.gradeLevel)
    setLength(questionData.length || 'medium')
  }



  const startRecording = async () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      setError('Speech recognition not supported in this browser')
      return
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    
    recognition.lang = language
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onstart = () => {
      setIsRecording(true)
    }

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setQuestion(transcript)
      setIsRecording(false)
    }

    recognition.onerror = () => {
      setError('Could not recognize speech. Please try again.')
      setIsRecording(false)
    }

    recognition.onend = () => {
      setIsRecording(false)
    }

    recognition.start()
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-200 mb-2">
          {t('modules.knowledge.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('modules.knowledge.description')}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Question Input and Answer */}
        <div className="xl:col-span-2">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Question Input */}
                    <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
                                  <QuestionMarkCircleIcon className="w-6 h-6 mr-2 text-blue-400" />
                  Ask Your Question
              </h2>

              <form onSubmit={askQuestion} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Question
                  </label>
                  <div className="relative">
                    <textarea
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      placeholder="e.g., Why is the sky blue?"
                      className="input-field h-24 resize-none pr-12"
                      required
                    />
                    <button
                      type="button"
                      onClick={startRecording}
                      disabled={isRecording}
                      className={`absolute right-3 top-3 p-2 rounded-full ${
                        isRecording 
                          ? 'bg-red-500 text-white animate-pulse' 
                          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                      }`}
                    >
                      <MicrophoneIcon className="w-4 h-4" />
                    </button>
                  </div>
                  {isRecording && (
                    <p className="text-sm text-red-600 mt-1">Recording... Speak your question</p>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Complexity Level
                    </label>
                    <select
                      value={gradeLevel}
                      onChange={(e) => setGradeLevel(e.target.value)}
                      className="input-field"
                    >
                      {gradeOptions.map(grade => (
                        <option key={grade.value} value={grade.value}>
                          {grade.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-300 mb-2">
                      Answer Language
                    </label>
                    <select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      className="input-field"
                    >
                      {languages.map(lang => (
                        <option key={lang.value} value={lang.value}>
                          {lang.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Answer Length
                  </label>
                  <select
                    value={length}
                    onChange={(e) => setLength(e.target.value)}
                    className="input-field"
                  >
                    {lengthOptions.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={loading || !question.trim()}
                  className="btn-primary w-full"
                >
                  {loading ? 'Getting Answer...' : 'Ask Question'}
                </button>
              </form>
            </div>

            {/* Answer */}
                    <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-xl font-semibold text-slate-200 mb-6">
            Answer
          </h2>

              {error && (
                <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                  {error}
                </div>
              )}

              {loading && (
                <div className="flex items-center justify-center h-40">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
                  <span className="ml-2 text-slate-300">Finding answer...</span>
                </div>
              )}

              {answer && !loading && (
                <div>
                  <div className="bg-slate-700 p-4 rounded-lg mb-4 max-h-60 overflow-y-auto border border-slate-600">
                    <p className="text-slate-200 leading-relaxed whitespace-pre-wrap">{answer}</p>
                  </div>


                </div>
              )}

              {!answer && !loading && !error && (
                <div className="text-center text-slate-400 h-40 flex items-center justify-center">
                  <div>
                    <QuestionMarkCircleIcon className="w-16 h-16 mx-auto text-slate-500 mb-4" />
                    <p>Ask a question to get an educational answer</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Common Questions */}
          <div className="mt-8 bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h3 className="text-lg font-semibold text-slate-200 mb-4">Common Questions</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {commonQuestions.map((q, index) => (
                <button
                  key={index}
                  onClick={() => setQuestion(q)}
                  className="text-left p-3 rounded border border-slate-600 hover:border-blue-400 hover:bg-slate-700 transition-colors duration-200"
                >
                  <span className="text-sm text-slate-300">{q}</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Past Questions Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Questions
              </h2>
              <button
                onClick={() => setShowPastQuestions(!showPastQuestions)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastQuestions ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastQuestions && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastQuestions.length > 0 ? (
                  pastQuestions.map((questionData) => (
                    <div
                      key={questionData.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastQuestion(questionData)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            {questionData.question}
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            Grade {questionData.gradeLevel} • {questionData.language.toUpperCase()} • {questionData.length || 'medium'} answer
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(questionData.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastQuestion(questionData.id)
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
                    <p className="text-slate-400 text-sm">No past questions</p>
                    <p className="text-xs text-slate-500 mt-1">Ask questions to see them here</p>
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

export default KnowledgeBase 