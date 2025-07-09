import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  DocumentTextIcon, 
  AcademicCapIcon,
  QuestionMarkCircleIcon,
  PhotoIcon,
  SpeakerWaveIcon,
  CalendarIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'
import { ActivityTypes, calculateAccurateStats, getRecentActivities } from '../utils/dashboard'

const Dashboard = () => {
  const { t } = useTranslation()
  const [stats, setStats] = useState({
    storiesGenerated: 0,
    worksheetsCreated: 0,
    questionsAnswered: 0,
    lessonPlans: 0
  })
  const [recentActivities, setRecentActivities] = useState([])

  useEffect(() => {
    loadDashboardData()
    
    // Add event listener for localStorage changes to refresh stats
    const handleStorageChange = () => {
      loadDashboardData()
    }
    
    window.addEventListener('storage', handleStorageChange)
    
    // Also listen for custom events from modules when data changes
    const handleDataChange = () => {
      loadDashboardData()
    }
    
    window.addEventListener('sahayak-data-changed', handleDataChange)
    
    return () => {
      window.removeEventListener('storage', handleStorageChange)
      window.removeEventListener('sahayak-data-changed', handleDataChange)
    }
  }, [])

  // Refresh data when component becomes visible (user navigates back)
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        loadDashboardData()
      }
    }
    
    document.addEventListener('visibilitychange', handleVisibilityChange)
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [])

  const loadDashboardData = () => {
    try {
      // Load accurate stats calculated from actual data
      const accurateStats = calculateAccurateStats()
      setStats(accurateStats)

      // Load recent activities
      const activities = getRecentActivities()
      setRecentActivities(activities.slice(0, 5)) // Show only last 5 activities
    } catch (error) {
      console.error('Error loading dashboard data:', error)
    }
  }

  const getActivityIcon = (activityType) => {
    const iconMap = {
      [ActivityTypes.CONTENT_GENERATED]: DocumentTextIcon,
      [ActivityTypes.WORKSHEET_CREATED]: AcademicCapIcon,
      [ActivityTypes.QUESTION_ANSWERED]: QuestionMarkCircleIcon,
      [ActivityTypes.VISUAL_GENERATED]: PhotoIcon,
      [ActivityTypes.ASSESSMENT_COMPLETED]: SpeakerWaveIcon,
      [ActivityTypes.LESSON_PLANNED]: CalendarIcon
    }
    return iconMap[activityType] || DocumentTextIcon
  }

  const modules = [
    {
      id: 'content',
      title: t('modules.content.title'),
      description: t('modules.content.description'),
      icon: DocumentTextIcon,
      color: 'bg-blue-500',
      href: '/content'
    },
    {
      id: 'worksheets',
      title: t('modules.worksheets.title'),
      description: t('modules.worksheets.description'),
      icon: AcademicCapIcon,
      color: 'bg-green-500',
      href: '/worksheets'
    },
    {
      id: 'knowledge',
      title: t('modules.knowledge.title'),
      description: t('modules.knowledge.description'),
      icon: QuestionMarkCircleIcon,
      color: 'bg-purple-500',
      href: '/knowledge'
    },
    {
      id: 'visuals',
      title: t('modules.visuals.title'),
      description: t('modules.visuals.description'),
      icon: PhotoIcon,
      color: 'bg-orange-500',
      href: '/visuals'
    },
    {
      id: 'assessment',
      title: t('modules.assessment.title'),
      description: t('modules.assessment.description'),
      icon: SpeakerWaveIcon,
      color: 'bg-red-500',
      href: '/assessment'
    },
    {
      id: 'planner',
      title: t('modules.planner.title'),
      description: t('modules.planner.description'),
      icon: CalendarIcon,
      color: 'bg-indigo-500',
      href: '/planner'
    }
  ]

  const getTimeSince = (timestamp) => {
    const now = new Date()
    const activityTime = new Date(timestamp)
    const diffInMinutes = Math.floor((now - activityTime) / (1000 * 60))
    
    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes} minutes ago`
    
    const diffInHours = Math.floor(diffInMinutes / 60)
    if (diffInHours < 24) return `${diffInHours} hours ago`
    
    const diffInDays = Math.floor(diffInHours / 24)
    return `${diffInDays} days ago`
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-200 mb-2">
          {t('dashboard.title')}
        </h1>
        <p className="text-lg text-slate-400">
          {t('dashboard.subtitle')}
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-600">
              <DocumentTextIcon className="w-6 h-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-semibold text-slate-200">{stats.storiesGenerated}</p>
              <p className="text-sm text-slate-400">Content Generated</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-green-600">
              <AcademicCapIcon className="w-6 h-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-semibold text-slate-200">{stats.worksheetsCreated}</p>
              <p className="text-sm text-slate-400">Worksheets Created</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-purple-600">
              <QuestionMarkCircleIcon className="w-6 h-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-semibold text-slate-200">{stats.questionsAnswered}</p>
              <p className="text-sm text-slate-400">Questions Answered</p>
            </div>
          </div>
        </div>
        
        <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-orange-600">
              <CalendarIcon className="w-6 h-6 text-white" />
            </div>
            <div className="ml-4">
              <p className="text-2xl font-semibold text-slate-200">{stats.lessonPlans}</p>
              <p className="text-sm text-slate-400">Lesson Plans</p>
            </div>
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules.map((module) => (
          <Link
            key={module.id}
            to={module.href}
            className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300 group"
          >
            <div className="flex items-start">
              <div className={`p-3 rounded-lg ${module.color}`}>
                <module.icon className="w-6 h-6 text-white" />
              </div>
              <div className="ml-4 flex-1">
                <h3 className="text-lg font-semibold text-slate-200 group-hover:text-blue-400 transition-colors duration-200">
                  {module.title}
                </h3>
                <p className="text-sm text-slate-400 mt-1">
                  {module.description}
                </p>
              </div>
              <ArrowRightIcon className="w-5 h-5 text-slate-400 group-hover:text-blue-400 transition-colors duration-200" />
            </div>
          </Link>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="mt-12">
        <h2 className="text-xl font-semibold text-slate-200 mb-6">Recent Activity</h2>
        <div className="bg-slate-800 rounded-2xl shadow-lg p-8 border border-slate-700 hover:shadow-xl transition-shadow duration-300">
          {recentActivities.length > 0 ? (
            <div className="space-y-4">
              {recentActivities.map((activity, index) => (
                <div key={index} className={`flex items-center justify-between py-3 ${index < recentActivities.length - 1 ? 'border-b border-slate-700' : ''}`}>
                  <div className="flex items-center">
                    <div className={`p-2 rounded-full ${activity.color}`}>
                      {(() => {
                        const IconComponent = getActivityIcon(activity.type)
                        return <IconComponent className="w-4 h-4 text-white" />
                      })()}
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-slate-200">
                        {activity.description}
                      </p>
                      <p className="text-xs text-slate-400">{getTimeSince(activity.timestamp)}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <p className="text-slate-400">No recent activity</p>
              <p className="text-sm text-slate-500 mt-1">Start using the modules to see your activity here!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Dashboard 