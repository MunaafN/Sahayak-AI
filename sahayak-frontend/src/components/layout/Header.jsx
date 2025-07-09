import { useState } from 'react'
import { Link } from 'react-router-dom'
import { signOut } from 'firebase/auth'
import { auth } from '../../config/firebase'
import { useTranslation } from 'react-i18next'
import { uiLanguages } from '../../config/languages'
import { 
  UserCircleIcon, 
  ChevronDownIcon,
  ArrowRightOnRectangleIcon,
  LanguageIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

const Header = ({ user }) => {
  const { t, i18n } = useTranslation()
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [languageDropdownOpen, setLanguageDropdownOpen] = useState(false)

  const handleLogout = async () => {
    try {
      await signOut(auth)
    } catch (error) {
      console.error('Error signing out:', error)
    }
  }

  const changeLanguage = (languageCode) => {
    i18n.changeLanguage(languageCode)
    localStorage.setItem('sahayak_language', languageCode)
    setLanguageDropdownOpen(false)
  }

  const getCurrentLanguage = () => {
    const currentLang = uiLanguages.find(lang => lang.code === i18n.language)
    return currentLang || uiLanguages[0]
  }

  return (
    <header className="bg-gradient-to-r from-slate-900 to-slate-800 shadow-sm">
      <div className="flex justify-end items-center pr-6 py-4">

        {/* Language Selector and User Profile */}
        <div className="flex items-center space-x-4">
          {/* Language Selector */}
          <div className="relative">
            <button
              onClick={() => setLanguageDropdownOpen(!languageDropdownOpen)}
              className="flex items-center space-x-2 p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
            >
              <LanguageIcon className="w-5 h-5 text-slate-300" />
              <span className="text-sm font-medium text-slate-200">
                {getCurrentLanguage().nativeName}
              </span>
              <ChevronDownIcon className="w-4 h-4 text-slate-400" />
            </button>

            {/* Language Dropdown */}
            {languageDropdownOpen && (
              <div className="dropdown-menu right-0 mt-2 w-64 fade-in z-dropdown">
                <div className="py-2 max-h-64 overflow-y-auto">
                  {uiLanguages.map((language) => (
                    <button
                      key={language.code}
                      onClick={() => changeLanguage(language.code)}
                      className={`flex items-center justify-between w-full px-4 py-3 text-sm hover:bg-gray-50 transition-colors duration-200 ${
                        i18n.language === language.code ? 'bg-gradient-to-r from-blue-50 to-purple-50 text-blue-700' : 'text-gray-700'
                      }`}
                    >
                      <span className="font-medium">{language.name}</span>
                      <span className="text-gray-500 text-xs">{language.nativeName}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* User Profile Dropdown */}
          <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-3 p-2 rounded-md hover:bg-slate-700 transition-colors duration-200"
          >
            {user.photoURL ? (
              <img 
                src={user.photoURL} 
                alt="Profile" 
                className="w-8 h-8 rounded-full"
              />
            ) : (
              <UserCircleIcon className="w-8 h-8 text-slate-300" />
            )}
            
            <div className="text-left">
              <p className="text-sm font-medium text-slate-200">
                {user.displayName || user.email}
              </p>
              <p className="text-xs text-slate-400">Teacher</p>
            </div>
            
            <ChevronDownIcon className="w-4 h-4 text-slate-400" />
          </button>

          {/* Dropdown Menu */}
          {dropdownOpen && (
            <div className="dropdown-menu right-0 mt-2 w-56 fade-in z-dropdown">
              <div className="py-2">
                <div className="px-4 py-3 text-sm text-gray-700 border-b border-gray-100">
                  <p className="font-semibold text-gray-900">{user.displayName || 'Teacher'}</p>
                  <p className="text-gray-500 text-xs">{user.email}</p>
                </div>
                
                <button
                  onClick={handleLogout}
                  className="flex items-center w-full px-4 py-3 text-sm text-gray-700 hover:bg-gradient-to-r hover:from-red-50 hover:to-red-100 hover:text-red-700 transition-all duration-200"
                >
                  <ArrowRightOnRectangleIcon className="w-4 h-4 mr-3" />
                  {t('nav.logout')}
                </button>
              </div>
            </div>
          )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header 