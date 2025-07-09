import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { 
  PhotoIcon, 
  EyeIcon, 
  ArrowDownTrayIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'
import { updateDashboardStats, ActivityTypes } from '../../utils/dashboard'
import api from '../../config/api'

const VisualAids = () => {
  const { t } = useTranslation()
  const [prompt, setPrompt] = useState('')
  const [style, setStyle] = useState('illustration')
  const [subject, setSubject] = useState('science')
  const [loading, setLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState('')
  const [error, setError] = useState('')
  const [pastVisuals, setPastVisuals] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_visuals')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastVisuals, setShowPastVisuals] = useState(true)

  const styles = [
    { value: 'illustration', label: 'Colorful Illustration' },
    { value: 'diagram', label: 'Educational Diagram' },
    { value: 'cartoon', label: 'Child-Friendly Cartoon' },
    { value: 'realistic', label: 'Realistic Drawing' }
  ]

  const subjects = [
    { value: 'science', label: 'Science' },
    { value: 'mathematics', label: 'Mathematics' },
    { value: 'social_studies', label: 'Social Studies' },
    { value: 'language', label: 'Language Arts' },
    { value: 'geography', label: 'Geography' },
    { value: 'history', label: 'History' }
  ]

  const examplePrompts = [
    'Water cycle diagram with evaporation, condensation, and precipitation',
    'Solar system with planets in order',
    'Parts of a plant - roots, stem, leaves, flowers',
    'Food chain in a forest ecosystem',
    'Human digestive system',
    'Phases of the moon',
    'Geometric shapes - triangle, circle, square, rectangle',
    'Map of India with major states'
  ]

  const generateVisual = async (e) => {
    e.preventDefault()
    if (!prompt.trim()) return

    setLoading(true)
    setError('')
    setGeneratedImage('')

    try {
      // Enhanced prompt that includes style and subject context
      const styleContext = {
        'illustration': 'colorful educational illustration',
        'diagram': 'clean educational diagram with labels',
        'cartoon': 'child-friendly cartoon style',
        'realistic': 'realistic educational illustration'
      }
      
      const subjectContext = {
        'science': 'scientific and educational',
        'mathematics': 'mathematical and geometric',
        'social_studies': 'cultural and historical',
        'language': 'clear text and symbols',
        'geography': 'geographical features',
        'history': 'historically accurate'
      }
      
      const enhancedPrompt = `${prompt.trim()}, ${styleContext[style] || 'educational illustration'}, ${subjectContext[subject] || 'educational'}, suitable for Indian school children`
      
      // Use GET request with prompt as query parameter
      const encodedPrompt = encodeURIComponent(enhancedPrompt)
      const response = await fetch(`${api.defaults.baseURL}/visuals/generate-image?prompt=${encodedPrompt}`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Unknown error occurred' }))
        throw new Error(errorData.error || `HTTP ${response.status}`)
      }
      
      // Check content type before parsing to avoid binary data errors
      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error(`Server returned ${contentType} instead of JSON. Please try again.`)
      }
      
      // Get the JSON response with server image URL
      const data = await response.json()
      if (!data.imageUrl) {
        throw new Error('Invalid response: missing image URL')
      }
      
      const imageUrl = `${api.defaults.baseURL}${data.imageUrl}`
      setGeneratedImage(imageUrl)
      
      // Save to past visuals
      const newVisual = {
        id: Date.now(),
        prompt: prompt.trim(),
        style,
        subject,
        imageUrl,
        timestamp: new Date().toISOString()
      }
      
      const updatedPastVisuals = [newVisual, ...pastVisuals].slice(0, 10) // Keep only last 10
      setPastVisuals(updatedPastVisuals)
      localStorage.setItem('sahayak_past_visuals', JSON.stringify(updatedPastVisuals))
      
      // Notify dashboard to refresh stats
      window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
      
      // Auto-expand past visuals to show the new item  
      setShowPastVisuals(true)
      
      // Update dashboard stats
      const description = `Generated ${style} visual for "${prompt.trim()}" in ${subject}`
      updateDashboardStats(ActivityTypes.VISUAL_GENERATED, description)
      
    } catch (error) {
      console.error('Visual generation error:', error)
      setError(error.message || 'Failed to generate visual. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const deletePastVisual = (id) => {
    const updatedPastVisuals = pastVisuals.filter(item => item.id !== id)
    setPastVisuals(updatedPastVisuals)
    localStorage.setItem('sahayak_past_visuals', JSON.stringify(updatedPastVisuals))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    decreaseDashboardStats(ActivityTypes.VISUAL_GENERATED, `Deleted visual aid`)
  }

  const loadPastVisual = (visual) => {
    setPrompt(visual.prompt)
    setStyle(visual.style)
    setSubject(visual.subject)
    setGeneratedImage(visual.imageUrl)
  }

  const downloadImage = async () => {
    if (generatedImage) {
      try {
        const link = document.createElement('a')
        link.href = generatedImage
        link.download = `visual_aid_${style}_${Date.now()}.png`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } catch (error) {
        console.error('Error downloading image:', error)
        setError('Failed to download image')
      }
    }
  }

  const openFullscreen = () => {
    if (generatedImage) {
      window.open(generatedImage, '_blank')
    }
  }

  const downloadTextVisual = () => {
    if (generatedImage) {
      const blob = new Blob([generatedImage], { type: 'text/plain' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.download = `visual_aid_description_${Date.now()}.txt`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString()
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-200 mb-2">
          {t('modules.visuals.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('modules.visuals.description')}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Input Form and Generated Visual */}
        <div className="xl:col-span-2">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Form */}
                    <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
                                  <PhotoIcon className="w-6 h-6 mr-2 text-blue-400" />
                  Visual Details
              </h2>

              <form onSubmit={generateVisual} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Description
                  </label>
                  <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Describe what you want to visualize..."
                    className="input-field h-24 resize-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Visual Style
                  </label>
                  <select
                    value={style}
                    onChange={(e) => setStyle(e.target.value)}
                    className="input-field"
                  >
                    {styles.map(s => (
                      <option key={s.value} value={s.value}>
                        {s.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2">
                    Subject Area
                  </label>
                  <select
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                    className="input-field"
                  >
                    {subjects.map(sub => (
                      <option key={sub.value} value={sub.value}>
                        {sub.label}
                      </option>
                    ))}
                  </select>
                </div>

                <button
                  type="submit"
                  disabled={loading || !prompt.trim()}
                  className="btn-primary w-full"
                >
                  {loading ? 'Generating Visual...' : 'Generate Visual Aid'}
                </button>
              </form>
            </div>

            {/* Generated Visual */}
            <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
              <h2 className="text-xl font-semibold text-slate-200 mb-6">
                Generated Visual
              </h2>

              {error && (
                <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                  {error}
                </div>
              )}

              {loading && (
                <div className="flex items-center justify-center h-80">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
                    <p className="text-slate-300">Creating your visual aid...</p>
                    <p className="text-sm text-slate-400 mt-2">This may take a few moments</p>
                  </div>
                </div>
              )}

              {generatedImage && !loading && (
                <div>
                  <div className="bg-slate-700 p-4 rounded-lg mb-4 border border-slate-600">
                    {/* Check if it's a URL (starts with http) or text description */}
                    {generatedImage.startsWith('http') ? (
                      <img
                        src={generatedImage}
                        alt="Generated visual aid"
                        className="w-full h-auto max-h-80 object-contain mx-auto rounded"
                      />
                    ) : (
                      /* Display as educational text description */
                                              <div className="bg-slate-600 p-6 rounded-lg border-2 border-slate-500 max-h-80 overflow-y-auto">
                        <pre className="whitespace-pre-wrap text-sm text-slate-200 font-mono leading-relaxed">
                          {generatedImage}
                        </pre>
                      </div>
                    )}
                  </div>

                  <div className="flex space-x-3">
                    {generatedImage.startsWith('http') ? (
                      <>
                        <button
                          onClick={openFullscreen}
                          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
                        >
                          <EyeIcon className="w-4 h-4 mr-2" />
                          View Full Size
                        </button>
                        <button
                          onClick={downloadImage}
                          className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
                        >
                          <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
                          Download
                        </button>
                      </>
                    ) : (
                      /* For text descriptions, offer download as text */
                      <button
                        onClick={downloadTextVisual}
                        className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
                      >
                        <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
                        Download Description
                      </button>
                    )}
                  </div>
                </div>
              )}

              {!generatedImage && !loading && !error && (
                <div className="text-center text-slate-400 h-80 flex items-center justify-center">
                  <div>
                    <PhotoIcon className="w-16 h-16 mx-auto text-slate-500 mb-4" />
                    <p>Generate a visual aid to see it here</p>
                    <p className="text-sm text-slate-500 mt-1">Perfect for explaining complex concepts</p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Past Visuals Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Visuals
              </h2>
              <button
                onClick={() => setShowPastVisuals(!showPastVisuals)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastVisuals ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastVisuals && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastVisuals.length > 0 ? (
                  pastVisuals.map((visual) => (
                    <div
                      key={visual.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastVisual(visual)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            {visual.prompt}
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            {visual.style} • {visual.subject}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(visual.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastVisual(visual.id)
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
                    <p className="text-slate-400 text-sm">No past visuals</p>
                    <p className="text-xs text-slate-500 mt-1">Generate visuals to see them here</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Example Prompts */}
      <div className="mt-8 bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Example Ideas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {examplePrompts.map((example, index) => (
            <button
              key={index}
              onClick={() => setPrompt(example)}
              className="text-left p-3 rounded border border-slate-600 hover:border-blue-400 hover:bg-slate-700 transition-colors duration-200"
            >
              <span className="text-sm text-slate-300">{example}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Tips */}
      <div className="mt-6 bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
        <h3 className="text-lg font-semibold text-slate-200 mb-4">Tips for Better Visuals</h3>
        <ul className="space-y-2 text-sm text-slate-300">
          <li>• Be specific about what you want to show (e.g., "water cycle with labeled stages")</li>
          <li>• For blackboard use, choose "Line Drawing" style for easy copying</li>
          <li>• Include the purpose (e.g., "for grade 3 students" or "simple diagram")</li>
          <li>• Mention if you want labels, arrows, or annotations</li>
        </ul>
      </div>
    </div>
  )
}

export default VisualAids 