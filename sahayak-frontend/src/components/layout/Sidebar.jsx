import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  HomeIcon, 
  DocumentTextIcon, 
  AcademicCapIcon,
  QuestionMarkCircleIcon,
  PhotoIcon,
  SpeakerWaveIcon,
  CalendarIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline'

const Sidebar = () => {
  const location = useLocation()
  const { t, i18n } = useTranslation()

  const navigation = [
    { name: t('nav.dashboard'), href: '/dashboard', icon: HomeIcon },
    { name: t('nav.content'), href: '/content', icon: DocumentTextIcon },
    { name: t('nav.worksheets'), href: '/worksheets', icon: AcademicCapIcon },
    { name: t('nav.knowledge'), href: '/knowledge', icon: QuestionMarkCircleIcon },
    { name: t('nav.visuals'), href: '/visuals', icon: PhotoIcon },
    { name: t('nav.assessment'), href: '/assessment', icon: SpeakerWaveIcon },
    { name: t('nav.planner'), href: '/planner', icon: CalendarIcon },
  ]

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng)
  }

  return (
    <div className="flex flex-col bg-gradient-to-b from-slate-900 to-slate-800 shadow-2xl w-64 h-full">
      {/* Header with Logo */}
      <div className="h-16 flex items-center pl-4">
        {/* Sahayak Logo */}
        <Link 
          to="/" 
          className="flex items-center hover:opacity-80 transition-opacity duration-200"
        >
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
            Sahayak-AI
          </h1>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`
                flex items-center px-3 py-3 rounded-xl transition-all duration-200 group
                ${isActive 
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg' 
                  : 'text-slate-300 hover:bg-slate-700 hover:text-white'
                }
              `}
            >
              <item.icon className="w-5 h-5 mr-3 flex-shrink-0" />
              <span className="font-medium">{item.name}</span>
            </Link>
          )
        })}
      </nav>

      {/* Language Switcher */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center mb-3">
          <GlobeAltIcon className="w-4 h-4 mr-2 text-slate-400" />
          <span className="text-sm font-medium text-slate-300">Language</span>
        </div>
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={() => changeLanguage('en')}
            className={`px-2 py-1 text-xs rounded-lg transition-colors duration-200 ${
              i18n.language === 'en' 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            EN
          </button>
          <button
            onClick={() => changeLanguage('hi')}
            className={`px-2 py-1 text-xs rounded-lg transition-colors duration-200 ${
              i18n.language === 'hi' 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            हिं
          </button>
          <button
            onClick={() => changeLanguage('mr')}
            className={`px-2 py-1 text-xs rounded-lg transition-colors duration-200 ${
              i18n.language === 'mr' 
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white' 
                : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
            }`}
          >
            मरा
          </button>
        </div>
      </div>
    </div>
  )
}

export default Sidebar 