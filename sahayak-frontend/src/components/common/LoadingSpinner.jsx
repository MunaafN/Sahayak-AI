import { useTranslation } from 'react-i18next'

const LoadingSpinner = ({ message }) => {
  const { t } = useTranslation()
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="flex flex-col items-center space-y-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p className="text-gray-600 text-sm">
          {message || t('common.loading')}
        </p>
      </div>
    </div>
  )
}

export default LoadingSpinner 