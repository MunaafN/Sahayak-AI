import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { 
  PhotoIcon, 
  AcademicCapIcon, 
  XMarkIcon, 
  ArrowDownTrayIcon,
  ClockIcon,
  TrashIcon,
  PlusIcon,
  MinusIcon
} from '@heroicons/react/24/outline'
import { updateDashboardStats, ActivityTypes } from '../../utils/dashboard'
import api from '../../config/api'

const WorksheetGenerator = () => {
  const { t } = useTranslation()
  const [uploadedImage, setUploadedImage] = useState(null)
  const [subject, setSubject] = useState('science')
  const [selectedGrades, setSelectedGrades] = useState(['3'])
  const [worksheets, setWorksheets] = useState({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [pastWorksheets, setPastWorksheets] = useState(() => {
    try {
      const saved = localStorage.getItem('sahayak_past_worksheets')
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })
  const [showPastWorksheets, setShowPastWorksheets] = useState(true)

  const subjects = [
    { value: 'science', label: 'Science' },
    { value: 'math', label: 'Mathematics' },
    { value: 'social_studies', label: 'Social Studies' },
    { value: 'english', label: 'English' },
    { value: 'hindi', label: 'Hindi' }
  ]

  const gradeOptions = [
    { value: '1', label: 'Grade 1' },
    { value: '2', label: 'Grade 2' },
    { value: '3', label: 'Grade 3' },
    { value: '4', label: 'Grade 4' },
    { value: '5', label: 'Grade 5' }
  ]

  const handleImageUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(e.target.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const toggleGrade = (grade) => {
    setSelectedGrades(prev => 
      prev.includes(grade) 
        ? prev.filter(g => g !== grade)
        : [...prev, grade]
    )
  }

  const generateWorksheets = async () => {
    if (!uploadedImage || selectedGrades.length === 0) return

    setLoading(true)
    setError('')
    setWorksheets({})

    try {
      // Use the new vision-based endpoint with llava-phi3
      const response = await api.post('/worksheets/generate-with-vision', {
        image: uploadedImage,
        grades: selectedGrades,
        subject: subject
      })
      
      const generatedWorksheets = response.data.worksheets
      setWorksheets(generatedWorksheets)
      
      // Save to past worksheets
      const newWorksheet = {
        id: Date.now(),
        subject,
        grades: selectedGrades,
        worksheets: generatedWorksheets,
        timestamp: new Date().toISOString()
      }
      
      const updatedPastWorksheets = [newWorksheet, ...pastWorksheets].slice(0, 10) // Keep only last 10
      setPastWorksheets(updatedPastWorksheets)
      localStorage.setItem('sahayak_past_worksheets', JSON.stringify(updatedPastWorksheets))
      
      // Notify dashboard to refresh stats
      window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
      
      // Auto-expand past worksheets to show the new item
      setShowPastWorksheets(true)
      
      // Update dashboard stats
      const description = `Generated worksheets for ${subject} - Grades ${selectedGrades.join(', ')}`
      updateDashboardStats(ActivityTypes.WORKSHEET_CREATED, description)
      
    } catch (error) {
      setError(error.response?.data?.message || 'Failed to generate worksheets')
    } finally {
      setLoading(false)
    }
  }

  const deletePastWorksheet = (id) => {
    const updatedPastWorksheets = pastWorksheets.filter(item => item.id !== id)
    setPastWorksheets(updatedPastWorksheets)
    localStorage.setItem('sahayak_past_worksheets', JSON.stringify(updatedPastWorksheets))
    
    // Notify dashboard to refresh stats
    window.dispatchEvent(new CustomEvent('sahayak-data-changed'))
    
    // Update dashboard stats
    decreaseDashboardStats(ActivityTypes.WORKSHEET_CREATED, `Deleted worksheet`)
  }

  const loadPastWorksheet = (worksheet) => {
    setSubject(worksheet.subject)
    setSelectedGrades(worksheet.grades)
    setWorksheets(worksheet.worksheets)
  }

  const downloadWorksheet = (grade) => {
    if (worksheets[grade]) {
      const element = document.createElement('a')
      const file = new Blob([worksheets[grade]], { type: 'text/plain' })
      element.href = URL.createObjectURL(file)
      element.download = `worksheet_grade_${grade}_${subject}.txt`
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
          {t('modules.worksheets.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('modules.worksheets.description')}
        </p>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
        {/* Input Section */}
        <div className="xl:col-span-1 space-y-6">
          {/* Image Upload */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h2 className="text-xl font-semibold text-slate-200 mb-4 flex items-center">
                              <PhotoIcon className="w-6 h-6 mr-2 text-blue-400" />
                Upload Textbook Page
            </h2>

            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                {uploadedImage ? (
                  <div className="relative">
                    <img 
                      src={uploadedImage} 
                      alt="Uploaded textbook page" 
                      className="max-w-full h-40 object-contain mx-auto rounded"
                    />
                    <button
                      onClick={() => setUploadedImage(null)}
                      className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600"
                    >
                      <XMarkIcon className="w-4 h-4" />
                    </button>
                  </div>
                ) : (
                  <div>
                    <PhotoIcon className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600 mb-4">Upload a textbook page image</p>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      id="image-upload"
                    />
                    <label
                      htmlFor="image-upload"
                      className="btn-primary cursor-pointer inline-block"
                    >
                      Choose Image
                    </label>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Settings */}
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <h3 className="text-lg font-semibold text-slate-200 mb-4">Settings</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Subject
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

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Target Grades
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {gradeOptions.map(grade => (
                    <button
                      key={grade.value}
                      onClick={() => toggleGrade(grade.value)}
                      className={`p-2 text-sm rounded border ${
                        selectedGrades.includes(grade.value)
                          ? 'bg-primary-100 border-primary-300 text-primary-700'
                          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      {grade.label}
                    </button>
                  ))}
                </div>
              </div>

              <button
                onClick={generateWorksheets}
                disabled={!uploadedImage || selectedGrades.length === 0 || loading}
                className="btn-primary w-full"
              >
                {loading ? 'Generating...' : 'Generate Worksheets'}
              </button>
            </div>
          </div>
        </div>

        {/* Output Section */}
        <div className="xl:col-span-2">
                  <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <h2 className="text-xl font-semibold text-slate-200 mb-6 flex items-center">
              <AcademicCapIcon className="w-6 h-6 mr-2 text-blue-400" />
              Generated Worksheets
            </h2>

            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center h-40">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400"></div>
                <span className="ml-2 text-slate-300">Generating worksheets...</span>
              </div>
            )}

            {Object.keys(worksheets).length > 0 && !loading && (
              <div className="space-y-6">
                {selectedGrades.map(grade => (
                  <div key={grade} className="border border-slate-600 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-3">
                      <h3 className="text-lg font-medium text-slate-200">
                        Grade {grade} Worksheet
                      </h3>
                      <button
                        onClick={() => downloadWorksheet(grade)}
                        className="flex items-center px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors duration-200"
                      >
                        <ArrowDownTrayIcon className="w-4 h-4 mr-1" />
                        Download
                      </button>
                    </div>
                    
                    <div className="bg-slate-700 p-4 rounded max-h-48 overflow-y-auto border border-slate-600">
                      <pre className="whitespace-pre-wrap text-sm text-slate-200">
                        {worksheets[grade] || 'No content generated for this grade'}
                      </pre>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {Object.keys(worksheets).length === 0 && !loading && !error && (
              <div className="text-center text-slate-400 h-40 flex items-center justify-center">
                <div>
                  <AcademicCapIcon className="w-16 h-16 mx-auto text-slate-500 mb-4" />
                  <p>Upload an image and generate worksheets</p>
                  <p className="text-sm text-slate-500 mt-1">Perfect for creating grade-appropriate activities</p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Past Worksheets Sidebar */}
        <div className="xl:col-span-1">
          <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-200 flex items-center">
                <ClockIcon className="w-6 h-6 mr-2 text-blue-400" />
                Past Worksheets
              </h2>
              <button
                onClick={() => setShowPastWorksheets(!showPastWorksheets)}
                className="p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
              >
                {showPastWorksheets ? (
                  <MinusIcon className="w-5 h-5 text-slate-400" />
                ) : (
                  <PlusIcon className="w-5 h-5 text-slate-400" />
                )}
              </button>
            </div>

            {showPastWorksheets && (
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {pastWorksheets.length > 0 ? (
                  pastWorksheets.map((worksheet) => (
                    <div
                      key={worksheet.id}
                      className="p-3 border border-slate-600 rounded-lg hover:bg-slate-700 transition-colors duration-200"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 cursor-pointer" onClick={() => loadPastWorksheet(worksheet)}>
                          <h4 className="font-medium text-slate-200 text-sm">
                            {worksheet.subject} Worksheets
                          </h4>
                          <p className="text-xs text-slate-400 mt-1">
                            Grades: {worksheet.grades.join(', ')}
                          </p>
                          <p className="text-xs text-slate-500 mt-1">
                            {formatTimestamp(worksheet.timestamp)}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            deletePastWorksheet(worksheet.id)
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
                    <p className="text-slate-400 text-sm">No past worksheets</p>
                    <p className="text-xs text-slate-500 mt-1">Generate worksheets to see them here</p>
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

export default WorksheetGenerator 