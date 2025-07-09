import { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { getLanguageOptions } from '../../config/languages'
import { 
  SpeakerWaveIcon, 
  MicrophoneIcon, 
  PlayIcon, 
  StopIcon, 
  DocumentTextIcon, 
  CheckCircleIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'
import { updateDashboardStats, decreaseDashboardStats, ActivityTypes } from '../../utils/dashboard'
import api from '../../config/api'

const ReadingAssessment = () => {
  const { t } = useTranslation()
  const [gradeLevel, setGradeLevel] = useState('3')
  const [language, setLanguage] = useState('en')
  const [wordLimit, setWordLimit] = useState('medium') // New word limit state
  const [readingText, setReadingText] = useState(`Once upon a time, in a small village surrounded by green hills, there lived a kind farmer named Ram. Every morning, Ram would wake up early to take care of his animals and water his plants. He had two cows, five goats, and many chickens. Ram loved his simple life and always helped his neighbors when they needed it. This is a sample text that will only change when you click "Generate New Reading Text" button.`)
  const [isRecording, setIsRecording] = useState(false)
  const [recordedAudio, setRecordedAudio] = useState(null)
  const [assessment, setAssessment] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [transcription, setTranscription] = useState('')
  const [isPlaying, setIsPlaying] = useState(false)
  const [pastAssessments, setPastAssessments] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_assessments')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastAssessments, setShowPastAssessments] = useState(true)
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const audioRef = useRef(null)

  const gradeOptions = [
    { value: '1', label: 'Grade 1' },
    { value: '2', label: 'Grade 2' },
    { value: '3', label: 'Grade 3' },
    { value: '4', label: 'Grade 4' },
    { value: '5', label: 'Grade 5' }
  ]

  const wordLimitOptions = [
    { value: 'short', label: 'Short (50-100 words)' },
    { value: 'medium', label: 'Medium (100-150 words)' },
    { value: 'long', label: 'Long (150-200 words)' }
  ]

  const languages = getLanguageOptions()

  const sampleTexts = {
    '1': {
      en: "The cat sits on a mat. It is a big cat. The cat is happy.",
      hi: "बिल्ली चटाई पर बैठी है। यह एक बड़ी बिल्ली है। बिल्ली खुश है।",
      mr: "मांजर चटईवर बसली आहे. ही एक मोठी मांजर आहे. मांजर आनंदी आहे."
    },
    '2': {
      en: "Once upon a time, there was a little bird. The bird lived in a beautiful tree. Every morning, the bird would sing a sweet song.",
      hi: "एक बार की बात है, एक छोटी चिड़िया थी। चिड़िया एक सुंदर पेड़ में रहती थी। हर सुबह, चिड़िया एक मधुर गीत गाती थी।",
      mr: "एकदा एक लहान पक्षी होता. तो पक्षी एका सुंदर झाडावर राहत होता. रोज सकाळी तो पक्षी गोड गाणे गात असे."
    },
    '3': {
      en: "Water is very important for all living things. Plants need water to grow. Animals drink water to stay alive. People use water for many things like cooking, cleaning, and drinking.",
      hi: "सभी जीवित चीजों के लिए पानी बहुत महत्वपूर्ण है। पौधों को बढ़ने के लिए पानी चाहिए। जानवर जीवित रहने के लिए पानी पीते हैं। लोग खाना बनाने, सफाई करने और पीने जैसी कई चीजों के लिए पानी का उपयोग करते हैं।",
      mr: "सर्व जिवंत गोष्टींसाठी पाणी खूप महत्त्वाचे आहे. रोपांना वाढण्यासाठी पाण्याची गरज असते. प्राणी जिवंत राहण्यासाठी पाणी पितात. लोक स्वयंपाक, साफसफाई आणि पिण्यासारख्या अनेक गोष्टींसाठी पाण्याचा वापर करतात."
    },
    '4': {
      en: "The solar system consists of the sun and all the objects that orbit around it. These include eight planets, their moons, asteroids, and comets. Earth is the third planet from the sun and the only planet known to support life.",
      hi: "सौर मंडल में सूर्य और उसके चारों ओर परिक्रमा करने वाली सभी वस्तुएं शामिल हैं। इनमें आठ ग्रह, उनके चंद्रमा, क्षुद्रग्रह और धूमकेतु शामिल हैं। पृथ्वी सूर्य से तीसरा ग्रह है और जीवन का समर्थन करने वाला एकमात्र ज्ञात ग्रह है।",
      mr: "सूर्यमालेत सूर्य आणि त्याभोवती फिरणाऱ्या सर्व वस्तूंचा समावेश होतो. यामध्ये आठ ग्रह, त्यांचे चंद्र, लघुग्रह आणि धूमकेतू यांचा समावेश आहे. पृथ्वी हा सूर्यापासून तिसरा ग्रह आहे आणि जीवनाला आधार देणारा एकमेव ज्ञात ग्रह आहे."
    },
    '5': {
      en: "Photosynthesis is the process by which green plants make their own food using sunlight, water, and carbon dioxide. During this process, plants produce oxygen as a byproduct, which is essential for most life forms on Earth. This process occurs mainly in the leaves of plants.",
      hi: "प्रकाश संश्लेषण वह प्रक्रिया है जिसके द्वारा हरे पौधे सूर्य प्रकाश, पानी और कार्बन डाइऑक्साइड का उपयोग करके अपना भोजन बनाते हैं। इस प्रक्रिया के दौरान, पौधे उपोत्पाद के रूप में ऑक्सीजन का उत्पादन करते हैं, जो पृथ्वी पर अधिकांश जीवन रूपों के लिए आवश्यक है। यह प्रक्रिया मुख्यतः पौधों की पत्तियों में होती है।",
      mr: "प्रकाशसंश्लेषण ही अशी प्रक्रिया आहे ज्याद्वारे हिरवी झाडे सूर्यप्रकाश, पाणी आणि कार्बन डायऑक्साइड वापरून स्वतःचे अन्न तयार करतात. या प्रक्रियेदरम्यान, झाडे उपउत्पादन म्हणून ऑक्सिजन तयार करतात, जो पृथ्वीवरील बहुतेक जीवांसाठी आवश्यक आहे. ही प्रक्रिया मुख्यतः झाडांच्या पानांमध्ये होते."
    }
  }

  useEffect(() => {
    // Only reset assessment and recording data when settings change, but keep the reading text unchanged
    // The reading text should only change when "Generate New Reading Text" button is clicked
    setAssessment(null)
    setTranscription('')
    setRecordedAudio(null)
  }, [gradeLevel, language, wordLimit])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      audioChunksRef.current = []

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        const audioUrl = URL.createObjectURL(audioBlob)
        setRecordedAudio({ blob: audioBlob, url: audioUrl })
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      setIsRecording(true)
      setError('')
    } catch (error) {
      setError('Microphone access denied. Please allow microphone access to record.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const playRecording = () => {
    if (recordedAudio && audioRef.current) {
      setIsPlaying(true)
      audioRef.current.src = recordedAudio.url
      audioRef.current.play()
    }
  }

  const assessReading = async () => {
    if (!recordedAudio || !readingText) return

    setLoading(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('audio', recordedAudio.blob)
      formData.append('original_text', readingText)
      formData.append('language', language)
      formData.append('grade_level', gradeLevel)
      formData.append('word_limit', wordLimit) // Append word limit

      const response = await api.post('/assessment/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const assessmentData = response.data
      setAssessment(assessmentData)
      setTranscription(assessmentData.transcription || '')
      
      // Save to past assessments
      const newAssessment = {
        id: Date.now(),
        readingText: readingText.substring(0, 100) + '...', // First 100 chars
        language,
        gradeLevel,
        assessment: assessmentData,
        transcription: assessmentData.transcription || '',
        timestamp: new Date().toISOString()
      }
      
      const updatedPastAssessments = [newAssessment, ...pastAssessments].slice(0, 10) // Keep only last 10
      setPastAssessments(updatedPastAssessments)
      localStorage.setItem('sahayak_past_assessments', JSON.stringify(updatedPastAssessments))
      
      // Notify dashboard to refresh stats
      window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
      
      // Auto-expand past assessments to show the new item
      setShowPastAssessments(true)
      
      // Update dashboard stats
      const description = `Completed reading assessment in ${language.toUpperCase()} for Grade ${gradeLevel}`
      updateDashboardStats(ActivityTypes.ASSESSMENT_COMPLETED, description)
      
    } catch (error) {
      setError(error.response?.data?.message || 'Failed to analyze reading')
    } finally {
      setLoading(false)
    }
  }

  const deletePastAssessment = (id) => {
    const itemToDelete = pastAssessments.find(item => item.id === id)
    const updatedPastAssessments = pastAssessments.filter(item => item.id !== id)
    setPastAssessments(updatedPastAssessments)
    localStorage.setItem('sahayak_past_assessments', JSON.stringify(updatedPastAssessments))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    if (itemToDelete) {
      decreaseDashboardStats(ActivityTypes.ASSESSMENT_COMPLETED, `Deleted assessment: Grade ${itemToDelete.gradeLevel}`)
    }
  }

  const loadPastAssessment = (assessmentData) => {
    setAssessment(assessmentData.assessment)
    setTranscription(assessmentData.transcription)
    setLanguage(assessmentData.language)
    setGradeLevel(assessmentData.gradeLevel)
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleString()
  }

  const generateNewText = async () => {
    setLoading(true)
    setError('')

    try {
      // Use the assessment API to generate reading text with specific word limit
      const response = await api.post('/assessment/generate-text', {
        grade_level: gradeLevel,
        language: language,
        difficulty: 'medium',
        word_limit: wordLimit
      })

      if (response.data && response.data.text) {
        setReadingText(response.data.text)
        setAssessment(null)
        setTranscription('')
        setRecordedAudio(null)
        setError('') // Clear any previous errors
      } else {
        // Fallback to a default text if API fails
        const fallbackText = `This is a generated reading passage for Grade ${gradeLevel} students in ${language === 'hi' ? 'हिंदी' : language === 'mr' ? 'मराठी' : 'English'}. Click "Generate New Reading Text" to get AI-generated content when the backend is running.`
        setReadingText(fallbackText)
        setError('Using sample text. Please ensure the backend server is running for AI-generated content.')
      }
    } catch (error) {
      console.error('Error generating new text:', error)
      // Provide a helpful fallback text
      const fallbackText = `This is a sample reading passage for Grade ${gradeLevel}. To get AI-generated reading texts in ${language === 'hi' ? 'Hindi' : language === 'mr' ? 'Marathi' : 'English'}, please ensure the backend server is running and try again.`
      setReadingText(fallbackText)
      setError('Could not generate new text. Using sample text instead. Please check if the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600'
    if (score >= 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreDescription = (score) => {
    if (score >= 90) return 'Excellent'
    if (score >= 80) return 'Good'
    if (score >= 70) return 'Fair'
    if (score >= 60) return 'Needs Practice'
    return 'Keep Trying'
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-200 mb-2">
          {t('modules.assessment.title')}
        </h1>
        <p className="text-lg text-slate-400">
          Record yourself reading the text aloud and get AI-powered feedback on your reading skills
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
        {/* Reading Text & Controls */}
        <div className="xl:col-span-3 space-y-8">
          {/* Settings Section */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h2 className="text-xl font-semibold text-slate-200 mb-4 flex items-center">
              <DocumentTextIcon className="w-6 h-6 mr-2 text-blue-400" />
              Reading Settings
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Grade Level
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
                  Language
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

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Word Limit
                </label>
                <select
                  value={wordLimit}
                  onChange={(e) => setWordLimit(e.target.value)}
                  className="input-field"
                >
                  {wordLimitOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <button
              onClick={generateNewText}
              disabled={loading}
              className="btn-secondary w-full"
            >
              {loading ? 'Generating...' : 'Generate New Reading Text'}
            </button>
          </div>

          {/* Reading Text - Full width and prominent */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h3 className="text-xl font-semibold text-slate-200 mb-6">Reading Text</h3>
            <div className="bg-slate-700 p-8 rounded-lg border border-slate-600 min-h-48">
              <p className="text-slate-200 leading-relaxed text-2xl font-serif tracking-wide text-center mx-auto max-w-4xl" style={{ lineHeight: '2.2' }}>
                {readingText}
              </p>
            </div>
          </div>

          {/* Recording Controls and Assessment Results in Two Columns */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Recording Controls */}
            <div className="space-y-6">
              <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
                <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center">
                  <MicrophoneIcon className="w-5 h-5 mr-2 text-blue-400" />
                  Audio Recording
                </h3>

                <div className="space-y-4">
                  <div className="flex items-center space-x-4">
                    {!isRecording ? (
                      <button
                        onClick={startRecording}
                        disabled={!readingText || loading}
                        className="flex items-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <MicrophoneIcon className="w-5 h-5 mr-2" />
                        Start Recording
                      </button>
                    ) : (
                      <button
                        onClick={stopRecording}
                        className="flex items-center px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 animate-pulse"
                      >
                        <StopIcon className="w-5 h-5 mr-2" />
                        Stop Recording
                      </button>
                    )}

                    {recordedAudio && !isRecording && (
                      <button
                        onClick={playRecording}
                        className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                      >
                        <PlayIcon className="w-5 h-5 mr-2" />
                        Play Recording
                      </button>
                    )}
                  </div>

                  {isRecording && (
                    <div className="flex items-center text-red-600">
                      <div className="w-3 h-3 bg-red-600 rounded-full animate-pulse mr-2"></div>
                      <span className="text-sm">Recording... Read the text aloud clearly</span>
                    </div>
                  )}

                  {recordedAudio && (
                    <div className="flex items-center justify-between p-3 bg-slate-700 rounded border border-slate-600">
                      <span className="text-sm text-slate-300">Recording ready</span>
                      <button
                        onClick={assessReading}
                        disabled={loading}
                        className="btn-primary"
                      >
                        {loading ? 'Analyzing...' : 'Analyze Reading'}
                      </button>
                    </div>
                  )}

                  <audio
                    ref={audioRef}
                    onEnded={() => setIsPlaying(false)}
                    className="hidden"
                  />
                </div>
              </div>

              {/* Right Column - Assessment Results */}
              <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
                <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
                  <CheckCircleIcon className="w-6 h-6 mr-2 text-blue-400" />
                  Reading Assessment Results
                </h2>

                {error && (
                  <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                    {error}
                  </div>
                )}

                {loading && (
                  <div className="flex items-center justify-center h-40">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto mb-4"></div>
                      <p className="text-slate-300">Analyzing your reading...</p>
                    </div>
                  </div>
                )}

                {assessment && !loading && (
                  <div className="space-y-4">
                    {/* Overall Score */}
                    <div className="text-center p-4 bg-slate-700 rounded-lg border border-slate-600">
                      <div className={`text-3xl font-bold ${getScoreColor(assessment.overall_score)}`}>
                        {assessment.overall_score}%
                      </div>
                      <div className="text-lg text-slate-400 mt-1">
                        {getScoreDescription(assessment.overall_score)}
                      </div>
                    </div>

                    {/* Detailed Metrics */}
                    <div className="space-y-3">
                      {assessment.accuracy && (
                        <div className="flex justify-between items-center p-3 bg-slate-700 rounded border border-slate-600">
                          <span className="font-medium text-blue-300">Accuracy</span>
                          <span className={`font-bold ${getScoreColor(assessment.accuracy)}`}>
                            {assessment.accuracy}%
                          </span>
                        </div>
                      )}

                      {assessment.fluency && (
                        <div className="flex justify-between items-center p-3 bg-slate-700 rounded border border-slate-600">
                          <span className="font-medium text-green-300">Fluency</span>
                          <span className={`font-bold ${getScoreColor(assessment.fluency)}`}>
                            {assessment.fluency}%
                          </span>
                        </div>
                      )}

                      {assessment.pronunciation && (
                        <div className="flex justify-between items-center p-3 bg-slate-700 rounded border border-slate-600">
                          <span className="font-medium text-purple-300">Pronunciation</span>
                          <span className={`font-bold ${getScoreColor(assessment.pronunciation)}`}>
                            {assessment.pronunciation}%
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Transcription */}
                    {transcription && (
                      <div className="mt-4">
                        <h4 className="font-medium text-slate-200 mb-2">What we heard:</h4>
                        <div className="bg-slate-700 p-3 rounded text-sm text-slate-300 max-h-32 overflow-y-auto border border-slate-600">
                          {transcription}
                        </div>
                      </div>
                    )}

                    {/* Feedback */}
                    {assessment.feedback && (
                      <div className="mt-4">
                        <h4 className="font-medium text-slate-200 mb-2">Feedback:</h4>
                        <div className="bg-slate-700 border border-slate-600 p-3 rounded text-sm text-slate-300">
                          {assessment.feedback}
                        </div>
                      </div>
                    )}

                    {/* Suggestions */}
                    {assessment.suggestions && assessment.suggestions.length > 0 && (
                      <div className="mt-4">
                        <h4 className="font-medium text-slate-200 mb-2">Suggestions for Improvement:</h4>
                        <ul className="space-y-1 text-sm text-slate-300">
                          {assessment.suggestions.map((suggestion, index) => (
                            <li key={index} className="flex items-start">
                              <span className="text-blue-400 mr-2">•</span>
                              {suggestion}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}

                {!assessment && !loading && !error && (
                  <div className="text-center text-slate-400 h-40 flex items-center justify-center">
                    <div>
                      <CheckCircleIcon className="w-16 h-16 mx-auto text-slate-500 mb-4" />
                      <p>Record yourself reading to get detailed feedback</p>
                      <p className="text-sm text-slate-500 mt-1">Get scores for accuracy, fluency, and pronunciation</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Past Assessments Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Assessments
              </h2>
              <button
                onClick={() => setShowPastAssessments(!showPastAssessments)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastAssessments ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastAssessments && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastAssessments.length > 0 ? (
                  pastAssessments.map((assessmentData) => (
                    <div
                      key={assessmentData.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastAssessment(assessmentData)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            Score: {assessmentData.assessment?.overall_score || 'N/A'}%
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            Grade {assessmentData.gradeLevel} • {assessmentData.language.toUpperCase()}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(assessmentData.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastAssessment(assessmentData.id)
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
                    <p className="text-slate-400 text-sm">No past assessments</p>
                    <p className="text-xs text-slate-500 mt-1">Complete assessments to see them here</p>
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

export default ReadingAssessment 