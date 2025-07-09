import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { 
  DocumentTextIcon, 
  AcademicCapIcon,
  QuestionMarkCircleIcon,
  PhotoIcon,
  SpeakerWaveIcon,
  CalendarIcon,
  SparklesIcon,
  GlobeAltIcon,
  BookOpenIcon,
  ArrowRightIcon,
  CheckIcon,
  StarIcon
} from '@heroicons/react/24/outline'

const Home = () => {
  const { t } = useTranslation()

  const features = [
    {
      name: 'Hyper-Local Content Generator',
      description: 'Generate educational stories and content in 40+ Indian languages with cultural context.',
      icon: DocumentTextIcon,
      color: 'bg-gradient-to-r from-blue-500 to-blue-600',
      href: '/content'
    },
    {
      name: 'AI Lesson Planner',
      description: 'Create structured lesson plans for any topic with AI assistance.',
      icon: CalendarIcon,
      color: 'bg-gradient-to-r from-indigo-500 to-indigo-600',
      href: '/planner'
    },
    {
      name: 'Smart Worksheets',
      description: 'Generate differentiated worksheets from textbook images using vision AI.',
      icon: AcademicCapIcon,
      color: 'bg-gradient-to-r from-green-500 to-green-600',
      href: '/worksheets'
    },
    {
      name: 'Knowledge Base',
      description: 'Get simple explanations for complex questions in your preferred language.',
      icon: QuestionMarkCircleIcon,
      color: 'bg-gradient-to-r from-purple-500 to-purple-600',
      href: '/knowledge'
    },
    {
      name: 'Visual Aids Generator',
      description: 'Create diagrams and illustrations to enhance teaching.',
      icon: PhotoIcon,
      color: 'bg-gradient-to-r from-orange-500 to-orange-600',
      href: '/visuals'
    },
    {
      name: 'Reading Assessment',
      description: 'AI-powered reading fluency assessment with instant feedback.',
      icon: SpeakerWaveIcon,
      color: 'bg-gradient-to-r from-red-500 to-red-600',
      href: '/assessment'
    }
  ]

  const benefits = [
    'Support most Indian languages',
    'Free and open-source AI tools',
    'Offline-capable with local AI',
    'Multi-grade classroom support',
    'Cultural context awareness',
    'No data privacy concerns'
  ]

  const testimonials = [
    {
      content: "Sahayak has transformed how I teach in my village school. Creating content in Marathi has never been easier!",
      author: "Priya Sharma",
      role: "Primary School Teacher, Maharashtra"
    },
    {
      content: "The AI lesson planner saves me hours of preparation time. I can focus more on actually teaching my students.",
      author: "Rajesh Kumar",
      role: "Government School Teacher, UP"
    },
    {
      content: "Finally, an educational tool that understands Indian languages and contexts. My students love the local stories!",
      author: "Meena Patel",
      role: "Rural School Principal, Gujarat"
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800">
              {/* Hero Section */}
        <div className="relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 to-purple-600/20"></div>
          
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="pt-20 pb-16 md:pt-28 md:pb-20">
              <div className="text-center">
                <div className="flex justify-center mb-6">
                  <div className="flex items-center space-x-2 bg-slate-700/80 backdrop-blur-sm rounded-full px-4 py-2 shadow-lg border border-slate-600">
                    <SparklesIcon className="w-5 h-5 text-blue-400" />
                    <span className="text-sm font-medium text-slate-200">AI-Powered Teaching Assistant</span>
                  </div>
                </div>
                
                <h1 className="text-4xl md:text-6xl font-bold text-white mb-6 leading-tight">
                  Meet <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">सहायक</span>
                  <br />
                  <span className="text-2xl md:text-4xl text-slate-300 font-medium">Your AI Teaching Companion</span>
                </h1>
                
                <p className="text-xl text-slate-300 mb-8 max-w-3xl mx-auto leading-relaxed">
                  Empower multi-grade classrooms with free, local AI tools. Create content in 40+ Indian languages, 
                  generate lesson plans, and assess student progress - all while keeping your data private.
                </p>
              
                              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <Link
                    to="/dashboard"
                    className="inline-flex items-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    Get Started Free
                    <ArrowRightIcon className="w-5 h-5 ml-2" />
                  </Link>
                  
                  <a
                    href="#features"
                    className="inline-flex items-center px-8 py-4 text-lg font-semibold text-slate-200 bg-slate-700/80 backdrop-blur-sm rounded-xl hover:bg-slate-600 border border-slate-600 transition-all duration-200 shadow-lg hover:shadow-xl"
                  >
                    <BookOpenIcon className="w-5 h-5 mr-2" />
                    Learn More
                  </a>
                </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div id="features" className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Everything You Need to Teach Better
            </h2>
            <p className="text-xl text-slate-300 max-w-2xl mx-auto">
              Comprehensive AI tools designed specifically for Indian educators and multi-grade classrooms.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Link
                key={feature.name}
                to={feature.href}
                className="group relative bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden border border-slate-700 hover:border-slate-600"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-slate-800/50 to-slate-700/50 group-hover:from-slate-700/50 group-hover:to-slate-600/50 transition-all duration-300"></div>
                
                <div className="relative p-8">
                  <div className={`w-12 h-12 ${feature.color} rounded-xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                    <feature.icon className="w-6 h-6 text-white" />
                  </div>
                  
                  <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors duration-300">
                    {feature.name}
                  </h3>
                  
                  <p className="text-slate-300 leading-relaxed">
                    {feature.description}
                  </p>
                  
                  <div className="mt-6 flex items-center text-blue-400 font-medium group-hover:text-blue-300">
                    Try it now
                    <ArrowRightIcon className="w-4 h-4 ml-2 transform group-hover:translate-x-1 transition-transform duration-300" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Benefits Section */}
      <div className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Why Teachers Choose Sahayak
            </h2>
            <p className="text-xl text-blue-100 max-w-2xl mx-auto">
              Built by educators, for educators. Designed to work in real Indian classroom conditions.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {benefits.map((benefit, index) => (
              <div
                key={index}
                className="flex items-center space-x-3 bg-white/10 backdrop-blur-sm rounded-lg p-4 hover:bg-white/20 transition-all duration-300"
              >
                <CheckIcon className="w-6 h-6 text-green-300 flex-shrink-0" />
                <span className="text-white font-medium">{benefit}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Testimonials Section */}
      <div className="py-20 bg-gradient-to-br from-slate-900 to-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Loved by Teachers Across India
            </h2>
            <p className="text-xl text-slate-300">
              See how Sahayak is transforming education in schools nationwide.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div
                key={index}
                className="bg-slate-800/50 backdrop-blur-sm rounded-2xl shadow-lg p-8 hover:shadow-xl transition-shadow duration-300 border border-slate-700"
              >
                <div className="flex items-center mb-4">
                  {[...Array(5)].map((_, i) => (
                    <StarIcon key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                
                <p className="text-slate-300 mb-6 italic leading-relaxed">
                  "{testimonial.content}"
                </p>
                
                <div>
                  <div className="font-semibold text-white">{testimonial.author}</div>
                  <div className="text-sm text-slate-400">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="py-20 bg-gradient-to-r from-gray-900 to-gray-800">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Transform Your Teaching?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of teachers already using Sahayak to create better learning experiences.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/dashboard"
              className="inline-flex items-center px-8 py-4 text-lg font-semibold text-gray-900 bg-white rounded-xl hover:bg-gray-100 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
            >
              <SparklesIcon className="w-5 h-5 mr-2" />
              Start Creating Today
            </Link>
            
            <div className="flex items-center space-x-4 text-gray-300">
              <GlobeAltIcon className="w-5 h-5" />
              <span>40+ Languages</span>
              <span>•</span>
              <span>100% Free</span>
              <span>•</span>
              <span>Privacy First</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center mb-4 md:mb-0">
              <h3 className="text-2xl font-bold text-white">सहायक</h3>
              <span className="ml-2 text-gray-400">Sahayak AI</span>
            </div>
            
            <div className="text-gray-400 text-center md:text-right">
              <p>Built with ❤️ for Indian educators</p>
              <p className="text-sm mt-1">Empowering education through AI</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home 