import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import api, { API_BASE_URL } from '../../config/api'
import { updateDashboardStats, decreaseDashboardStats, ActivityTypes } from '../../utils/dashboard'
import { getLanguageOptions, getLanguageName } from '../../config/languages'
import { 
  DocumentTextIcon, 
  ArrowDownTrayIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'

const ContentGenerator = () => {
  const { t } = useTranslation()
  const [formData, setFormData] = useState({
    topic: '',
    contentType: 'explanation',
    gradeLevel: '3',
    language: 'en',
    length: 'medium'
  })
  const [generatedContent, setGeneratedContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [pastContent, setPastContent] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_content')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastContent, setShowPastContent] = useState(true)

  const contentTypes = [
    { value: 'explanation', label: 'Simple Explanation' },
    { value: 'story', label: 'Educational Story' },
    { value: 'example', label: 'Real-life Examples' },
    { value: 'activity', label: 'Learning Activity' }
  ]

  const gradeOptions = [
    { value: '1', label: 'Grade 1-2 (Very Simple)' },
    { value: '3', label: 'Grade 3-4 (Simple)' },
    { value: '5', label: 'Grade 5+ (Detailed)' }
  ]

  const languages = getLanguageOptions()

  const lengthOptions = [
    { value: 'short', label: 'Short (100-150 words)' },
    { value: 'medium', label: 'Medium (200-300 words)' },
    { value: 'long', label: 'Long (400-500 words)' }
  ]

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const generateContent = async (e) => {
    e.preventDefault()
    if (!formData.topic.trim()) return

    setLoading(true)
    setError('')

    try {
      const response = await api.post('/content/generate', {
        topic: formData.topic,
        contentType: formData.contentType,
        gradeLevel: formData.gradeLevel,
        language: formData.language,
        length: formData.length
      })

      if (response.data.content) {
        setGeneratedContent(response.data.content)
        
        // Save to past content
        const newContent = {
          id: Date.now().toString(),
          topic: formData.topic,
          contentType: formData.contentType,
          gradeLevel: formData.gradeLevel,
          language: formData.language,
          length: formData.length,
          content: response.data.content,
          timestamp: new Date().toISOString()
        }
        
        const updatedPastContent = [newContent, ...pastContent]
        setPastContent(updatedPastContent)
        localStorage.setItem('sahayak_past_content', JSON.stringify(updatedPastContent))
        
        // Notify dashboard to refresh stats
        window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
        
        // Update dashboard stats
        updateDashboardStats(ActivityTypes.CONTENT_GENERATED, `Generated: ${formData.topic}`)
      } else {
        setError('No content was generated. Please try again.')
      }
    } catch (error) {
      console.error('Error generating content:', error)
      
      // Handle different error formats
      let errorMessage = 'Failed to generate content. Please try again.'
      
      if (error.response?.data) {
        const errorData = error.response.data
        
        // Handle validation errors (array format)
        if (Array.isArray(errorData)) {
          const messages = errorData.map(err => `${err.msg} (${err.loc?.join('.')})`).join(', ')
          errorMessage = `Validation error: ${messages}`
        }
        // Handle single error with detail
        else if (errorData.detail) {
          errorMessage = typeof errorData.detail === 'string' 
            ? errorData.detail 
            : JSON.stringify(errorData.detail)
        }
        // Handle simple message
        else if (errorData.message) {
          errorMessage = errorData.message
        }
      } else if (error.message) {
        errorMessage = error.message
      }
      
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const deletePastContent = (id) => {
    const updatedPastContent = pastContent.filter(content => content.id !== id)
    setPastContent(updatedPastContent)
    localStorage.setItem('sahayak_past_content', JSON.stringify(updatedPastContent))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    decreaseDashboardStats(ActivityTypes.CONTENT_GENERATED, `Deleted: ${pastContent.find(c => c.id === id)?.topic || 'Content'}`)
  }

  const loadPastContent = (content) => {
    setGeneratedContent(content.content)
    setFormData({
      topic: content.topic,
      contentType: content.contentType,
      gradeLevel: content.gradeLevel,
      language: content.language,
      length: content.length || 'medium'
    })
  }



  const downloadContent = () => {
    if (generatedContent) {
      const element = document.createElement('a')
      const file = new Blob([generatedContent], { type: 'text/plain' })
      element.href = URL.createObjectURL(file)
      element.download = `${formData.topic}_${formData.language}_grade${formData.gradeLevel}.txt`
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
          {t('modules.content.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('modules.content.description')}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Input Form */}
        <div className="xl:col-span-2">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
              <DocumentTextIcon className="w-6 h-6 mr-2 text-blue-400" />
              Content Details
            </h2>

            <form onSubmit={generateContent} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Topic / Subject
                </label>
                <input
                  type="text"
                  name="topic"
                  value={formData.topic}
                  onChange={handleInputChange}
                  placeholder="e.g., Water Cycle, Farmers in India, Solar System"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Content Type
                </label>
                <select
                  name="contentType"
                  value={formData.contentType}
                  onChange={handleInputChange}
                  className="input-field"
                >
                  {contentTypes.map(type => (
                    <option key={type.value} value={type.value}>
                      {type.label}
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
                  {gradeOptions.map(grade => (
                    <option key={grade.value} value={grade.value}>
                      {grade.label}
                    </option>
                  ))}
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

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Answer Length
                </label>
                <select
                  name="length"
                  value={formData.length}
                  onChange={handleInputChange}
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
                disabled={loading || !formData.topic}
                className="btn-primary w-full"
              >
                {loading ? 'Generating...' : 'Generate Content'}
              </button>
            </form>
          </div>

          {/* Generated Content */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300 mt-6">
            <h2 className="text-xl font-semibold text-slate-200 mb-6">
              Generated Content
            </h2>

            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
                <span className="ml-2 text-slate-300">Generating content...</span>
              </div>
            )}

            {generatedContent && !loading && (
              <div>
                <div className="bg-slate-700 p-4 rounded-lg mb-4 max-h-96 overflow-y-auto border border-slate-600">
                  <pre className="whitespace-pre-wrap text-sm text-slate-200 font-serif leading-relaxed">
                    {generatedContent}
                  </pre>
                </div>

                <div className="flex flex-wrap gap-3">
                  <button
                    onClick={downloadContent}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                  >
                    <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
                    Download
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Past Generated Content Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Content
              </h2>
              <button
                onClick={() => setShowPastContent(!showPastContent)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastContent ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastContent && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastContent.length > 0 ? (
                  pastContent.map((content) => (
                    <div
                      key={content.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastContent(content)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            {content.topic}
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            {content.contentType} • Grade {content.gradeLevel} • {content.language.toUpperCase()} • {content.length || 'medium'} length
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(content.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastContent(content.id)
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
                    <p className="text-slate-400 text-sm">No past content</p>
                    <p className="text-xs text-slate-500 mt-1">Generate content to see it here</p>
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

export default ContentGenerator 