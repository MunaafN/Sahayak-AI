import { 
  DocumentTextIcon, 
  AcademicCapIcon,
  QuestionMarkCircleIcon,
  PhotoIcon,
  SpeakerWaveIcon,
  CalendarIcon
} from '@heroicons/react/24/outline'

// Activity tracking utilities for dashboard
export const ActivityTypes = {
  CONTENT_GENERATED: 'content_generated',
  WORKSHEET_CREATED: 'worksheet_created',
  QUESTION_ANSWERED: 'question_answered',
  VISUAL_GENERATED: 'visual_generated',
  ASSESSMENT_COMPLETED: 'assessment_completed',
  LESSON_PLANNED: 'lesson_planned'
}

const getActivityConfig = (type) => {
  const configs = {
    [ActivityTypes.CONTENT_GENERATED]: {
      icon: DocumentTextIcon,
      color: 'bg-blue-500',
      statKey: 'storiesGenerated'
    },
    [ActivityTypes.WORKSHEET_CREATED]: {
      icon: AcademicCapIcon,
      color: 'bg-green-500',
      statKey: 'worksheetsCreated'
    },
    [ActivityTypes.QUESTION_ANSWERED]: {
      icon: QuestionMarkCircleIcon,
      color: 'bg-purple-500',
      statKey: 'questionsAnswered'
    },
    [ActivityTypes.VISUAL_GENERATED]: {
      icon: PhotoIcon,
      color: 'bg-orange-500',
      statKey: 'visualsGenerated'
    },
    [ActivityTypes.ASSESSMENT_COMPLETED]: {
      icon: SpeakerWaveIcon,
      color: 'bg-red-500',
      statKey: 'assessmentsCompleted'
    },
    [ActivityTypes.LESSON_PLANNED]: {
      icon: CalendarIcon,
      color: 'bg-indigo-500',
      statKey: 'lessonPlans'
    }
  }
  
  return configs[type] || configs[ActivityTypes.CONTENT_GENERATED]
}

// Function to calculate accurate stats from actual stored data
export const calculateAccurateStats = () => {
  try {
    // Count actual items from each module's localStorage
    const pastContent = localStorage.getItem('sahayak_past_content')
    const pastWorksheets = localStorage.getItem('sahayak_past_worksheets')
    const pastQuestions = localStorage.getItem('sahayak_past_questions')
    const pastVisuals = localStorage.getItem('sahayak_past_visuals')
    const pastAssessments = localStorage.getItem('sahayak_past_assessments')
    const pastLessonPlans = localStorage.getItem('sahayak_past_lesson_plans')

    const stats = {
      storiesGenerated: pastContent ? JSON.parse(pastContent).length : 0,
      worksheetsCreated: pastWorksheets ? JSON.parse(pastWorksheets).length : 0,
      questionsAnswered: pastQuestions ? JSON.parse(pastQuestions).length : 0,
      visualsGenerated: pastVisuals ? JSON.parse(pastVisuals).length : 0,
      assessmentsCompleted: pastAssessments ? JSON.parse(pastAssessments).length : 0,
      lessonPlans: pastLessonPlans ? JSON.parse(pastLessonPlans).length : 0
    }

    // Update the cached stats in localStorage to keep them in sync
    localStorage.setItem('sahayak_stats', JSON.stringify(stats))
    
    return stats
  } catch (error) {
    console.error('Error calculating accurate stats:', error)
    return {
      storiesGenerated: 0,
      worksheetsCreated: 0,
      questionsAnswered: 0,
      visualsGenerated: 0,
      assessmentsCompleted: 0,
      lessonPlans: 0
    }
  }
}

export const updateDashboardStats = (activityType, description) => {
  try {
    const config = getActivityConfig(activityType)
    
    // Instead of incrementing, recalculate accurate stats
    const accurateStats = calculateAccurateStats()
    
    // Add to recent activities
    const savedActivities = localStorage.getItem('sahayak_activities')
    const currentActivities = savedActivities ? JSON.parse(savedActivities) : []
    
    const newActivity = {
      type: activityType,
      description,
      timestamp: new Date().toISOString(),
      // Don't store the icon component directly - we'll map it when displaying
      color: config.color
    }
    
    // Add to beginning of array (most recent first)
    currentActivities.unshift(newActivity)
    
    // Keep only the last 20 activities
    const trimmedActivities = currentActivities.slice(0, 20)
    localStorage.setItem('sahayak_activities', JSON.stringify(trimmedActivities))
    
    console.log('Dashboard updated:', { stats: accurateStats, newActivity })
    
  } catch (error) {
    console.error('Error updating dashboard stats:', error)
  }
}

export const clearDashboardData = () => {
  try {
    localStorage.removeItem('sahayak_stats')
    localStorage.removeItem('sahayak_activities')
    console.log('Dashboard data cleared')
  } catch (error) {
    console.error('Error clearing dashboard data:', error)
  }
}

export const getDashboardStats = () => {
  // Always return accurate stats calculated from actual data
  return calculateAccurateStats()
}

export const getRecentActivities = () => {
  try {
    const savedActivities = localStorage.getItem('sahayak_activities')
    return savedActivities ? JSON.parse(savedActivities) : []
  } catch (error) {
    console.error('Error getting recent activities:', error)
    return []
  }
}

export const decreaseDashboardStats = (activityType, description) => {
  try {
    // Instead of decrementing, recalculate accurate stats
    const accurateStats = calculateAccurateStats()
    
    console.log('Dashboard stats recalculated after deletion:', { stats: accurateStats, deleted: description })
    
  } catch (error) {
    console.error('Error updating dashboard stats after deletion:', error)
  }
} 